from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainter, QColor, QFont, QPen

from app.chat_panel import ChatPanel


class FloatingWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.chat_panel = ChatPanel(self)
        self.drag_position = QPoint()
        self.was_dragging = False

        self.setup_window()

    def setup_window(self):
        # Set a clean size for our circular widget
        self.setFixedSize(60, 60)
        self.move(1200, 600)

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

    # --- DRAW THE CIRCLE DIRECTLY ON THE WIDGET ---
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the background circle (Matches #202123)
        painter.setBrush(QColor("#202123"))
        # Draw the border (Matches 2px #10a37f)
        painter.setPen(QPen(QColor("#10a37f"), 2))
        painter.drawEllipse(2, 2, 56, 56)

        # Draw the "AI" text
        painter.setPen(QColor("white"))
        font = QFont("Arial", 15, QFont.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, "AI")

    def open_chat(self):
        bubble_x = self.x()
        bubble_y = self.y()

        # Target coordinates
        target_x = bubble_x - 350
        target_y = bubble_y - 450 

        if target_y < 10:
            target_y = bubble_y + self.height() + 10

        # Also prevent it from clipping past the left side of the screen
        if target_x < 10:
            target_x = 10

        # Move and display the panel safely
        self.chat_panel.move(target_x, target_y)
        self.chat_panel.show()
        self.chat_panel.raise_()
        self.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.was_dragging = False
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.was_dragging = True
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.was_dragging:
                self.open_chat()
            event.accept()