"""Operações SQL da entidade ADOTANTES."""

from src.conexao.conexao import conectar
from src.controller.excecoes import (
    RegistroDuplicado,
    RegistroNaoEncontrado,
    RegistroReferenciado,
)
from src.model.adotante import Adotante


class ControllerAdotante:
    def existe(self, id_adotante: int) -> bool:
        consulta = "SELECT EXISTS(SELECT 1 FROM adotantes WHERE id_adotante = %s)"
        conexao = conectar()
        try:
            with conexao.cursor() as cursor:
                cursor.execute(consulta, (id_adotante,))
                return bool(cursor.fetchone()[0])
        finally:
            conexao.close()

    def inserir(self, adotante: Adotante) -> int:
        verifica = "SELECT 1 FROM adotantes WHERE cpf = %s OR email = %s"
        comando = """
            INSERT INTO adotantes (nome, cpf, telefone, email, cidade, ativo)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_adotante
        """
        conexao = conectar()
        try:
            with conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(verifica, (adotante.cpf, adotante.email))
                    if cursor.fetchone():
                        raise RegistroDuplicado("Já existe um adotante com esse CPF ou e-mail.")
                    cursor.execute(
                        comando,
                        (
                            adotante.nome,
                            adotante.cpf,
                            adotante.telefone,
                            adotante.email,
                            adotante.cidade,
                            adotante.ativo,
                        ),
                    )
                    adotante.id_adotante = int(cursor.fetchone()[0])
                    return adotante.id_adotante
        finally:
            conexao.close()

    def buscar_por_id(self, id_adotante: int) -> Adotante:
        consulta = """
            SELECT id_adotante, nome, cpf, telefone, email, cidade, ativo
            FROM adotantes
            WHERE id_adotante = %s
        """
        conexao = conectar()
        try:
            with conexao.cursor() as cursor:
                cursor.execute(consulta, (id_adotante,))
                linha = cursor.fetchone()
            if not linha:
                raise RegistroNaoEncontrado("Adotante não encontrado.")
            return Adotante(
                id_adotante=linha[0],
                nome=linha[1],
                cpf=linha[2],
                telefone=linha[3],
                email=linha[4],
                cidade=linha[5],
                ativo=linha[6],
            )
        finally:
            conexao.close()

    def listar_resumo(self, somente_ativos: bool = False) -> list[tuple]:
        consulta = """
            SELECT id_adotante, nome, cpf, cidade,
                   CASE WHEN ativo THEN 'ATIVO' ELSE 'INATIVO' END AS situacao
            FROM adotantes
        """
        parametros: tuple = ()
        if somente_ativos:
            consulta += " WHERE ativo = %s"
            parametros = (True,)
        consulta += " ORDER BY nome"
        conexao = conectar()
        try:
            with conexao.cursor() as cursor:
                cursor.execute(consulta, parametros)
                return cursor.fetchall()
        finally:
            conexao.close()

    def atualizar(self, adotante: Adotante) -> None:
        if adotante.id_adotante is None or not self.existe(adotante.id_adotante):
            raise RegistroNaoEncontrado("Adotante não encontrado para atualização.")
        duplicado = """
            SELECT 1 FROM adotantes
            WHERE (cpf = %s OR email = %s) AND id_adotante <> %s
        """
        comando = """
            UPDATE adotantes
            SET nome = %s, cpf = %s, telefone = %s, email = %s,
                cidade = %s, ativo = %s
            WHERE id_adotante = %s
        """
        conexao = conectar()
        try:
            with conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        duplicado,
                        (adotante.cpf, adotante.email, adotante.id_adotante),
                    )
                    if cursor.fetchone():
                        raise RegistroDuplicado("CPF ou e-mail já utilizado por outro adotante.")
                    cursor.execute(
                        comando,
                        (
                            adotante.nome,
                            adotante.cpf,
                            adotante.telefone,
                            adotante.email,
                            adotante.cidade,
                            adotante.ativo,
                            adotante.id_adotante,
                        ),
                    )
        finally:
            conexao.close()

    def quantidade_adocoes(self, id_adotante: int) -> int:
        consulta = "SELECT COUNT(1) FROM adocoes WHERE id_adotante = %s"
        conexao = conectar()
        try:
            with conexao.cursor() as cursor:
                cursor.execute(consulta, (id_adotante,))
                return int(cursor.fetchone()[0])
        finally:
            conexao.close()

    def excluir(self, id_adotante: int, remover_adocoes: bool = False) -> None:
        conexao = conectar()
        try:
            with conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_animal FROM adocoes WHERE id_adotante = %s",
                        (id_adotante,),
                    )
                    animais = [linha[0] for linha in cursor.fetchall()]
                    if animais and not remover_adocoes:
                        raise RegistroReferenciado(
                            "O adotante possui adoções e não pode ser excluído diretamente."
                        )
                    if animais:
                        cursor.execute(
                            "DELETE FROM adocoes WHERE id_adotante = %s",
                            (id_adotante,),
                        )
                        cursor.execute(
                            "UPDATE animais SET status_adocao = 'DISPONIVEL' "
                            "WHERE id_animal = ANY(%s)",
                            (animais,),
                        )
                    cursor.execute(
                        "DELETE FROM adotantes WHERE id_adotante = %s",
                        (id_adotante,),
                    )
                    if cursor.rowcount == 0:
                        raise RegistroNaoEncontrado("Adotante não encontrado para exclusão.")
        finally:
            conexao.close()

