from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class LanguageSelector(QWidget):
    """Initial language selection screen."""
    def __init__(self, on_selected):
        super().__init__()
        self.on_selected = on_selected
        self.setWindowTitle("LockSense - Select Language")
        self.setFixedSize(400, 350)
        self.setStyleSheet("background-color: #0f172a; color: white;")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        
        label = QLabel("Choose Language\nDil Seçin / Sprache wählen")
        label.setFont(QFont("Inter", 14, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("margin-bottom: 20px; color: #f8fafc;")
        layout.addWidget(label)
        
        langs = [("Türkçe", "tr"), ("English", "en"), ("Deutsch", "de")]
        for name, code in langs:
            btn = QPushButton(name)
            btn.setFixedSize(220, 50)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1e293b;
                    border: 1px solid #334155;
                    border-radius: 10px;
                    font-size: 14px;
                    color: #f1f5f9;
                }
                QPushButton:hover { 
                    background-color: #38bdf8; 
                    color: #0f172a; 
                    border-color: #38bdf8;
                }
            """)
            btn.clicked.connect(lambda ch, c=code: self.select(c))
            layout.addWidget(btn, alignment=Qt.AlignCenter)

    def select(self, code):
        self.on_selected(code)
        self.close()
