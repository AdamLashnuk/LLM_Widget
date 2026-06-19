import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QStackedWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor

class SettingPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: #ececec;
                font-family: "Segoe UI";
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
                /* Removed padding-left so it sits cleanly next to the icon */
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
                background-color: #333333; /* Highlights the active tab */
                color: #ffffff;
            }

            /* --- Content Area Styling --- */
            QLabel#pageTitle {
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
            
            QLabel.cardText {
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

        # Left Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(240) # Fixed width like a standard browser sidebar

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 25, 15, 25)
        sidebar_layout.setSpacing(8)

        # Settings Header (Icon + Title)
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_layout.setSpacing(10)
        header_layout.setContentsMargins(10, 0, 0, 0) # Nudge inward slightly

       # Load and scale the Portal icon
        icon_label = QLabel()
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(project_root, "assets", "portal.png")
        
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            # Dynamically target the white background and mask it out (make it transparent)
            mask = pixmap.createMaskFromColor(QColor(255, 255, 255), Qt.MaskOutColor)
            pixmap.setMask(mask)

            # Scale it down
            scaled_pixmap = pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)

        # Settings Title
        title = QLabel("Settings")
        title.setObjectName("sidebarTitle")
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title)
        
        sidebar_layout.addLayout(header_layout)
        sidebar_layout.addSpacing(15) # Gap before the buttons

        # Appearance Button
        self.appearance_btn = QPushButton("Appearance")
        self.appearance_btn.setProperty("class", "sidebarButton")
        self.appearance_btn.setCheckable(True) # Allows it to stay highlighted
        self.appearance_btn.setChecked(True)   # Default active state
        
        sidebar_layout.addWidget(self.appearance_btn)
        sidebar_layout.addStretch() # Pushes everything to the top

        # Right content area
        self.content_stack = QStackedWidget()
        
        # Appearance Page
        self.appearance_page = QWidget()
        app_layout = QVBoxLayout(self.appearance_page)
        app_layout.setContentsMargins(40, 40, 40, 40)
        app_layout.setAlignment(Qt.AlignTop)

        # Page Title
        app_title = QLabel("Appearance")
        app_title.setObjectName("pageTitle")
        app_layout.addWidget(app_title)

        # Example Setting Card (Mimics Brave's rounded setting containers)
        card = QFrame()
        card.setProperty("class", "settingCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        
        placeholder_text = QLabel("Appearance options will go here...")
        placeholder_text.setProperty("class", "cardText")
        card_layout.addWidget(placeholder_text)

        app_layout.addWidget(card)

        # Add the page to the stack
        self.content_stack.addWidget(self.appearance_page)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_stack)