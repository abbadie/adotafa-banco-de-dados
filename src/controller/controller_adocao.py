"""Operações SQL e regras de negócio da entidade ADOCOES."""

from src.conexao.conexao import conectar
from src.controller.excecoes import (
    RegistroNaoEncontrado,
    RegraDeNegocio,
)
from src.model.adocao import Adocao
from src.model.adotante import Adotante
from src.model.animal import Animal


class ControllerAdocao:
    def existe(self, id_adocao: int) -> bool:
        consulta = "SELECT EXISTS(SELECT 1 FROM adocoes WHERE id_adocao = %s)"
        conexao = conectar()
        try:
            with conexao.cursor() as cursor:
                cursor.execute(consulta, (id_adocao,))
                return bool(cursor.fetchone()[0])
        finally:
            conexao.close()

    @staticmethod
    def _validar_relacionamentos(cursor, adocao: Adocao, ignorar_id: int | None = None) -> None:
        cursor.execute(
            "SELECT ativo FROM adotantes WHERE id_adotante = %s",
            (adocao.adotante.id_adotante,),
        )
        linha_adotante = cursor.fetchone()
        if not linha_adotante:
            raise RegistroNaoEncontrado("Adotante não encontrado.")
        if not linha_adotante[0]:
            raise RegraDeNegocio("O adotante selecionado está inativo.")

        cursor.execute(
            "SELECT status_adocao, data_entrada FROM animais WHERE id_animal = %s",
            (adocao.animal.id_animal,),
        )
        linha_animal = cursor.fetchone()
        if not linha_animal:
            raise RegistroNaoEncontrado("Animal não encontrado.")
        if adocao.data_adocao < linha_animal[1]:
            raise RegraDeNegocio("A adoção não pode ocorrer antes da entrada do animal.")

        mesmo_animal_da_adocao = False
        if ignorar_id is not None:
            cursor.execute(
                "SELECT id_animal FROM adocoes WHERE id_adocao = %s",
                (ignorar_id,),
            )
            linha_atual = cursor.fetchone()
            mesmo_animal_da_adocao = bool(
                linha_atual and linha_atual[0] == adocao.animal.id_animal
            )

        consulta_uso = "SELECT id_adocao FROM adocoes WHERE id_animal = %s"
        parametros: tuple = (adocao.animal.id_animal,)
        if ignorar_id is not None:
            consulta_uso += " AND id_adocao <> %s"
            parametros = (adocao.animal.id_animal, ignorar_id)
        cursor.execute(consulta_uso, parametros)
        if cursor.fetchone():
            raise RegraDeNegocio("Esse animal já está vinculado a outra adoção.")
        if linha_animal[0] != "DISPONIVEL" and not mesmo_animal_da_adocao:
            raise RegraDeNegocio("O animal selecionado não está disponível para adoção.")

    def inserir(self, adocao: Adocao) -> int:
        if adocao.adotante.id_adotante is None or adocao.animal.id_animal is None:
            raise RegraDeNegocio("Adotante e animal devem possuir códigos válidos.")
        comando = """
            INSERT INTO adocoes (id_adotante, id_animal, data_adocao, taxa, observacoes)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_adocao
        """
        conexao = conectar()
        try:
            with conexao:
                with conexao.cursor() as cursor:
                    self._validar_relacionamentos(cursor, adocao)
                    cursor.execute(
                        comando,
                        (
                            adocao.adotante.id_adotante,
                            adocao.animal.id_animal,
                            adocao.data_adocao,
                            adocao.taxa,
                            adocao.observacoes or None,
                        ),
                    )
                    adocao.id_adocao = int(cursor.fetchone()[0])
                    cursor.execute(
                        "UPDATE animais SET status_adocao = 'ADOTADO' WHERE id_animal = %s",
                        (adocao.animal.id_animal,),
                    )
                    return adocao.id_adocao
        finally:
            conexao.close()

    def buscar_por_id(self, id_adocao: int) -> Adocao:
        consulta = """
            SELECT
                adocao.id_adocao, adocao.data_adocao, adocao.taxa, adocao.observacoes,
                adotante.id_adotante, adotante.nome, adotante.cpf, adotante.telefone,
                adotante.email, adotante.cidade, adotante.ativo,
                animal.id_animal, animal.nome, animal.especie, animal.sexo,
                animal.idade_aproximada, animal.porte, animal.status_adocao,
                animal.data_entrada
            FROM adocoes AS adocao
            INNER JOIN adotantes AS adotante ON adotante.id_adotante = adocao.id_adotante
            INNER JOIN animais AS animal ON animal.id_animal = adocao.id_animal
            WHERE adocao.id_adocao = %s
        """
        conexao = conectar()
        try:
            with conexao.cursor() as cursor:
                cursor.execute(consulta, (id_adocao,))
                linha = cursor.fetchone()
            if not linha:
                raise RegistroNaoEncontrado("Adoção não encontrada.")
            adotante = Adotante(
                id_adotante=linha[4],
                nome=linha[5],
                cpf=linha[6],
                telefone=linha[7],
                email=linha[8],
                cidade=linha[9],
                ativo=linha[10],
            )
            animal = Animal(
                id_animal=linha[11],
                nome=linha[12],
                especie=linha[13],
                sexo=linha[14],
                idade_aproximada=linha[15],
                porte=linha[16],
                status_adocao=linha[17],
                data_entrada=linha[18],
            )
            return Adocao(
                id_adocao=linha[0],
                data_adocao=linha[1],
                taxa=linha[2],
                observacoes=linha[3] or "",
                adotante=adotante,
                animal=animal,
            )
        finally:
            conexao.close()

    def listar_resumo(self) -> list[tuple]:
        consulta = """
            SELECT adocao.id_adocao, animal.nome, adotante.nome,
                   TO_CHAR(adocao.data_adocao, 'DD/MM/YYYY'), adocao.taxa
            FROM adocoes AS adocao
            INNER JOIN animais AS animal ON animal.id_animal = adocao.id_animal
            INNER JOIN adotantes AS adotante ON adotante.id_adotante = adocao.id_adotante
            ORDER BY adocao.data_adocao DESC, adocao.id_adocao DESC
        """
        conexao = conectar()
        try:
            with conexao.cursor() as cursor:
                cursor.execute(consulta)
                return cursor.fetchall()
        finally:
            conexao.close()

    def atualizar(self, adocao: Adocao) -> None:
        if adocao.id_adocao is None:
            raise RegistroNaoEncontrado("Adoção sem código para atualização.")
        consulta_anterior = "SELECT id_animal FROM adocoes WHERE id_adocao = %s"
        comando = """
            UPDATE adocoes
            SET id_adotante = %s, id_animal = %s, data_adocao = %s,
                taxa = %s, observacoes = %s
            WHERE id_adocao = %s
        """
        conexao = conectar()
        try:
            with conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(consulta_anterior, (adocao.id_adocao,))
                    linha = cursor.fetchone()
                    if not linha:
                        raise RegistroNaoEncontrado("Adoção não encontrada.")
                    animal_anterior = int(linha[0])
                    self._validar_relacionamentos(cursor, adocao, adocao.id_adocao)
                    cursor.execute(
                        comando,
                        (
                            adocao.adotante.id_adotante,
                            adocao.animal.id_animal,
                            adocao.data_adocao,
                            adocao.taxa,
                            adocao.observacoes or None,
                            adocao.id_adocao,
                        ),
                    )
                    if animal_anterior != adocao.animal.id_animal:
                        cursor.execute(
                            "UPDATE animais SET status_adocao = 'DISPONIVEL' WHERE id_animal = %s",
                            (animal_anterior,),
                        )
                    cursor.execute(
                        "UPDATE animais SET status_adocao = 'ADOTADO' WHERE id_animal = %s",
                        (adocao.animal.id_animal,),
                    )
        finally:
            conexao.close()

    def excluir(self, id_adocao: int) -> None:
        conexao = conectar()
        try:
            with conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_animal FROM adocoes WHERE id_adocao = %s",
                        (id_adocao,),
                    )
                    linha = cursor.fetchone()
                    if not linha:
                        raise RegistroNaoEncontrado("Adoção não encontrada para exclusão.")
                    id_animal = int(linha[0])
                    cursor.execute("DELETE FROM adocoes WHERE id_adocao = %s", (id_adocao,))
                    cursor.execute(
                        "UPDATE animais SET status_adocao = 'DISPONIVEL' WHERE id_animal = %s",
                        (id_animal,),
                    )
        finally:
            conexao.close()

