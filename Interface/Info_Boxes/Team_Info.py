# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPalette, QFont
from PySide6.QtWidgets import (QLabel, QPushButton, QWidget, QFrame,
                               QGridLayout)


class Team_Info(QWidget):
    def __init__(self, data, palette):
        QWidget.__init__(self)
        self.font = QFont()
        self.font.setItalic(True)
        self.palette = QPalette()

        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Panel)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.team_name = QLabel(data['Team']['Name'])
        self.team_name.setPalette(palette)
        self.team_name.setAlignment(Qt.AlignCenter)
        self.team_name.setAutoFillBackground(True)
        self.user_name = QLabel(data['Team']['Principal'])
        self.user_name.setFont(self.font)
        self.info_p1 = QLabel('DNF {} / Vit. {} / Pol. {} / Pts. {}'.format(
            0, 0, 0, 0))
        self.info_p1.setAlignment(Qt.AlignCenter)
        self.info_p2 = QLabel('DNF {} / Vit. {} / Pol. {} / Pts. {}'.format(
            0, 0, 0, 0))
        self.info_p2.setAlignment(Qt.AlignCenter)

        self.layout = QGridLayout()
        self.layout.addWidget(self.team_name, 0, 0, 1, 4)
        self.layout.addWidget(self.frame, 0, 0, 7, 4)
        self.layout.addWidget(QLabel('Chefe da Equipe'), 1, 1)
        self.layout.addWidget(self.user_name, 1, 2)
        self.layout.addWidget(QLabel('Piloto 1'), 2, 1)
        self.layout.addWidget(QLabel(data['Pilot 1']), 2, 2)
        self.layout.addWidget(self.info_p1, 3, 1, 1, 2)
        self.layout.addWidget(QLabel('Piloto 2'), 4, 1)
        self.layout.addWidget(QLabel(data['Pilot 2']), 4, 2)
        self.layout.addWidget(self.info_p2, 5, 1, 1, 2)
        self.layout.addWidget(QLabel('Reserva'), 6, 1)
        self.layout.addWidget(QLabel(data['Pilot 3']), 6, 2)
        self.setLayout(self.layout)
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)