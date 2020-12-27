# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPalette, QFont, QColor
from PySide6.QtWidgets import (QLabel, QPushButton, QWidget, QFrame,
                               QGridLayout)


class CarInfo(QWidget):
    def __init__(self, data: dict, palette):
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
        self.title = QLabel('Carro')
        self.title.setPalette(palette)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setAutoFillBackground(True)
        self.aero = QLabel(str(data['Aerodynamics']))
        self.relia = QLabel(str(data['Reliability']))
        self.motor = QLabel(str(data['Motor']))
        self.eletronics = QLabel(str(data['Electronics']))
        self.suspension = QLabel(str(data['Suspension']))
        self.overall = (data['Aerodynamics'] + data['Suspension'] +
                        data['Motor'] + data['Electronics']) / 4
        self.overall = QLabel(str(int(self.overall)))

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.title, 0, 0, 1, 4)
        self.layout.addWidget(self.frame, 0, 0, 7, 4)
        self.layout.addWidget(QLabel('Aerodinâmica'), 1, 1, Qt.AlignRight)
        self.layout.addWidget(self.aero, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel('Confiabilidade'), 2, 1, Qt.AlignRight)
        self.layout.addWidget(self.relia, 2, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel('Motor'), 3, 1, Qt.AlignRight)
        self.layout.addWidget(self.motor, 3, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel('Eletrônica'), 4, 1, Qt.AlignRight)
        self.layout.addWidget(self.eletronics, 4, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel('Suspensão'), 5, 1, Qt.AlignRight)
        self.layout.addWidget(self.suspension, 5, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel('Geral'), 6, 1, Qt.AlignRight)
        self.layout.addWidget(self.overall, 6, 2, Qt.AlignCenter)
        self.setLayout(self.layout)

        self.setMaximumWidth(250)

    @Slot()
    def update_info(self, data: dict):
        data = data['Team']
        self.aero.setText(str(data['Aerodynamics']))
        self.relia.setText(str(data['Reliability']))
        self.motor.setText(str(data['Motor']))
        self.eletronics.setText(str(data['Electronics']))
        self.suspension.setText(str(data['Suspension']))
        overall = (data['Aerodynamics'] + data['Suspension'] + data['Motor'] +
                   data['Electronics']) / 4
        self.overall.setText(str(int(overall)))


class FinancialInfo(QWidget):
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

        self.cash = QLabel('£ {} Mi'.format(data['Budget']))
        self.master = QLabel(data['Sponsor 1']['Name'])
        self.master_value = QLabel('£ {} Mi'.format(
            data['Sponsor 1']['Value']))
        self.sponsor1 = QLabel(data['Sponsor 2']['Name'])
        self.sponsor1_value = QLabel('£ {} Mi'.format(
            data['Sponsor 2']['Value']))
        self.sponsor2 = QLabel(data['Sponsor 3']['Name'])
        self.sponsor2_value = QLabel('£ {} Mi'.format(
            data['Sponsor 3']['Value']))
        self.sponsor3 = QLabel(data['Sponsor 4']['Name'])
        self.sponsor3_value = QLabel('£ {} Mi'.format(
            data['Sponsor 4']['Value']))
        self.sponsor4 = QLabel(data['Sponsor 5']['Name'])
        self.sponsor4_value = QLabel('£ {} Mi'.format(
            data['Sponsor 5']['Value']))

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.title, 0, 0, 1, 4)
        self.layout.addWidget(self.frame, 0, 0, 7, 4)
        self.layout.addWidget(QLabel('Caixa'), 1, 1, Qt.AlignLeft)
        self.layout.addWidget(self.cash, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.master, 2, 1, Qt.AlignLeft)
        self.layout.addWidget(self.master_value, 2, 2, Qt.AlignCenter)
        self.layout.addWidget(self.sponsor1, 3, 1, Qt.AlignLeft)
        self.layout.addWidget(self.sponsor1_value, 3, 2, Qt.AlignCenter)
        self.layout.addWidget(self.sponsor2, 4, 1, Qt.AlignLeft)
        self.layout.addWidget(self.sponsor2_value, 4, 2, Qt.AlignCenter)
        self.layout.addWidget(self.sponsor3, 5, 1, Qt.AlignLeft)
        self.layout.addWidget(self.sponsor3_value, 5, 2, Qt.AlignCenter)
        self.layout.addWidget(self.sponsor4, 6, 1, Qt.AlignLeft)
        self.layout.addWidget(self.sponsor4_value, 6, 2, Qt.AlignCenter)
        self.setLayout(self.layout)
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)
        self.setMaximumWidth(250)

    @Slot()
    def update_info(self, data: dict):
        data = data['Team']
        self.cash.setText('£ {} Mi'.format(data['Budget']))
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


