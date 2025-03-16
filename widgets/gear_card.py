from PyQt5.QtWidgets import QFrame, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class GearCard(QFrame):
    def __init__(self, title, image, parent=None):
        super().__init__(parent)
        print(f"Initializing GearCard with title: {title}, image: {image}")
        self.setStyleSheet("""
            QFrame {
                background-color: #1E1E2F;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.layout.setSpacing(10)

        self.image_label = QLabel(self)
        try:
            pixmap = QPixmap(image).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if pixmap.isNull():
                raise FileNotFoundError(f"Image {image} could not be loaded.")
            self.image_label.setPixmap(pixmap)
            print(f"Image loaded successfully, size: {pixmap.size()}")
        except Exception as e:
            print(f"Error loading image {image}: {e}")
            self.image_label.setText("Image Missing")
            self.image_label.setStyleSheet("color: #AAAAAA; font-size: 14px;")
            self.image_label.setFixedSize(50, 50)  # Ensure the placeholder has a size
            print("Set image_label to 'Image Missing'")
        self.layout.addWidget(self.image_label)
        print(f"image_label size: {self.image_label.size()}")

        self.title_label = QLabel(title, self)
        self.title_label.setStyleSheet("color: #00FFD1; font-size: 16px;")
        self.layout.addWidget(self.title_label, alignment=Qt.AlignLeft)
        print(f"title_label size: {self.title_label.size()}")

        self.setMinimumSize(300, 80)  # Ensure the widget has a minimum size
        self.setMaximumHeight(80)  # Prevent excessive height
        print(f"GearCard minimum size set to: {self.minimumSize()}")

    def update_theme(self, is_light_theme):
        card_bg_color = "#FFFFFF" if is_light_theme else "#1E1E2F"
        text_color = "#333333" if is_light_theme else "#00FFD1"
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {card_bg_color};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        self.title_label.setStyleSheet(f"color: {text_color}; font-size: 16px;")
        if self.image_label.text() == "Image Missing":
            self.image_label.setStyleSheet(f"color: {'#666666' if is_light_theme else '#AAAAAA'}; font-size: 14px;")