from PyQt5.QtWidgets import QFrame, QPushButton, QVBoxLayout
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, pyqtSignal, Qt
from PyQt5.QtGui import QFont

class Sidebar(QFrame):
    page_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        print("Initializing Sidebar...")

        # Sidebar properties
        self.sidebar_width = 250
        self.compressed_width = 50
        self.setMinimumWidth(self.compressed_width)
        self.setMaximumWidth(self.compressed_width)
        self.setStyleSheet("""
            background-color: #333333;
            color: #FFFFFF;
            border-right: 2px solid white; /* Thin white border for dark theme */
        """)
        print("Sidebar width set to 50px initially.")

        # Font settings
        self.setFont(QFont("Roboto", 14))
        print("Font set for Sidebar.")

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a clean look
        print("Main layout created.")

        # Toggle button
        self.toggle_button = QPushButton("≡", self)
        self.toggle_button.setFont(self.font())
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: blue;
                color: white;
                border: none;
                padding: 10px;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: #2C2C3E; /* Default hover effect for dark theme */
            }
        """)
        self.toggle_button.setFixedSize(50, 50)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        self.main_layout.addWidget(self.toggle_button, alignment=Qt.AlignTop | Qt.AlignLeft)
        print("Toggle button added.")

        # Navigation container
        self.nav_container = QFrame(self)
        self.nav_container.setStyleSheet("background-color: transparent;")
        self.button_layout = QVBoxLayout(self.nav_container)
        self.button_layout.setAlignment(Qt.AlignTop)
        self.create_buttons()
        self.main_layout.addWidget(self.nav_container)
        self.main_layout.addStretch()
        self.nav_container.setVisible(False)
        print("Navigation container initially hidden.")

    def create_buttons(self):
        """Create sidebar buttons."""
        print("Creating sidebar buttons...")
        options = ["Home", "Performance", "System"]
        for option in options:
            button = QPushButton(option, self)
            button.setFont(self.font())
            button.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 15px;
                    border: none;
                    background-color: transparent;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #2C2C3E; /* Default hover effect for dark theme */
                }
            """)
            button.clicked.connect(lambda _, page=option: self.page_changed.emit(page))
            self.button_layout.addWidget(button)
            print(f"Button '{option}' created.")
        print("Sidebar buttons added to container.")

    def toggle_sidebar(self):
        """Toggle the sidebar between expanded and compressed states."""
        print("Toggling sidebar...")
        current_width = self.width()
        is_compressed = current_width <= self.compressed_width
        new_width = self.sidebar_width if is_compressed else self.compressed_width

        # Animate the width change
        self.min_anim = QPropertyAnimation(self, b"minimumWidth")
        self.max_anim = QPropertyAnimation(self, b"maximumWidth")
        for anim in (self.min_anim, self.max_anim):
            anim.setDuration(300)
            anim.setStartValue(current_width)
            anim.setEndValue(new_width)
            anim.setEasingCurve(QEasingCurve.InOutQuart)
            anim.start()

        def on_animation_finished():
            self.nav_container.setVisible(new_width > self.compressed_width)
            print(f"Animation finished. New width: {self.width()}, Nav visible: {self.nav_container.isVisible()}")

        self.max_anim.finished.connect(on_animation_finished)

    def update_theme(self, is_light_theme):
        """Update the sidebar's styling based on the theme."""
        border_color = "black" if is_light_theme else "white"
        hover_color = "#F0F0F0" if is_light_theme else "#2C2C3E"  # Very light grey for light mode, dark grey for dark mode

        self.setStyleSheet(f"""
            background-color: {'#D0D0D0' if is_light_theme else '#333333'};
            color: {'#000000' if is_light_theme else '#FFFFFF'};
            border-right: 2px solid {border_color}; /* Thin border with theme-relative color */
        """)

        # Update hover effect for all buttons
        for i in range(self.button_layout.count()):
            button = self.button_layout.itemAt(i).widget()
            if button:
                button.setStyleSheet(f"""
                    QPushButton {{
                        text-align: left;
                        padding: 15px;
                        border: none;
                        background-color: transparent;
                        font-size: 16px;
                    }}
                    QPushButton:hover {{
                        background-color: {hover_color}; /* Theme-relative hover color */
                    }}
                """)
        print(f"Sidebar updated for {'light' if is_light_theme else 'dark'} theme.")