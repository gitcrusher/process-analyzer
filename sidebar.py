from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class Sidebar(QWidget):
    # Define signals
    button_clicked = pyqtSignal(str)  # Signal emitted when a navigation button is clicked, passes the page name
    theme_toggled = pyqtSignal(bool)  # Signal emitted when the theme toggle button is clicked, passes the theme state

    def __init__(self, parent=None):
        super().__init__(parent)
        print("Initializing Sidebar...")
        self.setFixedWidth(50)
        print("Sidebar width set to 50px initially.")

        # Set font (assuming the parent is FuturisticDashboard with custom_font)
        self.setFont(parent.custom_font if parent and hasattr(parent, 'custom_font') else QFont("Arial", 12))
        print("Font set for Sidebar.")

        # Main layout for the sidebar
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignTop)
        print("Main layout created.")

        # Theme toggle button
        self.toggle_button = QPushButton("☀", self)
        self.toggle_button.setFixedSize(30, 30)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #FFFFFF;
                border: none;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
            QPushButton:checked {
                background-color: #00FFD1;
                color: #000000;
            }
        """)
        self.toggle_button.clicked.connect(self.on_theme_toggled)
        self.layout.addWidget(self.toggle_button, alignment=Qt.AlignCenter)
        print("Toggle button added.")

        # Navigation buttons container
        self.nav_container = QFrame(self)
        self.nav_layout = QVBoxLayout(self.nav_container)
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_layout.setSpacing(10)
        self.nav_layout.setAlignment(Qt.AlignTop)

        print("Creating sidebar buttons...")
        self.buttons = {}
        for page in ["Home", "Performance", "System"]:
            btn = QPushButton(page, self.nav_container)
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1E1E2F;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #3A3A51;
                }
                QPushButton:checked {
                    background-color: #00FFD1;
                    color: #000000;
                }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, p=page: self.on_button_clicked(p))
            self.buttons[page] = btn
            self.nav_layout.addWidget(btn, alignment=Qt.AlignCenter)
            print(f"Button '{page}' created.")

        self.buttons["Home"].setChecked(True)  # Default to Home page
        self.nav_container.setVisible(False)
        print("Sidebar buttons added to container.")
        print("Navigation container initially hidden.")
        self.layout.addWidget(self.nav_container)

        # Expand/collapse sidebar on hover
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.setFixedWidth(200)
        for btn in self.buttons.values():
            btn.setFixedWidth(150)
        self.nav_container.setVisible(True)

    def leaveEvent(self, event):
        self.setFixedWidth(50)
        for btn in self.buttons.values():
            btn.setFixedWidth(30)
        self.nav_container.setVisible(False)

    def on_button_clicked(self, page):
        for btn in self.buttons.values():
            btn.setChecked(False)
        self.buttons[page].setChecked(True)
        print(f"Sidebar button clicked: {page}")
        self.button_clicked.emit(page)  # Emit the signal with the page name

    def on_theme_toggled(self):
        is_light_theme = self.toggle_button.isChecked()
        print(f"Theme toggled: {'Light' if is_light_theme else 'Dark'}")
        self.theme_toggled.emit(is_light_theme)  # Emit the signal with the theme state

    def update_theme(self, is_light_theme):
        bg_color = "#E0E0E0" if is_light_theme else "#1E1E2F"
        btn_bg_color = "#FFFFFF" if is_light_theme else "#1E1E2F"
        btn_text_color = "#333333" if is_light_theme else "#FFFFFF"
        btn_hover_color = "#CCCCCC" if is_light_theme else "#3A3A51"
        self.setStyleSheet(f"background-color: {bg_color};")
        for btn in self.buttons.values():
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {btn_bg_color};
                    color: {btn_text_color};
                    border: none;
                    border-radius: 15px;
                }}
                QPushButton:hover {{
                    background-color: {btn_hover_color};
                }}
                QPushButton:checked {{
                    background-color: #00FFD1;
                    color: #000000;
                }}
            """)
        self.toggle_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#CCCCCC' if is_light_theme else '#555555'};
                color: {'#333333' if is_light_theme else '#FFFFFF'};
                border: none;
                border-radius: 15px;
            }}
            QPushButton:hover {{
                background-color: {'#AAAAAA' if is_light_theme else '#777777'};
            }}
            QPushButton:checked {{
                background-color: #00FFD1;
                color: #000000;
            }}
        """)