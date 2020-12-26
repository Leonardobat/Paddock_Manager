# -*- coding: utf-8 -*-

from time import sleep
from Corrida.motor_corrida import Racing_Engine
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (QHeaderView, QHBoxLayout, QLabel,
                               QAbstractItemView, QMainWindow, QPushButton,
                               QTableWidget, QTableWidgetItem, QVBoxLayout,
                               QWidget, QProgressBar, QSizePolicy, QFrame,
                               QGridLayout)
from DB.DB import get_db
from .Race_Boxes.PilotBox import PilotBox


class Interface_Corrida(QWidget):
    db = get_db()
    normal_mode = Signal()

    def __init__(self):
        QWidget.__init__(self)
        self.items = 0
        self.pilots = []
        self.play_race = True

        self.import_data()
        self.dict_teams = {
            "Ferrari": {
                "Primary": QColor(255, 40, 0, 255),
                "Secondary": QColor(255, 242, 0, 255),
            },
            "Mercedes": {
                "Primary": QColor(127, 127, 127, 255),
                "Secondary": QColor(0, 0, 0, 255),
            },
            "Willians": {
                "Primary": QColor(135, 206, 235, 255),
                "Secondary": QColor(255, 255, 255, 255),
            },
        }
        # Test data
        self.dict_track = {
            "Name": "Spa-Francochamps",
            "Base Time": 1.7,
            "Difficult": 0.3,
            "Raced Laps": 0,
            "Total_Laps": 67,
            "Weather": 0,
        }

        self.racing = Racing_Engine(self.dict_pilot, self.dict_track)

        # Pilots
        for key in self.dict_pilot:
            if self.dict_pilot[key]["Owner"] != "IA":
                self.pilots.append(key)

        self.pilot1_box = PilotBox(self.pilots[0],
                                   self.dict_race[self.pilots[0]])
        self.pilot2_box = PilotBox(self.pilots[1],
                                   self.dict_race[self.pilots[1]])
        # Right
        self.restart_button = QPushButton("Restart")
        self.back_button = QPushButton("Back")
        self.back_button.setEnabled(False)
        self.play_button = QPushButton("Play")
        self.play_button.setMinimumSize(120, 120)
        self.pit_button = QPushButton("Pit Stop")

        # Left
        self.label_track = QLabel()
        text = "{0} - {1}/{2}".format(
            self.dict_track["Name"],
            self.dict_track["Raced Laps"],
            self.dict_track["Total_Laps"],
        )
        self.label_track.setText(text)
        self.label_track.setAlignment(Qt.AlignRight)
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Pilot", "Team", "Lap Time", "Gap"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.run = QPushButton("Run")
        self.run.setAutoRepeat(True)

        # Layout
        self.layout = QGridLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.label_info = QLabel("Dev Edition")
        self.label_info.setAlignment(Qt.AlignCenter)
        self.label_info.setFrameShape(QFrame.Panel)

        # Right Layout
        self.right_layout.addSpacing(25)
        self.right_layout.addWidget(self.restart_button)
        self.right_layout.addWidget(self.back_button)
        #self.right_layout.addSpacing(10)
        self.right_layout.addWidget(self.pilot1_box)
        self.right_layout.addSpacing(5)
        self.right_layout.addWidget(self.pilot2_box)
        self.right_layout.addSpacing(5)
        self.right_layout.addWidget(self.pit_button)
        self.right_layout.addStretch(1)
        self.right_layout.addWidget(self.play_button, 1)

        # Left Layout
        self.left_layout.addWidget(self.label_track)
        self.left_layout.addWidget(self.table)

        # Set the layout to the QWidget
        self.layout.addLayout(self.left_layout, 0, 0, 1, 1)
        self.layout.addLayout(self.right_layout, 0, 1, 1, 1)
        self.layout.addWidget(self.label_info, 1, 0, 1, 2)
        self.setLayout(self.layout)

        # Signals and Slots
        self.play_button.clicked.connect(self.run_race)
        self.restart_button.clicked.connect(self.restart_race)
        self.back_button.clicked.connect(self.to_main)
        self.pit_button.clicked.connect(self.pit_stop)
        self.run.pressed.connect(self.update_table)

        # Fill example data
        self.fill_table()

    @Slot()
    def restart_race(self):
        self.import_data()
        self.dict_track["Raced Laps"] = 0
        self.play_button.setEnabled(True)

    @Slot()
    def to_main(self):
        self.finish_race()
        self.normal_mode.emit()

    @Slot()
    def import_data(self):
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

    @Slot()
    def pit_stop(self):
        self.dict_race[self.pilots[0]]["Pit-Stop"] = True
        self.dict_race[self.pilots[1]]["Pit-Stop"] = True

    @Slot()
    def run_race(self):
        if self.play_race:
            self.run.setDown(True)
            self.play_race = False
            self.play_button.setText("Pause")
        else:
            self.run.setDown(False)
            self.play_race = True
            self.play_button.setText("Play")

    @Slot()
    def update_table(self):
        times_sorted = []
        times_sorted, self.dict_race = self.racing.run_a_lap(self.dict_race)
        num_pilots = len(times_sorted)

        self.table.setRowCount(0)
        self.items = 0
        for k in range(num_pilots):
            pilot_name, lap, gap = times_sorted[k]

            if k == 0:
                gap_item = QTableWidgetItem("Leader")
            else:
                gap_item = QTableWidgetItem(gap)
            gap_item.setTextAlignment(Qt.AlignCenter)
            team = self.dict_pilot[pilot_name]["Team"]
            team_item = QTableWidgetItem(team)
            team_item.setTextAlignment(Qt.AlignCenter)
            team_item.setBackground(self.dict_teams[team]["Primary"])
            team_item.setForeground(self.dict_teams[team]["Secondary"])

            lap_item = QTableWidgetItem(lap)
            lap_item.setTextAlignment(Qt.AlignCenter)
            pilot_item = QTableWidgetItem(pilot_name)
            pilot_item.setTextAlignment(Qt.AlignCenter)

            if self.items == 0:
                pilot_item.setBackground(QColor(255, 215, 0, 127))
            elif self.items == 1:
                pilot_item.setBackground(QColor(169, 169, 169, 127))
            elif self.items == 2:
                pilot_item.setBackground(QColor(205, 127, 50, 127))
            self.table.insertRow(self.items)
            id_item = QTableWidgetItem("{0}º".format(self.items + 1))
            self.table.setVerticalHeaderItem(self.items, id_item)
            self.table.setItem(self.items, 0, pilot_item)
            self.table.setItem(self.items, 1, team_item)
            self.table.setItem(self.items, 2, lap_item)
            self.table.setItem(self.items, 3, gap_item)
            self.items += 1

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
            sleep(0.1)
        else:
            self.run_race()
            self.play_button.setEnabled(False)
            self.back_button.setEnabled(True)
            self.list_positions = []
            for i in range(self.items):
                pilot = self.table.item(i, 0)
                self.list_positions.append(pilot.text())

    def fill_table(self):
        data = self.dict_race

        for key in data.keys():
            lap_item = QTableWidgetItem("0:0.000")
            lap_item.setTextAlignment(Qt.AlignCenter)

            gap_item = QTableWidgetItem("+0:0.000")
            gap_item.setTextAlignment(Qt.AlignCenter)

            team = self.dict_pilot[key]["Team"]
            team_item = QTableWidgetItem(team)
            team_item.setTextAlignment(Qt.AlignCenter)
            team_item.setBackground(self.dict_teams[team]["Primary"])
            team_item.setForeground(self.dict_teams[team]["Secondary"])

            pilot_item = QTableWidgetItem(key)
            pilot_item.setTextAlignment(Qt.AlignCenter)
            self.table.insertRow(self.items)
            id_item = QTableWidgetItem("{0}º".format(self.items + 1))
            self.table.setVerticalHeaderItem(self.items, id_item)
            self.table.setItem(self.items, 0, pilot_item)
            self.table.setItem(self.items, 1, team_item)
            self.table.setItem(self.items, 2, lap_item)
            self.table.setItem(self.items, 3, gap_item)
            self.items += 1

    @Slot()
    def finish_race(self):
        del self.dict_race
        del self.dict_pilot
        self.list_positions
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
        print(list_results)
