import re

class PasswordRules:
    """
    Şifre güvenlik kurallarını ve sabitlerini içeren sınıf.
    Tamamen yerel çalışır ve herhangi bir dış kütüphane gerektirmez.
    """
    
    MIN_LENGTH = 8
    DESIRED_LENGTH = 12
    
    # Karakter setleri kontrolleri için Regex desenleri
    HAS_UPPER = re.compile(r'[A-Z]')
    HAS_LOWER = re.compile(r'[a-z]')
    HAS_DIGIT = re.compile(r'\d')
    HAS_SPECIAL = re.compile(r'[!@#$%^&*(),.?":{}|<>]')
    
    # En yaygın ve zayıf şifreler listesi (Yerel kontrol için)
    # Bu liste gerçek bir uygulamada çok daha geniş tutulabilir.
    COMMON_PASSWORDS = [
        "123456", "password", "12345678", "qwerty", "12345", 
        "123456789", "admin", "password123", "welcome", "login",
        "şifre", "123123", "asdasd", "şifre123", "deneme"
    ]

    @staticmethod
    def get_rules_description():
        """Kuralların insan tarafından okunabilir açıklamasını döner."""
        return [
            f"En az {PasswordRules.MIN_LENGTH} karakter uzunluğunda olmalı.",
            "Büyük ve küçük harf içermeli.",
            "En az bir rakam içermeli.",
            "En az bir özel karakter (!@#$%^&* vb.) içermeli.",
            "Yaygın kullanılan kelimelerden kaçınılmalı."
        ]
