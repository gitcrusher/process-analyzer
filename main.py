from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont
from sidebar import Sidebar
from content_area import ContentArea

class FuturisticDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing FuturisticDashboard...")
        self.setWindowTitle("Process Analyzer")
        self.setGeometry(100, 100, 1200, 600)
        print("Main window geometry set.")

        # Load custom font
        font_db = QFontDatabase()
        # Update the font path to the actual path of your font file
        # Example: "C:/Users/hp/PycharmProjects/process analyzer/fonts/YourFont.ttf"
        font_id = font_db.addApplicationFont("path/to/your/font.ttf")  # Replace with actual font path
        if font_id != -1:
            font_families = font_db.applicationFontFamilies(font_id)
            if font_families:
                self.custom_font = QFont(font_families[0], 12)
                print(f"Font loaded successfully: {font_families[0]}")
            else:
                print("Font families not found, using default font.")
                self.custom_font = QFont("Arial", 12)
        else:
            print("Failed to load font, using default font.")
            self.custom_font = QFont("Arial", 12)

        self.setFont(self.custom_font)

        # Main layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        print("Main layout created.")

        # Sidebar
        self.sidebar = Sidebar(self)
        self.main_layout.addWidget(self.sidebar)
        print("Sidebar added to layout.")

        # Content Area
        self.content_area = ContentArea(self)
        self.main_layout.addWidget(self.content_area)
        print("Content area added to layout.")

        # Connect signals
        self.sidebar.button_clicked.connect(self.content_area.load_page)
        self.sidebar.theme_toggled.connect(self.content_area.toggle_theme)
        print("Signals connected.")

        print("FuturisticDashboard initialization completed.")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = FuturisticDashboard()
    window.show()
    print("Main window shown.")
    sys.exit(app.exec_())