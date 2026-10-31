"""Entidade que representa uma pessoa habilitada a adotar."""


class Adotante:
    def __init__(
        self,
        nome: str,
        cpf: str,
        telefone: str,
        email: str,
        cidade: str,
        ativo: bool = True,
        id_adotante: int | None = None,
    ) -> None:
        self.id_adotante = id_adotante
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.cidade = cidade
        self.ativo = ativo

    @property
    def id_adotante(self) -> int | None:
        return self._id_adotante

    @id_adotante.setter
    def id_adotante(self, valor: int | None) -> None:
        self._id_adotante = valor

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        valor = valor.strip()
        if len(valor) < 3:
            raise ValueError("O nome deve possuir ao menos 3 caracteres.")
        self._nome = valor

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, valor: str) -> None:
        somente_numeros = "".join(caractere for caractere in valor if caractere.isdigit())
        if len(somente_numeros) != 11:
            raise ValueError("O CPF deve possuir 11 dígitos.")
        self._cpf = somente_numeros

    @property
    def telefone(self) -> str:
        return self._telefone

    @telefone.setter
    def telefone(self, valor: str) -> None:
        valor = valor.strip()
        if len(valor) < 8:
            raise ValueError("Informe um telefone válido.")
        self._telefone = valor

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        valor = valor.strip().lower()
        if "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValueError("Informe um e-mail válido.")
        self._email = valor

    @property
    def cidade(self) -> str:
        return self._cidade

    @cidade.setter
    def cidade(self, valor: str) -> None:
        valor = valor.strip()
        if len(valor) < 2:
            raise ValueError("Informe uma cidade válida.")
        self._cidade = valor

    @property
    def ativo(self) -> bool:
        return self._ativo

    @ativo.setter
    def ativo(self, valor: bool) -> None:
        self._ativo = bool(valor)

    def to_string(self) -> str:
        situacao = "Ativo" if self.ativo else "Inativo"
        return (
            f"Adotante {self.id_adotante or '-'} | {self.nome} | CPF: {self.cpf} | "
            f"Telefone: {self.telefone} | {self.email} | {self.cidade} | {situacao}"
        )

    def __str__(self) -> str:
        return self.to_string()

