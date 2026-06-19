from PySide6.QtWidgets import (QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton)

class SettingPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: white;
                font-family: "Segoe UI";
            }

            QLabel {
                font-size: 20px;
                font-weight: 600;
            }

            QPushButton {
                background-color: transparent;
                border: none;
                color: #9f9f9f;
                font-size: 13px;
                padding: 4px;
            }
            
            QPushButton:hover {
                color: white;
            }
        """)

        self.create_pages()
        self.create_layout()
        self.show_settings()

    def create_pages(self):
        self.settings_page = QWidget()
        self.providers_page = QWidget()
        self.about_page = QWidget()

        # Main Settings Page
        settings_layout = QVBoxLayout()
        settings_layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Settings")

        providers_button = QPushButton("Providers  >")
        providers_button.clicked.connect(self.show_providers)

        about_button = QPushButton("About  >")
        about_button.clicked.connect(self.show_about)

        settings_layout.addWidget(title)

        settings_layout.addStretch()

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(providers_button)
        button_row.addWidget(about_button)

        settings_layout.addLayout(button_row)
        self.settings_page.setLayout(settings_layout)

        # Providers Page
        providers_layout = QVBoxLayout()
        providers_layout.setContentsMargins(30, 30, 30, 30)

        providers_back = QPushButton("← Back")
        providers_back.clicked.connect(self.show_settings)

        providers_title = QLabel("Providers")
        providers_text = QLabel("ChatGPT\nClaude\nGemini")

        providers_layout.addWidget(providers_back)
        providers_layout.addSpacing(20)
        providers_layout.addWidget(providers_title)
        providers_layout.addWidget(providers_text)
        providers_layout.addStretch()

        self.providers_page.setLayout(providers_layout)

        # About Page
        about_layout = QVBoxLayout()
        about_layout.setContentsMargins(30, 30, 30, 30)

        about_back = QPushButton("← Back")
        about_back.clicked.connect(self.show_settings)

        about_title = QLabel("About")
        about_text = QLabel("Portl v0.1\n\nDesktop AI Browser\nOne place for every AI.")

        about_layout.addWidget(about_back)
        about_layout.addSpacing(20)
        about_layout.addWidget(about_title)
        about_layout.addWidget(about_text)
        about_layout.addStretch()
        providers_button.setFixedSize(90, 32)
        about_button.setFixedSize(90, 32)
        self.about_page.setLayout(about_layout)

    def create_layout(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(self.settings_page)
        main_layout.addWidget(self.providers_page)
        main_layout.addWidget(self.about_page)

        self.setLayout(main_layout)

    def show_settings(self):
        self.settings_page.show()
        self.providers_page.hide()
        self.about_page.hide()

    def show_providers(self):
        self.settings_page.hide()
        self.providers_page.show()
        self.about_page.hide()

    def show_about(self):
        self.settings_page.hide()
        self.providers_page.hide()
        self.about_page.show()