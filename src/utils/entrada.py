"""Funções de leitura e validação para os menus de console."""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation


def ler_opcao(mensagem: str, opcoes: set[str]) -> str:
    while True:
        valor = input(mensagem).strip()
        if valor in opcoes:
            return valor
        print(f"Opção inválida. Escolha: {', '.join(sorted(opcoes))}.")


def ler_texto(mensagem: str, minimo: int = 1, padrao: str | None = None) -> str:
    while True:
        sufixo = f" [{padrao}]" if padrao not in (None, "") else ""
        valor = input(f"{mensagem}{sufixo}: ").strip()
        if not valor and padrao is not None:
            return padrao
        if len(valor) >= minimo:
            return valor
        print(f"Informe ao menos {minimo} caractere(s).")


def ler_inteiro(
    mensagem: str,
    minimo: int | None = None,
    maximo: int | None = None,
    padrao: int | None = None,
) -> int:
    while True:
        sufixo = f" [{padrao}]" if padrao is not None else ""
        valor = input(f"{mensagem}{sufixo}: ").strip()
        if not valor and padrao is not None:
            return padrao
        try:
            numero = int(valor)
        except ValueError:
            print("Informe um número inteiro.")
            continue
        if minimo is not None and numero < minimo:
            print(f"O valor mínimo é {minimo}.")
            continue
        if maximo is not None and numero > maximo:
            print(f"O valor máximo é {maximo}.")
            continue
        return numero


def ler_decimal(mensagem: str, padrao: Decimal | None = None) -> Decimal:
    while True:
        sufixo = f" [{padrao:.2f}]" if padrao is not None else ""
        valor = input(f"{mensagem}{sufixo}: ").strip().replace(",", ".")
        if not valor and padrao is not None:
            return padrao
        try:
            numero = Decimal(valor)
            if numero < 0:
                raise ValueError
            return numero.quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError):
            print("Informe um valor monetário igual ou maior que zero.")


def ler_data(mensagem: str, padrao: date | None = None) -> date:
    while True:
        sufixo = f" [{padrao:%d/%m/%Y}]" if padrao else ""
        valor = input(f"{mensagem} (DD/MM/AAAA){sufixo}: ").strip()
        if not valor and padrao is not None:
            return padrao
        try:
            data = datetime.strptime(valor, "%d/%m/%Y").date()
        except ValueError:
            print("Data inválida. Use o formato DD/MM/AAAA.")
            continue
        if data > date.today():
            print("A data não pode estar no futuro.")
            continue
        return data


def confirmar(mensagem: str) -> bool:
    return ler_opcao(f"{mensagem} [S/N]: ", {"S", "N", "s", "n"}).upper() == "S"


def pausar() -> None:
    input("\nPressione ENTER para continuar...")

