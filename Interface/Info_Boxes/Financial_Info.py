# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPalette, QFont, QColor
from PySide6.QtWidgets import (QLabel, QPushButton, QWidget, QFrame,
                               QGridLayout)


class Financial_Info(QWidget):
    def __init__(self, data, palette):
        QWidget.__init__(self)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Active, QPalette.Window,
                              QColor(255, 255, 255, 255))
        self.palette.setColor(QPalette.Active, QPalette.WindowText,
                              QColor(0, 0, 0, 255))

        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Panel)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.title = QLabel('Finanças')
        self.title.setPalette(palette)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setAutoFillBackground(True)

        self.cash = QLabel('£ {} Mi'.format(data['Team']['Budget']))
        self.master = QLabel(data['Team']['Sponsor 1']['Name'])
        self.master_value = QLabel('£ {} Mi'.format(
            data['Team']['Sponsor 1']['Value']))
        self.sponsor1 = QLabel(data['Team']['Sponsor 2']['Name'])
        self.sponsor1_value = QLabel('£ {} Mi'.format(
            data['Team']['Sponsor 2']['Value']))
        self.sponsor2 = QLabel(data['Team']['Sponsor 3']['Name'])
        self.sponsor2_value = QLabel('£ {} Mi'.format(
            data['Team']['Sponsor 3']['Value']))
        self.sponsor3 = QLabel(data['Team']['Sponsor 4']['Name'])
        self.sponsor3_value = QLabel('£ {} Mi'.format(
            data['Team']['Sponsor 4']['Value']))
        self.sponsor4 = QLabel(data['Team']['Sponsor 5']['Name'])
        self.sponsor4_value = QLabel('£ {} Mi'.format(
            data['Team']['Sponsor 5']['Value']))

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.title, 0, 0, 1, 4)
        self.layout.addWidget(self.frame, 0, 0, 7, 4)
        self.layout.addWidget(QLabel('Caixa'), 1, 1)
        self.layout.addWidget(self.cash, 1, 2)
        self.layout.addWidget(self.master, 2, 1)
        self.layout.addWidget(self.master_value, 2, 2)
        self.layout.addWidget(self.sponsor1, 3, 1)
        self.layout.addWidget(self.sponsor1_value, 3, 2)
        self.layout.addWidget(self.sponsor2, 4, 1)
        self.layout.addWidget(self.sponsor2_value, 4, 2)
        self.layout.addWidget(self.sponsor3, 5, 1)
        self.layout.addWidget(self.sponsor3_value, 5, 2)
        self.layout.addWidget(self.sponsor4, 6, 1)
        self.layout.addWidget(self.sponsor4_value, 6, 2)
        self.setLayout(self.layout)
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)

    @Slot()
    def update_info(self, data: dict):
        self.cash.setText(data['Budget'])
        self.master.setText(data['Sponsor 1']['Name'])
        self.master_value.setText('£ {} Mi'.format(data['Sponsor 1']['Value']))
        self.sponsor1.setText(data['Sponsor 2']['Name'])
        self.sponsor1_value.setText('£ {} Mi'.format(
            data['Sponsor 2']['Value']))
        self.sponsor2.setText(data['Sponsor 3']['Name'])
        self.sponsor2_value.setText('£ {} Mi'.format(
            data['Sponsor 3']['Value']))
        self.sponsor3.setText(data['Sponsor 4']['Name'])
        self.sponsor3_value.setText('£ {} Mi'.format(
            data['Sponsor 4']['Value']))
        self.sponsor4.setText(data['Sponsor 5']['Name'])
        self.sponsor4_value.setText('£ {} Mi'.format(
            data['Sponsor 5']['Value']))
