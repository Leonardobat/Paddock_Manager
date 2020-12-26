import sys
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QMainWindow, QApplication, QMenuBar, QStackedLayout, QWidget
from PySide6.QtGui import QAction, QPalette, QColor
from Interface.Corrida import Interface_Corrida
from Interface.Principal import Interface_Principal


class MainWindow(QMainWindow):
    def __init__(self, widgets: tuple):
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

        widgets[0].race_mode.connect(self.race_mode)
        widgets[1].normal_mode.connect(self.normal_mode)
        self.widget = QWidget()
        self.layout = QStackedLayout()
        self.layout.addWidget(widgets[0])
        self.layout.addWidget(widgets[1])
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setMaximumSize(780, 600)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

    @Slot()
    def race_mode(self):
        self.layout.setCurrentIndex(1)

    def normal_mode(self):
        self.layout.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widgets = (Interface_Principal(), Interface_Corrida())
    window = MainWindow(widgets)
    window.resize(780, 600)
    window.show()
    sys.exit(app.exec_())