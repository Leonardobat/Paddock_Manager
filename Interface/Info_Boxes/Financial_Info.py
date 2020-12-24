# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPalette, QFont
from PySide6.QtWidgets import (QLabel, QPushButton, QWidget, QFrame,
                               QGridLayout)


class Financial_Info(QWidget):
    def __init__(self, data, palette):
        QWidget.__init__(self)
        self.palette = QPalette()

        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Panel)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.title = QLabel('Finanças')
        self.title.setPalette(palette)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setAutoFillBackground(True)

        self.layout = QGridLayout()
        self.layout.addWidget(self.title, 0, 0, 1, 4)
        self.layout.addWidget(self.frame, 0, 0, 7, 4)
        self.layout.addWidget(QLabel('Caixa'), 1, 1)
        self.layout.addWidget(QLabel(data['Cash']), 1, 2)
        self.layout.addWidget(QLabel(data['Sponsor 1']['Name']), 2, 1)
        self.layout.addWidget(QLabel(data['Sponsor 1']['Value']), 2, 2)
        self.layout.addWidget(QLabel(data['Sponsor 2']['Name']), 3, 1)
        self.layout.addWidget(QLabel(data['Sponsor 2']['Value']), 3, 2)
        self.layout.addWidget(QLabel(data['Sponsor 3']['Name']), 4, 1)
        self.layout.addWidget(QLabel(data['Sponsor 3']['Value']), 4, 2)
        self.layout.addWidget(QLabel(data['Sponsor 4']['Name']), 5, 1)
        self.layout.addWidget(QLabel(data['Sponsor 4']['Value']), 5, 2)
        self.layout.addWidget(QLabel(data['Sponsor 5']['Name']), 6, 1)
        self.layout.addWidget(QLabel(data['Sponsor 5']['Value']), 6, 2)
        self.setLayout(self.layout)
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)