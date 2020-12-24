# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (QLabel, QPushButton, QWidget, QFrame,
                               QGridLayout)


class News_Info(QWidget):
    def __init__(self, msg, palette):
        QWidget.__init__(self)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Active, QPalette.Window,
                              QColor(255, 255, 255, 255))
        self.palette.setColor(QPalette.Active, QPalette.WindowText,
                              QColor(0, 0, 0, 255))
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)
        self.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel('Notícias')
        self.title.setPalette(palette)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setAutoFillBackground(True)
        if msg is not None:
            self.news = QLabel(msg)
        else:
            self.news = QLabel("Não há nenhuma notícia nova.")
        self.news.setAlignment(Qt.AlignCenter)
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Panel)
        self.frame.setFrameShadow(QFrame.Sunken)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.title, 0, 0)
        self.layout.addWidget(self.frame, 0, 0, 2, 1)
        self.layout.addWidget(self.news, 1, 0)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 3)
        self.setLayout(self.layout)

    @Slot()
    def update_news(self, data: dict):
        self.news.setText(data['msg'])