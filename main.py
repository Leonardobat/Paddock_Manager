import sys
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QMainWindow, QApplication, QMenuBar, QStackedLayout, QWidget
from PySide6.QtGui import QAction, QPalette, QColor
from Interface.Corrida import Interface_Corrida
from Interface.Principal import Interface_Principal


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Paddock Manager")

        # Menu
        self.menu = QMenuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)
        self.setMenuBar(self.menu)
        self.widget = Interface_Principal()
        self.widget.race_mode.connect(self.race_mode)
        self.setCentralWidget(self.widget)
        self.setMaximumSize(780, 600)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

    @Slot()
    def race_mode(self, title=None):
        self.hide()
        self.race = Interface_Corrida()
        self.race.setWindowTitle('Corrida - SPA')
        self.race.normal_mode.connect(self.normal_mode)
        self.race.resize(780, 600)
        self.race.show()

    @Slot()
    def normal_mode(self, results: list):
        self.show()
        print(results)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(780, 600)
    window.show()
    sys.exit(app.exec_())