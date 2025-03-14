class ThemeManager:
    def __init__(self):
        self.dark_mode = True  # Default to dark mode

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode

    def is_dark_mode(self):
        return self.dark_mode

    def get_theme(self):
        if self.dark_mode:
            return """
                QMainWindow {
                    background-color: black;
                }
                QLabel {
                    color: #FFFFFF;
                }
                QProgressBar {
                    background-color: #111111;
                    border: 2px solid #00FFC3;
                    border-radius: 10px;
                    text-align: center;
                    color: #FFFFFF;
                }
                QProgressBar::chunk {
                    background-color: #00FFC3;
                    border-radius: 10px;
                }
                QTableWidget {
                    background-color: black;
                    color: #FFFFFF;
                    border: 2px solid #00FFC3;
                    gridline-color: #00FFC3;
                }
                QHeaderView::section {
                    background-color: #333333;
                    color: #FFFFFF;
                    border: 1px solid #00FFC3;
                    padding: 4px;
                }
            """
        else:
            return """
                QMainWindow {
                    background-color: white;
                }
                QLabel {
                    color: #000000;
                }
                QProgressBar {
                    background-color: #DDDDDD;
                    border: 2px solid #007ACC;
                    border-radius: 10px;
                    text-align: center;
                    color: #000000;
                }
                QProgressBar::chunk {
                    background-color: #007ACC;
                    border-radius: 10px;
                }
                QTableWidget {
                    background-color: white;
                    color: #000000;
                    border: 2px solid #007ACC;
                    gridline-color: #007ACC;
                }
                QHeaderView::section {
                    background-color: #EEEEEE;
                    color: #000000;
                    border: 1px solid #007ACC;
                    padding: 4px;
                }
            """