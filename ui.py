import sys
import secrets
import string
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                             QProgressBar, QFrame, QScrollArea)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QFont, QColor, QPalette, QIcon, QClipboard

from ai_analyzer import AIAnalyzer

class RequirementItem(QFrame):
    """Gereksinim kontrol listesi öğesi."""
    def __init__(self, text):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.icon_label = QLabel("○") # Pending
        self.icon_label.setFixedWidth(20)
        self.icon_label.setStyleSheet("color: #555; font-weight: bold;")
        
        self.text_label = QLabel(text)
        self.text_label.setStyleSheet("color: #aaa; font-size: 13px;")
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        layout.addStretch()
        
        self.setStyleSheet("border: none;")

    def set_state(self, checked: bool):
        if checked:
            self.icon_label.setText("●")
            self.icon_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
            self.text_label.setStyleSheet("color: #eee; font-size: 13px;")
        else:
            self.icon_label.setText("○")
            self.icon_label.setStyleSheet("color: #555; font-weight: bold;")
            self.text_label.setStyleSheet("color: #777; font-size: 13px;")

class LockSenseUI(QMainWindow):
    """
    Premium Dark Edition UI.
    Real-time analysis, animations and modern aesthetics.
    """
    
    def __init__(self):
        super().__init__()
        self.analyzer = AIAnalyzer()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("LockSense AI")
        self.setMinimumSize(QSize(450, 700))
        self.setStyleSheet("background-color: #0f172a;") # Deep Dark Blue
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("LOCKSENSE AI")
        title.setFont(QFont("Inter", 22, QFont.Bold))
        title.setStyleSheet("color: #f8fafc; letter-spacing: 2px;")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("SECURE PASS ANALYZER")
        subtitle.setFont(QFont("Inter", 10))
        subtitle.setStyleSheet("color: #94a3b8; letter-spacing: 4px;")
        subtitle.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)
        
        # Input Area
        input_container = QWidget()
        input_vbox = QVBoxLayout(input_container)
        input_vbox.setContentsMargins(0, 0, 0, 0)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password...")
        self.password_input.setMinimumHeight(55)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e293b;
                border: 2px solid #334155;
                border-radius: 12px;
                padding: 0 15px;
                color: #f1f5f9;
                font-size: 18px;
            }
            QLineEdit:focus {
                border-color: #38bdf8;
            }
        """)
        self.password_input.textChanged.connect(self.on_text_changed)
        input_vbox.addWidget(self.password_input)
        
        # Action Buttons
        actions_layout = QHBoxLayout()
        
        self.btn_toggle = QPushButton("Show")
        self.btn_toggle.setCheckable(True)
        self.btn_toggle.setCursor(Qt.PointingHandCursor)
        self.btn_toggle.clicked.connect(self.toggle_visibility)
        self.btn_toggle.setStyleSheet("color: #38bdf8; background: transparent; border: none; font-weight: bold;")
        
        self.btn_generate = QPushButton("Generate")
        self.btn_generate.setCursor(Qt.PointingHandCursor)
        self.btn_generate.clicked.connect(self.generate_password)
        self.btn_generate.setStyleSheet("color: #94a3b8; background: transparent; border: none; font-weight: bold;")
        
        actions_layout.addWidget(self.btn_generate)
        actions_layout.addStretch()
        actions_layout.addWidget(self.btn_toggle)
        input_vbox.addLayout(actions_layout)
        
        main_layout.addWidget(input_container)
        
        # Progress & Score
        score_container = QWidget()
        score_layout = QVBoxLayout(score_container)
        
        self.status_label = QLabel("READY TO ANALYZE")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #64748b; font-weight: bold; font-size: 14px;")
        score_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1e293b;
                border-radius: 3px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: #64748b;
                border-radius: 3px;
            }
        """)
        score_layout.addWidget(self.progress_bar)
        
        main_layout.addWidget(score_container)
        
        # Checklist
        self.checks_frame = QFrame()
        self.checks_frame.setStyleSheet("background-color: #1e293b; border-radius: 12px; border: 1px solid #334155;")
        checks_vbox = QVBoxLayout(self.checks_frame)
        checks_vbox.setContentsMargins(20, 20, 20, 20)
        
        self.req_len = RequirementItem("Minimum 8 characters")
        self.req_up = RequirementItem("Upper case letters")
        self.req_lo = RequirementItem("Lower case letters")
        self.req_num = RequirementItem("Numbers (0-9)")
        self.req_spec = RequirementItem("Special characters (!@#$)")
        self.req_safe = RequirementItem("Not a common password")
        
        checks_vbox.addWidget(self.req_len)
        checks_vbox.addWidget(self.req_up)
        checks_vbox.addWidget(self.req_lo)
        checks_vbox.addWidget(self.req_num)
        checks_vbox.addWidget(self.req_spec)
        checks_vbox.addWidget(self.req_safe)
        
        main_layout.addWidget(self.checks_frame)
        
        # Copy Button
        self.btn_copy = QPushButton("COPY PASSWORD")
        self.btn_copy.setMinimumHeight(45)
        self.btn_copy.setCursor(Qt.PointingHandCursor)
        self.btn_copy.clicked.connect(self.copy_to_clipboard)
        self.btn_copy.setStyleSheet("""
            QPushButton {
                background-color: #334155;
                color: #f1f5f9;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #475569;
            }
        """)
        main_layout.addWidget(self.btn_copy)
        
        main_layout.addStretch()

    def toggle_visibility(self):
        if self.btn_toggle.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.btn_toggle.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.btn_toggle.setText("Show")

    def generate_password(self):
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        pwd = ''.join(secrets.choice(alphabet) for _ in range(16))
        self.password_input.setText(pwd)

    def copy_to_clipboard(self):
        cb = QApplication.clipboard()
        cb.setText(self.password_input.text())
        
        old_text = self.btn_copy.text()
        self.btn_copy.setText("COPIED!")
        QTimer.singleShot(1500, lambda: self.btn_copy.setText(old_text))

    def on_text_changed(self, text):
        result = self.analyzer.analyze(text)
        self.update_ui(result)

    def update_ui(self, result):
        score = result['score']
        status = result['status']
        checks = result['checks']
        
        # Update labels
        self.status_label.setText(status)
        
        # Color Logic
        color = "#ef4444" # Weak Red
        if score >= 75:
            color = "#22c55e" # Strong Green
        elif score >= 40:
            color = "#eab308" # Medium Yellow
        
        if not self.password_input.text():
            color = "#64748b"
            self.status_label.setText("READY TO ANALYZE")
            
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 14px;")
        
        # Animate Progress Bar
        self.anim = QPropertyAnimation(self.progress_bar, b"value")
        self.anim.setDuration(400)
        self.anim.setStartValue(self.progress_bar.value())
        self.anim.setEndValue(score)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()
        
        # Update Progress Bar Color
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #1e293b;
                border-radius: 3px;
                border: none;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)
        
        # Update Checklist
        self.req_len.set_state(checks['length'])
        self.req_up.set_state(checks['upper'])
        self.req_lo.set_state(checks['lower'])
        self.req_num.set_state(checks['digit'])
        self.req_spec.set_state(checks['special'])
        self.req_safe.set_state(checks['common'])
