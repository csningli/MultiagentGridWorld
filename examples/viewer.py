
import sys, os, math, random, time, datetime, json, optparse, numpy

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame.locals import *
from pygame.color import *


class Viewer :
    def __init__(self, category : str, screen_width : int, screen_height : int, width : int, height : int, starts : list, targets : list, obstacles : list, life : int = 1) :
        self.category = category
        self.starts = starts
        self.targets = targets
        self.obstacles = obstacles
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.life = life
        self.radius = 10

    def draw(self, screen) :
        if screen is not None :
            screen.fill(THECOLORS["black"])
            pygame.display.flip()

            x_lim = int(math.ceil(self.width / 2.0))
            y_lim = int(math.ceil(self.height / 2.0))
            for x in range(- x_lim - 1, x_lim + 2) :
                point = (int(self.screen_width / 2.0 + x * self.radius), int(self.screen_height / 2.0 - (- y_lim - 1) * self.radius))
                pygame.draw.rect(screen, THECOLORS["gray"], (point[0], point[1], self.radius, self.radius), 0)
                point = (int(self.screen_width / 2.0 + x * self.radius), int(self.screen_height / 2.0 - (y_lim + 1) * self.radius))
                pygame.draw.rect(screen, THECOLORS["gray"], (point[0], point[1], self.radius, self.radius), 0)
            for y in range(- y_lim - 1, y_lim + 2) :
                point = (int(self.screen_width / 2.0 + (- x_lim - 1) * self.radius), int(self.screen_height / 2.0 - y * self.radius))
                pygame.draw.rect(screen, THECOLORS["gray"], (point[0], point[1], self.radius, self.radius), 0)
                point = (int(self.screen_width / 2.0 + (x_lim + 1) * self.radius), int(self.screen_height / 2.0 - y * self.radius))
                pygame.draw.rect(screen, THECOLORS["gray"], (point[0], point[1], self.radius, self.radius), 0)

            for pose in self.obstacles :
                point = (int(self.screen_width / 2.0 + pose[0] * self.radius), int(self.screen_height / 2.0 - pose[1] * self.radius))
                pygame.draw.rect(screen, THECOLORS["gray"], (point[0], point[1], self.radius, self.radius), 0)
            for pose in self.targets :
                point = (int(self.screen_width / 2.0 + pose[0] * self.radius), int(self.screen_height / 2.0 - pose[1] * self.radius))
                pygame.draw.rect(screen, THECOLORS["red"], (point[0], point[1], self.radius, self.radius), 0)
            for pose in self.starts :
                point = (int(self.screen_width / 2.0 + pose[0] * self.radius), int(self.screen_height / 2.0 - pose[1] * self.radius))
                pygame.draw.rect(screen, THECOLORS["green"], (point[0], point[1], self.radius, self.radius), 0)
            screen.blit(pygame.font.Font(None, 16).render("Number of nodes: %d" % len(self.starts), 1, THECOLORS["white"]), (5, 5))
            pygame.display.set_caption("Viewer")
            pygame.display.flip()

    def run(self) :
        pygame.init()
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        running = True
        while running == True :
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN :
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_TAB :
                        timelabel = datetime.datetime.now().strftime('%Y%m%d%H%M%S_%f')
                        pygame.image.save(screen, timelabel + ".png")

            self.draw(screen)
            pygame.event.pump()


def parse_arguments_for_viewer_args() :
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", dest="config", help="Path to the configuration file.")
    parser.add_option("-w", "--width", dest="width", default=300, help="Width of the screen.")
    parser.add_option("-t", "--height", dest="height", default=300, help="Height of the screen.")
    parser.add_option("-a", "--category", dest="category", default="start", help="Category: start / target.")
    options, args = parser.parse_args()

    config = {}
    if os.path.isfile(options.config) :
        with open(options.config, 'r') as f :
            loaded = json.load(f)
            for key in ["starts", "targets", "obstacles", "width", "height", "life"] :
                config[key] = loaded.get(key, None)

        config["category"] = options.category
        config["screen_width"] = int(options.width)
        config["screen_height"] = int(options.height)
    else :
        print("[Viewer] Invalid path of log file: %s" % options.config)
    return config

if __name__ == "__main__" :

    args = parse_arguments_for_viewer_args()

    if len(args) > 0 :
        viewer = Viewer(**args)
        viewer.run()
