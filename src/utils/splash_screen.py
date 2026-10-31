"""Splash screen com contagens consultadas no banco."""

from src.conexao.conexao import conectar
from src.utils.config import DISCIPLINA, INTEGRANTES, NOME_SISTEMA, PROFESSOR, SEMESTRE


def consultar_contagens() -> dict[str, int]:
    consultas = {
        "adotantes": "SELECT COUNT(1) AS total_adotantes FROM adotantes",
        "animais": "SELECT COUNT(1) AS total_animais FROM animais",
        "adocoes": "SELECT COUNT(1) AS total_adocoes FROM adocoes",
    }
    totais: dict[str, int] = {}
    conexao = conectar()
    try:
        with conexao.cursor() as cursor:
            for entidade, consulta in consultas.items():
                cursor.execute(consulta)
                totais[entidade] = int(cursor.fetchone()[0])
        return totais
    finally:
        conexao.close()


def exibir_splash() -> None:
    totais = consultar_contagens()
    largura = 68
    print("#" * largura)
    print(f"# {NOME_SISTEMA:^{largura - 4}} #")
    print("#" + " " * (largura - 2) + "#")
    print(f"# {'TOTAL DE REGISTROS EXISTENTES':^{largura - 4}} #")
    print(f"#   1 - ADOTANTES: {totais['adotantes']:<44}#")
    print(f"#   2 - ANIMAIS:   {totais['animais']:<44}#")
    print(f"#   3 - ADOÇÕES:   {totais['adocoes']:<44}#")
    print("#" + " " * (largura - 2) + "#")
    print(f"# {'CRIADO POR:':<16}{'':<48}#")
    for nome in INTEGRANTES:
        print(f"# {'':<16}{nome:<48}#")
    print("#" + " " * (largura - 2) + "#")
    print(f"# DISCIPLINA: {DISCIPLINA:<53}#")
    print(f"# SEMESTRE:   {SEMESTRE:<53}#")
    print(f"# PROFESSOR:  {PROFESSOR:<53}#")
    print("#" * largura)

