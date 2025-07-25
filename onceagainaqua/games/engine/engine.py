from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import WindowProperties
import sys

class VoxelGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable default camera control
        self.disableMouse()

        # Set background color (sky blue)
        self.setBackgroundColor(0.5, 0.8, 1.0)

        # Create a simple voxel ground (10x10 blocks)
        self.create_ground()

        # Camera settings
        self.camera.setPos(5, -20, 3)
        self.camLens.setFov(90)

        # Mouse look
        self.accept("escape", sys.exit)
        self.props = WindowProperties()
        self.props.setCursorHidden(True)
        self.win.requestProperties(self.props)
        self.center_mouse()

        self.accept("w", self.set_key, ["forward", True])
        self.accept("w-up", self.set_key, ["forward", False])
        self.accept("s", self.set_key, ["backward", True])
        self.accept("s-up", self.set_key, ["backward", False])
        self.accept("a", self.set_key, ["left", True])
        self.accept("a-up", self.set_key, ["left", False])
        self.accept("d", self.set_key, ["right", True])
        self.accept("d-up", self.set_key, ["right", False])

        self.keys = {"forward": False, "backward": False, "left": False, "right": False}
        self.taskMgr.add(self.update, "update")

    def create_ground(self):
        cm = CardMaker("ground")
        cm.setFrame(-0.5, 0.5, -0.5, 0.5)
        for x in range(10):
            for y in range(10):
                tile = self.render.attachNewNode(cm.generate())
                tile.setPos(x, y, 0)
                tile.setHpr(0, -90, 0)
                tile.setColor(0.2, 0.8, 0.2, 1)  # Green

    def set_key(self, key, value):
        self.keys[key] = value

    def center_mouse(self):
        self.win.movePointer(0, int(self.win.getXSize() / 2), int(self.win.getYSize() / 2))

    def update(self, task):
        dt = globalClock.getDt()
        speed = 5

        # Mouse look
        if self.mouseWatcherNode.hasMouse():
            md = self.win.getPointer(0)
            x = md.getX()
            y = md.getY()
            self.camera.setH(self.camera.getH() - (x - self.win.getXSize() / 2) * 0.1)
            self.camera.setP(self.camera.getP() - (y - self.win.getYSize() / 2) * 0.1)
            self.center_mouse()

        # Movement
        direction = Vec3(0, 0, 0)
        if self.keys["forward"]:
            direction.y += 1
        if self.keys["backward"]:
            direction.y -= 1
        if self.keys["left"]:
            direction.x -= 1
        if self.keys["right"]:
            direction.x += 1

        direction.normalize()
        self.camera.setPos(self.camera, direction * speed * dt)

        return Task.cont

app = VoxelGame()
app.run()
