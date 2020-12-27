# -*- coding: utf-8 -*-
from time import sleep
import re
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (QHeaderView, QHBoxLayout, QLabel, QPushButton,
                               QWidget, QFrame, QGridLayout, QVBoxLayout)
from db import get_db
from gui.boxes import CarInfo, TeamInfo, FinancialInfo, NewsInfo, RaceInfo, PilotBox, TimingBox
from engine import RacingEngine


class InterfacePrincipal(QWidget):
    db = get_db()
    race_mode = Signal(int)
    update_signal = Signal(dict)

    def __init__(self):
        self.raceid = 1
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
        self.carbox = CarInfo(self.data['Team'], self.palette)
        self.teambox = TeamInfo(self.data, self.palette)
        self.finanbox = FinancialInfo(self.data['Team'], self.palette)
        self.newsbox = NewsInfo(None, self.palette)
        self.racebox = RaceInfo(self.data, self.palette)
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
        self.race_mode.emit(self.raceid)

    @Slot()
    def update_info(self, results: list):

        pilot1 = self.data['Pilot 1']['Name']
        pilot2 = self.data['Pilot 2']['Name']

        self.data['Pilot 1']['Info'] = self.update_pilot(pilot1, results)
        self.data['Pilot 2']['Info'] = self.update_pilot(pilot2, results)
        self.data['msg'] = '{} venceu o {}.'.format(
            results[0][0], self.data['Next_Track']['Name2'])

        self.raceid += 1
        track = self.db.execute(
            'SELECT Name, Country, Total_Laps FROM tracks WHERE id = ?',
            (self.raceid, )).fetchone()

        if re.search('a$', track['Country']) != None:
            name2 = 'GP da {}'.format(track['Country'])
        else:
            name2 = 'GP de {}'.format(track['Country'])

        self.data['Next_Track'] = {
            'Name1': track['Name'],
            'Name2': name2,
            'Total_Laps': track['Total_Laps'],
        }

        self.update_signal.emit(self.data)

    def update_pilot(self, pilot: str, results: list):
        if pilot == self.data['Pilot 1']['Name']:
            pilot_old = self.data['Pilot 1']['Info']
        else:
            pilot_old = self.data['Pilot 2']['Info']

        for result in results:
            if pilot in result:
                if result[2] > 0:
                    points = result[2] + pilot_old[3]
                else:
                    points = pilot_old[3]
                break

        if result[2] == 25:
            victories = pilot_old[1] + 1
        else:
            victories = pilot_old[1]
        return (pilot_old[0], victories, pilot_old[2], points)

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

        track = self.db.execute(
            'SELECT Name, Country, Total_Laps FROM tracks WHERE id = ?',
            (self.raceid, )).fetchone()

        if re.search('a$', track['Country']) != None:
            name2 = 'GP da {}'.format(track['Country'])
        else:
            name2 = 'GP de {}'.format(track['Country'])

        self.data = {
            'Team': team,
            'Pilot 1': pilot1,
            'Pilot 2': pilot2,
            'Pilot 3': pilot3,
            'Next_Track': {
                'Name1': track['Name'],
                'Name2': name2,
                'Total_Laps': track['Total_Laps'],
            }
        }


