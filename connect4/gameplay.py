# ----------------------------------------------------------------------
# @app    : Connect 4
# @author : Mustapha BENBRIKHO
# @date   : 14/08/2020
# ----------------------------------------------------------------------

from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectButton import DirectButton

import numpy as np
import csv


class Disc:
    """ Creation of a disc """

    def __init__(self, disc, color):
        """ Initialization of a disc """
        self.disc = disc
        self.color = color
        self.disc.setTexture(color)
        self.disc.setPos(0, 0, 6)
        self.disc.setScale(0.5, 0.5, 0.5)


def init_table(self):
    """ Load the table """
    print("Connect 4 > Load the table")
    self.table = self.loader.loadModel("connect4/models/table")
    self.table.reparentTo(self.render)
    self.table.setPos(0, 30, -8)
    self.table.setScale(2, 2, 2)
    self.table.setHpr(90, 0, 0)


def init_grid(self):
    """ Load the grid """
    print("Connect 4 > Load the grid")
    self.grid = self.loader.loadModel("connect4/models/grid")
    self.grid.reparentTo(self.render)
    self.grid.setColor(0.1, 0.2, 0.8, 1.0)
    self.grid.setHpr(90, 0, 0)
    self.grid.setScale(0.6, 0.6, 0.625)
    self.grid.setPos(3.6, 30, -6)
    self.gridContent = np.zeros(6*7)


# Keyboard inputs map
keyMap = {"left": False,"right": False,"down": False}


def updateKeyMap(key, state):
    """ Function that updates the input map """
    keyMap[key] = state


def init_keyboard(self):
    """ Management of keyboard inputs """
    print("Connect 4 > Load the keyboard handle")
    self.accept("arrow_left", updateKeyMap, ["left", True])
    self.accept("arrow_left-up", updateKeyMap, ["left", False])
    self.accept("arrow_right", updateKeyMap, ["right", True])
    self.accept("arrow_right-up", updateKeyMap, ["right", False])
    self.accept("arrow_down", updateKeyMap, ["down", True])
    self.accept("arrow_down-up", updateKeyMap, ["down", False])


def init_discs(self):
    """ Discs initialization """
    print("Connect 4 > Load the discs")
    self.red_texture = self.loader.loadTexture("connect4/tex/red_plastic.jpg")
    self.yellow_texture = self.loader.loadTexture("connect4/tex/yellow_plastic.jpg")
    self.discs = []
    for i in range(0, 44):
        self.disc = self.loader.loadModel("connect4/models/disc")
        self.disc.reparentTo(self.render)
        if i % 2 == 0:
            self.color_disc = Disc(self.disc, self.red_texture)
        else:
            self.color_disc = Disc(self.disc, self.yellow_texture)
        self.discs.append(self.color_disc)


def init_general_parameters(self):
    """ General parameters initialization """
    print("Connect 4 > Load general parameters (round, player ...)")
    self.round = 0
    self.player = 1
    self.speed = 40
    self.discs[self.round].disc.setPos(0, 30, 1.5)
    self.movement_V = False
    self.movement_H = False
    self.axes_H = [-3.6, -2.4, -1.2, 0, 1.2, 2.4, 3.6]
    self.axes_V = [0.25, -1.0, -2.25, -3.5, -4.75, -6]
    self.column = 3
    self.line = 5


def init_victory_cases(self):
    """ Read csv file cases """
    print("Connect 4 > Load the victory cases")
    self.results = []
    with open("connect4/csv/cases.csv") as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            self.results.append(row)


def init_victory_message(self):
    """ Victory text """
    print("Connect 4 > Load the victory message")
    font = self.loader.loadFont("connect4/font/Roboto-Medium.ttf")
    font.setPixelsPerUnit(60)
    self.text_victory = OnscreenText(text='', pos=(1.4, -0.8), scale=0.1)
    self.text_victory.setFg((0, 0, 0, 1))
    self.text_victory.setBg((1, 1, 1, 0))
    self.text_victory.setShadow((0.5, 0.5, 0.5, 1))


def init_audio(self):
    """ Sound Initialization """
    self.audio_coin = self.loader.loadMusic("connect4/audio/coin.ogg")


