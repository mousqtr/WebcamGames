# ----------------------------------------------------------------------
# Connect 4
# @author : Mustapha BENBRIKHO
# ----------------------------------------------------------------------

from connect4.gameplay import init
from connect4.gameplay import mainloop

from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import loadPrcFile
from direct.gui.DirectButton import DirectButton

loadPrcFile("config/Confinit.prc")
loadPrcFile("config/Config.prc")
loadPrcFile("config/Confauto.prc")


class Main(ShowBase):
    def __init__(self):
        """ Initialization of the connect 4"""
        print('General > Initialization')
        super().__init__()

        self.background = OnscreenImage(parent=self.render2dp, image="tex/bedroom.jpg") # Load an image object
        self.cam2dp.node().getDisplayRegion(0).setSort(-20)

        # Load the avatar
        self.arm = Actor("models/Tatsumi_models/Tatsumi_1", {"anim1": "models/Tatsumi_models/Tatsumi_1_anim"})
        self.arm.setPos(0, 50, -36)
        self.arm.setScale(20, 20, 20)
        self.arm.reparentTo(self.render)
        self.arm.play("anim1")

        # Button
        def run_connect4():
            init(self)
            self.taskMgr.add(self.loop, "loop")


        self.new_game_button = DirectButton(text="Connect 4", pos=(-1.5, 0, 0.9), frameSize=(-3, 3, -0.5, 1),
                                        scale=.1, text_scale=0.9, command=run_connect4)

    def loop(self, task):
        mainloop(self)
        return task.cont


        # run the game
        #loop(self)



# game = Connect4()
# game.run()

env = Main()
env.run()
