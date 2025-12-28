from password_rules import PasswordRules

class AIAnalyzer:
    """
    Şifre gücünü analiz eden heuirstic (sezgisel) AI motoru.
    Ağırlıklı puanlama sistemi ve bulanık mantık eşikleri kullanır.
    """
    
    def __init__(self):
        self.rules = PasswordRules()

    def analyze(self, password: str) -> dict:
        """
        Şifreyi analiz eder ve detaylı bir rapor döner.
        
        Args:
            password (str): Analiz edilecek şifre.
            
        Returns:
            dict: {score: int, status: str, suggestions: list}
        """
        if not password:
            return {
                "score": 0, 
                "status": "YOK", 
                "suggestions": ["Lütfen bir şifre giriniz."],
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
            suggestions.append("Şifrenizi biraz daha uzatmak güvenliği artıracaktır.")
        else:
            suggestions.append(f"Şifreniz çok kısa! En az {self.rules.MIN_LENGTH} karakter kullanın.")

        # 2. Karakter Çeşitliliği Analizi (40 Puan)
        diversity_score = 0
        if self.rules.HAS_UPPER.search(password):
            diversity_score += 10
        else:
            suggestions.append("Büyük harf ekleyiniz.")
            
        if self.rules.HAS_LOWER.search(password):
            diversity_score += 10
        else:
            suggestions.append("Küçük harf ekleyiniz.")
            
        if self.rules.HAS_DIGIT.search(password):
            diversity_score += 10
        else:
            suggestions.append("Rakam ekleyiniz.")
            
        if self.rules.HAS_SPECIAL.search(password):
            diversity_score += 10
        else:
            suggestions.append("Özel karakter ekleyiniz.")
            
        score += diversity_score

        # 3. Yaygın Şifre Kontrolü (-50 Puan Ceza)
        if password.lower() in self.rules.COMMON_PASSWORDS:
            score -= 50
            suggestions.append("DİKKAT: Bu çok yaygın bir şifredir, kolayca tahmin edilebilir!")

        # 4. Entropi ve Karmaşıklık Bonusu (30 Puan)
        # Farklı karakter sayısı kontrolü
        unique_chars = len(set(password))
        if unique_chars > length / 2 and length > 4:
            score += 20
        
        # Puan Sınırlandırma (0 - 100)
        score = max(0, min(100, score))
        
        # Durum Belirleme (AI Karar Mekanizması)
        status = self._get_status(score)
        
        if score == 100:
            suggestions = ["Mükemmel şifre! Güvenle kullanabilirsiniz."]

        # Kontrol Listesi Durumu (UI için)
        checks = {
            "length": length >= self.rules.MIN_LENGTH,
            "upper": bool(self.rules.HAS_UPPER.search(password)),
            "lower": bool(self.rules.HAS_LOWER.search(password)),
            "digit": bool(self.rules.HAS_DIGIT.search(password)),
            "special": bool(self.rules.HAS_SPECIAL.search(password)),
            "common": password.lower() not in self.rules.COMMON_PASSWORDS if password else False
        }

        return {
            "score": score,
            "status": status,
            "suggestions": suggestions,
            "checks": checks
        }

    def _get_status(self, score: int) -> str:
        """Puan değerine göre metinsel durum döner."""
        if score < 40:
            return "ZAYIF"
        elif score < 75:
            return "ORTA"
        else:
            return "GÜÇLÜ"