class NewsInfo(QWidget):
    def __init__(self, msg, palette):
        QWidget.__init__(self)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Active, QPalette.Window,
                              QColor(255, 255, 255, 255))
        self.palette.setColor(QPalette.Active, QPalette.WindowText,
                              QColor(0, 0, 0, 255))
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)
        self.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel('Notícias')
        self.title.setPalette(palette)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setAutoFillBackground(True)
        if msg is not None:
            self.news = QLabel(msg)
        else:
            self.news = QLabel("Não há nenhuma notícia nova.")
        self.news.setAlignment(Qt.AlignCenter)
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Panel)
        self.frame.setFrameShadow(QFrame.Sunken)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.title, 0, 0)
        self.layout.addWidget(self.frame, 0, 0, 2, 1)
        self.layout.addWidget(self.news, 1, 0)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 3)
        self.setLayout(self.layout)
        self.setMaximumHeight(250)

    @Slot()
    def update_news(self, data: dict):
        self.news.setText(data['msg'])


class RaceInfo(QWidget):
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


class TeamInfo(QWidget):
    def __init__(self, data, palette):
        QWidget.__init__(self)
        self.font = QFont()
        self.font.setItalic(True)
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
        self.team_name = QLabel(data['Team']['Name'])
        self.team_name.setPalette(palette)
        self.team_name.setAlignment(Qt.AlignCenter)
        self.team_name.setAutoFillBackground(True)
        self.user_name = QLabel(data['Team']['Principal'])
        self.user_name.setFont(self.font)
        self.pilot1 = QLabel(data['Pilot 1']['Name'])
        self.pilot2 = QLabel(data['Pilot 2']['Name'])
        self.pilot3 = QLabel(data['Pilot 3']['Name'])
        self.pilot1_info = QLabel(
            'DNF {} / Vit. {} / Pol. {} / Pts. {}'.format(
                *data['Pilot 1']['Info']))
        self.pilot1_info.setAlignment(Qt.AlignCenter)
        self.pilot2_info = QLabel(
            'DNF {} / Vit. {} / Pol. {} / Pts. {}'.format(
                *data['Pilot 2']['Info']))
        self.pilot2_info.setAlignment(Qt.AlignCenter)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.team_name, 0, 0, 1, 4)
        self.layout.addWidget(self.frame, 0, 0, 7, 4)
        self.layout.addWidget(QLabel('Chefe da Equipe'), 1, 1, Qt.AlignLeft)
        self.layout.addWidget(self.user_name, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel('Piloto 1'), 2, 1, Qt.AlignLeft)
        self.layout.addWidget(self.pilot1, 2, 2, Qt.AlignCenter)
        self.layout.addWidget(self.pilot1_info, 3, 1, 1, 2)
        self.layout.addWidget(QLabel('Piloto 2'), 4, 1, Qt.AlignLeft)
        self.layout.addWidget(self.pilot2, 4, 2, Qt.AlignCenter)
        self.layout.addWidget(self.pilot2_info, 5, 1, 1, 2)
        self.layout.addWidget(QLabel('Reserva'), 6, 1, Qt.AlignLeft)
        self.layout.addWidget(self.pilot3, 6, 2, Qt.AlignCenter)
        self.setLayout(self.layout)
        self.setMaximumWidth(250)

    @Slot()
    def update_info(self, data: dict):
        self.team_name.setText(data['Team']['Name'])
        self.user_name.setText(data['Team']['Principal'])
        self.pilot1.setText(data['Pilot 1']['Name'])
        self.pilot2.setText(data['Pilot 2']['Name'])
        self.pilot3.setText(data['Pilot 3']['Name'])
        self.pilot1_info.setText('DNF {} / Vit. {} / Pol. {} / Pts. {}'.format(
            *data['Pilot 1']['Info']))
        self.pilot2_info.setText('DNF {} / Vit. {} / Pol. {} / Pts. {}'.format(
            *data['Pilot 2']['Info']))
