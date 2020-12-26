from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPalette, QFont, QColor
from PySide6.QtWidgets import (QLabel, QPushButton, QWidget, QFrame,
                               QGridLayout, QProgressBar, QVBoxLayout)


class PilotBox(QWidget):
    def __init__(self, pilot_name: str, pilot_data: dict, palette=None):
        QWidget.__init__(self)

        self.dict_race = pilot_data
        self.pilot_name = QLabel(pilot_name)
        self.pilot_name.setAlignment(Qt.AlignCenter)
        self.pilot_tire_bar = QProgressBar()
        self.pilot_tire_bar.setRange(0, 100)
        self.pilot_tire_bar.setValue(pilot_data["Tires"])
        self.pilot_pitstops = QLabel("Pitstops: {}".format(
            pilot_data["Pit-Stops"]))
        self.pilot_pitstops.setAlignment(Qt.AlignCenter)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.layout.addWidget(self.frame, 0, 0, 5, 3)
        self.layout.addWidget(self.pilot_name, 1, 1)
        self.layout.addWidget(QLabel("Tires:"), 2, 1, Qt.AlignCenter)
        self.layout.addWidget(self.pilot_tire_bar, 3, 1, Qt.AlignCenter)
        self.layout.addWidget(self.pilot_pitstops, 4, 1)
        self.setLayout(self.layout)

    def update_info(self):
        self.pilot_tire_bar.setValue(self.dict_race["Tires"])
        self.pilot_pitstops.setText("Pitstops: {}".format(
            self.dict_race["Pit-Stops"]))
