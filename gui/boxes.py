# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPalette, QFont, QColor
from PySide6.QtWidgets import (QTableWidgetItem, QWidget, QTableWidget,
                               QGridLayout, QAbstractItemView, QHeaderView,
                               QLabel, QPushButton, QFrame, QProgressBar,
                               QVBoxLayout)


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
        overall = (data['Aerodynamics'] + data['Suspension'] + data['Motor'] +
                   data['Electronics']) / 4
        self.overall = QLabel(f"{overall:.0f}")

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.title, 0, 0, 1, 4)
        self.layout.addWidget(self.frame, 0, 0, 7, 4)
        self.layout.addWidget(QLabel('Aerodinâmica'), 1, 1, Qt.AlignRight)
        self.layout.addWidget(self.aero, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel('Confiabilidade'), 2, 1, Qt.AlignRight)
        self.layout.addWidget(self.relia, 2, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel(f'Motor({data["Manufacturer"]})'), 3, 1,
                              Qt.AlignRight)
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
        self.overall.setText(f"{overall:.0f}")


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

        self.budget = QLabel(f"£ {data['Budget']} Mi")
        self.master = QLabel(data['Sponsor 1']['Name'])
        self.master_value = QLabel(f"£ {data['Sponsor 1']['Value']} Mi")
        self.sponsor1 = QLabel(data['Sponsor 2']['Name'])
        self.sponsor1_value = QLabel(f"£ {data['Sponsor 2']['Value']} Mi")
        self.sponsor2 = QLabel(data['Sponsor 3']['Name'])
        self.sponsor2_value = QLabel(f"£ {data['Sponsor 3']['Value']} Mi")
        self.sponsor3 = QLabel(data['Sponsor 4']['Name'])
        self.sponsor3_value = QLabel(f"£ {data['Sponsor 4']['Value']} Mi")
        self.sponsor4 = QLabel(data['Sponsor 5']['Name'])
        self.sponsor4_value = QLabel(f"£ {data['Sponsor 5']['Value']} Mi")

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.title, 0, 0, 1, 4)
        self.layout.addWidget(self.frame, 0, 0, 7, 4)
        self.layout.addWidget(QLabel('Caixa'), 1, 1, Qt.AlignLeft)
        self.layout.addWidget(self.budget, 1, 2, Qt.AlignCenter)
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
        self.budget.setText(f"£ {data['Budget']:.2f} Mi")
        self.master.setText(data['Sponsor 1']['Name'])
        self.master_value.setText(f"£ {data['Sponsor 1']['Value']} Mi")
        self.sponsor1.setText(data['Sponsor 2']['Name'])
        self.sponsor1_value.setText(f"£ {data['Sponsor 2']['Value']} Mi")
        self.sponsor2.setText(data['Sponsor 3']['Name'])
        self.sponsor2_value.setText(f"£ {data['Sponsor 3']['Value']} Mi")
        self.sponsor3.setText(data['Sponsor 4']['Name'])
        self.sponsor3_value.setText(f"£ {data['Sponsor 4']['Value']} Mi")
        self.sponsor4.setText(data['Sponsor 5']['Name'])
        self.sponsor4_value.setText(f"£ {data['Sponsor 5']['Value']} Mi")


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


class PilotBox(QWidget):
    def __init__(self, pilot_name: str, pilot_data: dict, palette=None):
        QWidget.__init__(self)

        self.dict_race = pilot_data
        self.pilot_name = QLabel(pilot_name)
        self.pilot_name.setAlignment(Qt.AlignCenter)
        self.pilot_tire_bar = QProgressBar()
        self.pilot_tire_bar.setRange(0, 100)
        self.pilot_tire_bar.setValue(pilot_data["Tires"])
        self.pilot_pitstops = QLabel("Pitstops: {}".format(
            pilot_data["Pit-Stops"]))
        self.pilot_pitstops.setAlignment(Qt.AlignCenter)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.layout.addWidget(self.frame, 0, 0, 5, 3)
        self.layout.addWidget(self.pilot_name, 1, 1)
        self.layout.addWidget(QLabel("Tires:"), 2, 1, Qt.AlignCenter)
        self.layout.addWidget(self.pilot_tire_bar, 3, 1, Qt.AlignCenter)
        self.layout.addWidget(self.pilot_pitstops, 4, 1)
        self.setLayout(self.layout)

    def update_info(self):
        self.pilot_tire_bar.setValue(self.dict_race["Tires"])
        self.pilot_pitstops.setText("Pitstops: {}".format(
            self.dict_race["Pit-Stops"]))


