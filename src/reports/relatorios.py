"""Carrega consultas SQL da pasta src/sql e as executa no PostgreSQL."""

from pathlib import Path

from src.conexao.conexao import conectar


class Relatorios:
    DIRETORIO_SQL = Path(__file__).resolve().parents[1] / "sql"

    @classmethod
    def _executar(cls, nome_arquivo: str) -> tuple[list[str], list[tuple]]:
        caminho = cls.DIRETORIO_SQL / nome_arquivo
        consulta = caminho.read_text(encoding="utf-8")
        conexao = conectar()
        try:
            with conexao.cursor() as cursor:
                cursor.execute(consulta)
                cabecalhos = [coluna.name for coluna in cursor.description]
                linhas = cursor.fetchall()
            return cabecalhos, linhas
        finally:
            conexao.close()

    def adocoes_por_especie(self) -> tuple[list[str], list[tuple]]:
        return self._executar("relatorio_adocoes_por_especie.sql")

    def adocoes_detalhadas(self) -> tuple[list[str], list[tuple]]:
        return self._executar("relatorio_adocoes_detalhadas.sql")

