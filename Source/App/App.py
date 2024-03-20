import sys
import glfw
import glm
import imgui
from imgui.integrations.glfw import GlfwRenderer
import OpenGL.GL as gl
import esper
import Source.Util.dy as dy
import Source.Manager.ShaderManager as ShaderManager


def key_callback(window, key, scancode, action, mods):
    app = glfw.get_window_user_pointer(window)

    if action == glfw.PRESS:
        app.key_pressed = str(key)
    elif action == glfw.RELEASE:
        app.key_released = str(key)


def cursor_position_callback(window, xpos, ypos):
    app = glfw.get_window_user_pointer(window)
    app.mousePos = glm.vec2(xpos, ypos)


def frame_buffer_size_callback(window, width, height):
    app = glfw.get_window_user_pointer(window)
    gl.glViewport(0, 0, width, height)
    app.width = width
    app.height = height


def mouse_scroll_callback(window, xoffset, yoffset):
    # retrieve and cast to our App object
    app = glfw.get_window_user_pointer(window)
    app.mouseScroll = glm.vec2(xoffset, yoffset)


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def mouse_button_callback(window, button, action, mods):
    app = glfw.get_window_user_pointer(window)
    if action == glfw.PRESS:
        app.mouse_btn_pressed = button
    elif action == glfw.RELEASE:
        app.mouse_btn_released = button


class App:

    DEFAULT_MAP_DIR = "Resources/Map/"
    DEFAULT_MAP_NAME = "test_map.txt"

    def __init__(self):
        self.impl = None
        self.width = 1280
        self.height = 720
        self.window_name = "minimal ImGui/GLFW3 example"
        self.clear_color = glm.vec4(0.2, 0.3, 0.3, 1.0)
        self.io = None
        self.key_pressed = None
        self.key_released = None
        self.mouse_btn_pressed = None
        self.mouse_btn_released = None
        self.mouseScroll = glm.vec2(0, 0)
        self.mousePos = glm.vec2(-1, -1)
        self.window = self.impl_glfw_init()
        self.shader_manager = ShaderManager.ShaderManager()

    def prepare(self):
        # self.key_pressed = None
        # self.key_released = None
        # self.mouse_btn_pressed = None
        # self.mouse_btn_released = None
        # self.mouseScroll = glm.vec2(0, 0)
        pass

    def draw_spec(self):
        # fps
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(200, 20)
        imgui.begin("FPS", True,
                    imgui.WINDOW_NO_TITLE_BAR |
                    imgui.WINDOW_NO_RESIZE |
                    imgui.WINDOW_NO_MOVE |
                    imgui.WINDOW_NO_COLLAPSE)

        # input
        imgui.text("%.1f" % (1 / self.io.delta_time) + " FPS (%.6f " % self.io.delta_time + "ms)")
        imgui.end()

        imgui.set_next_window_position(0, 30)
        imgui.set_next_window_size(200, 150)
        imgui.begin("Input", False, imgui.WINDOW_NO_RESIZE |
                    imgui.WINDOW_NO_MOVE)
        imgui.text("Mouse pos: " + str(self.mousePos.x) + " " + str(self.mousePos.y))
        imgui.text(
            "Mouse delta: " + str(imgui.get_mouse_drag_delta().x) + " " + str(imgui.get_mouse_drag_delta().y))
        imgui.text("Mouse down:" + str(self.mouse_btn_pressed))
        imgui.text("Mouse released:" + str(self.mouse_btn_released))
        imgui.text("Mouse scroll: " + str(self.mouseScroll.x) + " " + str(self.mouseScroll.y))
        imgui.text("Key pressed: " + str(self.key_pressed))
        imgui.text("Key released: " + str(self.key_released))
        imgui.end()
        pass

    def on_create(self):
        dy.log.info("Program started")

        # cooking shaders
        self.shader_manager.hard_load_all_shaders()

        self.start_scene()
        pass

    def start_scene(self, map_name=DEFAULT_MAP_NAME):
        map_data = dy.read_text(self.DEFAULT_MAP_DIR + map_name)
        dy.log.info("Map data: \n" + map_data)
        pass

    def on_update(self, dt):
        esper.process(dt)
        pass

    def run(self):
        self.init()

        self.on_create()

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.impl.process_inputs()

            process_input(self.window)

            imgui.new_frame()

            self.draw_spec()

            self.on_update(self.io.delta_time)
            # show_test_window()

            gl.glClearColor(self.clear_color.x, self.clear_color.y, self.clear_color.z, self.clear_color.w)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            imgui.render()
            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

        self.on_close()

    def init(self):
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)
        glfw.set_char_callback(self.window, self.impl.char_callback)
        glfw.set_cursor_pos_callback(self.window, self.impl.mouse_callback)
        self.io = imgui.get_io()
        # register our callbacks
        glfw.set_key_callback(self.window, key_callback)
        glfw.set_cursor_pos_callback(self.window, cursor_position_callback)
        glfw.set_framebuffer_size_callback(self.window, frame_buffer_size_callback)
        glfw.set_scroll_callback(self.window, mouse_scroll_callback)
        glfw.set_mouse_button_callback(self.window, mouse_button_callback)
        # set current context
        glfw.set_window_user_pointer(self.window, self)

    def on_close(self):
        self.impl.shutdown()
        glfw.terminate()

    def impl_glfw_init(self):
        if not glfw.init():
            print("Could not initialize OpenGL context")
            sys.exit(1)

        # OS X supports only forward-compatible core profiles from 3.2
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

        # Create a windowed mode window and its OpenGL context
        self.window = glfw.create_window(int(self.width), int(self.height), self.window_name, None, None)
        glfw.make_context_current(self.window)

        if not self.window:
            glfw.terminate()
            print("Could not initialize Window")
            sys.exit(1)

        return self.window
