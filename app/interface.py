import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .modelos import SolicitacaoOrcamento, TipoImovel
from .servicos import CalculadoraOrcamento, GeradorCSV


def moeda(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class AplicacaoOrcamento(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Imobiliária R.M. - Orçamento de Aluguel")
        self.geometry("760x670")
        self.minsize(700, 620)
        self.configure(bg="#eef2f7")
        self.calculadora = CalculadoraOrcamento()
        self.gerador = GeradorCSV()
        self.ultimo_pedido = None
        self.ultimo_resultado = None
        self._criar_estilo()
        self._criar_tela()
        self._atualizar_campos()

    def _criar_estilo(self) -> None:
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 20, "bold"), foreground="#17324d")
        estilo.configure("Sub.TLabel", font=("Segoe UI", 10), foreground="#526579")
        estilo.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10)
        estilo.configure("Destaque.TButton", background="#1769aa", foreground="white")
        estilo.map("Destaque.TButton", background=[("active", "#125589")])

    def _criar_tela(self) -> None:
        principal = ttk.Frame(self, padding=24)
        principal.pack(fill="both", expand=True)
        ttk.Label(principal, text="Orçamento de aluguel", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(
            principal,
            text="Calcule a mensalidade e gere o cronograma anual do cliente.",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=(2, 18))

        formulario = ttk.LabelFrame(principal, text=" Dados do orçamento ", padding=18)
        formulario.pack(fill="x")
        formulario.columnconfigure(1, weight=1)

        self.cliente = tk.StringVar()
        self.tipo = tk.StringVar(value=TipoImovel.APARTAMENTO.value)
        self.quartos = tk.IntVar(value=1)
        self.criancas = tk.BooleanVar(value=True)
        self.garagem = tk.BooleanVar(value=False)
        self.vagas = tk.IntVar(value=0)
        self.parcelas = tk.IntVar(value=5)

        ttk.Label(formulario, text="Cliente:").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Entry(formulario, textvariable=self.cliente).grid(row=0, column=1, columnspan=3, sticky="ew", pady=6)
        ttk.Label(formulario, text="Tipo de imóvel:").grid(row=1, column=0, sticky="w", pady=6)
        combo_tipo = ttk.Combobox(
            formulario, textvariable=self.tipo,
            values=[item.value for item in TipoImovel], state="readonly"
        )
        combo_tipo.grid(row=1, column=1, sticky="ew", pady=6, padx=(0, 14))
        combo_tipo.bind("<<ComboboxSelected>>", lambda _evento: self._atualizar_campos())
        ttk.Label(formulario, text="Parcelas contrato:").grid(row=1, column=2, sticky="w", pady=6)
        ttk.Spinbox(formulario, from_=1, to=5, textvariable=self.parcelas, width=6).grid(row=1, column=3, sticky="w")

        self.lbl_quartos = ttk.Label(formulario, text="Quartos:")
        self.lbl_quartos.grid(row=2, column=0, sticky="w", pady=6)
        self.cmb_quartos = ttk.Combobox(formulario, textvariable=self.quartos, values=[1, 2], state="readonly")
        self.cmb_quartos.grid(row=2, column=1, sticky="ew", pady=6, padx=(0, 14))
        self.chk_garagem = ttk.Checkbutton(formulario, text="Adicionar garagem (+ R$ 300)", variable=self.garagem)
        self.chk_garagem.grid(row=2, column=2, columnspan=2, sticky="w")
        self.chk_criancas = ttk.Checkbutton(
            formulario, text="Cliente possui crianças", variable=self.criancas
        )
        self.chk_criancas.grid(row=3, column=0, columnspan=2, sticky="w", pady=6)
        self.lbl_vagas = ttk.Label(formulario, text="Vagas do estúdio:")
        self.spn_vagas = ttk.Spinbox(formulario, from_=0, to=20, textvariable=self.vagas, width=8)

        botoes = ttk.Frame(principal)
        botoes.pack(fill="x", pady=16)
        ttk.Button(botoes, text="Calcular orçamento", style="Destaque.TButton", command=self.calcular).pack(side="left")
        self.btn_csv = ttk.Button(botoes, text="Gerar CSV (12 meses)", command=self.gerar_csv, state="disabled")
        self.btn_csv.pack(side="left", padx=10)
        ttk.Button(botoes, text="Limpar", command=self.limpar).pack(side="right")

        resultado_frame = ttk.LabelFrame(principal, text=" Resultado ", padding=18)
        resultado_frame.pack(fill="both", expand=True)
        self.resultado_texto = tk.Text(
            resultado_frame, height=12, font=("Consolas", 11), bg="#ffffff",
            fg="#1f3347", relief="flat", padx=14, pady=14, state="disabled"
        )
        self.resultado_texto.pack(fill="both", expand=True)

    def _atualizar_campos(self) -> None:
        estudio = self.tipo.get() == TipoImovel.ESTUDIO.value
        estado_normal = "disabled" if estudio else "readonly"
        self.cmb_quartos.configure(state=estado_normal)
        self.chk_garagem.configure(state="disabled" if estudio else "normal")
        self.chk_criancas.configure(
            state="normal" if self.tipo.get() == TipoImovel.APARTAMENTO.value else "disabled"
        )
        if estudio:
            self.lbl_vagas.grid(row=3, column=2, sticky="w", pady=6)
            self.spn_vagas.grid(row=3, column=3, sticky="w")
            self.garagem.set(False)
        else:
            self.lbl_vagas.grid_remove()
            self.spn_vagas.grid_remove()

    def _montar_pedido(self) -> SolicitacaoOrcamento:
        return SolicitacaoOrcamento(
            cliente=self.cliente.get(), tipo=TipoImovel(self.tipo.get()),
            quartos=int(self.quartos.get()), possui_criancas=bool(self.criancas.get()),
            garagem=bool(self.garagem.get()), vagas_estudio=int(self.vagas.get()),
            parcelas_contrato=int(self.parcelas.get()),
        )

    def calcular(self) -> None:
        try:
            pedido = self._montar_pedido()
            resultado = self.calculadora.calcular(pedido)
        except (ValueError, tk.TclError) as erro:
            messagebox.showerror("Dados inválidos", str(erro))
            return
        self.ultimo_pedido, self.ultimo_resultado = pedido, resultado
        linhas = [
            f"Cliente:                    {pedido.cliente.strip()}",
            f"Imóvel:                     {pedido.tipo.value}",
            "-" * 50,
            f"Aluguel-base:               {moeda(resultado.aluguel_base)}",
            f"Adicionais:                 {moeda(resultado.adicionais)}",
            f"Desconto:                  -{moeda(resultado.desconto)}",
            f"ALUGUEL MENSAL:             {moeda(resultado.aluguel_mensal)}",
            "-" * 50,
            f"Contrato imobiliário:       {moeda(resultado.valor_contrato)}",
            f"Forma de pagamento:         {resultado.parcelas_contrato}x de {moeda(resultado.valor_parcela_contrato)}",
            f"Total no primeiro mês:      {moeda(resultado.aluguel_mensal + resultado.valor_parcela_contrato)}",
        ]
        self.resultado_texto.configure(state="normal")
        self.resultado_texto.delete("1.0", "end")
        self.resultado_texto.insert("1.0", "\n".join(linhas))
        self.resultado_texto.configure(state="disabled")
        self.btn_csv.configure(state="normal")

    def gerar_csv(self) -> None:
        if not self.ultimo_pedido or not self.ultimo_resultado:
            return
        nome = f"orcamento_{self.ultimo_pedido.cliente.strip().replace(' ', '_').lower()}.csv"
        destino = filedialog.asksaveasfilename(
            defaultextension=".csv", initialfile=nome,
            filetypes=[("Arquivo CSV", "*.csv")]
        )
        if destino:
            caminho = self.gerador.gerar(destino, self.ultimo_pedido, self.ultimo_resultado)
            messagebox.showinfo("Arquivo gerado", f"CSV salvo com sucesso em:\n{caminho}")

    def limpar(self) -> None:
        self.cliente.set("")
        self.tipo.set(TipoImovel.APARTAMENTO.value)
        self.quartos.set(1)
        self.criancas.set(True)
        self.garagem.set(False)
        self.vagas.set(0)
        self.parcelas.set(5)
        self.ultimo_pedido = self.ultimo_resultado = None
        self.resultado_texto.configure(state="normal")
        self.resultado_texto.delete("1.0", "end")
        self.resultado_texto.configure(state="disabled")
        self.btn_csv.configure(state="disabled")
        self._atualizar_campos()


def executar() -> None:
    AplicacaoOrcamento().mainloop()

