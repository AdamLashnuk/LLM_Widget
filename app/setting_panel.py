import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QStackedWidget, QButtonGroup)
from PySide6.QtCore import Qt, Signal, QSettings
from PySide6.QtGui import QPixmap, QColor, QImage

class SettingPanel(QWidget):
    # --- Define the custom signal at the class level ---
    color_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            /* Global widget rules (Restores the dark background to the right side) */
            QWidget {
                background-color: #1a1a1a;
                color: #ececec;
                font-family: "Segoe UI";
            }

            /* Rounds only the outer shell to fit the window */
            QWidget#settingPanelMain {
                border-radius: 12px; 
            }

            /* Keeps text and icons perfectly transparent */
            QLabel {
                background-color: transparent;
            }

            /* --- Sidebar Styling --- */
            QFrame#sidebar {
                background-color: #1f1f1f;
                border-right: 1px solid #333333;
            }

            QLabel#sidebarTitle {
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
            }

            QPushButton.sidebarButton {
                background-color: transparent;
                border: none;
                border-radius: 6px;
                color: #b4b4b4;
                font-size: 14px;
                font-weight: 500;
                text-align: left;
                padding: 10px 15px;
            }

            QPushButton.sidebarButton:hover {
                background-color: #2a2a2a;
                color: #ececec;
            }

            QPushButton.sidebarButton:checked {
                background-color: #333333;
                color: #ffffff;
            }

            /* --- Content Area Styling --- */
            QLabel#pageTitle {
                background-color: transparent;
                font-size: 24px;
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 10px;
            }

            QFrame.settingCard {
                background-color: #242424;
                border: 1px solid #333333;
                border-radius: 10px;
            }
            
            QLabel.cardTitle {
                background-color: transparent;
                font-size: 16px;
                font-weight: 500;
                color: #ffffff;
            }
            
            QLabel.cardText {
                background-color: transparent;
                font-size: 14px;
                color: #b4b4b4;
            }
        """)

        self.create_layout()

    def create_layout(self):
        # Main Horizontal Layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # -----------------------------------------
        # LEFT SIDEBAR
        # -----------------------------------------
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(240)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 25, 15, 25)
        sidebar_layout.setSpacing(8)

        # --- Settings Header (Icon + Title) ---
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_layout.setSpacing(10)
        header_layout.setContentsMargins(10, 0, 0, 0)

        icon_label = QLabel()
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(project_root, "assets", "portal.png")
        
        image = QImage(icon_path)
        if not image.isNull():
            image = image.convertToFormat(QImage.Format_ARGB32)
            for y in range(image.height()):
                for x in range(image.width()):
                    color = image.pixelColor(x, y)
                    if color.red() > 240 and color.green() > 240 and color.blue() > 240:
                        color.setAlpha(0)
                        image.setPixelColor(x, y, color)

            pixmap = QPixmap.fromImage(image)
            scaled_pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)

        title = QLabel("Settings")
        title.setObjectName("sidebarTitle")
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title)
        
        sidebar_layout.addLayout(header_layout)
        sidebar_layout.addSpacing(15)

        # Appearance Button
        self.appearance_btn = QPushButton("Appearance")
        self.appearance_btn.setProperty("class", "sidebarButton")
        self.appearance_btn.setCheckable(True)
        self.appearance_btn.setChecked(True)
        
        sidebar_layout.addWidget(self.appearance_btn)
        sidebar_layout.addStretch()

        # Right Content Area
        self.content_stack = QStackedWidget()
        
        # --- Appearance Page ---
        self.appearance_page = QWidget()
        app_layout = QVBoxLayout(self.appearance_page)
        app_layout.setContentsMargins(40, 40, 40, 40)
        app_layout.setAlignment(Qt.AlignTop)

        # Page Title
        app_title = QLabel("Appearance")
        app_title.setObjectName("pageTitle")
        app_layout.addWidget(app_title)

        # Window Resize Color Card
        card = QFrame()
        card.setProperty("class", "settingCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15) 
        
        # Sub-Title
        resize_title = QLabel("Window Resize Color")
        resize_title.setProperty("class", "cardTitle")
        card_layout.addWidget(resize_title)

        # Horizontal layout for the 4 color buttons
        color_layout = QHBoxLayout()
        color_layout.setAlignment(Qt.AlignLeft)
        color_layout.setSpacing(15)

        # --- NEW: Create a Button Group so only one can be checked at a time ---
        self.color_group = QButtonGroup(self)
        self.color_group.setExclusive(True)

        # 0. Transparent Button
        self.btn_transparent = QPushButton("✕")
        self.btn_transparent.setFixedSize(40, 40)
        self.btn_transparent.setCheckable(True) # Makes the button selectable
        self.btn_transparent.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                border: 2px dashed #444444; 
                border-radius: 8px;
                color: #555555;
                font-weight: bold;
            }
            QPushButton:hover { border: 2px dashed #b4b4b4; color: #b4b4b4; }
            QPushButton:checked { border: 2px solid #6366f1; color: #6366f1; } /* Blue active state */
        """)

        # 1. Grey Button
        self.btn_grey = QPushButton()
        self.btn_grey.setFixedSize(40, 40)
        self.btn_grey.setCheckable(True)
        self.btn_grey.setStyleSheet("""
            QPushButton {
                background-color: rgba(15, 15, 15, 220); 
                border: 2px solid #333333; 
                border-radius: 8px;
            }
            QPushButton:hover { border: 2px solid #b4b4b4; }
            QPushButton:checked { border: 2px solid #6366f1; }
        """)

        # 2. Purple Button
        self.btn_purple = QPushButton()
        self.btn_purple.setFixedSize(40, 40)
        self.btn_purple.setCheckable(True)
        self.btn_purple.setStyleSheet("""
            QPushButton {
                background-color: rgba(45, 25, 65, 140); 
                border: 2px solid #333333; 
                border-radius: 8px;
            }
            QPushButton:hover { border: 2px solid #b4b4b4; }
            QPushButton:checked { border: 2px solid #6366f1; }
        """)

        # 3. Deep Blue Button
        self.btn_blue = QPushButton()
        self.btn_blue.setFixedSize(40, 40)
        self.btn_blue.setCheckable(True)
        self.btn_blue.setStyleSheet("""
            QPushButton {
                background-color: rgba(15, 30, 50, 160); 
                border: 2px solid #333333; 
                border-radius: 8px;
            }
            QPushButton:hover { border: 2px solid #b4b4b4; }
            QPushButton:checked { border: 2px solid #6366f1; }
        """)

        # Add buttons to the exclusive group
        self.color_group.addButton(self.btn_transparent)
        self.color_group.addButton(self.btn_grey)
        self.color_group.addButton(self.btn_purple)
        self.color_group.addButton(self.btn_blue)

        # Add buttons to the visual row layout
        color_layout.addWidget(self.btn_transparent)
        color_layout.addWidget(self.btn_grey)
        color_layout.addWidget(self.btn_purple)
        color_layout.addWidget(self.btn_blue)

        # --- NEW: Check the user's saved setting to highlight the correct button automatically ---
        settings = QSettings("MyLLMWidget", "ChatPanel")
        saved_color = settings.value("resize_color", "rgba(15, 15, 15, 220)")

        if saved_color == "transparent":
            self.btn_transparent.setChecked(True)
        elif saved_color == "rgba(45, 25, 65, 140)":
            self.btn_purple.setChecked(True)
        elif saved_color == "rgba(15, 30, 50, 160)":
            self.btn_blue.setChecked(True)
        else:
            self.btn_grey.setChecked(True) # Defaults to grey

        card_layout.addLayout(color_layout)
        app_layout.addWidget(card)

        self.content_stack.addWidget(self.appearance_page)

        # Connect the buttons to emit their actual colors
        self.btn_transparent.clicked.connect(lambda: self.color_changed.emit("transparent"))
        self.btn_purple.clicked.connect(lambda: self.color_changed.emit("rgba(45, 25, 65, 140)"))
        self.btn_blue.clicked.connect(lambda: self.color_changed.emit("rgba(15, 30, 50, 160)"))
        self.btn_grey.clicked.connect(lambda: self.color_changed.emit("rgba(15, 15, 15, 220)"))

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_stack)