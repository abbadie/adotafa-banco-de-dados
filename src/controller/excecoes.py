"""Exceções de negócio exibidas pela interface de console."""


class RegistroNaoEncontrado(ValueError):
    pass


class RegistroDuplicado(ValueError):
    pass


class RegistroReferenciado(ValueError):
    pass


class RegraDeNegocio(ValueError):
    pass

