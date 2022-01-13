class Render:
    # set the size of the window
    def set_window_size(self, width: int, height: int):
        return

    # initialize the GL state
    def init_gl(self):
        return

    # free all GL resources
    def uninit_gl(self):
        return

    # update camera parameters and object orientation
    def render_camera(self):
        return

    # draw the scene
    def render(self):
        return

    # pass a key to the renderer
    def key_pressed(self, key: int):
        return

    # rotate scene around y-axis
    def rot_y(self, angle: float):
        return

    # rotate scene around x-axis
    def rot_x(self, angle: float):
        return

    # translate camera in z direction (scale distance)
    def trans_z(self, z: float):
        return
