"""Entidade que representa um animal acolhido."""

from datetime import date


class Animal:
    ESPECIES = {"CACHORRO", "GATO", "OUTRO"}
    SEXOS = {"M", "F"}
    PORTES = {"PEQUENO", "MEDIO", "GRANDE"}
    STATUS_VALIDOS = {"DISPONIVEL", "ADOTADO", "INDISPONIVEL"}

    def __init__(
        self,
        nome: str,
        especie: str,
        sexo: str,
        idade_aproximada: int,
        porte: str,
        data_entrada: date,
        status_adocao: str = "DISPONIVEL",
        id_animal: int | None = None,
    ) -> None:
        self.id_animal = id_animal
        self.nome = nome
        self.especie = especie
        self.sexo = sexo
        self.idade_aproximada = idade_aproximada
        self.porte = porte
        self.status_adocao = status_adocao
        self.data_entrada = data_entrada

    @property
    def id_animal(self) -> int | None:
        return self._id_animal

    @id_animal.setter
    def id_animal(self, valor: int | None) -> None:
        self._id_animal = valor

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        valor = valor.strip()
        if len(valor) < 2:
            raise ValueError("O nome do animal deve possuir ao menos 2 caracteres.")
        self._nome = valor

    @property
    def especie(self) -> str:
        return self._especie

    @especie.setter
    def especie(self, valor: str) -> None:
        valor = valor.strip().upper()
        if valor not in self.ESPECIES:
            raise ValueError("Espécie válida: CACHORRO, GATO ou OUTRO.")
        self._especie = valor

    @property
    def sexo(self) -> str:
        return self._sexo

    @sexo.setter
    def sexo(self, valor: str) -> None:
        valor = valor.strip().upper()
        if valor not in self.SEXOS:
            raise ValueError("Sexo válido: M ou F.")
        self._sexo = valor

    @property
    def idade_aproximada(self) -> int:
        return self._idade_aproximada

    @idade_aproximada.setter
    def idade_aproximada(self, valor: int) -> None:
        valor = int(valor)
        if not 0 <= valor <= 35:
            raise ValueError("A idade aproximada deve estar entre 0 e 35 anos.")
        self._idade_aproximada = valor

    @property
    def porte(self) -> str:
        return self._porte

    @porte.setter
    def porte(self, valor: str) -> None:
        valor = valor.strip().upper()
        if valor not in self.PORTES:
            raise ValueError("Porte válido: PEQUENO, MEDIO ou GRANDE.")
        self._porte = valor

    @property
    def status_adocao(self) -> str:
        return self._status_adocao

    @status_adocao.setter
    def status_adocao(self, valor: str) -> None:
        valor = valor.strip().upper()
        if valor not in self.STATUS_VALIDOS:
            raise ValueError("Status inválido para o animal.")
        self._status_adocao = valor

    @property
    def data_entrada(self) -> date:
        return self._data_entrada

    @data_entrada.setter
    def data_entrada(self, valor: date) -> None:
        if not isinstance(valor, date):
            raise ValueError("A data de entrada deve ser uma data válida.")
        if valor > date.today():
            raise ValueError("A data de entrada não pode estar no futuro.")
        self._data_entrada = valor

    def to_string(self) -> str:
        return (
            f"Animal {self.id_animal or '-'} | {self.nome} | {self.especie} | "
            f"Sexo: {self.sexo} | Idade: {self.idade_aproximada} | Porte: {self.porte} | "
            f"Status: {self.status_adocao} | Entrada: {self.data_entrada:%d/%m/%Y}"
        )

    def __str__(self) -> str:
        return self.to_string()

