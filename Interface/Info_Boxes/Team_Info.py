# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPalette, QFont, QColor
from PySide6.QtWidgets import (QLabel, QPushButton, QWidget, QFrame,
                               QGridLayout)


class Team_Info(QWidget):
    def __init__(self, data, palette):
        QWidget.__init__(self)
        self.font = QFont()
        self.font.setItalic(True)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Active, QPalette.Window,
                              QColor(255, 255, 255, 255))
        self.palette.setColor(QPalette.Active, QPalette.WindowText,
                              QColor(0, 0, 0, 255))
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)

        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Panel)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.team_name = QLabel(data['Team']['Name'])
        self.team_name.setPalette(palette)
        self.team_name.setAlignment(Qt.AlignCenter)
        self.team_name.setAutoFillBackground(True)
        self.user_name = QLabel(data['Team']['Principal'])
        self.user_name.setFont(self.font)
        self.pilot1 = QLabel(data['Pilot 1']['Name'])
        self.pilot2 = QLabel(data['Pilot 2']['Name'])
        self.pilot3 = QLabel(data['Pilot 3']['Name'])
        self.pilot1_info = QLabel(
            'DNF {} / Vit. {} / Pol. {} / Pts. {}'.format(
                *data['Pilot 1']['Info']))
        self.pilot1_info.setAlignment(Qt.AlignCenter)
        self.pilot2_info = QLabel(
            'DNF {} / Vit. {} / Pol. {} / Pts. {}'.format(
                *data['Pilot 2']['Info']))
        self.pilot2_info.setAlignment(Qt.AlignCenter)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.team_name, 0, 0, 1, 4)
        self.layout.addWidget(self.frame, 0, 0, 7, 4)
        self.layout.addWidget(QLabel('Chefe da Equipe'), 1, 1, Qt.AlignLeft)
        self.layout.addWidget(self.user_name, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel('Piloto 1'), 2, 1, Qt.AlignLeft)
        self.layout.addWidget(self.pilot1, 2, 2, Qt.AlignCenter)
        self.layout.addWidget(self.pilot1_info, 3, 1, 1, 2)
        self.layout.addWidget(QLabel('Piloto 2'), 4, 1, Qt.AlignLeft)
        self.layout.addWidget(self.pilot2, 4, 2, Qt.AlignCenter)
        self.layout.addWidget(self.pilot2_info, 5, 1, 1, 2)
        self.layout.addWidget(QLabel('Reserva'), 6, 1, Qt.AlignLeft)
        self.layout.addWidget(self.pilot3, 6, 2, Qt.AlignCenter)
        self.setLayout(self.layout)

    @Slot()
    def update_info(self, data: dict):
        self.team_name.setText(data['Team']['Name'])
        self.user_name.setText(data['Team']['Principal'])
        self.pilot1.setText(data['Pilot 1']['Name'])
        self.pilot2.setText(data['Pilot 2']['Name'])
        self.pilot3.setText(data['Pilot 3']['Name'])
        self.pilot1_info.setText('DNF {} / Vit. {} / Pol. {} / Pts. {}'.format(
            *data['Pilot 1']['Info']))
        self.pilot2_info.setText('DNF {} / Vit. {} / Pol. {} / Pts. {}'.format(
            *data['Pilot 2']['Info']))
