from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QSize, QRectF
from PyQt5.QtGui import QPainter, QPen, QColor

class CircularProgressBar(QFrame):
    def __init__(self, title, value, subtitle, parent=None):
        super().__init__(parent)
        print(f"Initializing CircularProgressBar: title={title}, value={value}, subtitle={subtitle}")
        self.title = title
        self.value = int(value.rstrip('%'))  # Remove '%' and convert to int
        self.subtitle = subtitle

        self.setStyleSheet("""
            QFrame {
                background-color: #1E1E2F;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        self.setFixedSize(150, 150)  # Fixed size for consistency

        # Layout for labels
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title label
        self.title_label = QLabel(title, self)
        self.title_label.setStyleSheet("color: #00FFD1; font-size: 16px;")
        layout.addWidget(self.title_label)

        # Percentage label (will be updated by paintEvent)
        self.percentage_label = QLabel(f"{self.value}%", self)
        self.percentage_label.setStyleSheet("color: #FF69B4; font-size: 20px; font-weight: bold;")
        layout.addWidget(self.percentage_label, alignment=Qt.AlignCenter)

        # Subtitle label
        self.subtitle_label = QLabel(subtitle, self)
        self.subtitle_label.setStyleSheet("color: #AAAAAA; font-size: 12px;")
        layout.addWidget(self.subtitle_label, alignment=Qt.AlignCenter)

        print(f"CircularProgressBar size: {self.size()}")

    def paintEvent(self, event):
        print(f"Rendering CircularProgressBar: title={self.title}, event={event}")
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.Antialiasing)
            # Define the rectangle for the circular progress
            rect = QRectF(25, 40, 100, 100)  # Centered within the widget

            # Background arc (full semi-circle)
            pen = QPen(QColor("#555555"), 10)
            painter.setPen(pen)
            painter.drawArc(rect, 0, 180 * 16)  # 180 degrees (semi-circle)

            # Progress arc
            progress_color = QColor("#FF69B4")  # Pink for progress
            pen = QPen(progress_color, 10)
            painter.setPen(pen)
            span_angle = min(max(self.value, 0), 100) / 100.0 * 180 * 16  # Clamp value between 0 and 100
            painter.drawArc(rect, 0, -int(span_angle))  # Negative to draw clockwise
            print(f"Progress arc drawn: value={self.value}, span_angle={span_angle}")
        except Exception as e:
            print(f"Error in paintEvent: {e}")
        finally:
            painter.end()
            print("Painter ended successfully")

    def update_theme(self, is_light_theme):
        print(f"Updating theme for CircularProgressBar: title={self.title}")
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
        self.title_label.setStyleSheet(f"color: {text_color}; font-size: 16px;")
        self.percentage_label.setStyleSheet("color: #FF69B4; font-size: 20px; font-weight: bold;")
        self.subtitle_label.setStyleSheet(f"color: {secondary_text_color}; font-size: 12px;")
        self.update()  # Force repaint for the progress arc