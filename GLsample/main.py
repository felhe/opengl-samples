import glfw
from RenderTriangle import RenderTriangle
from OpenGL.GL import *


def main():
    ui_width = 800
    ui_height = 600

    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)

    glfw.window_hint(glfw.DOUBLEBUFFER, glfw.TRUE)
    glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)
    glfw.window_hint(glfw.SAMPLES, 4)

    window = glfw.create_window(ui_width, ui_height, "OpenGL Example", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    renderer = RenderTriangle()
    renderer.init_gl()
    renderer.set_window_size(ui_width, ui_height)

    def resize_callback(_, width: int, height: int):
        renderer.set_window_size(width, height)

    def keyboard_callback(window, key: int, scan: int, action: int, mods: int):
        if key == glfw.KEY_Q:
            glfw.set_window_should_close(window, glfw.TRUE)
        if key == glfw.KEY_LEFT:
            renderer.rot_y(-2.0)
        if key == glfw.KEY_RIGHT:
            renderer.rot_y(2.0)
        if key == glfw.KEY_UP:
            renderer.rot_x(-2.0)
        if key == glfw.KEY_DOWN:
            renderer.rot_x(2.0)
        if key == glfw.KEY_KP_ADD:
            renderer.trans_z(1.0)
        if key == glfw.KEY_KP_SUBTRACT:
            renderer.trans_z(-1.0)
        if key == glfw.KEY_SPACE:
            renderer.divide_polygons()

        renderer.render_camera()

    glfw.set_window_size_callback(window, resize_callback)
    glfw.set_key_callback(window, keyboard_callback)

    while not glfw.window_should_close(window):
        renderer.render()
        glFlush()
        glfw.swap_buffers(window)
        glfw.wait_events()

    renderer.uninit_gl()
    del renderer
    glfw.terminate()


if __name__ == "__main__":
    main()
