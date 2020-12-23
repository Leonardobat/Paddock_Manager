import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QMainWindow, QApplication, QMenuBar
from PySide6.QtGui import QAction
from Interface.Interface_corrida import Interface_Corrida


class MainWindow(QMainWindow):
    def __init__(self, widget):
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
        self.setCentralWidget(widget)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Interface_Corrida()
    window = MainWindow(widget)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())