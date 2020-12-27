import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenuBar, QWidget
from PySide6.QtGui import QAction

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