from panda3d.core import loadPrcFileData
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
import numpy as np
import csv

confVars = """
win-size 1280 720
window-title Titre
undecorated false
show-frame-rate-meter true
show-scene-graph-analyzer-meter 1
sync-video 1
"""

loadPrcFileData("", confVars)

# Inputs map
keyMap = {
    "left": False,
    "right": False,
    "down": False
}


# Function that updates the input map
def updateKeyMap(key, state):
    keyMap[key] = state


class Disc:
    def __init__(self, disc, color):
        self.disc = disc
        self.color = color
        self.disc.setTexture(color)
        self.disc.setPos(0, 0, 7.5)
        self.disc.setScale(0.75, 0.75, 0.75)


class Connect4(ShowBase):
    def __init__(self):
        super().__init__()

        # Inputs management
        self.accept("arrow_left", updateKeyMap, ["left", True])
        self.accept("arrow_left-up", updateKeyMap, ["left", False])
        self.accept("arrow_right", updateKeyMap, ["right", True])
        self.accept("arrow_right-up", updateKeyMap, ["right", False])
        self.accept("arrow_down", updateKeyMap, ["down", True])
        self.accept("arrow_down-up", updateKeyMap, ["down", False])

        # General settings
        self.disable_mouse()
        self.set_background_color(1, 1, 0.9)

        # Grid management
        self.grid = self.loader.loadModel("../models/grille")
        self.grid.reparentTo(self.render)
        self.blue_grid = self.loader.loadTexture("../tex/blue_plastic.jpg")
        self.grid.setTexture(self.blue_grid)
        self.grid.setHpr(90, 0, 0)
        self.grid.setScale(1, 1, 1)
        self.grid.setPos(0, 40, -6.5)
        self.axes_H = [-6, -4, -2, 0, 2, 4, 6]
        self.axes_V = [-5, -3, -1, 1, 3, 5]
        self.index = 3

        # Discs management
        self.red_texture = self.loader.loadTexture("../tex/red_plastic.jpg")
        self.yellow_texture = self.loader.loadTexture("../tex/yellow_plastic.jpg")
        self.discs = []
        for i in range(0, 43):
            self.disc = self.loader.loadModel("../models/jeton")
            self.disc.reparentTo(self.render)
            if i % 2 == 0:
                self.color_disc = Disc(self.disc, self.red_texture)
            else:
                self.color_disc = Disc(self.disc, self.yellow_texture)
            self.discs.append(self.color_disc)

        self.round = 0
        self.speed = 20
        self.line = 0  # final line position
        self.discs[self.round].disc.setPos(0, 40, 7.5)
        self.movement_V = False
        self.movement_H = False

        # Grid content
        self.gridContent = np.zeros((6, 7))

        # Read csv file cases
        results = []
        with open("../csv/cases.csv") as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
            for row in reader:  # each row is a list
                results.append(row)
        print(results)

        # Addition of an update function
        self.taskMgr.add(self.mainloop, "mainloop")

    # Fonction d'actualisation
    def mainloop(self, task):
        dt = globalClock.getDt()
        # print(self.gridContent)

        pos = self.discs[self.round].disc.getPos()
        #pos.z = 7.5


        # left clic
        if keyMap["left"] and self.index != 0 and not self.movement_V:
            keyMap["left"] = False
            self.index -= 1
            self.movement_H = True

        # right clic
        if keyMap["right"] and self.index != 6 and not self.movement_V:
            keyMap["right"] = False
            self.index += 1
            self.movement_H = True

        # down clic
        if keyMap["down"] and self.gridContent[5][self.index] != 1 and not self.movement_V:
            keyMap["down"] = False

            # Compute new position
            while self.gridContent[self.line][self.index] != 0:
                self.line += 1
            self.movement_V = True

            # update presence grid
            self.gridContent[self.line][self.index] = 1

        if self.movement_V and pos.z != self.axes_V[self.line]:
            pos.z -= 0.5
            self.discs[self.round].disc.setPos(pos)

        # prepare next disc
        if self.movement_V and pos.z == self.axes_V[self.line]:
            pos.z = self.axes_V[self.line]
            self.line = 0
            self.discs[self.round].disc.setPos(pos)
            self.round += 1
            self.discs[self.round].disc.setPos(0, 40, 7.5)
            self.movement_V = False
            self.index = 3

        if self.movement_H:
            pos.x = self.axes_H[self.index]
            self.discs[self.round].disc.setPos(pos)
            self.movement_H = False

        return task.cont

# Boucle principal
game = Connect4()
game.run()
