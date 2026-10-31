from datetime import date
from decimal import Decimal
import unittest

from src.model.adocao import Adocao
from src.model.adotante import Adotante
from src.model.animal import Animal


class TestModelos(unittest.TestCase):
    def setUp(self) -> None:
        self.adotante = Adotante(
            id_adotante=1,
            nome="Ana Souza",
            cpf="123.456.789-01",
            telefone="(27) 99999-0000",
            email="ANA@EXAMPLE.COM",
            cidade="Vitória",
        )
        self.animal = Animal(
            id_animal=2,
            nome="Luna",
            especie="gato",
            sexo="f",
            idade_aproximada=2,
            porte="pequeno",
            data_entrada=date.today(),
        )

    def test_adotante_normaliza_cpf_e_email(self) -> None:
        self.assertEqual(self.adotante.cpf, "12345678901")
        self.assertEqual(self.adotante.email, "ana@example.com")

    def test_animal_normaliza_campos_controlados(self) -> None:
        self.assertEqual(self.animal.especie, "GATO")
        self.assertEqual(self.animal.sexo, "F")
        self.assertEqual(self.animal.porte, "PEQUENO")

    def test_adocao_mantem_objetos_associados(self) -> None:
        adocao = Adocao(
            id_adocao=3,
            adotante=self.adotante,
            animal=self.animal,
            data_adocao=date.today(),
            taxa="60.5",
            observacoes="Acompanhamento agendado.",
        )
        self.assertIs(adocao.adotante, self.adotante)
        self.assertIs(adocao.animal, self.animal)
        self.assertEqual(adocao.taxa, Decimal("60.50"))
        self.assertIn("Luna", adocao.to_string())

    def test_cpf_invalido_e_rejeitado(self) -> None:
        with self.assertRaises(ValueError):
            self.adotante.cpf = "123"

    def test_taxa_negativa_e_rejeitada(self) -> None:
        with self.assertRaises(ValueError):
            Adocao(
                adotante=self.adotante,
                animal=self.animal,
                data_adocao=date.today(),
                taxa="-1.00",
            )


if __name__ == "__main__":
    unittest.main()

