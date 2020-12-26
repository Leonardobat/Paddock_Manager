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
from DB.DB import get_db


class Interface_Principal(QWidget):
    db = get_db()
    race_mode = Signal()
    update_signal = Signal(dict)

    def __init__(self):
        QWidget.__init__(self)
        self.import_data()
        self.palette = QPalette()
        self.palette.setColor(QPalette.Active, QPalette.Window,
                              self.data['Team']['Primary_Color'])
        self.palette.setColor(QPalette.Active, QPalette.WindowText,
                              self.data['Team']['Secondary_Color'])
        self.palette_alternative = QPalette()
        self.palette_alternative.setColor(QPalette.Active, QPalette.Window,
                                          self.data['Team']['Secondary_Color'])
        self.palette_alternative.setColor(QPalette.Active, QPalette.WindowText,
                                          self.data['Team']['Primary_Color'])

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
        team = self.db.execute('SELECT * FROM teams WHERE id = 1').fetchone()
        team = dict(team)
        team['Primary_Color'] = QColor(int(team['Color1'][0:2], 16),
                                       int(team['Color1'][2:4], 16),
                                       int(team['Color1'][4:6], 16),
                                       int(team['Color1'][6:], 16))
        team['Secondary_Color'] = QColor(int(team['Color2'][0:2], 16),
                                         int(team['Color2'][2:4], 16),
                                         int(team['Color2'][4:6], 16),
                                         int(team['Color2'][6:], 16))

        team['Motor'] = self.db.execute(
            'SELECT Power FROM motors WHERE id = ?',
            (team['motorid'], ),
        ).fetchone()[0]

        team['Sponsor 1'] = {
            'Name':
            team['Sponsor_0'],
            'Value':
            self.db.execute(
                'SELECT Value FROM sponsors WHERE Name = ?',
                (team['Sponsor_0'], ),
            ).fetchone()[0]
        }

        team['Sponsor 2'] = {
            'Name':
            team['Sponsor_1'],
            'Value':
            self.db.execute(
                'SELECT Value FROM sponsors WHERE Name = ?',
                (team['Sponsor_1'], ),
            ).fetchone()[0]
        }

        team['Sponsor 3'] = {
            'Name':
            team['Sponsor_2'],
            'Value':
            self.db.execute(
                'SELECT Value FROM sponsors WHERE Name = ?',
                (team['Sponsor_2'], ),
            ).fetchone()[0]
        }

        team['Sponsor 4'] = {
            'Name':
            team['Sponsor_3'],
            'Value':
            self.db.execute(
                'SELECT Value FROM sponsors WHERE Name = ?',
                (team['Sponsor_3'], ),
            ).fetchone()[0]
        }

        team['Sponsor 5'] = {
            'Name':
            team['Sponsor_4'],
            'Value':
            self.db.execute(
                'SELECT Value FROM sponsors WHERE Name = ?',
                (team['Sponsor_4'], ),
            ).fetchone()[0]
        }

        pilot1 = dict(
            self.db.execute(
                'SELECT * FROM pilots WHERE Team = ?',
                (team['Name'], ),
            ).fetchall()[0])
        pilot1['Info'] = (0, 0, 0, 0)

        pilot2 = dict(
            self.db.execute(
                'SELECT * FROM pilots WHERE Team = ?',
                (team['Name'], ),
            ).fetchall()[1])
        pilot2['Info'] = (0, 0, 0, 0)

        pilot3 = {'Name': 'S. Vandoorne'}

        self.data = {
            'Team': team,
            'Pilot 1': pilot1,
            'Pilot 2': pilot2,
            'Pilot 3': pilot3,
            'Next_Track': {
                'Name1': 'Spa-Francochamps',
                'Name2': 'GP da Bélgica',
                'Total_Laps': 67,
            }
        }
        del team['Color1']
        del team['Color2']
        del team['Sponsor_1']
        del team['Sponsor_0']
        del team['Sponsor_2']
        del team['Sponsor_3']
        del team['Sponsor_4']
