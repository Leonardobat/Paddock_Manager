# -*- coding: utf-8 -*-
from time import sleep
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (QHeaderView, QHBoxLayout, QLabel, QPushButton,
                               QWidget, QFrame, QGridLayout, QVBoxLayout)
from db import db
from gui.boxes import CarInfo, TeamInfo, FinancialInfo, NewsInfo, RaceInfo, PilotBox, TimingBox
from engine import RacingEngine


class InterfacePrincipal(QWidget):
    database = db()
    race_mode = Signal(int)
    update_signal = Signal(dict)

    def __init__(self):
        self.raceid = 1
        QWidget.__init__(self)
        self.import_data()
        self.palette = QPalette()
        self.palette.setColor(QPalette.Active, QPalette.Window,
                              self.data['Team']['Primary'])
        self.palette.setColor(QPalette.Active, QPalette.WindowText,
                              self.data['Team']['Secondary'])
        self.palette_alt = QPalette()
        self.palette_alt.setColor(QPalette.Active, QPalette.Window,
                                  self.data['Team']['Secondary'])
        self.palette_alt.setColor(QPalette.Active, QPalette.WindowText,
                                  self.data['Team']['Primary'])

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
        ## Create a DB CLASS!!!

        pilot1 = self.data['Pilot 1']['Name']
        pilot2 = self.data['Pilot 2']['Name']

        self.data['Pilot 1']['Info'] = self.update_pilot(pilot1, results)
        self.data['Pilot 2']['Info'] = self.update_pilot(pilot2, results)
        self.data['msg'] = f"{results[0][0]} venceu o" \
            f" {self.data['Next_Track']['Name2']}."
        self.raceid += 1
        track = self.database.track_info(self.raceid)

        if track['Country'].endswith('a'):
            name2 = f"GP da {track['Country']}"
        else:
            name2 = f"GP de {track['Country']}"

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
        team = self.database.team_info(1)
        pilot1 = self.database.pilot_info(team['Name'], 0)
        pilot2 = self.database.pilot_info(team['Name'], 1)
        pilot3 = {'Name': 'S. Vandoorne'}

        track = self.database.track_info(self.raceid)
        if track['Country'].endswith('a'):
            name2 = f"GP da {track['Country']}"
        else:
            name2 = f"GP de {track['Country']}"

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
    database = db()
    normal_mode = Signal(list)

    def __init__(self, raceid: int):
        QWidget.__init__(self)
        self.items = 0
        self.player_pilots = []
        self.play_race = True

        # Test data
        self.import_data(raceid)

        self.TimmingTable = TimingBox(self.pilots, self.teams_colors)
        self.racing = RacingEngine(self.pilots, self.track, self.pilots_status)

        for key in self.pilots:
            if self.pilots[key]['Owner'] != 'IA':
                self.player_pilots.append(key)
        self.pilot1_box = PilotBox(self.player_pilots[0],
                                   self.pilots_status[self.player_pilots[0]])
        self.pilot2_box = PilotBox(self.player_pilots[1],
                                   self.pilots_status[self.player_pilots[1]])

        text = f"{self.track['Name']} - {self.track['Raced Laps']}" \
            f"/{self.track['Total_Laps']}"
        self.pilot1_box.update_info()
        self.pilot2_box.update_info()

        self.status = 'Mensagens'
        self.label_track = QLabel()
        self.label_track.setText(text)
        self.label_track.setAlignment(Qt.AlignRight)

        # Right
        self.back_button = QPushButton('Voltar')
        self.back_button.setEnabled(False)
        self.play_button = QPushButton('Play')
        self.play_button.setMinimumSize(120, 120)
        self.pit_button = QPushButton('Pit Stop')

        # Left
        self.run = QPushButton('Run')
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
        self.pilots_status[self.player_pilots[0]]['Pit-Stop'] = True
        self.pilots_status[self.player_pilots[1]]['Pit-Stop'] = True

    @Slot()
    def run_race(self):
        # Virtual Button, pressed.
        if self.play_race:
            self.run.setDown(True)
            self.play_race = False
            self.play_button.setText('Pause')
        else:
            self.run.setDown(False)
            self.play_race = True
            self.play_button.setText('Play')

    @Slot()
    def update_data(self):
        timming, self.status = self.racing.run()
        self.TimmingTable.update_table(timming)
        if self.track['Raced Laps'] < self.track['Total_Laps']:
            self.track['Raced Laps'] += 1
            text = f"{self.track['Name']} - {self.track['Raced Laps']}" \
            f"/{self.track['Total_Laps']}"
            self.label_track.setText(text)
            self.pilot1_box.update_info()
            self.pilot2_box.update_info()
            if self.status != '':
                text = f'Volta {self.track["Raced Laps"]}:{self.status}'
                self.label_info.setText(text)
            sleep(0.2)
        else:
            self.run_race()
            self.play_button.setEnabled(False)
            self.back_button.setEnabled(True)
            self.list_positions = []
            for i in range(self.TimmingTable.items):
                pilot = self.TimmingTable.table.item(i, 0)
                team = self.TimmingTable.table.item(i, 1)
                self.list_positions.append((pilot.text(), team.text()))

    def import_data(self, raceid):
        self.pilots_status = {}
        self.pilots = {}
        self.track = dict(self.database.track_info(raceid))
        self.track['Raced Laps'] = 0
        self.pilots = self.database.pilots_stats()

        for key in self.pilots:
            if self.pilots[key]['Team'] != 'Mercedes':
                self.pilots[key]['Owner'] = 'IA'
            else:
                self.pilots[key]['Owner'] = 'Player'
            self.pilots_status[key] = {
                'Total Time': 0,
                'Pit-Stop': False,
                'Tires': 100,
                'Car Health': 100,
                'Pit-Stops': 0,
            }

        self.teams_colors = self.database.teams_colors()

    @Slot()
    def finish_race(self):
        list_results = []
        for k in range(len(self.list_positions)):
            pilot, team = self.list_positions[k]
            if k == 0:
                list_results.append((pilot, 1, 25, team))
            elif k == 1:
                list_results.append((pilot, 2, 18, team))
            elif k == 2:
                list_results.append((pilot, 3, 15, team))
            elif k == 3:
                list_results.append((pilot, 4, 12, team))
            elif k == 4:
                list_results.append((pilot, 5, 10, team))
            elif k == 5:
                list_results.append((pilot, 6, 8, team))
            elif k == 6:
                list_results.append((pilot, 7, 6, team))
            elif k == 7:
                list_results.append((pilot, 8, 4, team))
            elif k == 8:
                list_results.append((pilot, 9, 2, team))
            elif k == 9:
                list_results.append((pilot, 10, 1, team))
            else:
                list_results.append((pilot, k + 1, 0, team))
        self.normal_mode.emit(list_results)
        self.close()