class InterfaceCorrida(QWidget):
    db = get_db()
    normal_mode = Signal(list)

    def __init__(self, raceid: int):
        QWidget.__init__(self)
        self.items = 0
        self.pilots = []
        self.play_race = True

        # Test data
        self.import_data(raceid)

        self.TimmingTable = TimingBox(self.dict_pilot, self.dict_teams)
        self.racing = RacingEngine(self.dict_pilot, self.dict_track,
                                   self.dict_race)

        for key in self.dict_pilot:
            if self.dict_pilot[key]["Owner"] != "IA":
                self.pilots.append(key)
        self.pilot1_box = PilotBox(self.pilots[0],
                                   self.dict_race[self.pilots[0]])
        self.pilot2_box = PilotBox(self.pilots[1],
                                   self.dict_race[self.pilots[1]])

        text = "{0} - {1}/{2}".format(
            self.dict_track["Name"],
            self.dict_track["Raced Laps"],
            self.dict_track["Total_Laps"],
        )
        self.pilot1_box.update_info()
        self.pilot2_box.update_info()

        self.status = "Mensagens"
        self.label_track = QLabel()
        self.label_track.setText(text)
        self.label_track.setAlignment(Qt.AlignRight)

        # Right
        self.back_button = QPushButton("Back")
        self.back_button.setEnabled(False)
        self.play_button = QPushButton("Play")
        self.play_button.setMinimumSize(120, 120)
        self.pit_button = QPushButton("Pit Stop")

        # Left
        self.run = QPushButton("Run")
        self.run.setAutoRepeat(True)

        # Layout
        self.layout = QGridLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.label_info = QLabel(self.status)
        self.label_info.setAlignment(Qt.AlignCenter)
        self.label_info.setFrameShape(QFrame.Panel)

        # Right Layout
        self.right_layout.addSpacing(25)
        self.right_layout.addWidget(self.back_button)
        self.right_layout.addSpacing(10)
        self.right_layout.addWidget(self.pilot1_box)
        self.right_layout.addSpacing(5)
        self.right_layout.addWidget(self.pilot2_box)
        self.right_layout.addSpacing(5)
        self.right_layout.addWidget(self.pit_button)
        self.right_layout.addStretch(1)
        self.right_layout.addWidget(self.play_button, 1)

        # Left Layout
        self.left_layout.addWidget(self.label_track)
        self.left_layout.addWidget(self.TimmingTable)

        # Set the layout to the QWidget
        self.layout.addLayout(self.left_layout, 0, 0, 1, 1)
        self.layout.addLayout(self.right_layout, 0, 1, 1, 1)
        self.layout.addWidget(self.label_info, 1, 0, 1, 2)
        self.setLayout(self.layout)

        # Signals and Slots
        self.play_button.clicked.connect(self.run_race)
        self.back_button.clicked.connect(self.finish_race)
        self.pit_button.clicked.connect(self.pit_stop)
        self.run.pressed.connect(self.update_data)

    @Slot()
    def pit_stop(self):
        self.dict_race[self.pilots[0]]["Pit-Stop"] = True
        self.dict_race[self.pilots[1]]["Pit-Stop"] = True

    @Slot()
    def run_race(self):
        # Virtual Button, pressed.
        if self.play_race:
            self.run.setDown(True)
            self.play_race = False
            self.play_button.setText("Pause")
        else:
            self.run.setDown(False)
            self.play_race = True
            self.play_button.setText("Play")

    @Slot()
    def update_data(self):
        timming, self.status = self.racing.run_a_lap()
        self.TimmingTable.update_table(timming)
        if self.dict_track["Raced Laps"] < self.dict_track["Total_Laps"]:
            self.dict_track["Raced Laps"] += 1
            text = "{0} - {1}/{2}".format(
                self.dict_track["Name"],
                self.dict_track["Raced Laps"],
                self.dict_track["Total_Laps"],
            )
            self.label_track.setText(text)
            self.pilot1_box.update_info()
            self.pilot2_box.update_info()
            if self.status != '':
                text = 'Volta {}:{}'.format(self.dict_track["Raced Laps"],
                                            self.status)
                self.label_info.setText(text)
            sleep(0.1)
        else:
            self.run_race()
            self.play_button.setEnabled(False)
            self.back_button.setEnabled(True)
            self.list_positions = []
            for i in range(self.TimmingTable.items):
                pilot = self.TimmingTable.table.item(i, 0)
                self.list_positions.append(pilot.text())

    def import_data(self, raceid):
        track = self.db.execute(
            'SELECT Name, Base_Time, Difficult, Total_Laps,'
            ' Weather FROM tracks WHERE id = ?', (raceid, )).fetchone()
        self.dict_track = {
            "Name": track['Name'],
            "Base Time": track['Base_Time'],
            "Difficult": track['Difficult'],
            "Raced Laps": 0,
            "Total_Laps": track['Total_Laps'],
            "Weather": track['Weather'],
        }

        pilot_keys = self.db.execute('SELECT Name FROM pilots').fetchall()
        pilot_keys = [i[0] for i in pilot_keys]
        self.dict_race = {}
        self.dict_pilot = {}
        for key in pilot_keys:
            self.dict_pilot[key] = dict(
                self.db.execute(
                    'SELECT Speed, Smoothness, Determination,'
                    ' Agressive, Overtaking, Team FROM pilots'
                    ' WHERE Name = ?',
                    (key, ),
                ).fetchone())
            team_data = list(
                self.db.execute(
                    'SELECT Aerodynamics, Electronics, Suspension,'
                    ' motorid, Reliability FROM teams WHERE Name = ?',
                    (self.dict_pilot[key]['Team'], ),
                ).fetchone())
            team_data[3] = self.db.execute(
                'SELECT Power FROM motors WHERE id = ?',
                (team_data[3], ),
            ).fetchone()[0]

            self.dict_pilot[key]['Car'] = sum(team_data[:4]) / 4
            if self.dict_pilot[key]['Team'] != 'Mercedes':
                self.dict_pilot[key]['Owner'] = 'IA'
            else:
                self.dict_pilot[key]['Owner'] = 'Player'
            self.dict_race[key] = {
                "Total Time": 0,
                "Pit-Stop": False,
                "Tires": 100,
                "Car Health": team_data[4],
                "Pit-Stops": 0,
            }

        team = self.db.execute(
            'SELECT Name, Color1, Color2 FROM teams').fetchall()
        team = [dict(i) for i in team]
        self.dict_teams = {}
        for data in team:
            name = data['Name']
            self.dict_teams[name] = {}
            self.dict_teams[name]['Primary'] = QColor(
                int(data['Color1'][0:2], 16), int(data['Color1'][2:4], 16),
                int(data['Color1'][4:6], 16), int(data['Color1'][6:], 16))
            self.dict_teams[name]['Secondary'] = QColor(
                int(data['Color2'][0:2], 16), int(data['Color2'][2:4], 16),
                int(data['Color2'][4:6], 16), int(data['Color2'][6:], 16))

    @Slot()
    def finish_race(self):
        list_results = []
        for k in range(len(self.list_positions)):
            if k == 0:
                list_results.append((self.list_positions[0], 1, 25))
            elif k == 1:
                list_results.append((self.list_positions[1], 2, 18))
            elif k == 2:
                list_results.append((self.list_positions[2], 3, 15))
            elif k == 3:
                list_results.append((self.list_positions[3], 4, 12))
            elif k == 4:
                list_results.append((self.list_positions[4], 5, 10))
            elif k == 5:
                list_results.append((self.list_positions[5], 6, 8))
            elif k == 6:
                list_results.append((self.list_positions[6], 7, 6))
            elif k == 7:
                list_results.append((self.list_positions[7], 8, 4))
            elif k == 8:
                list_results.append((self.list_positions[8], 9, 2))
            elif k == 9:
                list_results.append((self.list_positions[9], 10, 1))
            else:
                list_results.append((self.list_positions[k], k + 1, 0))
        self.normal_mode.emit(list_results)
        self.close()