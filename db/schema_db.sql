DROP TABLE IF EXISTS pilots;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS sponsors;
DROP TABLE IF EXISTS motors;
DROP TABLE IF EXISTS tracks;

CREATE TABLE pilots (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT UNIQUE NOT NULL,
  Country TEXT,
  Age INTEGER,
  Championships INTEGER,
  Poles INTEGER,
  Victories INTEGER,
  GP INTEGER,
  Agressive INTEGER,
  Determination INTEGER,
  Experience INTEGER,
  Marketing INTEGER,
  Overtaking INTEGER,
  Potential INTEGER,
  Qualification INTEGER ,
  Raining INTEGER,
  Smoothness INTEGER,
  Speed INTEGER,
  Team TEXT,
  Contract INTEGER,
  Salary REAL
);

CREATE TABLE teams (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name_Full TEXT UNIQUE,
  Name TEXT UNIQUE,
  Principal TEXT UNIQUE,
  Color1 TEXT,
  Color2 TEXT,
  Country TEXT,
  Championships INTEGER,
  Last_Position INTEGER,
  Budget INTEGER,
  Sponsor_0 TEXT,
  Sponsor_1 TEXT,
  Sponsor_2 TEXT,
  Sponsor_3 TEXT,
  Sponsor_4 TEXT,
  Enginners INTEGER,
  motorid INTEGER,
  Manufacturer TEXT,
  Aerodynamics INTEGER,
  Electronics INTEGER,
  Suspension INTEGER,
  Reliability INTEGER
);

CREATE TABLE motors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Manufacturer TEXT UNIQUE,
  Power INTEGER,
  Reliability INTEGER
);

CREATE TABLE tracks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT UNIQUE,
  Country TEXT,
  Base_Time INTEGER,
  Difficult INTEGER,
  Total_Laps INTEGER,
  Weather INTEGER
);

CREATE TABLE sponsors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT UNIQUE,
  Value INTEGER,
  Expectations INTEGER
);
