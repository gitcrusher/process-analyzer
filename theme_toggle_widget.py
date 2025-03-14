from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSlider
from PyQt5.QtCore import Qt, pyqtSignal

class ThemeToggleWidget(QWidget):
    theme_toggled = pyqtSignal()

    def __init__(self, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignRight)  # Align to the right
        layout.setContentsMargins(0, 10, 20, 10)  # Add padding

        # Slider for Theme Toggle
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMaximumWidth(60)
        self.slider.setMaximum(1)
        self.slider.setValue(1 if self.theme_manager.is_dark_mode() else 0)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #333333;
                height: 20px;
                border-radius: 10px;
            }
            QSlider::handle:horizontal {
                background: #00FFC3;
                width: 20px;
                height: 20px;
                margin: -5px 0;
                border-radius: 10px;
            }
            QSlider::sub-page:horizontal {
                background: #00FFC3;
                border-radius: 10px;
            }
        """)
        self.slider.valueChanged.connect(self.toggle_theme)

        layout.addWidget(self.slider)
        self.setLayout(layout)

    def toggle_theme(self):
        self.theme_manager.toggle_theme()
        self.theme_toggled.emit()