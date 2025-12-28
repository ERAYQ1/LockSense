import sys
import secrets
import string
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                             QProgressBar, QFrame, QScrollArea)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QFont, QColor, QPalette, QIcon, QClipboard

from ai_analyzer import AIAnalyzer
from ui_components import RadarChartWidget
from translations import TRANSLATIONS


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

    def set_state(self, checked: bool, is_dark: bool):
        # Renkleri temaya göre belirle
        success_color = "#2ecc71"
        pending_color = "#555" if is_dark else "#cbd5e1"
        text_active = "#eee" if is_dark else "#334155"
        text_inactive = "#777" if is_dark else "#94a3b8"

        if checked:
            self.icon_label.setText("●")
            self.icon_label.setStyleSheet(f"color: {success_color}; font-weight: bold;")
            self.text_label.setStyleSheet(f"color: {text_active}; font-size: 13px;")
        else:
            self.icon_label.setText("○")
            self.icon_label.setStyleSheet(f"color: {pending_color}; font-weight: bold;")
            self.text_label.setStyleSheet(f"color: {text_inactive}; font-size: 13px;")

class LockSenseUI(QMainWindow):
    """
    Premium Dark Edition UI.
    Real-time analysis, animations and modern aesthetics.
    """
    
    def __init__(self, lang="en"):
        super().__init__()
        self.lang = lang
        self.texts = TRANSLATIONS[lang]
        self.analyzer = AIAnalyzer(lang)
        self.is_dark = True
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("LockSense AI")
        self.setMinimumSize(QSize(450, 700))
        
        # Main Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none;")
        self.setCentralWidget(self.scroll)
        
        # Responsive Container (Centered)
        self.container = QWidget()
        self.scroll.setWidget(self.container)
        
        # Layouts
        self.outer_layout = QVBoxLayout(self.container)
        self.outer_layout.setAlignment(Qt.AlignHCenter)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        
        self.inner_widget = QWidget()
        self.inner_widget.setFixedWidth(450)
        self.outer_layout.addWidget(self.inner_widget)
        
        self.main_layout = QVBoxLayout(self.inner_widget)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header with Theme Toggle
        header_hbox = QHBoxLayout()
        
        self.header_vbox = QVBoxLayout()
        self.title = QLabel(self.texts["title"])
        self.title.setFont(QFont("Inter", 22, QFont.Bold))
        
        self.subtitle = QLabel(self.texts["subtitle"])
        self.subtitle.setFont(QFont("Inter", 10))
        
        self.header_vbox.addWidget(self.title)
        self.header_vbox.addWidget(self.subtitle)
        header_hbox.addLayout(self.header_vbox)
        header_hbox.addStretch()
        
        self.btn_theme = QPushButton("Dark")
        self.btn_theme.setCursor(Qt.PointingHandCursor)
        self.btn_theme.setFixedSize(60, 30)
        self.btn_theme.clicked.connect(self.toggle_theme)
        header_hbox.addWidget(self.btn_theme)
        
        self.main_layout.addLayout(header_hbox)
        
        # Input Area
        self.input_container = QWidget()
        input_vbox = QVBoxLayout(self.input_container)
        input_vbox.setContentsMargins(0, 0, 0, 0)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText(self.texts["input_placeholder"])
        self.password_input.setMinimumHeight(55)
        self.password_input.textChanged.connect(self.on_text_changed)
        input_vbox.addWidget(self.password_input)
        
        # Action Buttons
        actions_layout = QHBoxLayout()
        self.btn_generate = QPushButton(self.texts["generate"])
        self.btn_generate.setCursor(Qt.PointingHandCursor)
        self.btn_generate.clicked.connect(self.generate_password)
        
        self.btn_toggle = QPushButton(self.texts["show"])
        self.btn_toggle.setCheckable(True)
        self.btn_toggle.setCursor(Qt.PointingHandCursor)
        self.btn_toggle.clicked.connect(self.toggle_visibility)
        
        actions_layout.addWidget(self.btn_generate)
        actions_layout.addStretch()
        actions_layout.addWidget(self.btn_toggle)
        input_vbox.addLayout(actions_layout)
        self.main_layout.addWidget(self.input_container)
        
        # Progress & Score
        score_container = QWidget()
        score_layout = QVBoxLayout(score_container)
        self.status_label = QLabel(self.texts["ready"])
        self.status_label.setAlignment(Qt.AlignCenter)
        score_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        score_layout.addWidget(self.progress_bar)
        
        self.entropy_label = QLabel(f"{self.texts['entropy']}: 0.00 bits")
        self.entropy_label.setAlignment(Qt.AlignCenter)
        score_layout.addWidget(self.entropy_label)
        self.main_layout.addWidget(score_container)
        
        # Radar Chart
        self.radar_chart = RadarChartWidget()
        # Update Chart Labels
        self.radar_chart.labels = [
            self.texts["chart_len"], self.texts["chart_var"], 
            self.texts["chart_ent"], self.texts["chart_uni"], self.texts["chart_saf"]
        ]
        self.main_layout.addWidget(self.radar_chart, alignment=Qt.AlignCenter)
        
        # Checklist
        self.checks_frame = QFrame()
        checks_vbox = QVBoxLayout(self.checks_frame)
        checks_vbox.setContentsMargins(20, 20, 20, 20)
        
        self.req_len = RequirementItem(self.texts["req_len"])
        self.req_up = RequirementItem(self.texts["req_up"])
        self.req_lo = RequirementItem(self.texts["req_lo"])
        self.req_num = RequirementItem(self.texts["req_num"])
        self.req_spec = RequirementItem(self.texts["req_spec"])
        self.req_safe = RequirementItem(self.texts["req_safe"])
        
        for item in [self.req_len, self.req_up, self.req_lo, self.req_num, self.req_spec, self.req_safe]:
            checks_vbox.addWidget(item)
        self.main_layout.addWidget(self.checks_frame)
        
        # Copy Button
        self.btn_copy = QPushButton(self.texts["copy"])
        self.btn_copy.setMinimumHeight(45)
        self.btn_copy.setCursor(Qt.PointingHandCursor)
        self.btn_copy.clicked.connect(self.copy_to_clipboard)
        self.main_layout.addWidget(self.btn_copy)
        
        self.main_layout.addStretch()
        
        # Apply Initial Theme
        self.apply_theme()

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.btn_theme.setText("Dark" if self.is_dark else "Light")
        self.apply_theme()
        # Repaint existing state
        self.on_text_changed(self.password_input.text())

    def apply_theme(self):
        if self.is_dark:
            bg_color = "#0f172a"
            card_bg = "#1e293b"
            border_color = "#334155"
            text_main = "#f8fafc"
            text_sub = "#94a3b8"
            input_focus = "#38bdf8"
        else:
            bg_color = "#f8fafc"
            card_bg = "#ffffff"
            border_color = "#e2e8f0"
            text_main = "#0f172a"
            text_sub = "#64748b"
            input_focus = "#0284c7"

        self.setStyleSheet(f"background-color: {bg_color};")
        self.container.setStyleSheet(f"background-color: {bg_color};")
        
        self.title.setStyleSheet(f"color: {text_main}; letter-spacing: 2px;")
        self.subtitle.setStyleSheet(f"color: {text_sub}; letter-spacing: 4px;")
        
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {card_bg};
                border: 2px solid {border_color};
                border-radius: 12px;
                padding: 0 15px;
                color: {text_main};
                font-size: 18px;
            }}
            QLineEdit:focus {{ border-color: {input_focus}; }}
        """)
        
        btn_style = f"color: {input_focus}; background: transparent; border: none; font-weight: bold;"
        self.btn_toggle.setStyleSheet(btn_style)
        self.btn_generate.setStyleSheet(btn_style.replace(input_focus, text_sub))
        
        self.btn_theme.setStyleSheet(f"""
            QPushButton {{
                background-color: {card_bg};
                color: {text_main};
                border: 1px solid {border_color};
                border-radius: 6px;
                font-size: 11px;
            }}
            QPushButton:hover {{ background-color: {border_color}; }}
        """)
        
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{ background-color: {card_bg}; border-radius: 3px; border: none; }}
            QProgressBar::chunk {{ border-radius: 3px; }}
        """)
        
        self.checks_frame.setStyleSheet(f"background-color: {card_bg}; border-radius: 12px; border: 1px solid {border_color};")
        
        self.btn_copy.setStyleSheet(f"""
            QPushButton {{
                background-color: {text_main};
                color: {bg_color};
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{ opacity: 0.8; }}
        """)
        
        self.entropy_label.setStyleSheet(f"color: {text_sub}; font-size: 11px;")
        
        self.radar_chart.set_theme(self.is_dark)

    def toggle_visibility(self):
        if self.btn_toggle.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.btn_toggle.setText(self.texts["hide"])
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.btn_toggle.setText(self.texts["show"])

    def generate_password(self):
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        pwd = ''.join(secrets.choice(alphabet) for _ in range(16))
        self.password_input.setText(pwd)

    def copy_to_clipboard(self):
        cb = QApplication.clipboard()
        cb.setText(self.password_input.text())
        
        old_text = self.btn_copy.text()
        self.btn_copy.setText(self.texts["copied"])
        QTimer.singleShot(1500, lambda: self.btn_copy.setText(old_text))

    def on_text_changed(self, text):
        result = self.analyzer.analyze(text, lang=self.lang)
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
        self.req_len.set_state(checks['length'], self.is_dark)
        self.req_up.set_state(checks['upper'], self.is_dark)
        self.req_lo.set_state(checks['lower'], self.is_dark)
        self.req_num.set_state(checks['digit'], self.is_dark)
        self.req_spec.set_state(checks['special'], self.is_dark)
        self.req_safe.set_state(checks['common'], self.is_dark)

        # Update Entropy
        self.entropy_label.setText(f"{self.texts['entropy']}: {result.get('entropy', 0):.2f} bits")

        # Update Radar Chart
        self.radar_chart.animate_to(result.get("metrics", {}))
