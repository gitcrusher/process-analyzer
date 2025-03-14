import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QFrame, QWidget
from PyQt5.QtCore import Qt
from sidebar_module import Sidebar
from theme_module import ThemeManager
from system_vitals_module import SystemVitals
from theme_toggle_widget import ThemeToggleWidget

class FuturisticAIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Futuristic AI Process Analyzer")
        self.setGeometry(100, 100, 900, 600)

        # Initialize Theme Manager
        self.theme_manager = ThemeManager()

        # Main Layout
        self.main_layout = QHBoxLayout()

        # Sidebar
        self.sidebar = Sidebar(self.theme_manager)
        self.sidebar.setFixedWidth(200)  # Initial width
        self.main_layout.addWidget(self.sidebar)

        # Content Area
        self.content_area = QFrame()
        self.content_layout = SystemVitals(self.theme_manager)
        self.content_area.setLayout(self.content_layout)

        # Add Theme Toggle Widget to Top-Right Corner
        self.setup_theme_toggle()

        # Combine Sidebar and Content Area
        self.main_layout.addWidget(self.content_area)

        # Central Widget
        self.central_widget = QFrame()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def setup_theme_toggle(self):
        # Create a container for the theme toggle widget
        theme_container = QWidget()
        theme_container.setStyleSheet("background-color: transparent;")
        theme_layout = QHBoxLayout(theme_container)

        # Add Theme Toggle Widget
        self.theme_toggle = ThemeToggleWidget(self.theme_manager)
        self.theme_toggle.theme_toggled.connect(self.apply_theme)
        theme_layout.addStretch()  # Push the toggle to the right
        theme_layout.addWidget(self.theme_toggle)

        # Add the theme toggle container to the top of the content area
        self.content_layout.insertWidget(0, theme_container)

    def apply_theme(self):
        self.setStyleSheet(self.theme_manager.get_theme())

# Run the App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FuturisticAIApp()
    window.show()
    sys.exit(app.exec_())