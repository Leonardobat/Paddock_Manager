# -*- coding: utf-8 -*-
from random import SystemRandom
from math import sqrt


class Racing_Engine():
    def __init__(self, dict_pilot, dict_track):
        self.times_sorted, self.info = [], []
        self.data, self.stats, self.track = [], dict_pilot, dict_track
        self.gen = SystemRandom()

    def run_a_lap(self, dict_race):
        self.data = dict_race
        self.racing()
        return (self.info, self.data)

    def racing(self):
        for pilot_key in self.data.keys():
            old_time = self.data[pilot_key]["Total Time"]
            if self.stats[pilot_key]["Owner"] == "IA":
                if self.data[pilot_key]["Tires"] < 2:
                    self.data[pilot_key]["Pit-Stop"] = True
            lap = self.lap_time(pilot_key)
            total_time = lap + old_time
            if self.data[pilot_key]["Pit-Stop"]:  # Pit-Stop
                lap += 20
                total_time += 20
                # print(pilot_key, "Changed Tires")
                self.data[pilot_key]["Tires"] = 10
                self.data[pilot_key]["Pit-Stop"] = False
                self.data[pilot_key]["Pit-Stops"] += 1
                self.times_sorted.append([total_time, pilot_key, lap])
                self.info.append([0, pilot_key, 0, 0])
            else:
                self.times_sorted.append([total_time, pilot_key, lap])
                self.info.append([0, pilot_key, 0, 0])

        self.times_sorted.sort()
        num_pilots = len(self.times_sorted)

        for i in range(num_pilots):  # Overtakings + Gaps
            total_time, pilot_key, lap = self.times_sorted[i]
            if i != 0:
                prey_time, prey_key, prey_lap = self.times_sorted[i - 1]
                gap = total_time - prey_time
                if gap < 1:
                    over_diff = (7 + self.track["Difficult"] -
                                 (self.stats[pilot_key]["Technique"] -
                                  self.stats[prey_key]["Technique"]))
                    lucky = 10 * self.gen.random()

                    if lucky > over_diff:
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
        return

    def time_format(self, timming):
        time_formated = "{0:.0f}:{1:.3f}".format((timming // 60),
                                                 (timming % 60))
        return time_formated

    def lap_time(self, pilot_key):
        if self.data[pilot_key]["Tires"] > 0:
            base_time, weather = self.track["Base Time"], self.track["Weather"]
            technique = self.stats[pilot_key]["Technique"]
            concentration = self.stats[pilot_key]["Concentration"]
            smoothness = self.stats[pilot_key]["Smoothness"]
            rhythm = self.stats[pilot_key]["Rhythm"]
            car_overall = self.stats[pilot_key]["Car"]
            tires = self.data[pilot_key]["Tires"]
            spid = sqrt(technique * 0.5 + 0.5 * car_overall)
            lap = (
                60 * (base_time) - spid * (1 - 0.08 * weather) +
                5 * sqrt(weather) -
                0.01 * self.gen.random() * sqrt(tires * 0.3 + 0.7 * rhythm) /
                (weather + 1) - 0.1 * weather *
                (sqrt(concentration * 0.7 + 0.3 * car_overall) - 0.15 *
                 (concentration * 0.7 + 0.3 * car_overall)))

            self.data[pilot_key]["Tires"] -= (
                0.4 / sqrt(smoothness)) * 1  # Type of Tires
        else:
            lap = 1000
        return lap