# ----------------------------------------------------------------------
# @app    : Main program
# @author : Mustapha BENBRIKHO
# @date   : 14/08/2020
# ----------------------------------------------------------------------

from connect4.gameplay import Connect4

from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import loadPrcFile
from panda3d.core import TransparencyAttrib
from direct.gui.DirectButton import DirectButton


# Load the general settings files
loadPrcFile("config/Confinit.prc")
loadPrcFile("config/Config.prc")
loadPrcFile("config/Confauto.prc")


class Main(ShowBase):
    def __init__(self):
        """ Initialization of the connect 4"""
        print('General > Initialization')
        super().__init__()

        # General settings
        # self.disable_mouse()

        # Load the background
        self.background = OnscreenImage(parent=self.render2dp, image="tex/bedroom.jpg")
        self.cam2dp.node().getDisplayRegion(0).setSort(-20)

        # Load the avatar
        self.arm = Actor("models/Tatsumi_models/Tatsumi_1", {"anim1": "models/Tatsumi_models/Tatsumi_1_anim"})
        self.arm.setPos(0, 50, -36)
        self.arm.setScale(20, 20, 20)
        self.arm.reparentTo(self.render)
        self.arm.setPlayRate(4, "anim1")
        self.arm.play("anim1")

        # Load the buttons
        self.icon_connect4 = DirectButton(image="img/connect4.png", pos=(-1.5, 0, -0.8), scale=(0.2, 0.2, 0.2),
                                          relief=None, command=self.run_connect4)
        self.icon_connect4.setTransparency(TransparencyAttrib.MAlpha)

        self.games = []

    def run_connect4(self):
        """ Function that initializers the connect4 game """
        print("General > Run the Connect 4")
        self.hide_elements()
        connect4 = Connect4(self)
        self.games.append(connect4)
        self.taskMgr.add(self.loop, "loop")

    def show_elements(self):
        """ Function that shows the elements of the initial display """
        self.games = []
        self.icon_connect4.show()

    def hide_elements(self):
        """ Function that hides the elements of the initial display """
        self.icon_connect4.hide()

    def loop(self, task):
        """ Function that runs the connect4 game """
        if self.games[0].mainloop() == 0:
            self.show_elements()
            return task.done
        else:
            return task.cont


env = Main()
env.run()
