# -*- coding: utf-8 -*-
from random import SystemRandom
from math import sqrt, log

class Racing():
    def __init__(self, pilots: dict, track: dict, race: dict):
        self.stats, self.track = pilots, track
        self.gen, self.data = SystemRandom(), race
        self.weather = self.track['Weather']
        self.base_time = self.track['Base_Time'] * 60
        self.laps = 0

    def run(self):
        self.msg = ''
        timming, times_sorted = [], []
        for pilot_key in self.data.keys():
            old_time = self.data[pilot_key]['Total Time']
            if self.stats[pilot_key]['Owner'] == 'IA':
                if self.data[pilot_key]['Tires'] < 10:
                    self.data[pilot_key]['Pit-Stop'] = True
            lap = self.lap_time(pilot_key)
            total_time = lap + old_time
            if self.data[pilot_key]['Pit-Stop']:
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
                    overtake_diff = (self.track['Difficult'] -
                                     (self.stats[pilot_key]['Overtaking'] -
                                      self.stats[pilot_key]['Agressive'] +
                                      self.stats[prey_key]['Overtaking'] +
                                      self.stats[prey_key]['Agressive']) / 100)
                    lucky = self.gen.random()

                    if lucky > overtake_diff:
                        # Time from was overtook
                        prey_lap += 0.5
                        prey_time = total_time + 0.5
                        prey_gap = prey_time - times_sorted[0][0]
                        prey_gap_formated = self.time_format(prey_gap)
                        prey_gap_formated = f'+{prey_gap_formated}'
                        prey_lap_formated = self.time_format(prey_lap)
                        timming[i - 1] = [
                            prey_time,
                            prey_key,
                            prey_lap_formated,
                            prey_gap_formated,
                        ]

                        # Time from who overtook
                        leader_gap = total_time - times_sorted[0][0]
                        lap_formated = self.time_format(lap)
                        gap_formated = self.time_format(leader_gap)
                        gap_formated = f'+{gap_formated}'
                        timming.append([
                            total_time,
                            pilot_key,
                            lap_formated,
                            gap_formated,
                        ])
                        self.msg = (
                            f'{self.msg}\n{pilot_key} passou {prey_key}.')

                    else:
                        if gap < 0:
                            total_time = total_time - gap + 0.3
                        lap = prey_lap + 0.3
                        leader_gap = total_time - times_sorted[0][0] + 0.3
                        lap_formated = self.time_format(lap)
                        gap_formated = self.time_format(leader_gap)
                        gap_formated = f'+{gap_formated}'
                        timming.append([
                            total_time, pilot_key, lap_formated, gap_formated
                        ])

                else:
                    leader_gap = total_time - times_sorted[0][0]
                    lap_formated = self.time_format(lap)
                    gap_formated = self.time_format(leader_gap)
                    gap_formated = f'+{gap_formated}'
                    timming.append(
                        [total_time, pilot_key, lap_formated, gap_formated])
            else:
                lap_formated = self.time_format(lap)
                timming.append([total_time, pilot_key, lap_formated, 0])

            self.data[pilot_key]['Total Time'] = times_sorted[i][0]

        timming.sort()
        ret = ([i[1:] for i in timming], self.msg)
        return ret

    def time_format(self, timming: float) -> str:
        time_formated = f'{(timming // 60):.0f}:{(timming % 60):.3f}'
        return time_formated

    def lap_time(self, pilot_key: str) -> float:
        if self.data[pilot_key]['Tires'] > 0:
            total_laps = self.track['Total_Laps']
            car = self.stats[pilot_key]['Car']
            speed = sqrt(car * 0.7 + self.stats[pilot_key]['Speed'] * 0.3)
            concentration = self.stats[pilot_key]['Determination'] -\
                self.stats[pilot_key]['Agressive'] / 10
            smoothness = self.stats[pilot_key]['Smoothness'] - (100 / car)
            rhythm = (smoothness * 0.65 + 0.35 * concentration)
            tires = self.data[pilot_key]['Tires']

            lap = self.base_time - (
                speed + 2 * self.laps / total_laps
            ) + 40 * self.gen.random() / rhythm + log(101 - tires) / 5
            self.data[pilot_key]['Tires'] -= (10 + 2*self.gen.random()) / \
                sqrt(smoothness) * (100 / total_laps) * 1.2
        else:
            lap = self.base_time * 4
        return lap

    def pit_stop(self, pilot_key: str, total_time: float, lap: float) -> list:
        self.msg = f'{self.msg}\n{pilot_key} trocou os Pneus.'
        self.data[pilot_key]['Tires'] = 100
        self.data[pilot_key]['Pit-Stop'] = False
        self.data[pilot_key]['Pit-Stops'] += 1
        loss_time = 20 + self.gen.random()
        total_time += loss_time
        lap += loss_time
        ret = [total_time, pilot_key, lap]
        return ret
    
    