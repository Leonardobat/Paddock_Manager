# -*- coding: utf-8 -*-

from time import sleep
from Corrida.motor_corrida import Racing_Engine
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QVBoxLayout, QWidget, QProgressBar, QSizePolicy,
                               QFrame, QGridLayout)
from DB.DB import get_db
from .Race_Boxes.PilotBox import PilotBox
from .Race_Boxes.TimingBox import TimingBox


class Interface_Corrida(QWidget):
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
        self.racing = Racing_Engine(self.dict_pilot, self.dict_track,
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