
import sys, os, math, random, time, datetime, json, optparse, numpy

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame.locals import *
from pygame.color import *

class Player :
    def __init__(self, world, states, width = 600, height = 600, grid_size = 50) :
        self.world = world
        self.states = states
        self.width = width
        self.height = height
        self.grid_size = grid_size

    def draw_world(self, screen, info) :
        xcenter = int(math.ceil(self.width / 2.0))
        ycenter = int(math.ceil(self.height / 2.0))
        shift = math.floor(self.grid_size / 2)
        for x in range(- self.world.xlim, self.world.xlim + 2) :
            point0 = self.get_screen_point((x * self.grid_size - shift, - self.world.ylim * self.grid_size - shift))
            point1 = self.get_screen_point((x * self.grid_size - shift, self.world.ylim * self.grid_size + shift))
            pygame.draw.line(screen, THECOLORS["black"], (point0[0], point0[1]), (point1[0], point1[1]), 1)
        for y in range(- self.world.ylim, self.world.ylim + 2) :
            point0 = self.get_screen_point((- self.world.xlim * self.grid_size - shift, y * self.grid_size - shift))
            point1 = self.get_screen_point((self.world.xlim * self.grid_size + shift, y * self.grid_size - shift))
            pygame.draw.line(screen, THECOLORS["black"], (point0[0], point0[1]), (point1[0], point1[1]), 1)

    def draw_agent(self, screen, agent, info) :
        radius = math.floor(self.grid_size * 0.32 * (1 - info["delay"] * 0.2))
        color = THECOLORS["red"] if agent.id % 2 == 0 else THECOLORS["blue"]
        point = self.get_screen_point((info["pos"][0] * self.grid_size, info["pos"][1] * self.grid_size))
        pygame.draw.circle(screen, color, (point[0], point[1]), radius, 0)

    def draw_obt(self, screen, obt, info) :
        shift = math.floor(self.grid_size / 2)
        point = self.get_screen_point((info["pos"][0] * self.grid_size - shift, info["pos"][1] * self.grid_size + shift))
        pygame.draw.rect(screen, THECOLORS["black"], (point[0], point[1], self.grid_size, self.grid_size), 0)

    def draw_comment(self, screen, info) :
        screen.blit(pygame.font.Font(None, 16).render("Step: %d; Speed: %d" % (info["step"], info["speed"]), 1, THECOLORS["black"]), (5, self.height - 15))

    def draw(self, screen, step, speed) :
        if screen is not None and step >= 0 and step < len(self.states) :
            screen.fill(THECOLORS["lightgray"])
            pygame.display.flip()
            self.draw_world(screen = screen, info = {})
            for s in range(step, max(step - 1, -1), -1) :
                for i, state in enumerate(self.states[s]["agents"]) :
                    self.draw_agent(screen, self.world.agents[i],
                        info = {"pos" : (state[1], state[2]),
                                "delay" : step - s
                                })
                obt_style = {"color" : THECOLORS["black"]}
                for i, state in enumerate(self.states[s]["obts"]) :
                    self.draw_obt(screen, self.world.obts[i],
                        info = {"pos" : (state[1], state[2]),
                                "style": obt_style,
                                })
            self.draw_comment(screen, info = {"speed" : speed, "step" : step})
            pygame.display.set_caption("Grid World Player")
            pygame.display.flip()

    def get_screen_point(self, pos) :
        point = (int(self.width / 2.0 + pos[0]), int(self.height / 2.0 - pos[1]))
        return point

    def run(self) :
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
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
                        step = len(self.states) - 1
                    updated = True

            if paused == False and (phase is None or phase != 0) :
                if phase is None or phase > 0 :
                    step = min(len(self.states) - 1, step + 1)
                    updated = True
                    if phase is not None and phase > 0 :
                        phase -= 1
                else :
                    step = max(0, step - speed)
                    updated = True
                    if phase is not None and phase < 0 :
                        phase += 1
                if phase == 0 or step == len(self.states) - 1 :
                    paused = True
            if updated :
                self.draw(screen, step, speed)
                updated = False
            pygame.event.pump()
            clock.tick(speed)
