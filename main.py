# Rubix cube game in Python using Ursina engine

# Author: Light

# =================================

from ursina import *


# =================================


class Game(Ursina):
    def __init__(self):
        super().__init__()

        # -------------------------

        self.PARENT = None
        self.CUBES = None
        self.rotation_axes = None
        self.cubes_side_positions = None
        self.animation_time = None
        self.action_trigger = None

        self.LEFT = None
        self.BOTTOM = None
        self.TOP = None
        self.BACK = None
        self.RIGHT = None
        self.FACE = None
        self.SIDE_POSITIONS = None

        self.action_mode = None
        self.message = None

        self.LEFT_sensor = None
        self.RIGHT_sensor = None
        self.TOP_sensor = None
        self.BOTTOM_sensor = None
        self.BACK_sensor = None
        self.FACE_sensor = None

        # -------------------------

        window.fullscreen = True

        # Creating plane
        Entity(model='quad', scale=100, texture='white_cube', texture_scale=(100, 100),
               rotation_x=90, y=-5, color=color.light_gray)

        # Creating Sky sphere for superimposing sky texture
        Entity(model='sphere', scale=100, texture='textures/sky0', double_sided=True)

        # Mouse Controlled Camera
        EditorCamera()
        camera.world_position = (0, 0, -15)

        self.model, self.texture = 'models/custom_cube', 'textures/rubik_texture'
        self.load_game()

    def load_game(self):
        self.create_cube_positions()
        self.CUBES = [Entity(model=self.model, texture=self.texture, position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()

        self.rotation_axes = {'LEFT': 'x', 'RIGHT': 'x', 'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z'}
        self.cubes_side_positions = {'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM, 'RIGHT': self.RIGHT, 'TOP': self.TOP,
                                     'BACK': self.BACK, 'FACE': self.FACE}

        self.animation_time = 0.1

        # Trigger to allow next turn of a side
        self.action_trigger = True

        # -----------------------------------------

        # Switching between view mode and action mode

        self.action_mode = True
        self.message = Text(origin=(0, 9), color=color.black)
        self.toggle_game_mode()
        self.create_sensors()

    def create_sensors(self):
        create_sensor = lambda name, pos, scale: Entity(name=name, position=pos, model='cube', color=color.dark_gray,
                                                        scale=scale, collider='box', visible=False)

        self.LEFT_sensor = create_sensor(name='LEFT', pos=(-0.99, 0, 0), scale=(1.01, 3.01, 3.01))
        self.RIGHT_sensor = create_sensor(name='RIGHT', pos=(0.99, 0, 0), scale=(1.01, 3.01, 3.01))
        self.TOP_sensor = create_sensor(name='TOP', pos=(0, 1, 0), scale=(3.01, 1.01, 3.01))
        self.BOTTOM_sensor = create_sensor(name='BOTTOM', pos=(0, -1, 0), scale=(3.01, 1.01, 3.01))
        self.BACK_sensor = create_sensor(name='BACK', pos=(0, 0, 0.99), scale=(3.01, 3.01, 1.01))
        self.FACE_sensor = create_sensor(name='FACE', pos=(0, 0, -0.99), scale=(3.01, 3.01, 1.01))

    def toggle_game_mode(self):
        self.action_mode = not self.action_mode
        self.message.text = dedent(f"{'ACTION mode ON' if self.action_mode else 'VIEW mode ON'}"
                                   f" (press middle mouse button to switch mode)"
                                   f"\nWhile in action mode press the Right mouse button to rotate top and bottom faces"
                                   f" and the Left mouse button to rotate the rest.").strip()

    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger

    # Method to rotate the side of cube
    def rotate_side(self, side_name):
        self.action_trigger = False
        cube_positions = self.cubes_side_positions[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.re_parent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                eval(f'self.PARENT.animate_rotation_{rotation_axis}(90, duration=self.animation_time)')
        invoke(self.toggle_animation_trigger, delay=self.animation_time * 0.11)

    def re_parent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot

        self.PARENT.rotation = 0

    def create_cube_positions(self):
        self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.BOTTOM = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.FACE = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
        self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
        self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.TOP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.SIDE_POSITIONS = self.LEFT | self.BOTTOM | self.TOP | self.RIGHT | self.BACK | self.FACE

    def input(self, key, is_raw=False):
        if key in 'mouse1 mouse3' and self.action_mode and self.action_trigger:
            for hitinfo in mouse.collisions:
                collider_name = hitinfo.entity.name
                if (key == 'mouse1' and collider_name in 'LEFT RIGHT FACE BACK' or
                        key == 'mouse3' and collider_name in 'TOP BOTTOM'):
                    self.rotate_side(collider_name)
                    break

        if key == 'mouse2':
            self.toggle_game_mode()

        super().input(key)


# =================================


if __name__ == '__main__':
    game = Game()
    game.run()

# =========== END OF PROGRAM ==============
