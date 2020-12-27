# -*- coding: utf-8 -*-
from PySide6.QtGui import QColor
import sqlite3
from pathlib import Path


class db():
    def __init__(self, name='Data.db'):
        self.path = Path.cwd() / 'sav' / name
        self.db = sqlite3.connect(self.path,
                                  detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.row_factory = sqlite3.Row

    def create_new_db(self, name):
        self.path = Path.cwd() / 'sav' / '{}.db'.format(name)
        self.db = sqlite3.connect(self.path,
                                  detect_types=sqlite3.PARSE_DECLTYPES)
        with open('schema_db.sql') as f:
            self.db.executescript(f.read())
            self.db.execute("VACUUM")
            self.db.commit()
        return self.db

    def track_info(self, raceid: int) -> dict:
        track = self.db.execute('SELECT * FROM tracks WHERE id = ?',
                                (raceid, )).fetchone()
        return track

    # From this all methods will be realocated to class save

    def team_info(self, id: int) -> dict:
        team = self.db.execute('SELECT * FROM teams WHERE id = ?',
                               (id, )).fetchone()
        team = dict(team)
        team['Primary'] = QColor(int(team['Color1'][0:2], 16),
                                 int(team['Color1'][2:4], 16),
                                 int(team['Color1'][4:6], 16),
                                 int(team['Color1'][6:], 16))
        team['Secondary'] = QColor(int(team['Color2'][0:2], 16),
                                   int(team['Color2'][2:4], 16),
                                   int(team['Color2'][4:6], 16),
                                   int(team['Color2'][6:], 16))

        team['Motor'] = self.db.execute(
            'SELECT Power FROM motors WHERE id = ?',
            (team['motorid'], ),
        ).fetchone()[0]

        team['Sponsor 1'] = self.get_sponsor(team, 0)
        team['Sponsor 2'] = self.get_sponsor(team, 1)
        team['Sponsor 3'] = self.get_sponsor(team, 2)
        team['Sponsor 4'] = self.get_sponsor(team, 3)
        team['Sponsor 5'] = self.get_sponsor(team, 4)

        return team

    def get_sponsor(self, team: dict, id: int) -> dict:
        sponsor = {
            'Name':
            team['Sponsor_{}'.format(id)],
            'Value':
            self.db.execute(
                'SELECT Value FROM sponsors WHERE Name = ?',
                (team['Sponsor_{}'.format(id)], ),
            ).fetchone()[0],
        }
        return sponsor

    def teams_colors(self) -> dict:
        teams_colors = {}
        teams = self.db.execute('SELECT Name, Color1,'
                                ' Color2 FROM teams').fetchall()
        for team in teams:
            name = team['Name']
            teams_colors[name] = {}
            teams_colors[name]['Primary'] = QColor(
                int(team['Color1'][0:2], 16), int(team['Color1'][2:4], 16),
                int(team['Color1'][4:6], 16), int(team['Color1'][6:], 16))
            teams_colors[name]['Secondary'] = QColor(
                int(team['Color2'][0:2], 16), int(team['Color2'][2:4], 16),
                int(team['Color2'][4:6], 16), int(team['Color2'][6:], 16))

        return teams_colors

    def teams_overall(self) -> list:
        teams_overall = {}
        teams = self.db.execute('SELECT Name, Aerodynamics, Electronics,'
                                ' Suspension, motorid FROM teams').fetchall()
        motors = self.db.execute('SELECT id, Power FROM motors').fetchall()

        for team in teams:
            team = dict(team)
            for motor in motors:
                if team['motorid'] == motor['id']:
                    team['Motor'] = motor['Power']
                    overall = sum(list(team.values())[1:]) / 4
                    teams_overall[team['Name']] = overall
                    break

        return teams_overall

    def pilot_info(self, team: str, id) -> dict:
        pilot = self.db.execute('SELECT * FROM pilots WHERE Team = ?',
                                (team, )).fetchmany(id + 1)[-1]
        pilot = dict(pilot)
        pilot['Info'] = (0, 0, 0, 0)
        return pilot

    def pilots_stats(self) -> dict:
        teams_overall = self.teams_overall()
        pilots_keys = self.db.execute('SELECT Name FROM pilots').fetchall()
        pilots_keys = [i[0] for i in pilots_keys]
        pilots = {}
        for key in pilots_keys:
            pilots[key] = dict(
                self.db.execute(
                    'SELECT Speed, Smoothness, Determination,'
                    ' Agressive, Overtaking, Team FROM pilots'
                    ' WHERE Name = ?',
                    (key, ),
                ).fetchone())
            for team in teams_overall:
                if pilots[key]['Team'] == team:
                    pilots[key]['Car'] = teams_overall[team]
                    break

        return pilots

    def pilots(self) -> list:
        pilots = self.db.execute('SELECT Name, Team FROM pilots').fetchall()
        return pilots


class save():
    def __init__(self, name):
        self.path = Path.cwd() / 'sav' / '{}.sav'.format(name)
        self.db = sqlite3.connect(self.path,
                                  detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.row_factory = sqlite3.Row

    def create_new_save(self, name):
        path = Path.cwd() / 'sav' / '{}.sav'.format(name)
        db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
        db.row_factory = sqlite3.Row
        return db


def init_db():
    print("Starting Databases...")
    path = Path.cwd() / 'sav'
    db = sqlite3.connect((path / 'Data.db'),
                         detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    with Path.open((path / 'schema_db.sql')) as f:
        db.executescript(f.read())
        db.execute("VACUUM")
        db.commit()
        db.close()
    print("DB initialized")


if __name__ == '__main__':
    init_db()
