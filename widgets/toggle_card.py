from PyQt5.QtWidgets import QFrame, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class ToggleCard(QFrame):
    def __init__(self, title, toggle_text, toggle_state, parent=None):
        super().__init__(parent)
        print(f"Initializing ToggleCard: title={title}, toggle_text={toggle_text}, toggle_state={toggle_state}")
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

        title_label = QLabel(title, self)
        title_label.setStyleSheet("color: #00FFD1; font-size: 16px;")
        layout.addWidget(title_label)

        toggle_button = QPushButton(self)
        toggle_button.setCheckable(True)
        toggle_button.setChecked(toggle_state)
        toggle_button.setFixedSize(40, 20)
        toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                border: 2px solid #555555;
                border-radius: 10px;
            }
        """)
        self.slider = QFrame(toggle_button)
        self.slider.setFixedSize(16, 16)
        self.slider.setStyleSheet("""
            QFrame {
                background-color: #00FFD1;
                border-radius: 8px;
            }
        """)
        self.slider.move(2 if not toggle_state else 22, 2)
        layout.addWidget(toggle_button)

        toggle_label = QLabel(toggle_text, self)
        toggle_label.setStyleSheet("color: #AAAAAA; font-size: 12px;")
        layout.addWidget(toggle_label)

        self.setMinimumSize(300, 80)
        self.setMaximumHeight(80)
        print(f"ToggleCard size: {self.size()}")

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
                item.setStyleSheet(f"color: {text_color if i == 0 else secondary_text_color}; font-size: {16 if i == 0 else 12}px;")
            elif isinstance(item, QPushButton):
                item.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {'#CCCCCC' if is_light_theme else '#333333'};
                        border: 2px solid {'#AAAAAA' if is_light_theme else '#555555'};
                        border-radius: 10px;
                    }}
                """)
                for child in item.children():
                    if isinstance(child, QFrame):
                        child.setStyleSheet(f"""
                            QFrame {{
                                background-color: {'#00FF00' if is_light_theme else '#00FFD1'};
                                border-radius: 8px;
                            }}
                        """)