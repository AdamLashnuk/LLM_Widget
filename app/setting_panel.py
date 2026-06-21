import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QStackedWidget, QButtonGroup)
from PySide6.QtCore import Qt, Signal, QSettings
from PySide6.QtGui import QPixmap, QColor, QImage

class SettingPanel(QWidget):
    color_changed = Signal(str)
    clear_data_requested = Signal()

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            /* Global widget rules */
            QWidget {
                background-color: #1a1a1a;
                color: #ececec;
                font-family: "Segoe UI";
            }

            QWidget#settingPanelMain {
                border-radius: 12px; 
            }

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
            QLabel.pageTitle {
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
            
            /* --- Danger Button Styling --- */
            QPushButton.dangerButton {
                background-color: rgba(220, 38, 38, 0.15);
                border: 1px solid rgba(220, 38, 38, 0.5);
                color: #f87171;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton.dangerButton:hover {
                background-color: rgba(220, 38, 38, 0.25);
                color: #fca5a5;
            }
        """)

        self.create_layout()

    def create_layout(self):
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
        icon_path = os.path.join(project_root, "assets", "portalbig.png")
        
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

        # --- Sidebar Navigation Group ---
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        self.appearance_btn = QPushButton("Appearance")
        self.appearance_btn.setProperty("class", "sidebarButton")
        self.appearance_btn.setCheckable(True)
        self.appearance_btn.setChecked(True)
        self.nav_group.addButton(self.appearance_btn, 0)
        sidebar_layout.addWidget(self.appearance_btn)

        # --- CHANGED: Used && to render a single & symbol ---
        self.privacy_btn = QPushButton("Privacy && Data")
        self.privacy_btn.setProperty("class", "sidebarButton")
        self.privacy_btn.setCheckable(True)
        self.nav_group.addButton(self.privacy_btn, 1)
        sidebar_layout.addWidget(self.privacy_btn)

        sidebar_layout.addStretch()

        # -----------------------------------------
        # RIGHT CONTENT AREA
        # -----------------------------------------
        self.content_stack = QStackedWidget()
        
        # === PAGE 0: APPEARANCE ===
        self.appearance_page = QWidget()
        app_layout = QVBoxLayout(self.appearance_page)
        app_layout.setContentsMargins(40, 40, 40, 40)
        app_layout.setAlignment(Qt.AlignTop)

        app_title = QLabel("Appearance")
        app_title.setProperty("class", "pageTitle")
        app_layout.addWidget(app_title)

        card = QFrame()
        card.setProperty("class", "settingCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15) 
        
        resize_title = QLabel("Window Color")
        resize_title.setProperty("class", "cardTitle")
        card_layout.addWidget(resize_title)

        color_layout = QHBoxLayout()
        color_layout.setAlignment(Qt.AlignLeft)
        color_layout.setSpacing(15)

        self.color_group = QButtonGroup(self)
        self.color_group.setExclusive(True)

        self.btn_transparent = QPushButton("✕")
        self.btn_transparent.setFixedSize(40, 40)
        self.btn_transparent.setCheckable(True) 
        self.btn_transparent.setStyleSheet("""
            QPushButton { background-color: transparent; border: 2px dashed #444444; border-radius: 8px; color: #555555; font-weight: bold; }
            QPushButton:hover { border: 2px dashed #b4b4b4; color: #b4b4b4; }
            QPushButton:checked { border: 2px solid #6366f1; color: #6366f1; } 
        """)

        self.btn_grey = QPushButton()
        self.btn_grey.setFixedSize(40, 40)
        self.btn_grey.setCheckable(True)
        self.btn_grey.setStyleSheet("""
            QPushButton { background-color: rgba(15, 15, 15, 220); border: 2px solid #333333; border-radius: 8px; }
            QPushButton:hover { border: 2px solid #b4b4b4; }
            QPushButton:checked { border: 2px solid #6366f1; }
        """)

        self.btn_purple = QPushButton()
        self.btn_purple.setFixedSize(40, 40)
        self.btn_purple.setCheckable(True)
        self.btn_purple.setStyleSheet("""
            QPushButton { background-color: rgba(45, 25, 65, 140); border: 2px solid #333333; border-radius: 8px; }
            QPushButton:hover { border: 2px solid #b4b4b4; }
            QPushButton:checked { border: 2px solid #6366f1; }
        """)

        self.btn_blue = QPushButton()
        self.btn_blue.setFixedSize(40, 40)
        self.btn_blue.setCheckable(True)
        self.btn_blue.setStyleSheet("""
            QPushButton { background-color: rgba(15, 30, 50, 160); border: 2px solid #333333; border-radius: 8px; }
            QPushButton:hover { border: 2px solid #b4b4b4; }
            QPushButton:checked { border: 2px solid #6366f1; }
        """)

        self.color_group.addButton(self.btn_transparent)
        self.color_group.addButton(self.btn_grey)
        self.color_group.addButton(self.btn_purple)
        self.color_group.addButton(self.btn_blue)

        color_layout.addWidget(self.btn_transparent)
        color_layout.addWidget(self.btn_grey)
        color_layout.addWidget(self.btn_purple)
        color_layout.addWidget(self.btn_blue)

        settings = QSettings("MyLLMWidget", "ChatPanel")
        saved_color = settings.value("resize_color", "rgba(15, 15, 15, 220)")

        if saved_color == "transparent": self.btn_transparent.setChecked(True)
        elif saved_color == "rgba(45, 25, 65, 140)": self.btn_purple.setChecked(True)
        elif saved_color == "rgba(15, 30, 50, 160)": self.btn_blue.setChecked(True)
        else: self.btn_grey.setChecked(True) 

        card_layout.addLayout(color_layout)
        app_layout.addWidget(card)

        # === PAGE 1: PRIVACY ===
        self.privacy_page = QWidget()
        priv_layout = QVBoxLayout(self.privacy_page)
        priv_layout.setContentsMargins(40, 40, 40, 40)
        priv_layout.setAlignment(Qt.AlignTop)

        priv_title = QLabel("Privacy & Data")
        priv_title.setProperty("class", "pageTitle")
        priv_layout.addWidget(priv_title)

        priv_card = QFrame()
        priv_card.setProperty("class", "settingCard")
        priv_card_layout = QVBoxLayout(priv_card)
        priv_card_layout.setContentsMargins(20, 20, 20, 20)
        priv_card_layout.setSpacing(15)

        danger_title = QLabel("Clear Browsing Data")
        danger_title.setProperty("class", "cardTitle")
        priv_card_layout.addWidget(danger_title)

        danger_desc = QLabel("This will instantly log you out of all AI providers, clear your active session cookies, and wipe the widget's internal cache. Use this to protect your privacy or if a website is stuck in an endless login loop.")
        danger_desc.setProperty("class", "cardText")
        danger_desc.setWordWrap(True)
        priv_card_layout.addWidget(danger_desc)

        # The Red Button
        self.btn_clear_data = QPushButton("Clear All Data && Cookies")
        self.btn_clear_data.setProperty("class", "dangerButton")
        self.btn_clear_data.setCursor(Qt.PointingHandCursor)
        self.btn_clear_data.clicked.connect(lambda: self.clear_data_requested.emit())
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_clear_data)
        btn_layout.addStretch()
        priv_card_layout.addLayout(btn_layout)

        priv_layout.addWidget(priv_card)

        # Build the Stack
        self.content_stack.addWidget(self.appearance_page)
        self.content_stack.addWidget(self.privacy_page)

        # Connect Sidebar Buttons to Stack
        self.nav_group.idClicked.connect(self.content_stack.setCurrentIndex)

        # Connect Color Buttons
        self.btn_transparent.clicked.connect(lambda: self.color_changed.emit("transparent"))
        self.btn_purple.clicked.connect(lambda: self.color_changed.emit("rgba(45, 25, 65, 140)"))
        self.btn_blue.clicked.connect(lambda: self.color_changed.emit("rgba(15, 30, 50, 160)"))
        self.btn_grey.clicked.connect(lambda: self.color_changed.emit("rgba(15, 15, 15, 220)"))

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_stack)