# -*- coding: utf-8 -*-

from time import sleep
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QPainter, QColor, QPalette, QFont
from PySide6.QtWidgets import (QHeaderView, QHBoxLayout, QLabel,
                               QAbstractItemView, QMainWindow, QPushButton,
                               QTableWidget, QTableWidgetItem, QVBoxLayout,
                               QWidget, QProgressBar, QSizePolicy, QFrame,
                               QGridLayout)
from .Info_Boxes.Car_Info import Car_Info
from .Info_Boxes.Team_Info import Team_Info
from .Info_Boxes.Financial_Info import Financial_Info

class Interface_Principal(QWidget):
    race_mode = Signal()

    def __init__(self):
        QWidget.__init__(self)
        data = self.import_data()
        self.palette = QPalette()
        self.palette.setColor(QPalette.Active, QPalette.Window,
                              data['Team']['Color']['Primary'])
        self.palette.setColor(QPalette.Active, QPalette.WindowText,
                              data['Team']['Color']['Secondary'])
        self.palette_alternative = QPalette()
        self.palette_alternative.setColor(QPalette.Active, QPalette.Window,
                                          data['Team']['Color']['Secondary'])
        self.palette_alternative.setColor(QPalette.Active, QPalette.WindowText,
                                          data['Team']['Color']['Primary'])

        # Boxes
        self.carbox = Car_Info(data, self.palette)
        self.teambox = Team_Info(data, self.palette)
        self.finanbox = Financial_Info(data, self.palette)

        # News Box
        self.news_title = QLabel('Notícias')
        self.news_title.setPalette(self.palette)
        self.news_title.setAlignment(Qt.AlignCenter)
        self.news_title.setAutoFillBackground(True)
        self.news = QLabel('Notícias')
        self.news.setAlignment(Qt.AlignCenter)
        self.newsframe = QFrame()
        self.newsframe.setFrameShape(QFrame.Panel)
        self.newsframe.setFrameShadow(QFrame.Sunken)

        self.newsbox = QGridLayout()
        self.newsbox.addWidget(self.news_title, 0, 0)
        self.newsbox.addWidget(self.newsframe, 0, 0, 2, 1)
        self.newsbox.addWidget(self.news, 1, 0)
        self.newsbox.setRowStretch(0, 1)
        self.newsbox.setRowStretch(1, 3)

        # Race Box
        self.next_race = QLabel('Próximo GP:')
        self.next_race.setAlignment(Qt.AlignCenter)
        self.next_race.setFrameShape(QFrame.Panel)
        self.next_race.setFrameShadow(QFrame.Sunken)
        self.race_button = QPushButton('Corrida')
        self.race_button.clicked.connect(self.to_race)
        self.racebox = QGridLayout()
        self.racebox.addWidget(self.next_race, 0, 0)
        self.racebox.addWidget(self.race_button, 1, 0)

        # Layout
        self.grid = QGridLayout()
        self.grid.addWidget(self.carbox, 0, 0, 1, 1)
        self.grid.addWidget(self.teambox, 0, 1, 1, 1)
        self.grid.addWidget(self.finanbox, 0, 2, 1, 1)
        self.grid.addLayout(self.newsbox, 1, 0, 1, 2)
        self.grid.addLayout(self.racebox, 1, 2)
        self.grid.setRowStretch(0, 3)
        self.grid.setRowStretch(1, 1)
        self.setLayout(self.grid)
        #self.setPalette(self.palette)
        #self.setAutoFillBackground(True)

    @Slot()
    def to_race(self):
        self.race_mode.emit()

    def import_data(self):
        ret = {
            'Team': {
                'Name': 'Mercedes-AMG Petronas F1',
                'Principal': 'Toto Wolff',
                'Color': {
                    'Primary': QColor(255, 40, 0, 255),
                    'Secondary': QColor(255, 242, 0, 255),
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