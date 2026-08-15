from dataclasses import dataclass
from enum import Enum


class TipoImovel(str, Enum):
    APARTAMENTO = "Apartamento"
    CASA = "Casa"
    ESTUDIO = "Estúdio"


@dataclass(frozen=True)
class SolicitacaoOrcamento:
    cliente: str
    tipo: TipoImovel
    quartos: int = 1
    possui_criancas: bool = True
    garagem: bool = False
    vagas_estudio: int = 0
    parcelas_contrato: int = 5

    def validar(self) -> None:
        if not self.cliente.strip():
            raise ValueError("Informe o nome do cliente.")
        if not 1 <= self.parcelas_contrato <= 5:
            raise ValueError("O contrato deve ser parcelado entre 1 e 5 vezes.")
        if self.tipo in (TipoImovel.APARTAMENTO, TipoImovel.CASA):
            if self.quartos not in (1, 2):
                raise ValueError("Casas e apartamentos devem ter 1 ou 2 quartos.")
        elif self.vagas_estudio < 0:
            raise ValueError("A quantidade de vagas não pode ser negativa.")


@dataclass(frozen=True)
class ResultadoOrcamento:
    aluguel_base: float
    adicionais: float
    desconto: float
    aluguel_mensal: float
    valor_contrato: float
    parcelas_contrato: int

    @property
    def valor_parcela_contrato(self) -> float:
        return round(self.valor_contrato / self.parcelas_contrato, 2)

