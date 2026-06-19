from PySide6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame)
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PySide6.QtWidgets import QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
import os
from app.setting_panel import SettingPanel
from PySide6.QtWidgets import QSizePolicy

class ChatPanel(QWidget):
    def __init__(self, bubble=None):
        super().__init__()

        self.bubble = bubble
        self.drag_position = None

        self.setup_window()
        self.create_widgets()

        self.setting_panel = SettingPanel()
        self.setting_panel.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        self.setting_panel.hide()

        self.create_layout()

    def setup_window(self):
        self.setFixedSize(900, 700)

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                color: #ececec;
                font-family: "Segoe UI";
            }

            QFrame#mainContainer {
                background-color: rgba(15, 15, 15, 180);
                border: 1px solid rgba(255, 255, 255, 20);
                border-radius: 24px;
            }

            QLabel#title {
                font-size: 20px;
                font-weight: 600;
            }

            QPushButton {
                background-color: #303030;
                color: #ececec;
                border: 1px solid #444444;
                border-radius: 10px;
                padding: 8px 14px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #3a3a3a;
            }

            QPushButton#closeButton {
                background-color: transparent;
                border: none;
                color: #b4b4b4;
                font-size: 16px; 
                font-weight: 100;
                padding: 0px; 
                margin: 0px;
            }

            QPushButton#closeButton:hover {
                color: white;
                background-color: #333333;
                border-radius: 8px;
            }
                           
            QPushButton#addButton {
                font-size: 20px;
                font-weight: bold;
                padding: 0px;
                padding-bottom: 6px; 
            }

            QPushButton#settingsButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
            }

            QPushButton#settingsButton:hover {
                background-color: #333333;
            }
        """)

    def create_widgets(self):
        self.container = QFrame()
        self.container.setObjectName("mainContainer")

        self.chatgpt_button = QPushButton("ChatGPT")
        self.claude_button = QPushButton("Claude")
        self.gemini_button = QPushButton("Gemini")

        self.chatgpt_button.clicked.connect(self.open_chatgpt)
        self.claude_button.clicked.connect(self.open_claude)
        self.gemini_button.clicked.connect(self.open_gemini)

        self.close_button = QPushButton("✕")
        self.close_button.setObjectName("closeButton")
        self.close_button.setFixedSize(32, 32)
        self.close_button.clicked.connect(self.close_panel)


        # Add button
        self.add_button = QPushButton("+")
        self.add_button.setObjectName("addButton")
        self.add_button.setFixedSize(26, 26)

        # Settings button
        self.settings_button = QPushButton()
        self.settings_button.setObjectName("settingsButton")
        self.settings_button.setFixedSize(32, 32)
        self.settings_button.clicked.connect(self.open_settings)
        # Load and recolor the gear icon
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(project_root, "assets", "gearsettings.png")
        
        icon_pixmap = QPixmap(icon_path)
        if not icon_pixmap.isNull():
            painter = QPainter(icon_pixmap)
            # This line allows us to draw over the non-transparent parts of the PNG
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn) 
            painter.fillRect(icon_pixmap.rect(), QColor("#b4b4b4"))
            painter.end()
            
            self.settings_button.setIcon(QIcon(icon_pixmap))
            self.settings_button.setIconSize(QSize(20, 20))

        # Persistent logins stored in a local folder
        self.browser = QWebEngineView()

        self.profile = QWebEngineProfile("llm_profile", self.browser)

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        storage_path = os.path.join(project_root, "session_data")
        
        self.profile.setPersistentStoragePath(storage_path)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
        
        self.page = QWebEnginePage(self.profile, self.browser)
        self.browser.setPage(self.page)
        
        self.browser.setUrl(QUrl("https://chatgpt.com"))

    def create_layout(self):
        top_bar = QHBoxLayout()
        self.title_bar = QFrame()
        self.title_bar.setFixedHeight(45)

        top_bar.setContentsMargins(18, 4, 18, 4)
        
        top_bar.setAlignment(Qt.AlignVCenter)

        top_bar.addWidget(self.chatgpt_button)
        top_bar.addWidget(self.claude_button)
        top_bar.addWidget(self.gemini_button)
        top_bar.addWidget(self.add_button)


        top_bar.addStretch()
        top_bar.addWidget(self.settings_button)
        top_bar.addWidget(self.close_button, alignment=Qt.AlignVCenter)

        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(12, 12, 12, 12)
        self.title_bar.setLayout(top_bar)
        container_layout.addWidget(self.title_bar)



        self.content_area = QFrame()

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        content_layout.addWidget(self.browser)
        content_layout.addWidget(self.setting_panel)

        self.content_area.setLayout(content_layout)

        container_layout.addWidget(self.content_area)


        self.setting_panel.hide()

        self.container.setLayout(container_layout)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)

        self.setLayout(main_layout)

    def show_browser(self):
        self.setting_panel.hide()
        self.browser.show()

    def open_chatgpt(self):
        self.browser.setUrl(QUrl("https://chatgpt.com"))

    def open_claude(self):
        self.browser.setUrl(QUrl("https://claude.ai"))

    def open_gemini(self):
        self.browser.setUrl(QUrl("https://gemini.google.com"))

    def close_panel(self):
        if self.bubble:
            self.bubble.close_chat_with_animation()
        else:
            self.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.position().y() < 45:
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )
            event.accept()

    def open_settings(self):
        if self.setting_panel.isVisible():
            self.setting_panel.hide()
            self.browser.show()
        else:
            self.browser.hide()
            self.setting_panel.show()