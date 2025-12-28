import sys
from PySide6.QtWidgets import QApplication
from ui import LockSenseUI

def main():
    """
    Uygulamanın ana giriş noktası.
    """
    app = QApplication(sys.argv)
    
    # Uygulama genel font ayarı
    app.setStyle("Fusion")
    
    window = LockSenseUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
