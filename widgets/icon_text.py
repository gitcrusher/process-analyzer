from PyQt5.QtWidgets import QFrame, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class IconText(QFrame):
    def __init__(self, title, icon, text, parent=None):
        super().__init__(parent)
        print(f"Initializing IconText: title={title}, icon={icon}, text={text}")
        self.setStyleSheet("""
            QFrame {
                background-color: #1E1E2F;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.setSpacing(10)

        self.icon_label = QLabel(self)
        try:
            pixmap = QPixmap(icon).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if pixmap.isNull():
                raise FileNotFoundError(f"Icon {icon} could not be loaded.")
            self.icon_label.setPixmap(pixmap)
            print(f"Icon loaded successfully, size: {pixmap.size()}")
        except Exception as e:
            print(f"Error loading icon {icon}: {e}")
            self.icon_label.setText("Icon Missing")
            self.icon_label.setStyleSheet("color: #AAAAAA; font-size: 14px;")
            self.icon_label.setFixedSize(30, 30)  # Ensure the placeholder has a size
            print("Set icon_label to 'Icon Missing'")
        layout.addWidget(self.icon_label)

        self.text_label = QLabel(text, self)
        self.text_label.setStyleSheet("color: #AAAAAA; font-size: 14px;")
        layout.addWidget(self.text_label)

        self.setMinimumSize(300, 80)
        self.setMaximumHeight(80)
        print(f"IconText size: {self.size()}")

    def update_theme(self, is_light_theme):
        card_bg_color = "#FFFFFF" if is_light_theme else "#1E1E2F"
        text_color = "#333333" if is_light_theme else "#00FFD1"
        secondary_text_color = "#666666" if is_light_theme else "#AAAAAA"
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {card_bg_color};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        self.text_label.setStyleSheet(f"color: {secondary_text_color}; font-size: 14px;")
        if self.icon_label.text() == "Icon Missing":
            self.icon_label.setStyleSheet(f"color: {secondary_text_color}; font-size: 14px;")