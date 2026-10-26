import unittest
from runtime import servicos as s
from runtime.orqlang_runtime import executar_paralelo

class TestServicos(unittest.TestCase):
    def test_loja(self):
        self.assertEqual(s.buscar_usuario(1), "Ana")
        self.assertEqual(s.aplicar_desconto(s.calcular_total(100, 2), 10), 180.0)

    def test_monitoramento(self):
        self.assertTrue(s.verificar_limite(s.ler_temperatura(102), 60))

    def test_dados(self):
        self.assertEqual(s.calcular_media(s.carregar_valores("a")), 4.0)

    def test_runtime(self):
        self.assertEqual(executar_paralelo([("x", lambda: 2), ("y", lambda: 3)]), {"x": 2, "y": 3})

if __name__ == "__main__":
    unittest.main()
