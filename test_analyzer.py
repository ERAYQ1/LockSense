import unittest
from ai_analyzer import AIAnalyzer

class TestAIAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = AIAnalyzer()

    def test_empty_password(self):
        result = self.analyzer.analyze("")
        self.assertEqual(result['score'], 0)
        self.assertEqual(result['status'], "YOK")

    def test_weak_password(self):
        result = self.analyzer.analyze("123456")
        self.assertLess(result['score'], 40)
        self.assertEqual(result['status'], "ZAYIF")

    def test_medium_password(self):
        # Uzunluk + Bazı karakter çeşitliliği
        result = self.analyzer.analyze("Password123")
        self.assertGreaterEqual(result['score'], 40)
        self.assertLess(result['score'], 75)
        self.assertEqual(result['status'], "ORTA")

    def test_strong_password(self):
        # Kompleks şifre
        result = self.analyzer.analyze("C0mplex!Passw0rd_2025")
        self.assertGreaterEqual(result['score'], 75)
        self.assertEqual(result['status'], "GÜÇLÜ")

    def test_entropy_calculation(self):
        result = self.analyzer.analyze("aaaaa")
        # Tüm karakterler aynıysa entropi düşük olmalı (0 civarı)
        # Ama bit gücü H * L olduğu için log2(1) = 0 -> 0 * 5 = 0
        self.assertEqual(result['entropy'], 0.0)
        
        result_diff = self.analyzer.analyze("abcde")
        self.assertGreater(result_diff['entropy'], 0.0)

if __name__ == "__main__":
    unittest.main()
