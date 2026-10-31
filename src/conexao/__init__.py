"""Infraestrutura de conexão com o PostgreSQL."""

from src.conexao.conexao import ErroConexao, conectar

__all__ = ["ErroConexao", "conectar"]

