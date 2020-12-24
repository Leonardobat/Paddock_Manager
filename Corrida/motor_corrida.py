# -*- coding: utf-8 -*-
from random import SystemRandom
from math import sqrt, log


class Racing_Engine():
    def __init__(self, dict_pilot, dict_track):
        self.times_sorted, self.info = [], []
        self.data, self.stats, self.track = [], dict_pilot, dict_track
        self.gen = SystemRandom()
        self.weather = self.track["Weather"]
        self.base_time = self.track["Base Time"] * 60

    def run_a_lap(self, dict_race):
        self.data = dict_race
        self.racing()
        return ([i[1:] for i in self.info], self.data)

    def racing(self):

        for pilot_key in self.data.keys():
            old_time = self.data[pilot_key]["Total Time"]
            if self.stats[pilot_key]["Owner"] == "IA":
                if self.data[pilot_key]["Tires"] < 30:
                    self.data[pilot_key]["Pit-Stop"] = True
            lap = self.lap_time(pilot_key)
            total_time = lap + old_time
            if self.data[pilot_key]["Pit-Stop"]:
                self.pit_stop(pilot_key, total_time, lap)
            else:
                self.times_sorted.append([total_time, pilot_key, lap])
                self.info.append([0, pilot_key, 0, 0])

        self.times_sorted.sort()
        num_pilots = len(self.times_sorted)

        for i in range(num_pilots):
            total_time, pilot_key, lap = self.times_sorted[i]
            if i > 0:
                prey_time, prey_key, prey_lap = self.times_sorted[i - 1]
                gap = total_time - prey_time
                if gap < 1:
                    overtake_diff = (self.track["Difficult"] - (
                        (self.stats[pilot_key]["Overtaking"] +
                         self.stats[pilot_key]["Agressive"]) -
                        (self.stats[prey_key]["Overtaking"] +
                         self.stats[prey_key]["Agressive"])) / 100)
                    lucky = self.gen.random()

                    if lucky > overtake_diff:
                        # Time from was overtook
                        prey_lap = prey_lap + 0.3
                        prey_time = total_time + 0.3
                        prey_gap = prey_time - self.times_sorted[0][0]
                        prey_gap_formated = "+{0}".format(
                            self.time_format(prey_gap))
                        prey_lap_formated = self.time_format(prey_lap)
                        self.info[i - 1] = [
                            prey_time,
                            prey_key,
                            prey_lap_formated,
                            prey_gap_formated,
                        ]

                        # Time from who overtook
                        leader_gap = total_time - self.times_sorted[0][0]
                        lap_formated = self.time_format(lap)
                        gap_formated = "+{0}".format(
                            self.time_format(leader_gap))
                        self.info[i] = [
                            total_time,
                            pilot_key,
                            lap_formated,
                            gap_formated,
                        ]
                        # msg = str(pilot_key) + ' has passed ' + str(prey_key)
                        # print(msg)

                    else:
                        if gap < 0:
                            total_time = total_time - gap + 0.3
                        lap = prey_lap + 0.3
                        leader_gap = total_time - self.times_sorted[0][0] + 0.3
                        lap_formated = self.time_format(lap)
                        gap_formated = "+{0}".format(
                            self.time_format(leader_gap))
                        self.info[i] = [
                            total_time,
                            pilot_key,
                            lap_formated,
                            gap_formated,
                        ]

                else:
                    leader_gap = total_time - self.times_sorted[0][0]
                    lap_formated = self.time_format(lap)
                    gap_formated = "+{0}".format(self.time_format(leader_gap))
                    self.info[i] = [
                        total_time, pilot_key, lap_formated, gap_formated
                    ]
            else:
                lap_formated = self.time_format(lap)
                self.info[0] = [total_time, pilot_key, lap_formated, 0]

            self.data[pilot_key]["Total Time"] = self.times_sorted[i][0]

        self.info.sort()

    def time_format(self, timming):
        time_formated = "{0:.0f}:{1:.3f}".format((timming // 60),
                                                 (timming % 60))
        return time_formated

    def lap_time(self, pilot_key):
        if self.data[pilot_key]["Tires"] > 0:
            car = self.stats[pilot_key]["Car"]
            speed = sqrt(car * 0.65 + self.stats[pilot_key]["Speed"] * 0.35)
            concentration = self.stats[pilot_key][
                "Determination"] - self.stats[pilot_key]["Agressive"] / 10
            smoothness = self.stats[pilot_key]["Smoothness"] - (1 / car)
            rhythm = (smoothness * 0.6 + 0.2 * concentration)
            tires = self.data[pilot_key]["Tires"]

            lap = self.base_time - speed * 0.9 + log(101 - tires) / 8 + (
                self.gen.random() * rhythm / concentration) / 10
            self.data[pilot_key]["Tires"] -= (10 / sqrt(smoothness)) * (
                100 / self.track["Total_Laps"])
        else:
            lap = self.track["Base Time"] * 10
        return lap

    def pit_stop(self, pilot_key, total_time, lap):
        # print(pilot_key, "Changed Tires")
        self.data[pilot_key]["Tires"] = 100
        self.data[pilot_key]["Pit-Stop"] = False
        self.data[pilot_key]["Pit-Stops"] += 1
        self.times_sorted.append([total_time + 20, pilot_key, lap + 20])
        self.info.append([0, pilot_key, 0, 0])