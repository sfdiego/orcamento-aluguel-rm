import csv
import tempfile
import unittest
from pathlib import Path

from app.modelos import SolicitacaoOrcamento, TipoImovel
from app.servicos import CalculadoraOrcamento, GeradorCSV


class TesteCalculadora(unittest.TestCase):
    def setUp(self):
        self.calc = CalculadoraOrcamento()

    def pedido(self, **alteracoes):
        dados = dict(cliente="Cliente Teste", tipo=TipoImovel.APARTAMENTO)
        dados.update(alteracoes)
        return SolicitacaoOrcamento(**dados)

    def test_apartamento_basico_com_criancas(self):
        self.assertEqual(self.calc.calcular(self.pedido()).aluguel_mensal, 700.00)

    def test_apartamento_completo_sem_criancas(self):
        r = self.calc.calcular(self.pedido(quartos=2, garagem=True, possui_criancas=False))
        self.assertEqual(r.adicionais, 500.00)
        self.assertEqual(r.desconto, 60.00)
        self.assertEqual(r.aluguel_mensal, 1_140.00)

    def test_casa_completa(self):
        r = self.calc.calcular(self.pedido(tipo=TipoImovel.CASA, quartos=2, garagem=True))
        self.assertEqual(r.aluguel_mensal, 1_450.00)

    def test_estudio_quatro_vagas(self):
        r = self.calc.calcular(self.pedido(tipo=TipoImovel.ESTUDIO, vagas_estudio=4))
        self.assertEqual(r.adicionais, 370.00)
        self.assertEqual(r.aluguel_mensal, 1_570.00)

    def test_contrato_em_cinco_vezes(self):
        r = self.calc.calcular(self.pedido(parcelas_contrato=5))
        self.assertEqual(r.valor_parcela_contrato, 400.00)

    def test_csv_tem_doze_meses(self):
        pedido = self.pedido(parcelas_contrato=2)
        resultado = self.calc.calcular(pedido)
        with tempfile.TemporaryDirectory() as pasta:
            destino = GeradorCSV().gerar(Path(pasta) / "teste.csv", pedido, resultado)
            with destino.open(encoding="utf-8-sig") as arquivo:
                linhas = list(csv.DictReader(arquivo, delimiter=";"))
        self.assertEqual(len(linhas), 12)
        self.assertEqual(linhas[0]["parcela_contrato"], "1000.00")
        self.assertEqual(linhas[2]["parcela_contrato"], "0.00")

    def test_csv_ajusta_arredondamento_do_contrato(self):
        pedido = self.pedido(parcelas_contrato=3)
        resultado = self.calc.calcular(pedido)
        with tempfile.TemporaryDirectory() as pasta:
            destino = GeradorCSV().gerar(Path(pasta) / "teste.csv", pedido, resultado)
            with destino.open(encoding="utf-8-sig") as arquivo:
                linhas = list(csv.DictReader(arquivo, delimiter=";"))
        total = sum(float(linha["parcela_contrato"]) for linha in linhas)
        self.assertEqual(total, 2_000.00)


if __name__ == "__main__":
    unittest.main()
