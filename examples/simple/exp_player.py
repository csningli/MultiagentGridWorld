
import sys

sys.path.append("../..")

from player import *

class SimplePlayer(Player) :
    def __init__(self, screen_width : int, screen_height : int, targets : list, obstacles : list, data : list, width : int, height : int, life : int = 1) :
        super(SimplePlayer, self).__init__(screen_width = screen_width, screen_height = screen_height, targets = targets, obstacles = obstacles, data = data, width = width, height = height, life = life)
        self.tracks = [[] for i in range(len(data[0]))]

    def draw_record(self, screen, record, color = "green") :
        super(SimplePlayer, self).draw_record(screen, record, color)
        for id, pos in enumerate(record) :
            self.tracks[id].append(pos)
            for i in range(len(self.tracks[id])) :
                if i < len(self.tracks[id]) - 1 :
                    start = self.get_screen_point((self.tracks[id][i][0] * self.radius + self.radius / 2.0, self.tracks[id][i][1] * self.radius - self.radius / 2.0))
                    end = self.get_screen_point((self.tracks[id][i + 1][0] * self.radius + self.radius / 2.0, self.tracks[id][i + 1][1] * self.radius - self.radius / 2.0))
                    pygame.draw.line(screen, THECOLORS["cyan"], start, end)


if __name__ == "__main__" :
    config = {
        "targets" : [],
        "obstacles" : [],
        "data" : [],
        "width" : 20,
        "height" : 20,
        "life" : 1,
    }

    log = ""
    for file in os.listdir(".") :
        name, ext = os.path.splitext(file)
        if ext == ".log" :
            log = file

    if log != "" and os.path.isfile(log) :
        with open(log, 'r') as f :
            loaded = json.load(f)
            for key, value in config.items() :
                config[key] = loaded.get(key, value)

        config["screen_width"] = 300
        config["screen_height"] = 300

        player = SimplePlayer(**config)
        player.run()
    else :
        print("Cannot find the log file.")
