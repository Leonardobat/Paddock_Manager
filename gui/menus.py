# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPalette, QColor, QAction
from PySide6.QtWidgets import (QTableWidgetItem, QWidget, QTableWidget,
                               QMenuBar, QGridLayout, QAbstractItemView,
                               QHeaderView)
from db import db


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
    database = db()

    def __init__(self, results: dict, palette=None):
        QWidget.__init__(self)
        self.pilots = self.database.pilots()
        tracks = self.database.tracks()
        self.teams_colors = self.database.teams_colors()
        self.results = results
        self.items = 0
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setColumnCount(3 + len(tracks))
        header = ['Pilot', 'Equipe', 'Pts.']
        for track in tracks:
            header.append(track)
        self.table.setHorizontalHeaderLabels(header)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)

        self.layout = QGridLayout()
        self.layout.addWidget(self.table, 0, 0)
        self.setLayout(self.layout)
        self.fill_table()
        self.table.setSortingEnabled(True)
        self.table.sortItems(2, Qt.DescendingOrder)

    def fill_table(self):
        max_points = self.max_points()

        for pilot in self.pilots:
            team = pilot['Team']
            team_item = QTableWidgetItem(team)
            team_item.setTextAlignment(Qt.AlignCenter)

            pilot_item = QTableWidgetItem(pilot['Name'])
            pilot_item.setTextAlignment(Qt.AlignCenter)

            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, pilot_item)
            self.table.setItem(self.items, 1, team_item)
            points = 0
            if self.results != []:
                i = 0
                for result in self.results:
                    for _pilot in result:
                        if _pilot[0] == pilot['Name']:
                            _result_item = QTableWidgetItem(f'{_pilot[2]:02d}')
                            _result_item.setTextAlignment(Qt.AlignCenter)
                            points += _pilot[2]
                            self.table.setItem(self.items, 3 + i, _result_item)
                    i += 1
            if max_points > 99:
                points_item = QTableWidgetItem((f'{points:03d}'))
            else:
                points_item = QTableWidgetItem((f'{points:02d}'))
            points_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(self.items, 2, points_item)
            self.items += 1

        return

    def max_points(self):
        _max_points = 0
        if self.results != []:
            for result in self.results:
                points = 0
                for pilot in result:
                    points += pilot[2]
                    if points > _max_points:
                        _max_points = points
                        points = 0
        return _max_points


class TeamResults(QWidget):
    database = db()

    def __init__(self, results: dict, palette=None):
        QWidget.__init__(self)
        self.teams_colors = self.database.teams_colors()
        tracks = self.database.tracks()
        self.results = results
        self.items = 0
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setColumnCount(2 + len(tracks))
        header = ['Equipe', 'Pts.']
        for track in tracks:
            header.append(track)
        self.table.setHorizontalHeaderLabels(header)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)

        self.layout = QGridLayout()
        self.layout.addWidget(self.table, 0, 0)
        self.setLayout(self.layout)
        self.fill_table()
        self.table.setSortingEnabled(True)
        self.table.sortItems(1, Qt.DescendingOrder)

    def fill_table(self):
        max_points = self.max_points()
        for team in self.teams_colors:
            team_item = QTableWidgetItem(team)
            team_item.setTextAlignment(Qt.AlignCenter)

            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, team_item)
            total_points = 0
            if self.results != []:
                i, total_points = 0, 0
                for result in self.results:
                    _points = 0
                    for _pilot in result:
                        if _pilot[3] == team:
                            _points += _pilot[2]
                    total_points += _points
                    _result_item = QTableWidgetItem(f'{_points:02d}')
                    _result_item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(self.items, 2 + i, _result_item)
                    i += 1
            if max_points > 99:
                points_item = QTableWidgetItem((f'{total_points:03d}'))
            else:
                points_item = QTableWidgetItem((f'{total_points:02d}'))
            points_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(self.items, 1, points_item)
            self.items += 1

        return

    def max_points(self):
        _max_points = 0
        if self.results != []:
            for team in self.teams_colors:
                points = 0
                for result in self.results:
                    for pilot in result:
                        if pilot[3] == team:
                            points += pilot[2]
                if points > _max_points:
                    _max_points = points
        return _max_points