import csv
from pathlib import Path

from .modelos import ResultadoOrcamento, SolicitacaoOrcamento, TipoImovel


class CalculadoraOrcamento:
    VALOR_CONTRATO = 2_000.00
    VALORES_BASE = {
        TipoImovel.APARTAMENTO: 700.00,
        TipoImovel.CASA: 900.00,
        TipoImovel.ESTUDIO: 1_200.00,
    }

    def calcular(self, pedido: SolicitacaoOrcamento) -> ResultadoOrcamento:
        pedido.validar()
        base = self.VALORES_BASE[pedido.tipo]
        adicionais = 0.0

        if pedido.tipo == TipoImovel.APARTAMENTO:
            if pedido.quartos == 2:
                adicionais += 200.00
            if pedido.garagem:
                adicionais += 300.00
        elif pedido.tipo == TipoImovel.CASA:
            if pedido.quartos == 2:
                adicionais += 250.00
            if pedido.garagem:
                adicionais += 300.00
        else:
            # Até uma vaga é cobrada pelo pacote inicial de duas vagas (R$ 250).
            # A partir da terceira, acrescentam-se R$ 60 por vaga excedente.
            if pedido.vagas_estudio > 0:
                adicionais += 250.00
                adicionais += max(0, pedido.vagas_estudio - 2) * 60.00

        subtotal = base + adicionais
        desconto = 0.0
        if pedido.tipo == TipoImovel.APARTAMENTO and not pedido.possui_criancas:
            desconto = round(subtotal * 0.05, 2)

        return ResultadoOrcamento(
            aluguel_base=base,
            adicionais=adicionais,
            desconto=desconto,
            aluguel_mensal=round(subtotal - desconto, 2),
            valor_contrato=self.VALOR_CONTRATO,
            parcelas_contrato=pedido.parcelas_contrato,
        )


class GeradorCSV:
    CABECALHO = [
        "mes", "cliente", "tipo_imovel", "aluguel",
        "parcela_contrato", "total_mes"
    ]

    def gerar(
        self,
        destino: str | Path,
        pedido: SolicitacaoOrcamento,
        resultado: ResultadoOrcamento,
    ) -> Path:
        caminho = Path(destino)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        parcela = resultado.valor_parcela_contrato
        with caminho.open("w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(self.CABECALHO)
            for mes in range(1, 13):
                if mes < resultado.parcelas_contrato:
                    contrato_mes = parcela
                elif mes == resultado.parcelas_contrato:
                    # Ajusta o último centavo quando a divisão não é exata (ex.: 3x).
                    contrato_mes = round(
                        resultado.valor_contrato - parcela * (resultado.parcelas_contrato - 1), 2
                    )
                else:
                    contrato_mes = 0.0
                escritor.writerow([
                    mes,
                    pedido.cliente.strip(),
                    pedido.tipo.value,
                    f"{resultado.aluguel_mensal:.2f}",
                    f"{contrato_mes:.2f}",
                    f"{resultado.aluguel_mensal + contrato_mes:.2f}",
                ])
        return caminho
