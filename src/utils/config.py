"""Configurações centralizadas da aplicação."""

import os


NOME_SISTEMA = "ADOTAFÁ - SISTEMA DE ADOÇÃO RESPONSÁVEL"
DISCIPLINA = "BANCO DE DADOS"
PROFESSOR = "HOWARD ROATTI"
SEMESTRE = "2026/2"

_integrantes = os.getenv(
    "INTEGRANTES",
    "Davi Noronha da Matta Baptista",
)
INTEGRANTES = [nome.strip() for nome in _integrantes.split(";") if nome.strip()]

CONFIGURACAO_BANCO = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "adotafa"),
    "user": os.getenv("DB_USER", "adotafa_app"),
    "password": os.getenv("DB_PASSWORD", "troque_esta_senha"),
}

MENU_PRINCIPAL = """
+==============================================================+
|                        MENU PRINCIPAL                        |
+==============================================================+
|  1 - Relatórios                                               |
|  2 - Inserir registros                                      |
|  3 - Remover registros                                      |
|  4 - Atualizar registros                                    |
|  0 - Sair                                                   |
+==============================================================+
"""

MENU_ENTIDADES = """
+==============================================================+
|                      ESCOLHA A ENTIDADE                      |
+==============================================================+
|  1 - Adotantes                                              |
|  2 - Animais                                                |
|  3 - Adoções                                                |
|  0 - Voltar                                                 |
+==============================================================+
"""

MENU_RELATORIOS = """
+==============================================================+
|                         RELATÓRIOS                            |
+==============================================================+
|  1 - Resumo de adoções por espécie                         |
|  2 - Adoções detalhadas (junção das tabelas)              |
|  0 - Voltar                                                 |
+==============================================================+
"""

