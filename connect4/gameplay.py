# ----------------------------------------------------------------------
# @app    : Connect 4
# @author : Mustapha BENBRIKHO
# @date   : 14/08/2020
# ----------------------------------------------------------------------

from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectButton import DirectButton
from direct.interval.IntervalGlobal import Parallel, Sequence
from panda3d.core import Point3

import numpy as np
import csv

import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

class Disc:
    """ Creation of a disc """

    def __init__(self, id, disc, r, g, b):
        """ Initialization of a disc """
        self.id = id
        self.disc = disc
        self.disc.setColor(r, g, b, 1.0)
        self.disc.setPos(0, 0, 6)
        self.disc.setScale(0.5, 0.5, 0.5)


class Connect4:
    def __init__(self, p_base):

        self.base = p_base
        self.render = p_base.render

        # Keyboard inputs map
        self.keyMap = {"left": False, "right": False, "down": False, "drop": False}

        # Global parameters
        self.player = 1
        self.speed = 15
        self.movement_V = False
        self.movement_H = False
        self.axes_H = [-3.6, -2.4, -1.2, 0, 1.2, 2.4, 3.6]
        self.axes_V = [0.25, -1.0, -2.25, -3.5, -4.75, -6]
        self.column = 3
        self.line = 5
        self.quit_game_bool = False
        self.round = 0

        # Initialization of audio coin
        self.audio_coin = self.base.loader.loadMusic("connect4/audio/coin.ogg")

        # Initialization of the table
        self.table = self.base.loader.loadModel("connect4/models/table")
        self.table.reparentTo(self.render)
        self.table.setScale(2, 2, 2)
        self.table.setHpr(90, 0, 0)
        self.table_anim_start = self.table.posInterval(3, Point3(0, 30, -8), startPos=Point3(0, 0, -8))
        self.table_anim_end = self.table.posInterval(3, Point3(0, 0, -8), startPos=Point3(0, 30, -8))

        # Initialization of the grid
        self.grid = self.base.loader.loadModel("connect4/models/grid")
        self.grid.reparentTo(self.render)
        self.grid.setColor(0.1, 0.2, 0.8, 1.0)
        self.grid.setHpr(90, 0, 0)
        self.grid.setScale(0.6, 0.6, 0.625)
        self.grid_anim_start = self.grid.posInterval(3, Point3(3.6, 30, -6), startPos=Point3(3.6, 30, 0))
        self.grid_anim_end = self.grid.posInterval(3, Point3(3.6, 30, 0), startPos=Point3(3.6, 30, -6))
        self.gridContent = np.zeros(6 * 7)

        # Initialization of the discs
        self.discs = []
        self.nb_discs = 44
        for i in range(0, self.nb_discs):
            disc = self.base.loader.loadModel("connect4/models/disc")
            disc.reparentTo(self.render)
            if i % 2 == 0:
                color_disc = Disc(i, disc, 1.0, 0.0, 0.0)
            else:
                color_disc = Disc(i, disc, 1.0, 1.0, 0.0)
            self.discs.append(color_disc)
        self.first_disc_anim = self.discs[self.round].disc.posInterval(3, Point3(0, 30, 1.5), startPos=Point3(0, 0, 8))

        # Initialization of start sequences
        self.init_sequence = Parallel(self.table_anim_start, self.grid_anim_start, self.first_disc_anim, name="p_start")
        self.init_sequence.start()

        # Initialization of keys
        self.base.accept("arrow_left", self.updateKeyMap, ["left", True])
        self.base.accept("arrow_left-up", self.updateKeyMap, ["left", False])
        self.base.accept("arrow_right", self.updateKeyMap, ["right", True])
        self.base.accept("arrow_right-up", self.updateKeyMap, ["right", False])
        self.base.accept("arrow_down", self.updateKeyMap, ["down", True])
        self.base.accept("arrow_down-up", self.updateKeyMap, ["down", False])
        self.base.accept("space", self.updateKeyMap, ["drop", True])
        self.base.accept("space-up", self.updateKeyMap, ["drop", False])

        # Initialization of winning cases
        self.results = []
        with open("connect4/csv/cases.csv") as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                self.results.append(row)

        # Initialization of fonts
        self.font = self.base.loader.loadFont("connect4/font/Roboto-Medium.ttf")
        self.font.setPixelsPerUnit(60)

        # Initialization of the victory text
        self.text_victory = OnscreenText(text='', pos=(1.4, -0.8), scale=0.1)
        self.text_victory.setFg((0, 0, 0, 1))
        self.text_victory.setBg((1, 1, 1, 0))
        self.text_victory.setShadow((0.5, 0.5, 0.5, 1))

        # Initialization of buttons
        self.load_game_button = DirectButton(text="Load", pos=(-1.5, 0, 0.75), frameSize=(-3, 3, -0.5, 1), scale=.1,
                                             text_scale=0.9, command=self.load_game)

        self.new_game_button = DirectButton(text="New game", pos=(-1.5, 0, 0.9), frameSize=(-3, 3, -0.5, 1), scale=.1,
                                            text_scale=0.9, command=self.new_game)
        self.button_changed = False

        self.save_game_button = DirectButton(text="Save", pos=(-1.5, 0, 0.6), frameSize=(-3, 3, -0.5, 1), scale=.1,
                                             text_scale=0.9, command=self.save_game)

        self.quit_game_button = DirectButton(text="Quit", pos=(-1.5, 0, -0.95), frameSize=(-3, 3, -0.5, 1), scale=.1,
                                             text_scale=0.9, command=self.quit_game)

        self.hand_control_button = DirectButton(text="Activer le contrôle \n visuel", pos=(1.5, 0, -0.9), frameSize=(-3, 3, -1, 0.8), scale=.1,
                                             text_scale=0.5, command=self.activate_hand_control)
        # Mode
        # (mode 0 : default mode)
        # (mode 1 : hand control mode)
        self.mode = 0

        self.disc_caught = -1

        # Initialization of the right hand
        self.right_hand = self.base.loader.loadModel("connect4/models/hand")
        self.right_hand.reparentTo(self.render)
        self.right_hand.setPos(3.6, -20, 0)
        self.right_hand.setColor(0.88, 0.67, 0.41, 1.0)
        self.right_hand.setHpr(90, -90, 0)
        self.right_hand.setScale(0.2, 0.2, 0.2)

        # self.left_hand = self.base.loader.loadModel("connect4/models/hand")
        # self.left_hand.reparentTo(self.render)
        # self.left_hand.setPos(-3.6, -20, 0)
        # self.left_hand.setColor(0.88, 0.67, 0.41, 1.0)
        # self.left_hand.setHpr(90, -90, 180)
        # self.left_hand.setScale(0.2, 0.2, 0.2)

    def activate_hand_control(self):
        if self.mode == 0:
            self.mode = 1
            self.hand_control_button.setText("Désactiver le contrôle \n visuel")
            self.right_hand.setPos(3.6, 30, 0)
            self.new_game()
            # self.left_hand.setPos(-3.6, 20, 0)
        else:
            self.mode = 0
            self.hand_control_button.setText("Activer le contrôle \n visuel")
            self.right_hand.setPos(3.6, -20, 0)
            # self.left_hand.setPos(-3.6, -20, 0)

    def updateKeyMap(self, key, state):
        """ Function that updates the input map """
        self.keyMap[key] = state

    def load_game(self):
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

    def new_game(self):
        """ New game functions used for new game button """
        print("Connect 4 > New game")

        self.gridContent = np.zeros(6 * 7)
        self.round = 0
        self.text_victory.setText('')

        if self.mode == 0:
            for i in range(0, 42):
                self.discs[i].disc.setPos(100, 100, 100)
            self.discs[self.round].disc.setPos(0, 30, 1.5)

        elif self.mode == 1:
            pos_xr = [-8.4, -7.2, -6.0,
                      -12, -10.8, -9.6, -8.4, -7.2, -6.0,
                      -12, -10.8, -9.6, -8.4, -7.2, -6.0,
                      -12, -10.8, -9.6, -8.4, -7.2, -6.0]
            pos_xy = [8.4, 7.2, 6.0,
                      12, 10.8, 9.6, 8.4, 7.2, 6.0,
                      12, 10.8, 9.6, 8.4, 7.2, 6.0,
                      12, 10.8, 9.6, 8.4, 7.2, 6.0]
            pos_z = [-6.4, -6.4, -6.4,
                     -5.2, -5.2, -5.2, -5.2, -5.2, -5.2,
                     -4.0, -4.0, -4.0, -4.0, -4.0, -4.0,
                     -2.8, -2.8, -2.8, -2.8, -2.8, -2.8]
            n = 0
            p = 0
            for i in range(0, 42):
                if i % 2 == 0:
                    self.discs[i].disc.setPos(pos_xr[n], 30, pos_z[n])
                    n += 1
                else:
                    self.discs[i].disc.setPos(pos_xy[p], 30, pos_z[p])
                    p += 1

    def save_game(self):
        """ Save game functions used for save game button """
        print("Connect 4 > Save the game")
        grid = [int(j) for j in self.gridContent]
        grid_content_str = ','.join([str(elem) for elem in grid])
        f = open("connect4/safeguard/safeguard.txt", "a")
        f.write(grid_content_str + "\n")
        f.close()

    def quit_game(self):
        """ Quit game functions used for quit game button """
        print("Connect 4 > Quit the game")
        for i in range(0, self.nb_discs):
            self.discs[i].disc.removeNode()
        self.grid.removeNode()
        self.table.removeNode()
        self.new_game_button.destroy()
        self.save_game_button.destroy()
        self.load_game_button.destroy()
        self.quit_game_button.destroy()
        self.quit_game_bool = True

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

    def mainloop(self):
        """ Main loop of the connect 4 game """

        # If quit_button is clicked
        if self.quit_game_bool:
            return 0

        # Get the clock
        dt = globalClock.getDt()

        # Change the button "New game" to "Restart" for the first round
        if self.round == 1 and self.button_changed == False:
            self.new_game_button["text"] = "Restart"
            self.button_changed = True
            print("Connect 4 > Main loop")

        # Get the position of the current disc
        pos = self.discs[self.round].disc.getPos()

        if self.mode == 0:
            # Left click
            if self.keyMap["left"] and self.column != 0 and not self.movement_V:
                self.keyMap["left"] = False
                self.column -= 1
                self.movement_H = True

            # Right click
            if self.keyMap["right"] and self.column != 6 and not self.movement_V:
                self.keyMap["right"] = False
                self.column += 1
                self.movement_H = True

            # down clic
            if self.keyMap["down"] and self.gridContent[self.column] == 0 and not self.movement_V:
                # To have only one click
                self.keyMap["down"] = False

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
            if self.movement_V and pos.z >= self.axes_V[self.line]:
                pos.z -= self.speed * dt
                self.discs[self.round].disc.setPos(pos)

            # Set the disc position / Prepare next disc
            if self.movement_V and pos.z <= self.axes_V[self.line]:
                pos.z = self.axes_V[self.line]
                self.discs[self.round].disc.setPos(pos)
                self.audio_coin.play()
                self.movement_V = False
                self.line = 0
                self.column = 3
                self.round += 1
                if self.round < 42:
                    self.discs[self.round].disc.setPos(0, 30, 1.5)

            # Horizontal movement
            if self.movement_H:
                pos.x = self.axes_H[self.column]
                self.discs[self.round].disc.setPos(pos)
                self.movement_H = False

        # Detect hand position
        if cap.isOpened() and self.mode == 1:
            success, image = cap.read()

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            image.flags.writeable = False
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for idx, landmark in enumerate(hand_landmarks.landmark):
                        if idx == 9:
                            x = 24 * landmark.x - 12
                            z = - 14 * landmark.y + 7
                            self.right_hand.setPos(x, 30, z)

                            if self.disc_caught == -1:
                                for i in range(0, 42):
                                    if (abs(self.right_hand.getPos().x - 0.5 - self.discs[i].disc.getPos().x) < 0.5) \
                                            and abs(self.right_hand.getPos().z - self.discs[i].disc.getPos().z) < 0.5:
                                        print(self.discs[i].id)
                                        self.disc_caught = self.discs[i].id
                                        self.discs[self.disc_caught].disc.setPos(x - 0.5, 30, z + 0.5)
                            else:
                                self.discs[self.disc_caught].disc.setPos(x - 0.5, 30, z + 0.5)

                            if self.keyMap["drop"]:
                                self.keyMap["drop"] = False
                            # self.discs[self.round].disc.setPos(x - 0.5, 30, z + 0.5)


        return 1
