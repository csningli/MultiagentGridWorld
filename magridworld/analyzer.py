
import sys, os, math, random, time, datetime, json, optparse, numpy

from utils import *

class Analyzer :
    def __init__(self, targets : list, obstacles : list, data : list, width : int, height : int, life : int) :
        self.targets = [pos for pos in targets]
        self.obstacles = [pos for pos in obstacles]
        self.data = data
        self.width = width
        self.height = height
        self.life = life
        self.summary = {}
        self.analyze()

    def analyze(self) :
        stable_agents = []
        stable_count = 0
        stable_mark = [False for i in range(len(self.targets))]
        last_positions = [numpy.array(target) for target in self.targets]
        move_dists = [None for i in range(len(self.targets))]
        min_dists = [None for i in range(len(self.targets))]
        move_times = [None for i in range(len(self.targets))]
        min_times = [None for i in range(len(self.targets))]
        for record in self.data :
            stable_agents.append([])
            for i in range(len(record)) :
                if stable_mark[i] == False :
                    pos = record[i]
                    if pos == self.targets[i] :
                        stable_agents[-1].append(i)
                        stable_mark[i] = True
                    if move_dists[i] is not None :
                        move_dists[i] += l1_dist(pos, last_positions[i])
                    else :
                        move_dists[i] = 0.0
                        min_dists[i] = l1_dist(pos, self.targets[i])
                    if move_times[i] is not None :
                        move_times[i] += 1
                    else :
                        move_times[i] = 0.0
                        min_times[i] = l1_dist(pos, self.targets[i])
                    last_positions[i] = pos
            stable_count += len(stable_agents[-1])
            if stable_count >= len(self.targets) and self.summary.get("all_at_targets") is None :
                self.summary["all_at_targets"] = "{0: d}".format(len(stable_agents) - 1)
            if stable_count >= len(self.targets) * 0.9 and self.summary.get("90_at_targets") is None :
                self.summary["90_at_targets"] = "{0: d}".format(len(stable_agents) - 1)

        if len(move_dists) > 0 :
            self.summary["avg_travel_dist"] = "{0: .4f}".format(sum(move_dists) / len(move_dists))
            detour_ratios = []
            for i in range(len(self.targets)) :
                if min_dists[i] > 0 :
                    detour_ratios.append(move_dists[i] / min_dists[i])
                else :
                    detour_ratios.append(1.0)
            self.summary["avg_detour_d_ratio"] = "{0: .4f}".format(sum(detour_ratios) / len(detour_ratios))

        if len(move_times) > 0 :
            self.summary["avg_travel_time"] = "{0: .4f}".format(sum(move_times) / len(move_times))
            detour_ratios = []
            for i in range(len(self.targets)) :
                if min_times[i] > 0 :
                    detour_ratios.append(move_times[i] / min_times[i])
                else :
                    detour_ratios.append(1.0)
            self.summary["avg_detour_t_ratio"] = "{0: .4f}".format(sum(detour_ratios) / len(detour_ratios))


        for key in ["all_at_targets", "90_at_targets", "avg_travel_dist", "avg_travel_time", "avg_detour_d_ratio", "avg_detour_t_ratio"] :
            if self.summary.get(key, None) is None :
                self.summary[key] = "N/A"

    def report(self) :
        print("=" * 50)
        print("Analysis Report")
        print("-" * 50)
        for key, result in self.summary.items() :
            print("{0: <10s} : {1: >10s}".format(key, result))
        print("=" * 50)
        

def parse_arguments_for_analyzer_args() :
    parser = optparse.OptionParser()
    parser.add_option("-g", "--log", dest="log", help="Path to the log file.")
    options, args = parser.parse_args()

    config = {}
    if os.path.isfile(options.log) :
        with open(options.log, 'r') as f :
            loaded = json.load(f)
            for key in ["targets", "obstacles", "data", "width", "height", "life"] :
                config[key] = loaded.get(key, None)
    else :
        print("[Analyzer] Invalid path of log file: %s" % options.log)
    return config


if __name__ == "__main__" :
    args = parse_arguments_for_analyzer_args()
    if len(args) > 0 :
        analyzer = Analyzer(**args)
        analyzer.report()
