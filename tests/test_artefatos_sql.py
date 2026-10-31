from pathlib import Path
import unittest


RAIZ = Path(__file__).resolve().parents[1]


class TestArtefatosSQL(unittest.TestCase):
    def test_modelo_possui_tres_tabelas_e_duas_chaves_estrangeiras(self) -> None:
        sql = (RAIZ / "sql" / "01_criacao_tabelas.sql").read_text(encoding="utf-8").upper()
        self.assertIn("CREATE TABLE IF NOT EXISTS ADOTANTES", sql)
        self.assertIn("CREATE TABLE IF NOT EXISTS ANIMAIS", sql)
        self.assertIn("CREATE TABLE IF NOT EXISTS ADOCOES", sql)
        self.assertGreaterEqual(sql.count("FOREIGN KEY"), 2)
        self.assertIn("UNIQUE (ID_ANIMAL)", sql)

    def test_relatorio_de_sumarizacao_usa_group_by(self) -> None:
        sql = (
            RAIZ / "src" / "sql" / "relatorio_adocoes_por_especie.sql"
        ).read_text(encoding="utf-8").upper()
        self.assertIn("GROUP BY", sql)
        self.assertIn("COUNT(", sql)
        self.assertIn("SUM(", sql)

    def test_relatorio_detalhado_usa_juncoes(self) -> None:
        sql = (
            RAIZ / "src" / "sql" / "relatorio_adocoes_detalhadas.sql"
        ).read_text(encoding="utf-8").upper()
        self.assertGreaterEqual(sql.count("INNER JOIN"), 2)


if __name__ == "__main__":
    unittest.main()

