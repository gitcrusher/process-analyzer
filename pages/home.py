from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame, QLabel, QHBoxLayout, QScrollArea, QLayout
from PyQt5.QtCore import Qt, QEvent, QSize, QRect, QPoint
from PyQt5.QtGui import QFont
from widgets import GearCard, CircularProgressBar, ImageProgress, IconText, ErrorCard, ToggleCard

class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)
        self.items = []
        self._in_layout = False  # Flag to prevent recursive calls

    def addItem(self, item):
        self.items.append(item)

    def count(self):
        return len(self.items)

    def itemAt(self, index):
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        if self._in_layout:
            print("Recursive call detected in heightForWidth, returning 0")
            return 0
        self._in_layout = True
        height = self.doLayout(QRect(0, 0, width, 0), True)
        self._in_layout = False
        return height

    def setGeometry(self, rect):
        if self._in_layout:
            print("Recursive call detected in setGeometry, skipping")
            return
        self._in_layout = True
        super().setGeometry(rect)
        self.doLayout(rect, False)
        self._in_layout = False

    def sizeHint(self):
        size = QSize()
        for item in self.items:
            size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def minimumSize(self):
        return self.sizeHint()

    def doLayout(self, rect, test_only=False):
        x = rect.x()
        y = rect.y()
        line_height = 0
        spacing = self.spacing()
        available_width = rect.width() - (self.contentsMargins().left() + self.contentsMargins().right())

        for item in self.items:
            widget = item.widget()
            if widget and widget.property("full_width"):
                if x > rect.x():
                    y += line_height + spacing
                    x = rect.x()
                widget_size = QSize(available_width, widget.sizeHint().height())
                if not test_only:
                    item.setGeometry(QRect(QPoint(x, y), widget_size))
                    print(f"Setting geometry for widget in FlowLayout: x={x}, y={y}, size={widget_size}")
                y += widget_size.height() + spacing
                line_height = 0
                x = rect.x()
            else:
                widget_size = item.sizeHint()
                next_x = x + widget_size.width() + spacing
                if next_x - spacing > rect.right() and line_height > 0:
                    x = rect.x()
                    y += line_height + spacing
                    next_x = x + widget_size.width() + spacing
                    line_height = 0
                if not test_only:
                    item.setGeometry(QRect(QPoint(x, y), widget_size))
                    print(f"Setting geometry for widget in FlowLayout: x={x}, y={y}, size={widget_size}")
                x = next_x
                line_height = max(line_height, widget_size.height())

        final_height = y + line_height - rect.y()
        print(f"FlowLayout final height: {final_height}")
        return final_height

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("Entering HomePage.__init__...")
        self.parent = parent

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(20, 20, 20, 20)

        print("Creating gear section...")
        self.gear_section = self.create_dropdown_section("MY GEAR (1)", [
            {"type": "gear", "title": "VICTUS Laptop", "image": "victus_laptop.png", "full_width": True}
        ])
        if self.gear_section:
            self.layout.addWidget(self.gear_section)
            print("Gear section added to layout.")
        else:
            print("Gear section is empty or not visible, skipping.")

        print("Creating widgets section...")
        self.widgets_section = self.create_dropdown_section("WIDGETS (10)", [
            {"type": "progress", "title": "CPU", "value": "7%", "subtitle": "48°C"},
            {"type": "progress", "title": "GPU", "value": "0%", "subtitle": "44°C"},
            {"type": "progress", "title": "RAM", "value": "94%", "subtitle": "14.9GB / 16GB"},
            {"type": "image_progress", "title": "OMEN AI BETA", "image": "omen_ai.png", "progress": 50, "full_width": True},
            {"type": "icon_text", "title": "RECENT GAMES", "icon": "gamepad.png", "text": "There are no recently played games", "full_width": True},
            {"type": "error", "title": "TOP DEALS", "message": "We encountered some problems...", "button_text": "RETRY"},
            {"type": "error", "title": "GALLERY", "message": "We encountered some problems...", "button_text": "RETRY"},
            {"type": "toggle", "title": "BOOSTER", "toggle_text": "Boost all my games", "toggle_state": True},
            {"type": "progress", "title": "CPU (2)", "value": "7%", "subtitle": "48°C"},
            {"type": "progress", "title": "GPU (2)", "value": "0%", "subtitle": "44°C"},
        ])
        if self.widgets_section:
            self.layout.addWidget(self.widgets_section)
            print("Widgets section added to layout.")
        else:
            print("Widgets section is empty or not visible, skipping.")
        print("HomePage.__init__ completed.")

    def create_dropdown_section(self, title, items):
        print(f"Creating dropdown section: {title}")
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
        header_layout.addWidget(QLabel(title, self))
        header_layout.addStretch()
        header_button.setLayout(header_layout)
        section_layout.addWidget(header_button)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setStyleSheet("background-color: transparent; border: none;")

        content_widget = QWidget(self)
        content_layout = FlowLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)

        widget_count = 0
        for item in items:
            print(f"Creating widget for item: {item['type']}")
            try:
                if item["type"] == "gear":
                    card = GearCard(item["title"], item["image"], self)
                elif item["type"] == "progress":
                    card = CircularProgressBar(item["title"], item["value"], item["subtitle"], self)
                elif item["type"] == "image_progress":
                    card = ImageProgress(item["title"], item["image"], item["progress"], self)
                elif item["type"] == "icon_text":
                    card = IconText(item["title"], item["icon"], item["text"], self)
                elif item["type"] == "error":
                    card = ErrorCard(item["title"], item["message"], item["button_text"], self)
                elif item["type"] == "toggle":
                    card = ToggleCard(item["title"], item["toggle_text"], item["toggle_state"], self)
                else:
                    print(f"Unknown widget type: {item['type']}")
                    continue
                card.setProperty("full_width", item.get("full_width", False))
                card.setMaximumWidth(300 if not item.get("full_width", False) else 0)
                content_layout.addWidget(card)
                widget_count += 1
                print(f"Added widget: {item['type']}")
            except Exception as e:
                print(f"Error creating widget {item['type']}: {e}")

        if widget_count == 0:
            print(f"No widgets added to section '{title}', returning None.")
            return None

        scroll_area.setWidget(content_widget)
        content_height = content_layout.heightForWidth(scroll_area.width())
        print(f"Content height for section '{title}': {content_height}")
        if content_height <= 0:
            print(f"Content for section '{title}' has no visible height, returning None.")
            return None

        section_layout.addWidget(scroll_area)
        scroll_area.setMinimumHeight(content_height + 20)  # Ensure the scroll area has enough height
        scroll_area.setVisible(True)  # Set to visible by default
        print(f"Scroll area size for section '{title}': {scroll_area.size()}")
        print(f"Scroll area visibility for section '{title}': {scroll_area.isVisible()}")

        def wheel_event(event):
            if scroll_area.isVisible():
                scroll_value = scroll_area.verticalScrollBar().value()
                if event.angleDelta().y() > 0:
                    scroll_area.verticalScrollBar().setValue(scroll_value - 20)
                else:
                    scroll_area.verticalScrollBar().setValue(scroll_value + 20)
                event.accept()

        scroll_area.wheelEvent = wheel_event

        def toggle_content():
            is_visible = scroll_area.isVisible()
            scroll_area.setVisible(not is_visible)
            header_button.setChecked(not is_visible)
            print(f"Section '{title}' visibility toggled to: {not is_visible}")

        header_button.clicked.connect(toggle_content)
        print(f"Dropdown section '{title}' created with {widget_count} widgets.")
        return section

    def update_theme(self, is_light_theme):
        print("Updating HomePage theme...")
        bg_color = "#F0F0F0" if is_light_theme else "#2C2C3E"
        card_bg_color = "#FFFFFF" if is_light_theme else "#1E1E2F"
        header_bg_color = "#E0E0E0" if is_light_theme else "#1E1E2F"
        text_color = "#333333" if is_light_theme else "#00FFD1"
        secondary_text_color = "#666666" if is_light_theme else "#AAAAAA"
        hover_color = "#D0D0D0" if is_light_theme else "#3A3A51"

        self.setStyleSheet(f"background-color: {bg_color};")
        for section in [self.gear_section, self.widgets_section]:
            if section is None:  # Skip if section is None
                continue
            section.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg_color};
                    border-radius: 10px;
                    margin-bottom: 20px;
                }}
            """)
            for i in range(section.layout().count()):
                widget = section.layout().itemAt(i).widget()
                if isinstance(widget, QPushButton):
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
                elif isinstance(widget, QScrollArea):
                    content_widget = widget.widget()
                    if content_widget and content_widget.layout():
                        for j in range(content_widget.layout().count()):
                            card = content_widget.layout().itemAt(j).widget()
                            if card:
                                if hasattr(card, 'update_theme'):
                                    card.update_theme(is_light_theme)
                                else:
                                    card.setStyleSheet(f"""
                                        QFrame {{
                                            background-color: {card_bg_color};
                                            border-radius: 10px;
                                            padding: 15px;
                                        }}
                                    """)
                                for m in range(card.layout().count()):
                                    item = card.layout().itemAt(m).widget()
                                    if isinstance(item, QLabel):
                                        item.setStyleSheet(f"color: {text_color if m == 0 else secondary_text_color}; font-size: 16px;")
                                    elif isinstance(item, QPushButton):
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
                                    elif isinstance(item, QFrame) and not isinstance(card, CircularProgressBar):
                                        item.setStyleSheet(f"""
                                            QFrame {{
                                                background-color: {'#CCCCCC' if is_light_theme else '#555555'};
                                                border-radius: 10px;
                                            }}
                                        """)
                                        for l in range(len(item.children())):
                                            sub_item = item.children()[l]
                                            if isinstance(sub_item, QFrame):
                                                sub_item.setStyleSheet(f"background-color: {'#00FF00' if is_light_theme else '#00FF00'}; border-radius: 8px;")
        print(f"Home page updated for {'light' if is_light_theme else 'dark'} theme.")