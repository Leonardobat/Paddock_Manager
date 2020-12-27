from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPalette, QFont, QColor
from PySide6.QtWidgets import (QTableWidgetItem, QWidget, QTableWidget,
                               QGridLayout, QAbstractItemView, QHeaderView)


class Results_Pilot(QWidget):
    def __init__(self, results: dict, palette=None):
        QWidget.__init__(self)
        self.results = results
        self.items = 0
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Pilot", "Team", "Lap Time", "Gap"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.layout = QGridLayout()
        #self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.table, 0, 0)
        self.setLayout(self.layout)
        self.fill_table()

    def fill_table(self):
        for key in self.dict_pilot:
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