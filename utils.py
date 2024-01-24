from ursina import *
import os


class Block:
    def __init__(self, material, pos, solid):
        self.material = material
        self.pos = pos
        self.solid = solid
        self.texture = str(f"assets/textures/{material}.png")
        self.collider = None
        if not os.path.exists(self.texture):
            self.texture = "assets/missing.png"
        if bool(solid):
            self.collider = "box"
        self.box = Entity(model="cube", texture=load_texture(self.texture), position=pos, collider=self.collider)
