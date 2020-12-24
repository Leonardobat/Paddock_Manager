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


class Interface_Corrida(QWidget):
    db = get_db()
    normal_mode = Signal()

    def __init__(self):
        QWidget.__init__(self)
        self.items = 0
        self.pilots = []
        self.play_race = True

        # Test data
        self.dict_pilot = {
            "C. Sainz": {
                "Speed": 77,
                "Smoothness": 83,
                "Determination": 85,
                "Agressive": 74,
                "Overtaking": 77,
                "Car": 78,
                "Team": "Ferrari",
                "Owner": "IA",
            },
            "C. Leclerc": {
                "Speed": 80,
                "Smoothness": 79,
                "Determination": 87,
                "Agressive": 81,
                "Overtaking": 80,
                "Car": 80,
                "Team": "Ferrari",
                "Owner": "IA",
            },
            "L. Hamilton": {
                "Speed": 91,
                "Smoothness": 93,
                "Determination": 98,
                "Agressive": 75,
                "Overtaking": 90,
                "Car": 95,
                "Team": "Mercedes",
                "Owner": "Player",
            },
            "V. Bottas": {
                "Speed": 83,
                "Smoothness": 87,
                "Determination": 78,
                "Agressive": 72,
                "Overtaking": 82,
                "Car": 95,
                "Team": "Mercedes",
                "Owner": "Player",
            },
            "G. Russell": {
                "Speed": 85,
                "Smoothness": 78,
                "Determination": 90,
                "Agressive": 78,
                "Overtaking": 79,
                "Car": 67,
                "Team": "Willians",
                "Owner": "IA",
            },
        }
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
        self.dict_track = {
            "Name": "Spa-Francochamps",
            "Base Time": 1.7,
            "Difficult": 0.3,
            "Raced Laps": 0,
            "Total_Laps": 67,
            "Weather": 0,
        }

        # Pilots
        for key in self.dict_pilot:
            if self.dict_pilot[key]["Owner"] != "IA":
                self.pilots.append(key)

        self.pilot1_name = QLabel(self.pilots[0])
        self.pilot1_name.setAlignment(Qt.AlignCenter)
        self.pilot1_label_tire = QLabel("Tires:")
        self.pilot1_tire_bar = QProgressBar()
        self.pilot1_tire_bar.setSizePolicy(QSizePolicy.Preferred,
                                           QSizePolicy.Minimum)
        self.pilot1_tire_bar.setRange(0, 100)
        self.pilot1_tire_bar.setValue(self.dict_race[self.pilots[0]]["Tires"])
        self.pilot1_label_pitstops = QLabel("Pitstops: {}".format(
            self.dict_race[self.pilots[0]]["Pit-Stops"]))

        self.pilot2_name = QLabel(self.pilots[1])
        self.pilot2_name.setAlignment(Qt.AlignCenter)
        self.pilot2_label_tire = QLabel("Tires:")
        self.pilot2_tire_bar = QProgressBar()
        self.pilot2_tire_bar.setSizePolicy(QSizePolicy.Preferred,
                                           QSizePolicy.Minimum)
        self.pilot2_tire_bar.setRange(0, 100)
        self.pilot2_tire_bar.setValue(self.dict_race[self.pilots[1]]["Tires"])
        self.pilot2_label_pitstops = QLabel("Pitstops: {}".format(
            self.dict_race[self.pilots[1]]["Pit-Stops"]))

        # Right
        self.restart_button = QPushButton("Restart")
        self.back_button = QPushButton("Back")
        self.back_button.setEnabled(False)
        self.pit_button = QPushButton("Pit Stop")
        self.play_button = QPushButton("Play")
        self.play_button.setMinimumSize(120, 120)

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
        self.pilots_layout = QVBoxLayout()
        self.pilot1_layout = QGridLayout()
        self.pilot2_layout = QGridLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.label_info = QLabel("Dev Edition")
        self.label_info.setAlignment(Qt.AlignCenter)
        self.label_info.setFrameShape(QFrame.Panel)

        # Pilots Info Layout
        self.box_1 = QFrame()
        self.box_1.setFrameShape(QFrame.StyledPanel)
        self.pilot1_layout.addWidget(self.box_1, 0, 0, 6, 3)
        self.pilot1_layout.addWidget(self.pilot1_name, 1, 1)
        self.pilot1_layout.addWidget(self.pilot1_label_tire, 2, 1)
        self.pilot1_layout.addWidget(self.pilot1_tire_bar, 3, 1)
        self.pilot1_layout.addWidget(self.pilot1_label_pitstops, 4, 1)

        self.box_2 = QFrame()
        self.box_2.setFrameShape(QFrame.StyledPanel)
        self.pilot2_layout.addWidget(self.box_2, 0, 0, 6, 3)
        self.pilot2_layout.addWidget(self.pilot2_name, 1, 1)
        self.pilot2_layout.addWidget(self.pilot2_label_tire, 2, 1)
        self.pilot2_layout.addWidget(self.pilot2_tire_bar, 3, 1)
        self.pilot2_layout.addWidget(self.pilot2_label_pitstops, 4, 1)

        self.pilots_layout.addLayout(self.pilot1_layout)
        self.pilots_layout.addSpacing(5)
        self.pilots_layout.addLayout(self.pilot2_layout)
        self.pilots_layout.addSpacing(5)
        self.pilots_layout.addWidget(self.pit_button, 0)

        # Right Layout
        self.right_layout.addSpacing(25)
        self.right_layout.addWidget(self.restart_button)
        self.right_layout.addWidget(self.back_button)
        #self.right_layout.addSpacing(10)
        self.right_layout.addLayout(self.pilots_layout)
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
        times_sorted, self.dict_race = Racing_Engine(
            self.dict_pilot, self.dict_track).run_a_lap(self.dict_race)
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
            sleep(0.2)
            self.dict_track["Raced Laps"] += 1
            text = "{0} - {1}/{2}".format(
                self.dict_track["Name"],
                self.dict_track["Raced Laps"],
                self.dict_track["Total_Laps"],
            )
            self.label_track.setText(text)
            self.pilot1_tire_bar.setValue(
                self.dict_race[self.pilots[0]]["Tires"])
            self.pilot2_tire_bar.setValue(
                self.dict_race[self.pilots[1]]["Tires"])
            self.pilot1_label_pitstops.setText("Pitstops: {0}".format(
                self.dict_race[self.pilots[0]]["Pit-Stops"]))
            self.pilot2_label_pitstops.setText("Pitstops: {0}".format(
                self.dict_race[self.pilots[1]]["Pit-Stops"]))
        else:
            self.run_race()
            self.play_button.setEnabled(False)
            self.back_button.setEnabled(True)

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
    def to_main(self):
        self.normal_mode.emit()

    @Slot()
    def clear_data(self):
        pass

    @Slot()
    def import_data(self):
        pilot_keys = self.db.execute('SELECT Name FROM pilots').fetchall()
        pilot_keys = [i[0] for i in pilot_keys]
        self.dict_race = {}
        for key in pilot_keys:
            self.dict_pilot[key] = dict(
                self.db.execute(
                    'SELECT (Speed, Smoothness, Determination,'
                    ' Agressive, Overtaking, Team) FROM pilots'
                    ' WHERE Name = ?',
                    (key, ),
                ).fetchone())

            if self.dict_pilot[key]['Team'] != 'Mercerdes':
                self.dict_pilot[key]['Owner'] = 'IA'
            else:
                self.dict_pilot[key]['Owner'] = 'Player'
            self.dict_race[key] = {
                "Total Time": 0,
                "Pit-Stop": False,
                "Tires": 100,
                "Car Health": 100,
                "Pit-Stops": 0,
            }

    @Slot()
    def restart_race(self):
        self.import_data()

        self.dict_track["Raced Laps"] = 0
        self.play_button.setEnabled(True)
