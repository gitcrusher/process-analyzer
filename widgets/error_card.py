from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class ErrorCard(QFrame):
    def __init__(self, title, message, button_text, parent=None):
        super().__init__(parent)
        print(f"Initializing ErrorCard: title={title}, message={message}, button_text={button_text}")
        self.setStyleSheet("""
            QFrame {
                background-color: #1E1E2F;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)

        title_label = QLabel(title, self)
        title_label.setStyleSheet("color: #00FFD1; font-size: 16px;")
        layout.addWidget(title_label)

        message_label = QLabel(message, self)
        message_label.setStyleSheet("color: #AAAAAA; font-size: 14px;")
        layout.addWidget(message_label)

        retry_button = QPushButton(button_text, self)
        retry_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #FFFFFF;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
        """)
        layout.addWidget(retry_button)

        self.setMinimumSize(300, 150)
        self.setMaximumHeight(150)
        print(f"ErrorCard size: {self.size()}")

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
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i).widget()
            if isinstance(item, QLabel):
                item.setStyleSheet(f"color: {text_color if i == 0 else secondary_text_color}; font-size: {16 if i == 0 else 14}px;")
            elif isinstance(item, QPushButton):
                item.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {'#CCCCCC' if is_light_theme else '#555555'};
                        color: {'#333333' if is_light_theme else '#FFFFFF'};
                        border: none;
                        padding: 5px 10px;
                        border-radius: 5px;
                    }}
                    QPushButton:hover {{
                        background-color: {'#AAAAAA' if is_light_theme else '#777777'};
                    }}
                """)