from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectButton import DirectButton
import numpy as np
import csv
from panda3d.core import loadPrcFile

loadPrcFile("config/Confinit.prc")
loadPrcFile("config/Config.prc")
loadPrcFile("config/Confauto.prc")

class Disc:
    def __init__(self, disc, color):
        self.disc = disc
        self.color = color
        self.disc.setTexture(color)
        self.disc.setPos(0, 0, 6)
        self.disc.setScale(0.5, 0.5, 0.5)

# Inputs map
keyMap = {
    "left": False,
    "right": False,
    "down": False
}


def updateKeyMap(key, state):
    """ Function that updates the input map """
    keyMap[key] = state



class Connect4(ShowBase):
    def __init__(self):
        """ Initialization of the connect 4"""
        print('Connect4 created.')
        super().__init__()

        self.background = OnscreenImage(parent=self.render2dp, image="tex/bedroom.jpg") # Load an image object
        self.cam2dp.node().getDisplayRegion(0).setSort(-20)

        # Load the avatar
        self.arm = Actor("models/Tatsumi_models/Tatsumi_1", {"anim1": "models/Tatsumi_models/Tatsumi_1_anim"})
        self.arm.setPos(0, 50, -36)
        self.arm.setScale(20, 20, 20)
        self.arm.reparentTo(self.render)
        self.arm.play("anim1")

        # Load the table
        self.table = self.loader.loadModel("models/table")
        self.table.reparentTo(self.render)
        self.table.setPos(0, 30, -8)
        self.table.setScale(2, 2, 2)
        self.table.setHpr(90, 0, 0)

        # Inputs management
        self.accept("arrow_left", updateKeyMap, ["left", True])
        self.accept("arrow_left-up", updateKeyMap, ["left", False])
        self.accept("arrow_right", updateKeyMap, ["right", True])
        self.accept("arrow_right-up", updateKeyMap, ["right", False])
        self.accept("arrow_down", updateKeyMap, ["down", True])
        self.accept("arrow_down-up", updateKeyMap, ["down", False])

        # General settings
        # self.disable_mouse()
        self.set_background_color(1, 1, 0.9)

        # Grid management
        self.grid = self.loader.loadModel("models/grid")
        self.grid.reparentTo(self.render)
        self.blue_grid = self.loader.loadTexture("tex/blue_plastic.jpg")
        self.grid.setTexture(self.blue_grid)
        self.grid.setHpr(90, 0, 0)
        self.grid.setScale(0.6, 0.6, 0.6)
        self.grid.setPos(0, 30, -6.5)
        self.axes_H = [-3.6, -2.4, -1.2, 0, 1.2, 2.4, 3.6]
        self.axes_V = [0.25, -1.0, -2.25, -3.5, -4.75, -6]
        self.column = 3
        self.line = 5

        # Discs initialization
        self.red_texture = self.loader.loadTexture("tex/red_plastic.jpg")
        self.yellow_texture = self.loader.loadTexture("tex/yellow_plastic.jpg")
        self.discs = []
        for i in range(0, 44):
            self.disc = self.loader.loadModel("models/disc")
            self.disc.reparentTo(self.render)
            if i % 2 == 0:
                self.color_disc = Disc(self.disc, self.red_texture)
            else:
                self.color_disc = Disc(self.disc, self.yellow_texture)
            self.discs.append(self.color_disc)

        # Other parameters initialization
        self.round = 0
        self.player = 1
        self.speed = 40
        self.discs[self.round].disc.setPos(0, 30, 1.5)
        self.movement_V = False
        self.movement_H = False

        # Grid content
        self.gridContent = np.zeros(6*7)

        # Read csv file cases
        self.results = []
        with open("csv/cases.csv") as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                self.results.append(row)

        # Addition of an update function
        self.taskMgr.add(self.mainloop, "mainloop")

        # Victory text
        font = self.loader.loadFont("font/Roboto-Medium.ttf")
        font.setPixelsPerUnit(60)
        self.text_victory = OnscreenText(text='', pos=(1.4, -0.8), scale=0.1)
        self.text_victory.setFg((0, 0, 0, 1))
        self.text_victory.setBg((1, 1, 1, 0))
        self.text_victory.setShadow((0.5, 0.5, 0.5, 1))

        # Button new game
        def new_game():
            print("New game ...")
            self.gridContent = np.zeros(6 * 7)
            for i in range(0, 44):
                self.discs[i].disc.setPos(0, 0, 1.5)
            self.round = 0
            self.discs[self.round].disc.setPos(0, 30, 1.5)
            self.text_victory.setText('')

        # Button save game
        def save_game():
            print("Save the game ...")
            grid_content_str = ','.join([str(elem) for elem in self.gridContent])
            f = open("safeguard/safeguard.txt", "a")
            f.write(grid_content_str + "\n")
            f.close()

        # Button load game
        def load_game():
            print("Load a game ...")
            f1 = open("safeguard/safeguard.txt", "r")
            last_line = f1.readlines()[-1]
            f1.close()
            last_line_list = last_line.split(',')
            k = 0
            p = 1
            round = 0
            for i in range(0, 42):
                col = i % 7
                line = i // 7
                if last_line_list[i] == '1.0':
                    self.discs[k].disc.setPos(self.axes_H[col], 30, self.axes_V[line])
                    k += 2
                    round += 1
                elif last_line_list[i] == '2.0':
                    self.discs[p].disc.setPos(self.axes_H[col], 30, self.axes_V[line])
                    p += 2
                    round += 1
            self.round = round
            self.discs[self.round].disc.setPos(0, 30, 1.5)
            self.gridContent = [int(float(j)) for j in last_line_list]

        # Button 1
        self.new_game_button = DirectButton(text="New game", pos=(-1.5, 0, 0.9), frameSize=(-3, 3, -0.5, 1),
                                       scale=.1, text_scale=0.9, command=new_game)

        # Button 2
        self.load_game_button = DirectButton(text="Load", pos=(-1.5, 0, 0.75), frameSize=(-3, 3, -0.5, 1),
                         scale=.1, text_scale=0.9, command=load_game)

        # Button 2
        self.load_game_button = DirectButton(text="Save", pos=(-1.5, 0, 0.60), frameSize=(-3, 3, -0.5, 1),
                         scale=.1, text_scale=0.9, command=save_game)
        self.button_changed = False

    def __del__(self):
        print('Destructor called, connect4 deleted.')

    def mainloop(self, task):
        """ Main loop of the connect 4 game """
        dt = globalClock.getDt()

        pos = self.discs[self.round].disc.getPos()

        # Left click
        if keyMap["left"] and self.column != 0 and not self.movement_V:
            keyMap["left"] = False
            self.column -= 1
            self.movement_H = True

        # Right click
        if keyMap["right"] and self.column != 6 and not self.movement_V:
            keyMap["right"] = False
            self.column += 1
            self.movement_H = True

        # down clic
        if keyMap["down"] and self.gridContent[self.column] == 0 and not self.movement_V:
            # To have only one click
            keyMap["down"] = False

            # Find the position
            line_fixed = 0
            self.line = 5
            while line_fixed == 0 and self.line >= 0:
                if self.gridContent[7 * self.line + self.column] != 0:
                    self.line -= 1
                else:
                    line_fixed = 1
            self.movement_V = True

            # check if there is a victory or not
            victory = self.check_victory()
            if victory == 1:
                self.text_victory.setText('Red wins')
            if victory == 2:
                self.text_victory.setText('Yellow wins')

        # Progressive vertical movement
        if self.movement_V and pos.z != self.axes_V[self.line]:
            pos.z -= 0.25
            self.discs[self.round].disc.setPos(pos)

        # Set the disc position / Prepare next disc
        if self.movement_V and pos.z == self.axes_V[self.line]:
            self.movement_V = False
            self.line = 0
            self.column = 3
            self.round += 1
            self.discs[self.round].disc.setPos(0, 30, 1.5)

        # Horizontal movement
        if self.movement_H:
            pos.x = self.axes_H[self.column]
            self.discs[self.round].disc.setPos(pos)
            self.movement_H = False

        if self.round == 1 and self.button_changed == False:
            self.new_game_button["text"] = "Restart"
            self.button_changed = True

        return task.cont


    def check_victory(self):
        """
        Function that check if there is a victory case
        @return 1 if red wins and 2 if yellow wins
        """

        if self.round % 2 == 0:
            disc_type = 1
        else:
            disc_type = 2
        self.gridContent[7 * self.line + self.column] = disc_type

        for i in range(69):
            for j in range(4):
                if self.results[i][j] == 7 * self.line + self.column:
                    if (self.gridContent[int(self.results[i][0])] == disc_type) and (
                            self.gridContent[int(self.results[i][1])] == disc_type) and (
                            self.gridContent[int(self.results[i][2])] == disc_type) and (
                            self.gridContent[int(self.results[i][3])] == disc_type):
                        return disc_type
        return 0