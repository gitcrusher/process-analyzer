from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame, QLabel, QHBoxLayout, QProgressBar
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap

class CircularProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: transparent;
            }
            QProgressBar::chunk {
                border-radius: 10px;
                background-color: #FF69B4; /* Pinkish color */
            }
        """)
        self.setFixedSize(80, 80)  # Fixed size for the circular progress bar

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        value = self.value()
        max_value = self.maximum()

        # Draw the outer circle
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#3A3A51"))  # Dark grey background
        painter.drawEllipse(rect)

        # Draw the progress arc
        if value > 0:
            angle = int(360 * (value / max_value))
            painter.setBrush(QColor("#FF69B4"))  # Pinkish color for progress
            painter.drawPie(rect, 90 * 16, -angle * 16)

        # Draw the percentage text
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Roboto", 12))
        painter.drawText(rect, Qt.AlignCenter, f"{value}%")

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Store parent for theme updates
        # Main layout for the Home page
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(20, 20, 20, 20)
        # Gear Section
        self.gear_section = self.create_dropdown_section("MY GEAR (1)", [
            {"type": "gear", "title": "VICTUS Laptop", "image": "victus_laptop.png"}
        ])
        self.layout.addWidget(self.gear_section)
        # Widgets Section (renamed as per image)
        self.widgets_section = self.create_dropdown_section("WIDGETS (7)", [
            {"type": "progress_group", "items": [
                {"title": "CPU", "value": 7, "subtitle": "41°C"},
                {"title": "GPU", "value": 0, "subtitle": "36°C"},
                {"title": "RAM", "value": 94, "subtitle": "14.7GB / 16GB"}
            ]},
            {"type": "image_progress", "title": "OMEN AI BETA", "image": "omen_ai.png", "progress": 50},
            {"type": "icon_text", "title": "RECENT GAMES", "icon": "gamepad.png", "text": "There are no recently played games"},
            {"type": "error", "title": "TOP DEALS", "message": "We encountered some problems...", "button_text": "RETRY"},
            {"type": "error", "title": "GALLERY", "message": "We encountered some problems...", "button_text": "RETRY"},
            {"type": "toggle", "title": "BOOSTER", "toggle_text": "Boost all my games", "toggle_state": True}
        ])
        self.layout.addWidget(self.widgets_section)

    def create_dropdown_section(self, title, items):
        """Create a collapsible dropdown section with cards."""
        section = QFrame(self)
        section.setStyleSheet("""
            QFrame {
                background-color: #2C2C3E;
                border-radius: 10px;
                margin-bottom: 20px;
            }
        """)
        section_layout = QVBoxLayout(section)
        section_layout.setContentsMargins(10, 10, 10, 10)
        # Dropdown header (button with icon placeholder)
        header_button = QPushButton(self)
        header_button.setStyleSheet("""
            QPushButton {
                background-color: #1E1E2F;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border: none;
                padding: 10px;
                border-radius: 5px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #3A3A51;
            }
        """)
        header_button.setCheckable(True)
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel(title, self))  # Title
        header_layout.addStretch()  # Push icon to the right
        header_button.setLayout(header_layout)
        section_layout.addWidget(header_button)
        # Content area (cards with flex layout)
        content_area = QFrame(self)
        content_area.setStyleSheet("background-color: transparent;")
        content_area.setVisible(False)  # Initially collapsed
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)
        content_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        # Add cards to the content area with wrapping
        current_row = QHBoxLayout()
        current_row.setSpacing(10)
        for item in items:
            card = self.create_card(item)
            card.setMaximumWidth(300)  # Set a maximum width for small rectangles
            current_row.addWidget(card)
            # If the row is "full" (e.g., 3 cards), start a new row
            if current_row.count() >= 3:
                content_layout.addLayout(current_row)
                current_row = QHBoxLayout()
                current_row.setSpacing(10)
        # Add the last row if it has any items
        if current_row.count() > 0:
            content_layout.addLayout(current_row)
        section_layout.addWidget(content_area)
        # Toggle visibility of the content area
        def toggle_content():
            is_visible = content_area.isVisible()
            content_area.setVisible(not is_visible)
            header_button.setChecked(not is_visible)
        header_button.clicked.connect(toggle_content)
        return section

    def create_card(self, item):
        """Create a card based on the item type."""
        card = QFrame(self)
        card.setStyleSheet("""
            QFrame {
                background-color: #1E1E2F;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)
        if item["type"] == "gear":
            # Gear card with image and text
            pixmap = QPixmap(item["image"]).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label = QLabel(self)
            image_label.setPixmap(pixmap)
            card_layout.addWidget(image_label)
            card_layout.addWidget(QLabel(item["title"], self), alignment=Qt.AlignCenter)
        elif item["type"] == "progress_group":
            # Progress group card (e.g., CPU, GPU, RAM)
            group_layout = QHBoxLayout()
            group_layout.setSpacing(20)
            for progress_item in item["items"]:
                progress_card = QFrame(self)
                progress_card.setStyleSheet("""
                    QFrame {
                        background-color: transparent;
                        border: none;
                    }
                """)
                progress_layout = QVBoxLayout(progress_card)
                progress_layout.setAlignment(Qt.AlignCenter)
                # Title
                title_label = QLabel(progress_item["title"], self)
                title_label.setStyleSheet("color: #00FFD1; font-size: 14px;")
                progress_layout.addWidget(title_label)
                # Circular progress bar
                progress_bar = CircularProgressBar(self)
                progress_bar.setValue(progress_item["value"])
                progress_layout.addWidget(progress_bar)
                # Subtitle
                subtitle_label = QLabel(progress_item["subtitle"], self)
                subtitle_label.setStyleSheet("color: #AAAAAA; font-size: 12px;")
                progress_layout.addWidget(subtitle_label)
                group_layout.addWidget(progress_card)
            card_layout.addLayout(group_layout)
        elif item["type"] == "image_progress":
            # Image with progress bar (e.g., OMEN AI BETA)
            pixmap = QPixmap(item["image"]).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label = QLabel(self)
            image_label.setPixmap(pixmap)
            card_layout.addWidget(image_label)
            progress_label = QLabel("Your FPS —", self)
            progress_label.setStyleSheet("color: #AAAAAA; font-size: 12px;")
            card_layout.addWidget(progress_label)
            # Simple progress bar (placeholder)
            progress_frame = QFrame(self)
            progress_frame.setFixedWidth(100)
            progress_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: #555555;
                    border-radius: 5px;
                    height: 10px;
                }}
                QFrame::chunk {{
                    background-color: #00FF00;
                    width: {item['progress']}%;
                    border-radius: 5px;
                }}
            """)
            card_layout.addWidget(progress_frame)
        elif item["type"] == "icon_text":
            # Icon with text (e.g., RECENT GAMES)
            pixmap = QPixmap(item["icon"]).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label = QLabel(self)
            image_label.setPixmap(pixmap)
            card_layout.addWidget(image_label)
            text_label = QLabel(item["text"], self)
            text_label.setStyleSheet("color: #AAAAAA; font-size: 14px;")
            card_layout.addWidget(text_label)
        elif item["type"] == "error":
            # Error card with retry button (e.g., TOP DEALS, GALLERY)
            icon_label = QLabel(self)
            icon_label.setPixmap(QPixmap("wrench.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            card_layout.addWidget(icon_label)
            message_label = QLabel(item["message"], self)
            message_label.setStyleSheet("color: #AAAAAA; font-size: 14px;")
            card_layout.addWidget(message_label)
            retry_button = QPushButton(item["button_text"], self)
            retry_button.setStyleSheet("""
                QPushButton {
                    background-color: #555555;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #777777;
                }
            """)
            card_layout.addWidget(retry_button)
        elif item["type"] == "toggle":
            # Toggle card (e.g., BOOSTER)
            icon_label = QLabel(self)
            icon_label.setPixmap(QPixmap("boost.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            card_layout.addWidget(icon_label)
            text_label = QLabel(item["toggle_text"], self)
            text_label.setStyleSheet("color: #AAAAAA; font-size: 14px;")
            card_layout.addWidget(text_label)
            # Simple toggle switch
            toggle_frame = QFrame(self)
            toggle_frame.setFixedSize(40, 20)
            toggle_frame.setStyleSheet("""
                QFrame {
                    background-color: #555555;
                    border-radius: 10px;
                }
            """)
            toggle_slider = QFrame(toggle_frame)
            toggle_slider.setFixedSize(16, 16)
            toggle_slider.setStyleSheet("background-color: #00FF00; border-radius: 8px;")
            toggle_slider.move(22 if not item["toggle_state"] else 2, 2)  # Move to right if Off, left if On
            card_layout.addWidget(toggle_frame)
        return card

    def update_theme(self, is_light_theme):
        """Update the theme of the Home page based on the parent’s theme state."""
        bg_color = "#F0F0F0" if is_light_theme else "#2C2C3E"
        card_bg_color = "#FFFFFF" if is_light_theme else "#1E1E2F"
        header_bg_color = "#E0E0E0" if is_light_theme else "#1E1E2F"
        text_color = "#333333" if is_light_theme else "#00FFD1"
        secondary_text_color = "#666666" if is_light_theme else "#AAAAAA"
        border_color = "black" if is_light_theme else "white"
        hover_color = "#D0D0D0" if is_light_theme else "#3A3A51"

        # Update section styling
        self.setStyleSheet(f"background-color: {bg_color};")
        for section in [self.gear_section, self.widgets_section]:
            section.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg_color};
                    border-radius: 10px;
                    margin-bottom: 20px;
                }}
            """)
            for i in range(section.layout().count()):
                widget = section.layout().itemAt(i).widget()
                if isinstance(widget, QPushButton):  # Header button
                    widget.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {header_bg_color};
                            color: {text_color};
                            font-size: 18px;
                            font-weight: bold;
                            border: none;
                            padding: 10px;
                            border-radius: 5px;
                            text-align: left;
                        }}
                        QPushButton:hover {{
                            background-color: {hover_color};
                        }}
                    """)
                elif isinstance(widget, QFrame) and widget != section:  # Content area
                    for j in range(widget.layout().count()):
                        row_layout = widget.layout().itemAt(j).layout()
                        if row_layout:
                            for k in range(row_layout.count()):
                                card = row_layout.itemAt(k).widget()
                                if card:
                                    card.setStyleSheet(f"""
                                        QFrame {{
                                            background-color: {card_bg_color};
                                            border-radius: 10px;
                                            padding: 15px;
                                        }}
                                    """)
                                    for m in range(card.layout().count()):
                                        item = card.layout().itemAt(m).widget()
                                        if isinstance(item, QLabel):  # Text labels
                                            item.setStyleSheet(f"""
                                                color: {text_color if m == 0 else secondary_text_color};
                                                font-size: 16px;
                                            """)
                                        elif isinstance(item, QPushButton):  # Buttons (e.g., Retry)
                                            item.setStyleSheet(f"""
                                                QPushButton {{
                                                    background-color: {'#CCCCCC' if is_light_theme else '#555555'};
                                                    color: {text_color};
                                                    border: none;
                                                    padding: 5px 10px;
                                                    border-radius: 5px;
                                                }}
                                                QPushButton:hover {{
                                                    background-color: {'#AAAAAA' if is_light_theme else '#777777'};
                                                }}
                                            """)
                                        elif isinstance(item, QFrame):  # Progress or toggle frame
                                            item.setStyleSheet(f"""
                                                QFrame {{
                                                    background-color: {'#CCCCCC' if is_light_theme else '#555555'};
                                                    border-radius: 10px;
                                                }}
                                            """)
                                            for l in range(len(item.children())):
                                                sub_item = item.children()[l]
                                                if isinstance(sub_item, QFrame):  # Toggle slider or progress chunk
                                                    sub_item.setStyleSheet(f"""
                                                        background-color: {'#00FF00' if is_light_theme else '#00FF00'};
                                                        border-radius: 8px;
                                                    """)
        print(f"Home page updated for {'light' if is_light_theme else 'dark'} theme.")