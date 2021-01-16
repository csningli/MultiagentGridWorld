
import sys, os, math, random, time, datetime, json, optparse, numpy

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame.locals import *
from pygame.color import *

class Player :
    def __init__(self, screen_width : int, screen_height : int, targets : list, obstacles : list, data : list, width : int, height : int, life : int = 1) :
        self.targets = targets
        self.obstacles = obstacles
        self.data = data
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.life = life
        self.radius = 10

    def draw(self, screen, step, speed) :
        if screen is not None and step >= 0 and step < len(self.data) :
            screen.fill(THECOLORS["black"])
            pygame.display.flip()

            self.draw_border(screen = screen)
            self.draw_targets(screen = screen)
            self.draw_obstacles(screen = screen)
            self.draw_record(screen = screen, record = self.data[step])

            screen.blit(pygame.font.Font(None, 16).render("Speed: %d; Step: %d" % (speed, step), 1, THECOLORS["white"]), (5, 5))
            pygame.display.set_caption("Player")
            pygame.display.flip()

    def draw_border(self, screen, color = "darkgray") :
        x_lim = int(math.ceil(self.width / 2.0))
        y_lim = int(math.ceil(self.height / 2.0))
        for x in range(- x_lim - 1, x_lim + 2) :
            point = self.get_screen_point((x * self.radius, (- y_lim - 1) * self.radius))
            pygame.draw.rect(screen, THECOLORS[color], (point[0], point[1], self.radius, self.radius), 0)
            point = self.get_screen_point((x * self.radius, (y_lim + 1) * self.radius))
            pygame.draw.rect(screen, THECOLORS[color], (point[0], point[1], self.radius, self.radius), 0)
        for y in range(- y_lim - 1, y_lim + 2) :
            point = (int(self.screen_width / 2.0 + (- x_lim - 1) * self.radius), int(self.screen_height / 2.0 - y * self.radius))
            point = self.get_screen_point(((- x_lim - 1) * self.radius, y * self.radius))
            pygame.draw.rect(screen, THECOLORS[color], (point[0], point[1], self.radius, self.radius), 0)
            point = self.get_screen_point(((x_lim + 1) * self.radius, y * self.radius))
            pygame.draw.rect(screen, THECOLORS[color], (point[0], point[1], self.radius, self.radius), 0)

    def draw_obstacles(self, screen, color = "darkgray") :
        for pose in self.obstacles :
            point = self.get_screen_point((pose[0] * self.radius, pose[1] * self.radius))
            pygame.draw.rect(screen, THECOLORS[color], (point[0], point[1], self.radius, self.radius), 0)

    def draw_targets(self, screen, color = "red") :
        for pose in self.targets :
            point = self.get_screen_point((pose[0] * self.radius, pose[1] * self.radius))
            pygame.draw.rect(screen, THECOLORS[color], (point[0], point[1], self.radius, self.radius), 0)

    def draw_record(self, screen, record, color = "green") :
        for pose in record :
            point = self.get_screen_point((pose[0] * self.radius, pose[1] * self.radius))
            pygame.draw.rect(screen, THECOLORS[color], (point[0], point[1], self.radius, self.radius), 0)

    def get_screen_point(self, pos) :
        point = (int(self.screen_width / 2.0 + pos[0]), int(self.screen_height / 2.0 - pos[1]))
        return point

    def run(self) :
        pygame.init()
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        clock = pygame.time.Clock()
        speed = 1     # number of rounds in one second
        phase = None     # number of steps to run; None for ever
        running = True
        paused = True
        updated = True
        step = 0

        while running == True :
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN :
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE :
                        paused = not paused
                        if paused == False :
                            phase = None
                    if event.key == K_TAB :
                        timelabel = datetime.datetime.now().strftime('%Y%m%d%H%M%S_%f')
                        pygame.image.save(screen, timelabel + ".png")
                elif event.type == KEYUP :
                    if event.key == K_UP :
                        speed = speed + 1
                    elif event.key == K_DOWN :
                        speed = max(1, speed - 1)
                    elif event.key == K_RIGHT :
                        if paused == True :
                            phase = 1
                            paused = False
                    elif event.key == K_LEFT :
                        if paused == True :
                            phase = -1
                            paused = False
                    elif event.key == K_s :
                        step = 0
                    elif event.key == K_e :
                        step = len(self.data) - 1
                    updated = True

            if paused == False and (phase is None or phase != 0) :
                if phase is None or phase > 0 :
                    step = min(len(self.data) - 1, step + 1)
                    updated = True
                    if phase is not None and phase > 0 :
                        phase -= 1
                else :
                    step = max(0, step - speed)
                    updated = True
                    if phase is not None and phase < 0 :
                        phase += 1
                if phase == 0 or step == len(self.data) - 1 :
                    paused = True
            if updated :
                self.draw(screen, step, speed)
                updated = False
            pygame.event.pump()
            clock.tick(speed)


def parse_arguments_for_player_args() :
    parser = optparse.OptionParser()
    parser.add_option("-g", "--log", dest="log", help="Path to the log file.")
    parser.add_option("-w", "--width", dest="width", default=300, help="Width of the screen.")
    parser.add_option("-t", "--height", dest="height", default=300, help="Height of the screen.")
    options, args = parser.parse_args()

    config = {}

    if os.path.isfile(options.log) :
        with open(options.log, 'r') as f :
            loaded = json.load(f)
            for key in ["targets", "obstacles", "data", "width", "height", "life"] :
                config[key] = loaded.get(key, None)
        config["screen_width"] = int(options.width)
        config["screen_height"] = int(options.height)
    else :
        print("[Player] Invalid path of log file: %s" % options.log)

    return config


if __name__ == "__main__" :
    args = parse_arguments_for_player_args()
    if len(args) > 0 :
        player = Player(**args)
        player.run()