class TimingBox(QWidget):
    def __init__(self, pilot_data: dict, team_data: dict, palette=None):
        QWidget.__init__(self)
        self.items = 0
        self.dict_pilot = pilot_data
        self.dict_teams = team_data

        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Pilot", "Team", "Lap Time", "Gap"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.table, 0, 0)
        self.setLayout(self.layout)
        self.fill_table()

    @Slot()
    def update_table(self, times_sorted: dict):
        num_pilots = len(times_sorted)

        self.table.setRowCount(0)
        self.items = 0
        for k in range(num_pilots):
            pilot_name, lap, gap = times_sorted[k]

            if k == 0:
                gap_item = QTableWidgetItem("Leader")
            else:
                gap_item = QTableWidgetItem(gap)
            gap_item.setTextAlignment(Qt.AlignCenter)
            team = self.dict_pilot[pilot_name]["Team"]
            team_item = QTableWidgetItem(team)
            team_item.setTextAlignment(Qt.AlignCenter)
            team_item.setBackground(self.dict_teams[team]["Primary"])
            team_item.setForeground(self.dict_teams[team]["Secondary"])

            lap_item = QTableWidgetItem(lap)
            lap_item.setTextAlignment(Qt.AlignCenter)
            pilot_item = QTableWidgetItem(pilot_name)
            pilot_item.setTextAlignment(Qt.AlignCenter)

            if self.items == 0:
                pilot_item.setBackground(QColor(255, 215, 0, 127))
            elif self.items == 1:
                pilot_item.setBackground(QColor(169, 169, 169, 127))
            elif self.items == 2:
                pilot_item.setBackground(QColor(205, 127, 50, 127))
            self.table.insertRow(self.items)
            id_item = QTableWidgetItem(f"{(self.items + 1)}º")
            self.table.setVerticalHeaderItem(self.items, id_item)
            self.table.setItem(self.items, 0, pilot_item)
            self.table.setItem(self.items, 1, team_item)
            self.table.setItem(self.items, 2, lap_item)
            self.table.setItem(self.items, 3, gap_item)
            self.items += 1

    def fill_table(self):
        for key in self.dict_pilot:
            lap_item = QTableWidgetItem("0:0.000")
            lap_item.setTextAlignment(Qt.AlignCenter)

            gap_item = QTableWidgetItem("+0:0.000")
            gap_item.setTextAlignment(Qt.AlignCenter)

            team = self.dict_pilot[key]["Team"]
            team_item = QTableWidgetItem(team)
            team_item.setTextAlignment(Qt.AlignCenter)
            team_item.setBackground(self.dict_teams[team]["Primary"])
            team_item.setForeground(self.dict_teams[team]["Secondary"])

            pilot_item = QTableWidgetItem(key)
            pilot_item.setTextAlignment(Qt.AlignCenter)
            self.table.insertRow(self.items)
            id_item = QTableWidgetItem(f"{(self.items + 1)}º")
            self.table.setVerticalHeaderItem(self.items, id_item)
            self.table.setItem(self.items, 0, pilot_item)
            self.table.setItem(self.items, 1, team_item)
            self.table.setItem(self.items, 2, lap_item)
            self.table.setItem(self.items, 3, gap_item)
            self.items += 1
