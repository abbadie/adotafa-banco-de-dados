from decimal import Decimal
import unittest

from src.utils.tabela import montar_tabela


class TestTabela(unittest.TestCase):
    def test_monta_tabela_com_cabecalho_e_valores(self) -> None:
        resultado = montar_tabela(
            ["Nome", "Ativo", "Taxa"],
            [("Luna", True, Decimal("60.00"))],
        )
        self.assertIn("Nome", resultado)
        self.assertIn("Luna", resultado)
        self.assertIn("Sim", resultado)
        self.assertIn("60.00", resultado)

    def test_informa_quando_nao_ha_registros(self) -> None:
        self.assertEqual(montar_tabela(["Nome"], []), "Nenhum registro encontrado.")


if __name__ == "__main__":
    unittest.main()

