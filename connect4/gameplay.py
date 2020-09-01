from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectButton import DirectButton
import numpy as np
import csv

# Disc of the connect4
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




def init(base):
    """ Initialization of the connect 4"""

    print('Connect 4 > Initialization')

    # Load the table
    base.table = base.loader.loadModel("connect4/models/table")
    base.table.reparentTo(base.render)
    base.table.setPos(0, 30, -8)
    base.table.setScale(2, 2, 2)
    base.table.setHpr(90, 0, 0)

    # Load the grid
    base.grid = base.loader.loadModel("connect4/models/grid")
    base.grid.reparentTo(base.render)
    base.blue_grid = base.loader.loadTexture("connect4/tex/blue_plastic.jpg")
    base.grid.setTexture(base.blue_grid)
    base.grid.setHpr(90, 0, 0)
    base.grid.setScale(0.6, 0.6, 0.6)
    base.grid.setPos(0, 30, -6.5)

    # Inputs management
    base.accept("arrow_left", updateKeyMap, ["left", True])
    base.accept("arrow_left-up", updateKeyMap, ["left", False])
    base.accept("arrow_right", updateKeyMap, ["right", True])
    base.accept("arrow_right-up", updateKeyMap, ["right", False])
    base.accept("arrow_down", updateKeyMap, ["down", True])
    base.accept("arrow_down-up", updateKeyMap, ["down", False])

    # General settings
    # self.disable_mouse()

    # Discs initialization
    base.red_texture = base.loader.loadTexture("connect4/tex/red_plastic.jpg")
    base.yellow_texture = base.loader.loadTexture("connect4/tex/yellow_plastic.jpg")
    base.discs = []
    for i in range(0, 44):
        base.disc = base.loader.loadModel("connect4/models/disc")
        base.disc.reparentTo(base.render)
        if i % 2 == 0:
            base.color_disc = Disc(base.disc, base.red_texture)
        else:
            base.color_disc = Disc(base.disc, base.yellow_texture)
        base.discs.append(base.color_disc)

    # Other parameters initialization
    base.round = 0
    base.player = 1
    base.speed = 40
    base.discs[base.round].disc.setPos(0, 30, 1.5)
    base.movement_V = False
    base.movement_H = False

    base.axes_H = [-3.6, -2.4, -1.2, 0, 1.2, 2.4, 3.6]
    base.axes_V = [0.25, -1.0, -2.25, -3.5, -4.75, -6]
    base.column = 3
    base.line = 5

    # Grid content
    base.gridContent = np.zeros(6*7)

    # Read csv file cases
    base.results = []
    with open("connect4/csv/cases.csv") as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            base.results.append(row)

    # Victory text
    font = base.loader.loadFont("connect4/font/Roboto-Medium.ttf")
    font.setPixelsPerUnit(60)
    base.text_victory = OnscreenText(text='', pos=(1.4, -0.8), scale=0.1)
    base.text_victory.setFg((0, 0, 0, 1))
    base.text_victory.setBg((1, 1, 1, 0))
    base.text_victory.setShadow((0.5, 0.5, 0.5, 1))

    # Sound Initialization
    base.audio_coin = base.loader.loadMusic("connect4/audio/coin.ogg")


    # Button load game
    def load_game():
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
                base.discs[k].disc.setPos(base.axes_H[col], 30, base.axes_V[line])
                k += 2
                round += 1
            elif last_line_list[i] == '2':
                base.discs[p].disc.setPos(base.axes_H[col], 30, base.axes_V[line])
                p += 2
                round += 1
        base.round = round
        base.discs[base.round].disc.setPos(0, 30, 1.5)
        base.gridContent = [int(j) for j in last_line_list]

    # Button new game
    def new_game():
        print("Connect 4 > New game")
        base.gridContent = np.zeros(6 * 7)
        for i in range(0, 44):
            base.discs[i].disc.setPos(0, 0, 1.5)
        base.round = 0
        base.discs[base.round].disc.setPos(0, 30, 1.5)
        base.text_victory.setText('')

    # Button save game
    def save_game():
        print("Connect 4 > Save the game")
        grid = [int(j) for j in base.gridContent]
        grid_content_str = ','.join([str(elem) for elem in grid])
        f = open("connect4/safeguard/safeguard.txt", "a")
        f.write(grid_content_str + "\n")
        f.close()

    # Button 1
    base.new_game_button = DirectButton(text="New game", pos=(-1.5, 0, 0.9), frameSize=(-3, 3, -0.5, 1),
                                   scale=.1, text_scale=0.9, command=new_game)

    # Button 2
    base.load_game_button = DirectButton(text="Load", pos=(-1.5, 0, 0.75), frameSize=(-3, 3, -0.5, 1),
                     scale=.1, text_scale=0.9, command=load_game)

    # Button 2
    base.load_game_button = DirectButton(text="Save", pos=(-1.5, 0, 0.60), frameSize=(-3, 3, -0.5, 1),
                     scale=.1, text_scale=0.9, command=save_game)
    base.button_changed = False




def mainloop(base):
    """ Main loop of the connect 4 game """


    dt = globalClock.getDt()

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
    print(base.gridContent)
    print(base.column)
    if keyMap["down"] and base.gridContent[base.column] == 0 and not base.movement_V:
        print("Down click")
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

    if base.round == 1 and base.button_changed == False:
        base.new_game_button["text"] = "Restart"
        base.button_changed = True
        print("Connect 4 > Main loop")




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

