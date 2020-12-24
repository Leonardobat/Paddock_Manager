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
from .Info_Boxes.News_Info import News_Info
from .Info_Boxes.Race_Info import Race_Info


class Interface_Principal(QWidget):
    race_mode = Signal()
    update_signal = Signal(dict)

    def __init__(self):
        QWidget.__init__(self)
        self.data = self.import_data()
        self.palette = QPalette()
        self.palette.setColor(QPalette.Active, QPalette.Window,
                              self.data['Team']['Color']['Primary'])
        self.palette.setColor(QPalette.Active, QPalette.WindowText,
                              self.data['Team']['Color']['Secondary'])
        self.palette_alternative = QPalette()
        self.palette_alternative.setColor(
            QPalette.Active, QPalette.Window,
            self.data['Team']['Color']['Secondary'])
        self.palette_alternative.setColor(
            QPalette.Active, QPalette.WindowText,
            self.data['Team']['Color']['Primary'])

        # Boxes
        self.carbox = Car_Info(self.data, self.palette)
        self.teambox = Team_Info(self.data, self.palette)
        self.finanbox = Financial_Info(self.data, self.palette)
        self.newsbox = News_Info(None, self.palette)
        self.racebox = Race_Info(self.data, self.palette)
        self.update_signal.connect(self.carbox.update_info)
        self.update_signal.connect(self.teambox.update_info)
        self.update_signal.connect(self.finanbox.update_info)
        self.update_signal.connect(self.newsbox.update_news)
        self.update_signal.connect(self.racebox.update_info)
        self.racebox.race_button.clicked.connect(self.to_race)

        # Layout
        self.grid = QGridLayout()
        self.grid.addWidget(self.carbox, 0, 0, 1, 1)
        self.grid.addWidget(self.teambox, 0, 1, 1, 1)
        self.grid.addWidget(self.finanbox, 0, 2, 1, 1)
        self.grid.addWidget(self.newsbox, 1, 0, 1, 2)
        self.grid.addWidget(self.racebox, 1, 2)
        self.grid.setRowStretch(0, 3)
        self.grid.setRowStretch(1, 1)
        self.setLayout(self.grid)
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)

    @Slot()
    def to_race(self):
        self.race_mode.emit()

    @Slot()
    def update_info(self):
        if 'msg' not in self.data:
            self.data['msg'] = 'Não há nenhuma notícia nova.'
        self.update_signal.emit(self.data)

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
            'Pilot 1': {
                'Name': 'L. Hamilton',
                'Info': (0, 0, 0, 0)
            },
            'Pilot 2': {
                'Name': 'V. Bottas',
                'Info': (0, 0, 0, 0)
            },
            'Pilot 3': {
                'Name': 'S. Vandoorne',
                'Info': (0, 0, 0, 0)
            },
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
            'Next_Track': {
                'Name1': 'Spa-Francochamps',
                'Name2': 'GP da Bélgica',
                'Total_Laps': 67,
            }
        }
        return ret