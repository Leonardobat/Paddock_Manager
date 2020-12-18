DROP TABLE IF EXISTS list_pilots;
DROP TABLE IF EXISTS list_teams;
DROP TABLE IF EXISTS list_sponsors;
DROP TABLE IF EXISTS list_motors;

CREATE TABLE list_pilots (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT UNIQUE NOT NULL,
  Country TEXT NOT NULL,
  Age INTEGER NOT NULL,
  Championships INTEGER,
  Poles INTEGER,
  Victories INTEGER,
  GP INTEGER,
  Concentration REAL NOT NULL,
  Determination REAL NOT NULL,
  Experience REAL NOT NULL,
  Qualification REAL NOT NULL,
  Marketing REAL NOT NULL,
  Raining REAL NOT NULL,
  Rhythm REAL NOT NULL,
  Smoothness REAL NOT NULL,
  Technique REAL NOT NULL,
  Potential REAL,
  Team TEXT NOT NULL,
  Salary REAL NOT NULL,
  Contract REAL NOT NULL
);

CREATE TABLE list_teams (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT UNIQUE NOT NULL,
  Country TEXT NOT NULL,
  Championships INTEGER,
  Last_Position INTEGER,
  Budget REAL NOT NULL,
  Sponsor_0 TEXT,
  Sponsor_1 TEXT,
  Sponsor_2 TEXT,
  Sponsor_3 TEXT,
  Sponsor_4 TEXT,
  Enginners REAL NOT NULL,
  Motor TEXT,
  Manufacturer INTEGER,
  Aerodynamics REAL NOT NULL,
  Suspension REAL NOT NULL,
  Suspension REAL NOT NULL,
  Reliability REAL NOT NULL
);

CREATE TABLE list_motors (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  Manufacturer TEXT UNIQUE NOT NULL,
  Power REAL NOT NULL,
  Reliability REAL NOT NULL
);

CREATE TABLE list_sponsors (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT UNIQUE NOT NULL,
  Country TEXT NOT NULL,
  Value REAL NOT NULL,
  Expectations INTEGER NOT NULL
);
