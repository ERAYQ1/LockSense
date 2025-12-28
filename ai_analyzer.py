import re
import math
from password_rules import PasswordRules
from translations import TRANSLATIONS

class AIAnalyzer:
    """
    Şifre gücünü analiz eden heuirstic (sezgisel) AI motoru.
    Ağırlıklı puanlama sistemi ve bulanık mantık eşikleri kullanır.
    """
    
    def __init__(self, lang="en"):
        self.rules = PasswordRules()
        self.lang = lang
        self.texts = TRANSLATIONS.get(lang, TRANSLATIONS["en"])

    def analyze(self, password: str, lang=None) -> dict:
        """
        Şifreyi analiz eder ve detaylı bir rapor döner.
        """
        if lang:
            self.lang = lang
            self.texts = TRANSLATIONS.get(lang, TRANSLATIONS["en"])

        if not password:
            return {
                "score": 0, 
                "status": self.texts["ready"], 
                "suggestions": [self.texts["empty_msg"]],
                "checks": {
                    "length": False, "upper": False, "lower": False, 
                    "digit": False, "special": False, "common": False
                }
            }

        score = 0
        suggestions = []
        
        # 1. Uzunluk Analizi (30 Puan)
        length = len(password)
        if length >= self.rules.DESIRED_LENGTH:
            score += 30
        elif length >= self.rules.MIN_LENGTH:
            score += 15
            suggestions.append(self.texts["sugg_len_long"])
        else:
            suggestions.append(self.texts["sugg_len_short"])

        # 2. Karakter Çeşitliliği Analizi (40 Puan)
        diversity_score = 0
        if self.rules.HAS_UPPER.search(password):
            diversity_score += 10
        else:
            suggestions.append(self.texts["sugg_up"])
            
        if self.rules.HAS_LOWER.search(password):
            diversity_score += 10
        else:
            suggestions.append(self.texts["sugg_lo"])
            
        if self.rules.HAS_DIGIT.search(password):
            diversity_score += 10
        else:
            suggestions.append(self.texts["sugg_num"])
            
        if self.rules.HAS_SPECIAL.search(password):
            diversity_score += 10
        else:
            suggestions.append(self.texts["sugg_spec"])
            
        score += diversity_score

        # 3. Yaygın Şifre Kontrolü (-50 Puan Ceza)
        if password.lower() in self.rules.COMMON_PASSWORDS:
            score -= 50
            suggestions.append(self.texts["sugg_common"])

        # 5. Shannon Entropisi Analizi
        entropy = self._calculate_entropy(password)
        
        # Puan Sınırlandırma (0 - 100)
        score = max(0, min(100, score))
        
        # Durum Belirleme (AI Karar Mekanizması)
        status = self._get_status(score)
        
        if score == 100:
            suggestions = [self.texts["excellent"]]

        # Kontrol Listesi Durumu (UI için)
        checks = {
            "length": length >= self.rules.MIN_LENGTH,
            "upper": bool(self.rules.HAS_UPPER.search(password)),
            "lower": bool(self.rules.HAS_LOWER.search(password)),
            "digit": bool(self.rules.HAS_DIGIT.search(password)),
            "special": bool(self.rules.HAS_SPECIAL.search(password)),
            "common": password.lower() not in self.rules.COMMON_PASSWORDS if password else False
        }

        # 6. Radar Grafik Metrikleri (0.0 - 1.0)
        metrics = {
            "length": min(1.0, length / 16),
            "variety": (bool(self.rules.HAS_UPPER.search(password)) + 
                        bool(self.rules.HAS_LOWER.search(password)) + 
                        bool(self.rules.HAS_DIGIT.search(password)) + 
                        bool(self.rules.HAS_SPECIAL.search(password))) / 4,
            "entropy": min(1.0, entropy / 128) if length > 0 else 0, # 128 bit ideal kabul edildi
            "uniqueness": len(set(password)) / length if length > 0 else 0,
            "safety": 0.0 if password.lower() in self.rules.COMMON_PASSWORDS else 1.0
        }

        return {
            "score": score,
            "status": status,
            "suggestions": suggestions,
            "checks": checks,
            "entropy": round(entropy, 2),
            "metrics": metrics
        }

    def _calculate_entropy(self, password: str) -> float:
        """
        Şifrenin Shannon Entropisini hesaplar.
        H = -sum(p_i * log2(p_i))
        """
        if not password:
            return 0.0
        
        length = len(password)
        frequencies = {}
        for char in password:
            frequencies[char] = frequencies.get(char, 0) + 1
            
        entropy = 0.0
        for count in frequencies.values():
            p_i = count / length
            entropy -= p_i * math.log2(p_i)
            
        # Toplam bit gücü (H * uzunluk)
        return entropy * length

    def _get_status(self, score: int) -> str:
        """Puan değerine göre metinsel durum döner."""
        if score < 40:
            return self.texts["weak"]
        elif score < 75:
            return self.texts["medium"]
        else:
            return self.texts["strong"]
