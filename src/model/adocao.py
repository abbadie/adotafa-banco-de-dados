"""Entidade associativa entre adotante e animal."""

from datetime import date
from decimal import Decimal

from src.model.adotante import Adotante
from src.model.animal import Animal


class Adocao:
    def __init__(
        self,
        adotante: Adotante,
        animal: Animal,
        data_adocao: date,
        taxa: Decimal | float | str,
        observacoes: str = "",
        id_adocao: int | None = None,
    ) -> None:
        self.id_adocao = id_adocao
        self.adotante = adotante
        self.animal = animal
        self.data_adocao = data_adocao
        self.taxa = taxa
        self.observacoes = observacoes

    @property
    def id_adocao(self) -> int | None:
        return self._id_adocao

    @id_adocao.setter
    def id_adocao(self, valor: int | None) -> None:
        self._id_adocao = valor

    @property
    def adotante(self) -> Adotante:
        return self._adotante

    @adotante.setter
    def adotante(self, valor: Adotante) -> None:
        if not isinstance(valor, Adotante):
            raise ValueError("A adoção deve receber um objeto Adotante.")
        self._adotante = valor

    @property
    def animal(self) -> Animal:
        return self._animal

    @animal.setter
    def animal(self, valor: Animal) -> None:
        if not isinstance(valor, Animal):
            raise ValueError("A adoção deve receber um objeto Animal.")
        self._animal = valor

    @property
    def data_adocao(self) -> date:
        return self._data_adocao

    @data_adocao.setter
    def data_adocao(self, valor: date) -> None:
        if not isinstance(valor, date):
            raise ValueError("A data da adoção deve ser uma data válida.")
        if valor > date.today():
            raise ValueError("A data da adoção não pode estar no futuro.")
        self._data_adocao = valor

    @property
    def taxa(self) -> Decimal:
        return self._taxa

    @taxa.setter
    def taxa(self, valor: Decimal | float | str) -> None:
        taxa = Decimal(str(valor))
        if taxa < 0:
            raise ValueError("A taxa não pode ser negativa.")
        self._taxa = taxa.quantize(Decimal("0.01"))

    @property
    def observacoes(self) -> str:
        return self._observacoes

    @observacoes.setter
    def observacoes(self, valor: str) -> None:
        valor = valor.strip()
        if len(valor) > 300:
            raise ValueError("As observações devem possuir no máximo 300 caracteres.")
        self._observacoes = valor

    def to_string(self) -> str:
        return (
            f"Adoção {self.id_adocao or '-'} | Animal: {self.animal.nome} | "
            f"Adotante: {self.adotante.nome} | Data: {self.data_adocao:%d/%m/%Y} | "
            f"Taxa: R$ {self.taxa:.2f} | Observações: {self.observacoes or '-'}"
        )

    def __str__(self) -> str:
        return self.to_string()