def init_load_button(self):
    """ Load button Initialization """
    print('Connect 4 > Load loading button ')

    def load_game():
        """ Load game functions used for load game button """
        print("Connect 4 > Load a game")
        f1 = open("connect4/safeguard/safeguard.txt", "r")
        last_line = f1.readlines()[-1]
        f1.close()
        last_line_list = last_line.split(',')
        k = 0
        p = 1
        round = 0
        for i in range(0, 42):
            col = i % 7
            line = i // 7
            if last_line_list[i] == '1':
                self.discs[k].disc.setPos(self.axes_H[col], 30, self.axes_V[line])
                k += 2
                round += 1
            elif last_line_list[i] == '2':
                self.discs[p].disc.setPos(self.axes_H[col], 30, self.axes_V[line])
                p += 2
                round += 1
        self.round = round
        self.discs[self.round].disc.setPos(0, 30, 1.5)
        self.gridContent = [int(j) for j in last_line_list]

    self.load_game_button = DirectButton(text="Load", pos=(-1.5, 0, 0.75), frameSize=(-3, 3, -0.5, 1), scale=.1, text_scale=0.9, command=load_game)


def init_new_button(self):
    """ New button Initialization """
    print("Connect 4 > Load new button ")

    def new_game():
        """ New game functions used for new game button """
        print("Connect 4 > New game")
        self.gridContent = np.zeros(6 * 7)
        for i in range(0, 44):
            self.discs[i].disc.setPos(0, 0, 1.5)
        self.round = 0
        self.discs[self.round].disc.setPos(0, 30, 1.5)
        self.text_victory.setText('')

    self.new_game_button = DirectButton(text="New game", pos=(-1.5, 0, 0.9), frameSize=(-3, 3, -0.5, 1), scale=.1,
                                        text_scale=0.9, command=new_game)
    self.button_changed = False


def init_save_button(self):
    """ New game functions used for new game button """
    print("Connect 4 > Load save button ")

    def save_game():
        """ Save game functions used for save game button """
        print("Connect 4 > Save the game")
        grid = [int(j) for j in self.gridContent]
        grid_content_str = ','.join([str(elem) for elem in grid])
        f = open("connect4/safeguard/safeguard.txt", "a")
        f.write(grid_content_str + "\n")
        f.close()

    self.save_game_button = DirectButton(text="Save", pos=(-1.5, 0, 0.60), frameSize=(-3, 3, -0.5, 1), scale=.1, text_scale=0.9, command=save_game)


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


def init(base):
    """ Initialization of the connect 4"""
    print('Connect 4 > Initialization')
    init_table(base)
    init_grid(base)
    init_keyboard(base)
    init_discs(base)
    init_general_parameters(base)
    init_victory_cases(base)
    init_victory_message(base)
    init_audio(base)
    init_load_button(base)
    init_new_button(base)
    init_save_button(base)


def mainloop(base):
    """ Main loop of the connect 4 game """

    # Get the clock
    dt = globalClock.getDt()

    # Get the position of the current disc
    pos = base.discs[base.round].disc.getPos()

    # Left click
    if keyMap["left"] and base.column != 0 and not base.movement_V:
        keyMap["left"] = False
        base.column -= 1
        base.movement_H = True

    # Right click
    if keyMap["right"] and base.column != 6 and not base.movement_V:
        keyMap["right"] = False
        base.column += 1
        base.movement_H = True

    # down clic
    if keyMap["down"] and base.gridContent[base.column] == 0 and not base.movement_V:
        # To have only one click
        keyMap["down"] = False

        # Find the position
        line_fixed = 0
        base.line = 5
        while line_fixed == 0 and base.line >= 0:
            if base.gridContent[7 * base.line + base.column] != 0:
                base.line -= 1
            else:
                line_fixed = 1
        base.movement_V = True

        # check if there is a victory or not
        victory = check_victory(base)
        if victory == 1:
            base.text_victory.setText('Red wins')
        if victory == 2:
            base.text_victory.setText('Yellow wins')

    # Progressive vertical movement
    if base.movement_V and pos.z != base.axes_V[base.line]:
        pos.z -= 0.25
        base.discs[base.round].disc.setPos(pos)

    # Set the disc position / Prepare next disc
    if base.movement_V and pos.z == base.axes_V[base.line]:
        base.audio_coin.play()
        base.movement_V = False
        base.line = 0
        base.column = 3
        base.round += 1
        base.discs[base.round].disc.setPos(0, 30, 1.5)

    # Horizontal movement
    if base.movement_H:
        pos.x = base.axes_H[base.column]
        base.discs[base.round].disc.setPos(pos)
        base.movement_H = False

    # Change the button "New game" to "Restart" for the first round
    if base.round == 1 and base.button_changed == False:
        base.new_game_button["text"] = "Restart"
        base.button_changed = True
        print("Connect 4 > Main loop")