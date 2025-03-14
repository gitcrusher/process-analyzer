from PyQt5.QtWidgets import QFrame, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class Sidebar(QFrame):
    def __init__(self, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        self.is_minimized = False
        self.setup_ui()

    def setup_ui(self):
        # Set Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove padding for full-width buttons
        layout.setSpacing(0)  # No spacing between buttons

        # Hamburger Menu Button
        self.toggle_sidebar_button = QPushButton("≡")  # Three horizontal lines
        self.toggle_sidebar_button.setObjectName("hamburgerButton")  # For styling
        self.toggle_sidebar_button.clicked.connect(self.toggle_sidebar)
        layout.addWidget(self.toggle_sidebar_button, alignment=Qt.AlignCenter)  # Center the button

        # Buttons
        self.basic_button = QPushButton("Basic View")
        self.detailed_button = QPushButton("Detailed View")

        # Add Buttons to Layout
        layout.addWidget(self.basic_button)
        layout.addWidget(self.detailed_button)

        # Spacer
        layout.addStretch()

        # Apply Styles
        self.style_sidebar()
        self.setLayout(layout)

        # Default State: Expanded
        self.setFixedWidth(200)

    def style_sidebar(self):
        # Sidebar Background Color
        background_color = "#333333" if self.theme_manager.is_dark_mode() else "#EEEEEE"
        text_color = "#FFFFFF" if self.theme_manager.is_dark_mode() else "#000000"
        hover_color = "#555555" if self.theme_manager.is_dark_mode() else "#CCCCCC"

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {background_color};
                border: none;
            }}
            QPushButton {{
                background-color: {background_color};
                color: {text_color};
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 14px;
                border-bottom: 1px solid {hover_color};
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton#hamburgerButton {{
                background-color: {background_color};
                color: {text_color};
                border: none;
                padding: 10px;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px; /* Rounded corners for the square */
            }}
            QPushButton#hamburgerButton:hover {{
                background-color: {hover_color};
            }}
        """)

    def toggle_sidebar(self):
        if self.is_minimized:
            # Expand the sidebar
            self.setFixedSize(200, self.height())  # Reset width to expanded size
            self.basic_button.show()
            self.detailed_button.show()
            self.is_minimized = False
        else:
            # Collapse the sidebar into a square
            self.setFixedSize(50, 50)  # Square size: 50x50
            self.basic_button.hide()
            self.detailed_button.hide()
            self.is_minimized = True