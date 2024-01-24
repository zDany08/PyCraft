from ursina.prefabs.first_person_controller import FirstPersonController
from utils import *

app = Ursina(title="PyCraft", icon="assets/icon.ico", borderless=False, fullscreen=True)
window.fps_counter.disable()
window.collider_counter.disable()
window.entity_counter.disable()
window.exit_button.hide()
Sky(color=color.cyan)
player = FirstPersonController(position=(0, 8, 0))
player.gravity = 0.3
exit_text = Text(text="Press \"ALT + F4\" to exit.", x=-0.89, y=0.49)
blocks = list()
placeable_materials = ["grass", "dirt", "stone", "bricks", "glass", "wood", "tnt"]
selected_material = placeable_materials[0]


def update():
    if player.position[1] <= -64:
        exit()
    for block in blocks:
        if block.box.hovered:
            block.box.color = color.tint(color.rgb(80, 80, 80))
        else:
            if block.box.color == color.tint(color.rgb(80, 80, 80)):
                block.box.color = color.tint(color.rgb(255, 255, 255))


def input(key):
    global selected_material
    match key:
        case Keys.left_shift:
            index = placeable_materials.index(selected_material)
            if index == len(placeable_materials) - 1:
                selected_material = placeable_materials[0]
            else:
                selected_material = placeable_materials[index + 1]
        case _:
            pass
    for block in blocks:
        if block.box.hovered:
            match key:
                case Keys.left_mouse_down:
                    if not block.material == "bedrock":
                        blocks.remove(block)
                        destroy(block.box)
                        # invoke(Audio, "assets/sounds/break.ogg", delay=0)
                case Keys.right_mouse_down:
                    block = Block(selected_material, block.box.position + mouse.normal, True)
                    if block.material == "tnt":
                        invoke(Func(explode, block), delay=3)
                    else:
                        blocks.append(block)
                    # invoke(Audio, "assets/sounds/place.ogg", delay=0)
                case _:
                    pass


def explode(tnt):
    for x in range(int(tnt.box.position[0] - 1), int(tnt.box.position[0] + 2)):
        for y in range(int(tnt.box.position[1] - 1), int(tnt.box.position[1] + 2)):
            for z in range(int(tnt.box.position[2] - 1), int(tnt.box.position[2] + 2)):
                for l_block in blocks:
                    if l_block.box.position == (x, y, z) and not l_block.material == "bedrock":
                        destroy(l_block.box)
                        blocks.remove(l_block)
    destroy(tnt.box)


def generate_chunk(px, py, pz):
    for x in range(px, px + 8):
        for y in range(py, py + 8):
            for z in range(pz, pz + 8):
                material = ""
                if y == 7:
                    material = "grass"
                elif 8 > y > 3:
                    material = "dirt"
                elif y == 0:
                    material = "bedrock"
                else:
                    material = "stone"
                blocks.append(Block(material, (x, y, z), True))


generate_chunk(0, 0, 0)
app.run()
