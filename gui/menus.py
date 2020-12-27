# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPalette, QColor, QAction
from PySide6.QtWidgets import (QTableWidgetItem, QWidget, QTableWidget,
                               QMenuBar, QGridLayout, QAbstractItemView,
                               QHeaderView)


class Menus(QMenuBar):
    def __init__(self):
        QMenuBar.__init__(self)
        self.file_menu = self.addMenu("Arquivo")
        self.results_menu = self.addMenu("Resultados")

        # Exit QAction
        self.exit_action = QAction("Sair", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.file_menu.addAction(self.exit_action)

        self.results_pilots_action = QAction("Pilotos", self)
        self.results_teams_action = QAction("Equipes", self)
        self.results_menu.addAction(self.results_pilots_action)
        self.results_menu.addAction(self.results_teams_action)


class PilotResults(QWidget):
    def __init__(self, results: dict, palette=None):
        QWidget.__init__(self)
        self.results = results
        self.items = 0
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Pilot", "Team", "MON", "SPA"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.layout = QGridLayout()
        #self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.table, 0, 0)
        self.setLayout(self.layout)
        self.fill_table()

    def fill_table(self):
        keys = list(self.results.keys())
        if keys != []:
            pilots = self.results[keys[0]].keys()
            for pilot in pilots:
                team = 'NULL'
                team_item = QTableWidgetItem(team)
                team_item.setTextAlignment(Qt.AlignCenter)

                pilot_item = QTableWidgetItem(pilot)
                pilot_item.setTextAlignment(Qt.AlignCenter)

                self.table.insertRow(self.items)
                self.table.setItem(self.items, 0, pilot_item)
                self.table.setItem(self.items, 1, team_item)
                i = 0
                for track in self.results:
                    result_item = QTableWidgetItem(
                        str(self.results[track][pilot]))
                    self.table.setItem(self.items, 2 + i, result_item)
                    i += 1
                self.items += 1