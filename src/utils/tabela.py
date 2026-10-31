"""Renderiza resultados SQL em tabelas simples e legíveis no console."""

from decimal import Decimal


def _texto(valor: object) -> str:
    if valor is None:
        return "-"
    if isinstance(valor, bool):
        return "Sim" if valor else "Não"
    if isinstance(valor, Decimal):
        return f"{valor:.2f}"
    return str(valor)


def montar_tabela(cabecalhos: list[str], linhas: list[tuple]) -> str:
    if not linhas:
        return "Nenhum registro encontrado."

    dados = [[_texto(valor) for valor in linha] for linha in linhas]
    larguras = [
        min(35, max(len(str(cabecalho)), *(len(linha[indice]) for linha in dados)))
        for indice, cabecalho in enumerate(cabecalhos)
    ]

    def formatar_linha(valores: list[str]) -> str:
        celulas = []
        for indice, valor in enumerate(valores):
            limite = larguras[indice]
            exibido = valor if len(valor) <= limite else valor[: limite - 3] + "..."
            celulas.append(f" {exibido:<{limite}} ")
        return "|" + "|".join(celulas) + "|"

    separador = "+" + "+".join("-" * (largura + 2) for largura in larguras) + "+"
    partes = [separador, formatar_linha([str(item) for item in cabecalhos]), separador]
    partes.extend(formatar_linha(linha) for linha in dados)
    partes.append(separador)
    return "\n".join(partes)

