# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPalette, QFont, QColor
from PySide6.QtWidgets import (QLabel, QPushButton, QWidget, QFrame,
                               QGridLayout)


class Car_Info(QWidget):
    def __init__(self, data: dict, palette):
        QWidget.__init__(self)
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
        self.title = QLabel('Carro')
        self.title.setPalette(palette)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setAutoFillBackground(True)
        self.aero = QLabel(str(data['Aerodynamics']))
        self.relia = QLabel(str(data['Reliability']))
        self.motor = QLabel(str(data['Motor']))
        self.eletronics = QLabel(str(data['Electronics']))
        self.suspension = QLabel(str(data['Suspension']))
        self.overall = (data['Aerodynamics'] + data['Suspension'] +
                        data['Motor'] + data['Electronics']) / 4
        self.overall = QLabel(str(int(self.overall)))

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.title, 0, 0, 1, 4)
        self.layout.addWidget(self.frame, 0, 0, 7, 4)
        self.layout.addWidget(QLabel('Aerodinâmica'), 1, 1, Qt.AlignRight)
        self.layout.addWidget(self.aero, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel('Confiabilidade'), 2, 1, Qt.AlignRight)
        self.layout.addWidget(self.relia, 2, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel('Motor'), 3, 1, Qt.AlignRight)
        self.layout.addWidget(self.motor, 3, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel('Eletrônica'), 4, 1, Qt.AlignRight)
        self.layout.addWidget(self.eletronics, 4, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel('Suspensão'), 5, 1, Qt.AlignRight)
        self.layout.addWidget(self.suspension, 5, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel('Geral'), 6, 1, Qt.AlignRight)
        self.layout.addWidget(self.overall, 6, 2, Qt.AlignCenter)
        self.setLayout(self.layout)

        self.setMaximumWidth(250)

    @Slot()
    def update_info(self, data: dict):
        data = data['Team']
        self.aero.setText(str(data['Aerodynamics']))
        self.relia.setText(str(data['Reliability']))
        self.motor.setText(str(data['Motor']))
        self.eletronics.setText(str(data['Electronics']))
        self.suspension.setText(str(data['Suspension']))
        overall = (data['Aerodynamics'] + data['Suspension'] + data['Motor'] +
                   data['Electronics']) / 4
        self.overall.setText(str(int(overall)))
