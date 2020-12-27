import sys
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QMainWindow, QApplication, QStackedLayout, QWidget
from PySide6.QtGui import QAction, QPalette, QColor
from gui import InterfacePrincipal, InterfaceCorrida
from gui.menus import Menus, PilotResults

class MainWindow(QMainWindow):
    results_signal = Signal(list)

    def __init__(self):
        self.results = {}
        QMainWindow.__init__(self)
        self.menu = Menus()
        self.setWindowTitle("Paddock Manager")
        self.menu.exit_action.triggered.connect(self.exit_app)
        self.menu.results_pilots_action.triggered.connect(self.show_results)
        self.setMenuBar(self.menu)
        self.widget = InterfacePrincipal()
        self.widget.race_mode.connect(self.race_mode)
        self.results_signal.connect(self.widget.update_info)
        self.setCentralWidget(self.widget)
        self.setMaximumSize(780, 600)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

    @Slot()
    def race_mode(self, raceid):
        self.raceid = raceid
        self.hide()
        self.race = InterfaceCorrida(self.raceid)
        self.race.setWindowTitle('Corrida')
        self.race.normal_mode.connect(self.normal_mode)
        self.race.resize(780, 600)
        self.race.show()

    @Slot()
    def normal_mode(self, results: list):
        self.show()
        self.results_signal.emit(results)
        self.results[self.raceid] = {}
        for result in results:
            self.results[self.raceid][result[0]] = result[1]

    @Slot()
    def show_results(self):
        self.results_pilots = PilotResults(self.results)
        self.results_pilots.setWindowTitle('Resultados')
        self.results_pilots.resize(780, 600)
        self.results_pilots.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(780, 600)
    window.show()
    sys.exit(app.exec_())