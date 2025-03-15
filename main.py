from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QHBoxLayout
from PyQt5.QtGui import QFontDatabase, QFont
import sys
from sidebar import Sidebar
from content_area import ContentArea

class FuturisticDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing FuturisticDashboard...")

        # Set up the main window
        self.setWindowTitle("Futuristic Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        print("Main window geometry set.")

        # Load custom font
        font_path = "fonts/Roboto/static/Roboto-Regular.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print(f"Error: Failed to load font from {font_path}. Falling back to default font.")
            self.setFont(QFont("Arial", 12))
        else:
            print("Font loaded successfully.")
            self.setFont(QFont("Roboto", 12))

        # Main layout
        self.central_widget = QFrame()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a clean look

        # Add sidebar
        self.sidebar = Sidebar(self)
        self.layout.addWidget(self.sidebar, stretch=0)
        print("Sidebar added to layout.")

        # Add content area
        self.content_area = ContentArea(self)
        self.layout.addWidget(self.content_area, stretch=1)
        print("Content area added to layout.")

        # Connect signals
        self.sidebar.page_changed.connect(self.content_area.load_page)
        self.content_area.theme_changed.connect(self.update_theme)
        print("Signals connected.")

        # Load the Home page by default
        self.content_area.load_page("Home")
        print("Default page 'Home' loaded.")

    def update_theme(self, is_light_theme):
        """Update the theme of the entire dashboard."""
        print(f"Updating theme to {'light' if is_light_theme else 'dark'}")

        # Update central widget background
        self.central_widget.setStyleSheet(
            "background-color: #F0F0F0;" if is_light_theme else "background-color: #121212;"
        )

        # Update sidebar styling
        self.sidebar.update_theme(is_light_theme)

        # Update content area styling
        self.content_area.update_theme()

        print(f"Theme updated to {'light' if is_light_theme else 'dark'}.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use Fusion style for a modern look
    window = FuturisticDashboard()
    window.show()
    sys.exit(app.exec_())