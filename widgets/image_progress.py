from PyQt5.QtWidgets import QFrame, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class ImageProgress(QFrame):
    def __init__(self, title, image, progress, parent=None):
        super().__init__(parent)
        print(f"Initializing ImageProgress: title={title}, image={image}, progress={progress}")
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
        layout.addWidget(self.image_label)

        progress_label = QLabel("Your FPS —", self)
        progress_label.setStyleSheet("color: #AAAAAA; font-size: 12px;")
        layout.addWidget(progress_label)

        progress_frame = QFrame(self)
        progress_frame.setFixedWidth(100)
        progress_frame.setFixedHeight(10)
        progress_frame.setStyleSheet(f"""
            QFrame {{
                background-color: #555555;
                border-radius: 5px;
            }}
        """)
        progress_bar = QFrame(progress_frame)
        progress_bar.setFixedWidth(int(progress * 100 / 100))  # Scale progress to width
        progress_bar.setFixedHeight(10)
        progress_bar.setStyleSheet("""
            QFrame {
                background-color: #00FF00;
                border-radius: 5px;
            }
        """)
        layout.addWidget(progress_frame)

        self.setMinimumSize(300, 80)
        self.setMaximumHeight(80)
        print(f"ImageProgress size: {self.size()}")

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
                if item.text() == "Image Missing":
                    item.setStyleSheet(f"color: {secondary_text_color}; font-size: 14px;")
                else:
                    item.setStyleSheet(f"color: {secondary_text_color}; font-size: 12px;")
            elif isinstance(item, QFrame):
                item.setStyleSheet(f"""
                    QFrame {{
                        background-color: {'#CCCCCC' if is_light_theme else '#555555'};
                        border-radius: 5px;
                    }}
                """)
                for child in item.children():
                    if isinstance(child, QFrame):
                        child.setStyleSheet(f"""
                            QFrame {{
                                background-color: {'#00FF00' if is_light_theme else '#00FF00'};
                                border-radius: 5px;
                            }}
                        """)