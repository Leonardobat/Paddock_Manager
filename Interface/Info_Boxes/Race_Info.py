from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPalette, QFont, QColor
from PySide6.QtWidgets import (QLabel, QPushButton, QWidget, QFrame,
                               QGridLayout)


class Race_Info(QWidget):
    def __init__(self, data, palette):
        QWidget.__init__(self)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Active, QPalette.Window,
                              QColor(255, 255, 255, 255))
        self.palette.setColor(QPalette.Active, QPalette.WindowText,
                              QColor(0, 0, 0, 255))
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)

        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Panel)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.title = QLabel('Próximo GP')
        self.title.setPalette(palette)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setAutoFillBackground(True)
        text = '{Name2}\n{Name1}\n{Total_Laps} Voltas\n'.format(
            **data['Next_Track'])
        self.next_race = QLabel(text)
        self.next_race.setAlignment(Qt.AlignCenter)
        self.race_button = QPushButton('Corrida')

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 2)
        self.layout.setRowStretch(2, 1)
        self.layout.addWidget(self.title, 0, 0)
        self.layout.addWidget(self.frame, 0, 0, 3, 1)
        self.layout.addWidget(self.next_race, 1, 0)
        self.layout.addWidget(self.race_button, 2, 0)
        self.setLayout(self.layout)

    @Slot()
    def update_info(self, data: dict):
        text = '{Name2}\n{Name1}\n{Total_Laps} Voltas\n'.format(
            **data['Next_Track'])
        self.next_race.setText(text)