# -*- coding: utf-8 -*-
from random import SystemRandom
from math import sqrt, log


class Racing_Engine():
    def __init__(self, dict_pilot, dict_track, dict_race):
        self.stats, self.track = dict_pilot, dict_track
        self.gen, self.data = SystemRandom(), dict_race
        self.weather = self.track["Weather"]
        self.base_time = self.track["Base Time"] * 60

    def run_a_lap(self):
        info = self.racing()
        return ([i[1:] for i in info], self.msg)

    def racing(self):
        self.msg = ''
        ret, times_sorted = [], []
        for pilot_key in self.data.keys():
            old_time = self.data[pilot_key]["Total Time"]
            if self.stats[pilot_key]["Owner"] == "IA":
                if self.data[pilot_key]["Tires"] < 30:
                    self.data[pilot_key]["Pit-Stop"] = True
            lap = self.lap_time(pilot_key)
            total_time = lap + old_time
            if self.data[pilot_key]["Pit-Stop"]:
                times_sorted.append(self.pit_stop(pilot_key, total_time, lap))
            else:
                times_sorted.append([total_time, pilot_key, lap])

        times_sorted.sort()
        num_pilots = len(self.data.keys())

        for i in range(num_pilots):
            total_time, pilot_key, lap = times_sorted[i]
            if i > 0:
                prey_time, prey_key, prey_lap = times_sorted[i - 1]
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
                        prey_gap = prey_time - times_sorted[0][0]
                        prey_gap_formated = "+{0}".format(
                            self.time_format(prey_gap))
                        prey_lap_formated = self.time_format(prey_lap)
                        ret[i - 1] = [
                            prey_time,
                            prey_key,
                            prey_lap_formated,
                            prey_gap_formated,
                        ]

                        # Time from who overtook
                        leader_gap = total_time - times_sorted[0][0]
                        lap_formated = self.time_format(lap)
                        gap_formated = "+{0}".format(
                            self.time_format(leader_gap))
                        ret.append([
                            total_time,
                            pilot_key,
                            lap_formated,
                            gap_formated,
                        ])
                        self.msg += '\n{} passou {}'.format(
                            pilot_key, prey_key)

                    else:
                        if gap < 0:
                            total_time = total_time - gap + 0.3
                        lap = prey_lap + 0.3
                        leader_gap = total_time - times_sorted[0][0] + 0.3
                        lap_formated = self.time_format(lap)
                        gap_formated = "+{0}".format(
                            self.time_format(leader_gap))
                        ret.append([
                            total_time, pilot_key, lap_formated, gap_formated
                        ])

                else:
                    leader_gap = total_time - times_sorted[0][0]
                    lap_formated = self.time_format(lap)
                    gap_formated = "+{0}".format(self.time_format(leader_gap))
                    ret.append(
                        [total_time, pilot_key, lap_formated, gap_formated])
            else:
                lap_formated = self.time_format(lap)
                ret.append([total_time, pilot_key, lap_formated, 0])

            self.data[pilot_key]["Total Time"] = times_sorted[i][0]

        ret.sort()
        return ret

    def time_format(self, timming: float) -> str:
        time_formated = "{0:.0f}:{1:.3f}".format((timming // 60),
                                                 (timming % 60))
        return time_formated

    def lap_time(self, pilot_key: str) -> float:
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
                100 / self.track["Total_Laps"]) * 1.2
        else:
            lap = self.base_time * 4
        return lap

    def pit_stop(self, pilot_key: str, total_time: float, lap: float) -> list:
        self.msg += '\n{} trocou os Pneus'.format(pilot_key)
        self.data[pilot_key]["Tires"] = 100
        self.data[pilot_key]["Pit-Stop"] = False
        self.data[pilot_key]["Pit-Stops"] += 1
        return [total_time + 20, pilot_key, lap + 20]