"""Teste opcional de ponta a ponta contra um PostgreSQL configurado.

Execute somente em um banco de desenvolvimento:
RUN_DB_TESTS=1 python -m unittest tests.test_integracao_postgresql -v
"""

from datetime import date
from decimal import Decimal
import os
import unittest

from src.controller.controller_adocao import ControllerAdocao
from src.controller.controller_adotante import ControllerAdotante
from src.controller.controller_animal import ControllerAnimal
from src.controller.excecoes import RegistroReferenciado
from src.model.adocao import Adocao
from src.model.adotante import Adotante
from src.model.animal import Animal
from src.reports.relatorios import Relatorios


@unittest.skipUnless(
    os.getenv("RUN_DB_TESTS") == "1",
    "Defina RUN_DB_TESTS=1 para executar contra o PostgreSQL de desenvolvimento.",
)
class TestIntegracaoPostgreSQL(unittest.TestCase):
    def setUp(self) -> None:
        self.adotantes = ControllerAdotante()
        self.animais = ControllerAnimal()
        self.adocoes = ControllerAdocao()
        self.id_adotante: int | None = None
        self.id_animal: int | None = None
        self.id_adocao: int | None = None

    def tearDown(self) -> None:
        if self.id_adocao is not None and self.adocoes.existe(self.id_adocao):
            self.adocoes.excluir(self.id_adocao)
        if self.id_animal is not None and self.animais.existe(self.id_animal):
            self.animais.excluir(self.id_animal, remover_adocao=True)
        if self.id_adotante is not None and self.adotantes.existe(self.id_adotante):
            self.adotantes.excluir(self.id_adotante, remover_adocoes=True)

    def test_crud_relacionamentos_e_relatorios(self) -> None:
        adotante = Adotante(
            nome="Teste Integracao",
            cpf="97654321098",
            telefone="(27) 99999-1111",
            email="integracao.adotafa@example.com",
            cidade="Serra",
        )
        self.id_adotante = self.adotantes.inserir(adotante)

        animal = Animal(
            nome="Teste Animal",
            especie="GATO",
            sexo="F",
            idade_aproximada=2,
            porte="PEQUENO",
            data_entrada=date.today(),
        )
        self.id_animal = self.animais.inserir(animal)

        adocao = Adocao(
            adotante=adotante,
            animal=animal,
            data_adocao=date.today(),
            taxa="45.00",
            observacoes="Registro criado pelo teste de integracao.",
        )
        self.id_adocao = self.adocoes.inserir(adocao)

        adotante.cidade = "Vitoria"
        self.adotantes.atualizar(adotante)
        self.assertEqual(self.adotantes.buscar_por_id(self.id_adotante).cidade, "Vitoria")

        animal.nome = "Teste Animal Atualizado"
        self.animais.atualizar(animal)
        self.assertEqual(self.animais.buscar_por_id(self.id_animal).nome, animal.nome)

        adocao.taxa = "55.00"
        adocao.observacoes = "Acompanhamento confirmado."
        self.adocoes.atualizar(adocao)
        atualizada = self.adocoes.buscar_por_id(self.id_adocao)
        self.assertEqual(atualizada.taxa, Decimal("55.00"))
        self.assertEqual(atualizada.observacoes, "Acompanhamento confirmado.")

        with self.assertRaises(RegistroReferenciado):
            self.adotantes.excluir(self.id_adotante)

        resumo_cabecalhos, resumo_linhas = Relatorios().adocoes_por_especie()
        detalhe_cabecalhos, detalhe_linhas = Relatorios().adocoes_detalhadas()
        self.assertIn("Quantidade de adoções", resumo_cabecalhos)
        self.assertTrue(resumo_linhas)
        self.assertIn("Adotante", detalhe_cabecalhos)
        self.assertTrue(any(linha[0] == self.id_adocao for linha in detalhe_linhas))


if __name__ == "__main__":
    unittest.main()

