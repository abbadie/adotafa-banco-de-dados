"""Fábrica de conexões do AdotaFá."""

from src.utils.config import CONFIGURACAO_BANCO


class ErroConexao(RuntimeError):
    """Erro amigável ao abrir a conexão com o PostgreSQL."""


def conectar():
    """Abre uma nova conexão; cada operação encerra a sua ao terminar."""
    try:
        import psycopg2
    except ImportError as erro:
        raise ErroConexao(
            "O driver psycopg2 não está instalado. Execute: pip install -r requirements.txt"
        ) from erro

    try:
        return psycopg2.connect(**CONFIGURACAO_BANCO, connect_timeout=5)
    except psycopg2.Error as erro:
        detalhe = str(erro).strip().splitlines()[0] if str(erro).strip() else "erro desconhecido"
        raise ErroConexao(
            "Não foi possível conectar ao PostgreSQL. Confira as variáveis DB_* "
            f"e se o serviço está ativo. Detalhe: {detalhe}"
        ) from erro

