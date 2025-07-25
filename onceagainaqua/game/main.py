from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, GeoMipTerrain, TextureStage
from panda3d.core import Filename
import random

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.accept("escape", exit)
        self.disableMouse()

        # Player setup
        self.player = self.camera
        self.player.setPos(0, 0, 10)
        self.speed = 10
        self.key_map = {"forward": False, "backward": False, "left": False, "right": False}
        self.accept("w", self.set_key, ["forward", True])
        self.accept("w-up", self.set_key, ["forward", False])
        self.accept("s", self.set_key, ["backward", True])
        self.accept("s-up", self.set_key, ["backward", False])
        self.accept("a", self.set_key, ["left", True])
        self.accept("a-up", self.set_key, ["left", False])
        self.accept("d", self.set_key, ["right", True])
        self.accept("d-up", self.set_key, ["right", False])

        # Terrain & sky
        self.chunks = {}
        self.chunk_size = 128
        self.load_chunks_around_player()
        self.load_skybox()

        self.taskMgr.add(self.update, "update")

    def set_key(self, key, value):
        self.key_map[key] = value

    def update(self, task):
        dt = globalClock.getDt()
        move_vec = Vec3(0, 0, 0)

        if self.key_map["forward"]: move_vec.y += self.speed * dt
        if self.key_map["backward"]: move_vec.y -= self.speed * dt
        if self.key_map["left"]: move_vec.x -= self.speed * dt
        if self.key_map["right"]: move_vec.x += self.speed * dt

        self.player.setPos(self.player.getPos() + move_vec)

        self.skybox.setPos(self.player.getPos())
        self.load_chunks_around_player()

        return task.cont

    def generate_chunk(self, x_offset, y_offset):
        terrain = GeoMipTerrain(f"chunk_{x_offset}_{y_offset}")
        terrain.setHeightfield(Filename("textures/noise.png"))  # Use a procedural or dummy heightmap
        terrain.setBlockSize(32)
        terrain.setNear(40)
        terrain.setFar(100)
        terrain.setFocalPoint(self.camera)
        terrain_root = terrain.getRoot()
        terrain_root.setPos(x_offset * self.chunk_size, y_offset * self.chunk_size, 0)
        terrain_root.reparentTo(render)
        terrain.generate()
        return terrain

    def load_chunks_around_player(self):
        px = int(self.player.getX() / self.chunk_size)
        py = int(self.player.getY() / self.chunk_size)

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                cx, cy = px + dx, py + dy
                key = (cx, cy)
                if key not in self.chunks:
                    self.chunks[key] = self.generate_chunk(cx, cy)

    def load_skybox(self):
        self.skybox = loader.loadModel("models/skybox.egg")
        tex = loader.loadTexture("textures/blue_sky.jpg")
        self.skybox.setTexture(tex, 1)
        self.skybox.setScale(500)
        self.skybox.reparentTo(render)

game = Game()
game.run()