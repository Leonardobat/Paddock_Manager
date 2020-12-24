# -*- coding: utf-8 -*-

from time import sleep
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QPainter, QColor, QPalette, QFont
from PySide6.QtWidgets import (QHeaderView, QHBoxLayout, QLabel,
                               QAbstractItemView, QMainWindow, QPushButton,
                               QTableWidget, QTableWidgetItem, QVBoxLayout,
                               QWidget, QProgressBar, QSizePolicy, QFrame,
                               QGridLayout)


class Interface_Principal(QWidget):
    race_mode = Signal()

    def __init__(self):
        QWidget.__init__(self)
        self.font = QFont()
        self.font.setItalic(True)
        data = self.import_data()
        self.palette = QPalette()
        self.palette.setColor(QPalette.Active, QPalette.Window,
                              data['Team']['Color']['Primary'])
        self.palette.setColor(QPalette.Active, QPalette.WindowText,
                              data['Team']['Color']['Secondary'])
        self.palette_title = QPalette()
        self.palette_title.setColor(QPalette.Active, QPalette.Window,
                                    data['Team']['Color']['Secondary'])
        self.palette_title.setColor(QPalette.Active, QPalette.WindowText,
                                    data['Team']['Color']['Primary'])

        # Car Info
        self.carbox = QGridLayout()
        self.carframe = QFrame()
        self.carframe.setFrameShape(QFrame.Box)
        self.carbox_title = QLabel('Carro')
        self.carbox_title.setPalette(self.palette_title)
        self.carbox_title.setAlignment(Qt.AlignCenter)
        self.carbox_title.setAutoFillBackground(True)
        self.carbox.addWidget(self.carbox_title, 0, 0, 1, 4)
        self.carbox.addWidget(self.carframe, 0, 0, 7, 4)
        self.carbox.addWidget(QLabel('Aerodinâmica'), 1, 1)
        self.aero = QLabel(str(data['Car']['Aerodynamics']))
        self.carbox.addWidget(self.aero, 1, 2)
        self.carbox.addWidget(QLabel('Confiabilidade'), 2, 1)
        self.relia = QLabel(str(data['Car']['Reliability']))
        self.carbox.addWidget(self.relia, 2, 2)
        self.carbox.addWidget(QLabel('Motor'), 3, 1)
        self.motor = QLabel(str(data['Car']['Motor']))
        self.carbox.addWidget(self.motor, 3, 2)
        self.carbox.addWidget(QLabel('Eletrônica'), 4, 1)
        self.eletronics = QLabel(str(data['Car']['Electronics']))
        self.carbox.addWidget(self.eletronics, 4, 2)
        self.carbox.addWidget(QLabel('Suspensão'), 5, 1)
        self.suspension = QLabel(str(data['Car']['Suspension']))
        self.carbox.addWidget(self.suspension, 5, 2)
        self.carbox.addWidget(QLabel('Geral'), 6, 1)
        self.overall = (data['Car']['Aerodynamics'] +
                        data['Car']['Suspension'] + data['Car']['Motor'] +
                        data['Car']['Electronics']) / 4
        self.overall = QLabel(str(int(self.overall)))
        self.carbox.addWidget(
            self.overall,
            6,
            2,
        )

        # Team Info
        self.teamframe = QFrame()
        self.teamframe.setFrameShape(QFrame.Box)
        self.teambox = QGridLayout()
        self.team_name = QLabel(data['Team']['Name'])
        self.team_name.setPalette(self.palette_title)
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

        self.teambox.addWidget(self.team_name, 0, 0, 1, 4)
        self.teambox.addWidget(self.teamframe, 0, 0, 7, 4)
        self.teambox.addWidget(QLabel('Chefe da Equipe'), 1, 1)
        self.teambox.addWidget(self.user_name, 1, 2)
        self.teambox.addWidget(QLabel('Piloto 1'), 2, 1)
        self.teambox.addWidget(QLabel(data['Pilot 1']), 2, 2)
        self.teambox.addWidget(self.info_p1, 3, 1, 1, 2)
        self.teambox.addWidget(QLabel('Piloto 2'), 4, 1)
        self.teambox.addWidget(QLabel(data['Pilot 2']), 4, 2)
        self.teambox.addWidget(self.info_p2, 5, 1, 1, 2)
        self.teambox.addWidget(QLabel('Reserva'), 6, 1)
        self.teambox.addWidget(QLabel(data['Pilot 3']), 6, 2)

        # Financial Info
        self.finframe = QFrame()
        self.finframe.setFrameShape(QFrame.Box)
        self.finanbox = QGridLayout()
        self.finanbox_title = QLabel('Finanças')
        self.finanbox_title.setPalette(self.palette_title)
        self.finanbox_title.setAlignment(Qt.AlignCenter)
        self.finanbox_title.setAutoFillBackground(True)
        self.finanbox.addWidget(self.finanbox_title, 0, 0, 1, 4)
        self.finanbox.addWidget(self.finframe, 0, 0, 7, 4)
        self.finanbox.addWidget(QLabel('Caixa'), 1, 1)
        self.finanbox.addWidget(QLabel(data['Cash']), 1, 2)
        self.finanbox.addWidget(QLabel(data['Sponsor 1']['Name']), 2, 1)
        self.finanbox.addWidget(QLabel(data['Sponsor 1']['Value']), 2, 2)
        self.finanbox.addWidget(QLabel(data['Sponsor 2']['Name']), 3, 1)
        self.finanbox.addWidget(QLabel(data['Sponsor 2']['Value']), 3, 2)
        self.finanbox.addWidget(QLabel(data['Sponsor 3']['Name']), 4, 1)
        self.finanbox.addWidget(QLabel(data['Sponsor 3']['Value']), 4, 2)
        self.finanbox.addWidget(QLabel(data['Sponsor 4']['Name']), 5, 1)
        self.finanbox.addWidget(QLabel(data['Sponsor 4']['Value']), 5, 2)
        self.finanbox.addWidget(QLabel(data['Sponsor 5']['Name']), 6, 1)
        self.finanbox.addWidget(QLabel(data['Sponsor 5']['Value']), 6, 2)

        # Layout
        self.grid = QGridLayout()
        self.grid.addLayout(self.carbox, 0, 0, 1, 1)
        self.grid.addLayout(self.teambox, 0, 1, 1, 1)
        self.grid.addLayout(self.finanbox, 0, 2, 1, 1)
        self.news = QLabel('DEV')
        self.grid.addWidget(self.news, 1, 0, 1, 1)
        self.next_race = QLabel('DEV')
        self.grid.addWidget(self.next_race, 1, 1, 1, 1)
        button = QPushButton('Corrida')
        button.clicked.connect(self.to_race)
        self.grid.addWidget(button, 1, 2, 1, 1)
        self.grid.setRowStretch(0, 1)
        self.grid.setRowStretch(1, 2)
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)
        self.setLayout(self.grid)

    @Slot()
    def to_race(self):
        self.race_mode.emit()

    def import_data(self):
        ret = {
            'Team': {
                'Name': 'Mercedes-AMG Petronas F1',
                'Principal': 'Toto Wolff',
                'Color': {
                    'Primary': QColor(127, 127, 127, 255),
                    'Secondary': QColor(0, 0, 0, 255),
                }
            },
            'Pilot 1': 'L. Hamilton',
            'Pilot 2': 'V. Bottas',
            'Pilot 3': 'S. Vandoorne',
            'Sponsor 1': {
                'Name': 'Petronas',
                'Value': '£ 60 Mi'
            },
            'Sponsor 2': {
                'Name': 'Ineos',
                'Value': '£ 40 Mi'
            },
            'Sponsor 3': {
                'Name': 'EPSON',
                'Value': '£ 10 Mi'
            },
            'Sponsor 4': {
                'Name': 'UBS',
                'Value': '£ 10 Mi'
            },
            'Sponsor 5': {
                'Name': 'BOSE',
                'Value': '£ 10 Mi'
            },
            'Cash': '£ 300 Mi',
            'Car': {
                'Aerodynamics': 100,
                'Electronics': 100,
                'Motor': 100,
                'Suspension': 100,
                'Reliability': 100,
            },
        }
        return ret