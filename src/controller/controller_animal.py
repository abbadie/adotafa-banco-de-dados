"""Operações SQL da entidade ANIMAIS."""

from src.conexao.conexao import conectar
from src.controller.excecoes import (
    RegistroNaoEncontrado,
    RegistroReferenciado,
)
from src.model.animal import Animal


class ControllerAnimal:
    def existe(self, id_animal: int) -> bool:
        consulta = "SELECT EXISTS(SELECT 1 FROM animais WHERE id_animal = %s)"
        conexao = conectar()
        try:
            with conexao.cursor() as cursor:
                cursor.execute(consulta, (id_animal,))
                return bool(cursor.fetchone()[0])
        finally:
            conexao.close()

    def inserir(self, animal: Animal) -> int:
        comando = """
            INSERT INTO animais (
                nome, especie, sexo, idade_aproximada, porte, status_adocao, data_entrada
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_animal
        """
        conexao = conectar()
        try:
            with conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        comando,
                        (
                            animal.nome,
                            animal.especie,
                            animal.sexo,
                            animal.idade_aproximada,
                            animal.porte,
                            animal.status_adocao,
                            animal.data_entrada,
                        ),
                    )
                    animal.id_animal = int(cursor.fetchone()[0])
                    return animal.id_animal
        finally:
            conexao.close()

    def buscar_por_id(self, id_animal: int) -> Animal:
        consulta = """
            SELECT id_animal, nome, especie, sexo, idade_aproximada,
                   porte, status_adocao, data_entrada
            FROM animais
            WHERE id_animal = %s
        """
        conexao = conectar()
        try:
            with conexao.cursor() as cursor:
                cursor.execute(consulta, (id_animal,))
                linha = cursor.fetchone()
            if not linha:
                raise RegistroNaoEncontrado("Animal não encontrado.")
            return Animal(
                id_animal=linha[0],
                nome=linha[1],
                especie=linha[2],
                sexo=linha[3],
                idade_aproximada=linha[4],
                porte=linha[5],
                status_adocao=linha[6],
                data_entrada=linha[7],
            )
        finally:
            conexao.close()

    def listar_resumo(self, somente_disponiveis: bool = False) -> list[tuple]:
        consulta = """
            SELECT id_animal, nome, especie, porte, status_adocao
            FROM animais
        """
        parametros: tuple = ()
        if somente_disponiveis:
            consulta += " WHERE status_adocao = %s"
            parametros = ("DISPONIVEL",)
        consulta += " ORDER BY nome"
        conexao = conectar()
        try:
            with conexao.cursor() as cursor:
                cursor.execute(consulta, parametros)
                return cursor.fetchall()
        finally:
            conexao.close()

    def atualizar(self, animal: Animal) -> None:
        if animal.id_animal is None or not self.existe(animal.id_animal):
            raise RegistroNaoEncontrado("Animal não encontrado para atualização.")
        comando = """
            UPDATE animais
            SET nome = %s, especie = %s, sexo = %s, idade_aproximada = %s,
                porte = %s, status_adocao = %s, data_entrada = %s
            WHERE id_animal = %s
        """
        conexao = conectar()
        try:
            with conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        comando,
                        (
                            animal.nome,
                            animal.especie,
                            animal.sexo,
                            animal.idade_aproximada,
                            animal.porte,
                            animal.status_adocao,
                            animal.data_entrada,
                            animal.id_animal,
                        ),
                    )
        finally:
            conexao.close()

    def quantidade_adocoes(self, id_animal: int) -> int:
        consulta = "SELECT COUNT(1) FROM adocoes WHERE id_animal = %s"
        conexao = conectar()
        try:
            with conexao.cursor() as cursor:
                cursor.execute(consulta, (id_animal,))
                return int(cursor.fetchone()[0])
        finally:
            conexao.close()

    def excluir(self, id_animal: int, remover_adocao: bool = False) -> None:
        conexao = conectar()
        try:
            with conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        "SELECT 1 FROM adocoes WHERE id_animal = %s",
                        (id_animal,),
                    )
                    referenciado = cursor.fetchone() is not None
                    if referenciado and not remover_adocao:
                        raise RegistroReferenciado(
                            "O animal possui uma adoção e não pode ser excluído diretamente."
                        )
                    if referenciado:
                        cursor.execute(
                            "DELETE FROM adocoes WHERE id_animal = %s",
                            (id_animal,),
                        )
                    cursor.execute(
                        "DELETE FROM animais WHERE id_animal = %s",
                        (id_animal,),
                    )
                    if cursor.rowcount == 0:
                        raise RegistroNaoEncontrado("Animal não encontrado para exclusão.")
        finally:
            conexao.close()

