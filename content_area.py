from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QScrollArea, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QPoint, QEvent
from PyQt5.QtGui import QFont
from pages.home import HomePage
from pages.performance import PerformancePage
from pages.system import SystemPage

class ThemeToggleButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 20)
        self.setCheckable(True)
        self.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                border: 2px solid #555555;
                border-radius: 10px;
            }
        """)

        self.slider = QFrame(self)
        self.slider.setFixedSize(16, 16)
        self.slider.setStyleSheet("""
            QFrame {
                background-color: #00FFD1;
                border-radius: 8px;
            }
        """)
        self.slider.move(2, 2)

        self.mode_label = QLabel(self)
        self.mode_label.setFont(QFont("Arial", 10))
        self.mode_label.setAlignment(Qt.AlignCenter)
        self.mode_label.setGeometry(0, 0, 40, 20)
        self.update_label_and_color()

        self.clicked.connect(self.animate_toggle)
        self.clicked.connect(self.update_label_and_color)

    def animate_toggle(self):
        self.animation = QPropertyAnimation(self.slider, b"pos")
        self.animation.setDuration(200)
        start_pos = self.slider.pos()
        end_pos = QPoint(22, 2) if self.isChecked() else QPoint(2, 2)
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.start()

    def update_label_and_color(self):
        label_text = "🌙" if not self.isChecked() else "☀"
        text_color = "#FFFFFF" if not self.isChecked() else "#333333"
        self.mode_label.setStyleSheet(f"color: {text_color};")
        self.mode_label.setText(label_text)

class ContentArea(QFrame):
    theme_changed = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        print("Initializing ContentArea...")

        self.is_light_theme = False
        self.setStyleSheet("background-color: #121212;")
        self.setMinimumHeight(600)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.top_layout = QHBoxLayout()
        self.top_layout.addStretch()
        self.theme_toggle = ThemeToggleButton(self)
        self.theme_toggle.clicked.connect(self.toggle_theme)
        self.top_layout.addWidget(self.theme_toggle)
        self.main_layout.addLayout(self.top_layout)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.setStyleSheet("background-color: transparent; border: none;")

        self.content_widget = QWidget(self)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignTop)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.scroll_area.setWidget(self.content_widget)

        self.main_layout.addWidget(self.scroll_area)

        self.load_page("Home")
        print("Default page 'Home' loaded.")

        self.scroll_area.wheelEvent = self.wheel_event

    def wheel_event(self, event):
        if self.scroll_area.isVisible():
            scroll_value = self.scroll_area.verticalScrollBar().value()
            if event.angleDelta().y() > 0:
                self.scroll_area.verticalScrollBar().setValue(scroll_value - 20)
            else:
                self.scroll_area.verticalScrollBar().setValue(scroll_value + 20)
            event.accept()

    def toggle_theme(self):
        self.is_light_theme = not self.is_light_theme
        self.update_theme()
        print(f"Emitting theme_changed: {self.is_light_theme}")
        self.theme_changed.emit(self.is_light_theme)

    def update_theme(self):
        print(f"Updating content area theme to {'light' if self.is_light_theme else 'dark'}")
        self.setStyleSheet("background-color: #F0F0F0;" if self.is_light_theme else "background-color: #121212;")
        for i in range(self.content_layout.count()):
            item = self.content_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, QFrame):
                    for j in range(widget.layout().count()):
                        sub_item = widget.layout().itemAt(j)
                        if sub_item and sub_item.widget() and isinstance(sub_item.widget(), QLabel):
                            sub_item.widget().setStyleSheet(
                                "color: #333333; font-size: 24px;" if self.is_light_theme else "color: #00FFD1; font-size: 24px;"
                            )
        print("Content area theme updated.")

    def load_page(self, page_name):
        print(f"Loading page: {page_name}")
        for i in reversed(range(self.content_layout.count())):
            item = self.content_layout.takeAt(i)
            if item and item.widget():
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()
        self.content_layout.update()

        try:
            if page_name == "Home":
                print("Attempting to instantiate HomePage...")
                page = HomePage(self)
                print("HomePage instantiated successfully.")
            elif page_name == "Performance":
                page = PerformancePage(self)
            elif page_name == "System":
                page = SystemPage(self)
            else:
                page = QLabel(f"Page not found: {page_name}", self)
                page.setStyleSheet(
                    "color: red; font-size: 24px;" if not self.is_light_theme else "color: darkred; font-size: 24px;"
                )

            self.content_layout.addWidget(page, alignment=Qt.AlignTop)
            self.content_layout.addStretch()
            print(f"Page '{page_name}' loaded successfully.")

        except ImportError as e:
            print(f"ImportError in load_page: {e}")
            error_label = QLabel("Error loading page (check imports)", self)
            error_label.setStyleSheet(
                "color: red; font-size: 24px;" if not self.is_light_theme else "color: darkred; font-size: 24px;"
            )
            self.content_layout.addWidget(error_label)

        except Exception as e:
            print(f"Unexpected error in load_page: {e}")
            error_label = QLabel("Error loading page", self)
            error_label.setStyleSheet(
                "color: red; font-size: 24px;" if not self.is_light_theme else "color: darkred; font-size: 24px;"
            )
            self.content_layout.addWidget(error_label)