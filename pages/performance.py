from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class PerformancePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("This is the Performance Page", self)
        label.setStyleSheet("""
            color: #00FFD1;
            font-size: 24px;
        """)
        layout.addWidget(label)