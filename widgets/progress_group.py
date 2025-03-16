from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel
from utils import Qt
from widgets.circular_progress import CircularProgressBar

class ProgressGroup(QFrame):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #1E1E2F;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        layout = QHBoxLayout(self)
        layout.setSpacing(20)

        for item in items:
            progress_card = QFrame(self)
            progress_card.setStyleSheet("background-color: transparent; border: none;")
            progress_layout = QVBoxLayout(progress_card)
            progress_layout.setAlignment(Qt.AlignCenter)

            # Title
            title_label = QLabel(item["title"], self)
            title_label.setStyleSheet("color: #00FFD1; font-size: 14px;")
            progress_layout.addWidget(title_label)

            # Circular progress bar
            progress_bar = CircularProgressBar(self)
            progress_bar.setValue(item["value"])
            progress_layout.addWidget(progress_bar)

            # Subtitle
            subtitle_label = QLabel(item["subtitle"], self)
            subtitle_label.setStyleSheet("color: #AAAAAA; font-size: 12px;")
            progress_layout.addWidget(subtitle_label)

            layout.addWidget(progress_card)