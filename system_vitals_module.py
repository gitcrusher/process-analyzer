import psutil
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView

class SystemVitals(QVBoxLayout):
    def __init__(self, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        self.display_basic_view()

    def display_basic_view(self):
        self.clear_layout()

        # CPU Usage
        cpu_label = QLabel("CPU Usage")
        cpu_progress = QProgressBar()
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_progress.setValue(int(cpu_usage))
        cpu_value_label = QLabel(f"{cpu_usage}%")

        self.addWidget(cpu_label)
        self.addWidget(cpu_progress)
        self.addWidget(cpu_value_label)

        # Memory Usage
        memory_label = QLabel("Memory Usage")
        memory_progress = QProgressBar()
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        memory_progress.setValue(int(memory_usage))
        memory_value_label = QLabel(f"{memory_usage}%")

        self.addWidget(memory_label)
        self.addWidget(memory_progress)
        self.addWidget(memory_value_label)

    def clear_layout(self):
        while self.count():
            child = self.takeAt(0)
            if child.widget():
                child.widget().deleteLater()