import sys
from PySide6.QtWidgets import QApplication
from ui import LockSenseUI
from language_selector import LanguageSelector

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    main_window = None

    def on_language_selected(lang):
        nonlocal main_window
        main_window = LockSenseUI(lang=lang)
        main_window.show()

    selector = LanguageSelector(on_selected=on_language_selected)
    selector.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
