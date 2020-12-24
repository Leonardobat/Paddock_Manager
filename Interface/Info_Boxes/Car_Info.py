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

        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Panel)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.title = QLabel('Carro')
        self.title.setPalette(palette)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setAutoFillBackground(True)
        self.aero = QLabel(str(data['Team']['Aerodynamics']))
        self.relia = QLabel(str(data['Team']['Reliability']))
        self.motor = QLabel(str(data['Team']['Motor']))
        self.eletronics = QLabel(str(data['Team']['Electronics']))
        self.suspension = QLabel(str(data['Team']['Suspension']))
        self.overall = (data['Team']['Aerodynamics'] +
                        data['Team']['Suspension'] + data['Team']['Motor'] +
                        data['Team']['Electronics']) / 4
        self.overall = QLabel(str(int(self.overall)))

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.title, 0, 0, 1, 4)
        self.layout.addWidget(self.frame, 0, 0, 7, 4)
        self.layout.addWidget(QLabel('Aerodinâmica'), 1, 1)
        self.layout.addWidget(self.aero, 1, 2)
        self.layout.addWidget(QLabel('Confiabilidade'), 2, 1)
        self.layout.addWidget(self.relia, 2, 2)
        self.layout.addWidget(QLabel('Motor'), 3, 1)
        self.layout.addWidget(self.motor, 3, 2)
        self.layout.addWidget(QLabel('Eletrônica'), 4, 1)
        self.layout.addWidget(self.eletronics, 4, 2)
        self.layout.addWidget(QLabel('Suspensão'), 5, 1)
        self.layout.addWidget(self.suspension, 5, 2)
        self.layout.addWidget(QLabel('Geral'), 6, 1)
        self.layout.addWidget(self.overall, 6, 2)
        self.setLayout(self.layout)
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)

    @Slot()
    def update_info(self, data: dict):
        self.aero.setText(str(data['Car']['Aerodynamics']))
        self.relia.setText(str(data['Car']['Reliability']))
        self.motor.setText(str(data['Car']['Motor']))
        self.eletronics.setText(str(data['Car']['Electronics']))
        self.suspension.setText(str(data['Car']['Suspension']))
        overall = (data['Car']['Aerodynamics'] + data['Car']['Suspension'] +
                   data['Car']['Motor'] + data['Car']['Electronics']) / 4
        self.overall.setText(str(int(overall)))
