import tkinter as tk
from tkinter import ttk
import psutil
import platform

class ProcessAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Analyzer")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # Create Notebook (Tabbed Interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create Pages
        self.system_vitals_page = ttk.Frame(self.notebook)
        self.system_info_page = ttk.Frame(self.notebook)

        # Add Pages to Notebook
        self.notebook.add(self.system_vitals_page, text="System Vitals")
        self.notebook.add(self.system_info_page, text="System Information")

        # Style Configuration
        style = ttk.Style()
        style.theme_use("clam")  # Use a theme that supports customization
        style.configure("TFrame", background="black")
        style.configure("TLabel", background="black", foreground="white")
        style.configure("TButton", background="gray", foreground="white")

        # System Vitals Page
        self.setup_system_vitals_page()

        # System Information Page
        self.setup_system_info_page()

    def setup_system_vitals_page(self):
        # Create a frame for mode selection
        mode_frame = ttk.Frame(self.system_vitals_page)
        mode_frame.pack(fill=tk.X, pady=10)

        # Mode Buttons
        self.view_mode = tk.StringVar(value="basic")
        basic_button = ttk.Radiobutton(mode_frame, text="Basic View", variable=self.view_mode, value="basic",
                                       command=self.update_system_vitals_view)
        detailed_button = ttk.Radiobutton(mode_frame, text="Detailed View", variable=self.view_mode, value="detailed",
                                          command=self.update_system_vitals_view)
        basic_button.pack(side=tk.LEFT, padx=10)
        detailed_button.pack(side=tk.LEFT, padx=10)

        # Content Frame for System Vitals
        self.vitals_content_frame = ttk.Frame(self.system_vitals_page)
        self.vitals_content_frame.pack(fill=tk.BOTH, expand=True)

        # Initialize with Basic View
        self.update_system_vitals_view()

    def update_system_vitals_view(self):
        # Clear existing content
        for widget in self.vitals_content_frame.winfo_children():
            widget.destroy()

        if self.view_mode.get() == "basic":
            self.display_basic_view()
        else:
            self.display_detailed_view()

    def display_basic_view(self):
        # Basic View: Display CPU and Memory Usage
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_usage = memory.percent

        ttk.Label(self.vitals_content_frame, text=f"CPU Usage: {cpu_usage}%", font=("Arial", 14)).pack(pady=10)
        ttk.Label(self.vitals_content_frame, text=f"Memory Usage: {memory_usage}%", font=("Arial", 14)).pack(pady=10)

    def display_detailed_view(self):
        # Detailed View: Display Per-Process Information
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                cpu_usage = proc.info['cpu_percent']
                memory_usage = proc.info['memory_info'].rss / (1024 * 1024)  # Convert to MB
                processes.append((pid, name, cpu_usage, round(memory_usage, 2)))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Sort processes by CPU usage
        processes.sort(key=lambda x: x[2], reverse=True)

        # Create a Treeview widget
        columns = ('PID', 'Name', 'CPU (%)', 'Memory (MB)')
        tree = ttk.Treeview(self.vitals_content_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for proc in processes[:20]:  # Show top 20 processes
            tree.insert('', 'end', values=proc)

        tree.pack(fill=tk.BOTH, expand=True)

    def setup_system_info_page(self):
        # Display Static System Information
        info_frame = ttk.Frame(self.system_info_page)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        system_info = {
            "OS": platform.system(),
            "OS Version": platform.version(),
            "Processor": platform.processor(),
            "Number of Cores": psutil.cpu_count(logical=True),
            "Total Memory": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB"
        }

        for i, (key, value) in enumerate(system_info.items()):
            ttk.Label(info_frame, text=f"{key}: {value}", font=("Arial", 12)).grid(row=i, column=0, sticky="w", pady=5)

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessAnalyzerApp(root)
    root.mainloop()