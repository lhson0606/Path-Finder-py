import enum
import os
import sys

import OpenGL.GL as gl
import esper
import glfw
import glm
import imgui
from imgui.integrations.glfw import GlfwRenderer

import Source.ECS as ECS
import Source.ECS.Component.MapComponent as MapComponent
import Source.ECS.Component.RenderComponent as RenderComponent
import Source.ECS.Component.GridComponent as GridComponent
import Source.Manager.ShaderManager as ShaderManager
import Source.Map.Map
import Source.Render.Camera as Camera
import Source.Util.dy as dy
from Source.Map.Map import Map
from Source.Test.testwindow import show_test_window

import Source.ECS.Processor.RenderProcessor as RenderProcessor
from Source.Map.Map import open_existed_map

from OpenGL.GLU import *

import tkinter as tk
from tkinter import filedialog

import Source.Map.MapContext as MapContext


def mouse_btn_str(button):
    switcher = {
        glfw.MOUSE_BUTTON_LEFT: "Left",
        glfw.MOUSE_BUTTON_RIGHT: "Right",
        glfw.MOUSE_BUTTON_MIDDLE: "Middle",
        glfw.MOUSE_BUTTON_4: "Mouse 4",
        glfw.MOUSE_BUTTON_5: "Mouse 5"
    }

    return switcher.get(button, "None")


def key_callback(window, key, scancode, action, mods):
    app = glfw.get_window_user_pointer(window)

    if action == glfw.PRESS:
        app.key_pressed = str(key)
    elif action == glfw.RELEASE:
        app.key_released = str(key)


def cursor_position_callback(window, xpos, ypos):
    app = glfw.get_window_user_pointer(window)

    if app.context == app.Context.SCENE:

        if app.mouse_first_time_enter:
            app.mouse_first_time_enter = False
            return

        mouse_dx = xpos - app.mousePos.x
        mouse_dy = ypos - app.mousePos.y
        # we are using Oz as the up axis and Ox as the right axis
        app.cur_map_context.camera.process_mouse_movement(-mouse_dx, -mouse_dy)
        app.update_view()

    app.mousePos = glm.vec2(xpos, ypos)

    pass


def frame_buffer_size_callback(window, width, height):
    app = glfw.get_window_user_pointer(window)

    if width == 0 or height == 0:
        return

    gl.glViewport(0, 0, width, height)
    app.width = width
    app.height = height
    app.projection = glm.perspective(glm.radians(app.cur_map_context.camera.fov), float(width) / height, 0.1, 500.0)
    app.update_projection()


def mouse_scroll_callback(window, xoffset, yoffset):
    # retrieve and cast to our App object
    app = glfw.get_window_user_pointer(window)
    app.mouse_scroll = glm.vec2(xoffset, yoffset)

    if app.context == app.Context.SCENE:
        app.camera.process_mouse_scroll(yoffset)
        app.projection = glm.perspective(glm.radians(app.camera.fov), float(app.width) / app.height, 0.1, 500.0)
        app.update_projection()


def process_input(window):
    app = glfw.get_window_user_pointer(window)

    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        if app.context == app.Context.SCENE:
            app.cur_map_context.camera.process_keyboard(Camera.Camera.Movement.FORWARD, app.io.delta_time)

    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        if app.context == app.Context.SCENE:
            app.cur_map_context.camera.process_keyboard(Camera.Camera.Movement.BACKWARD, app.io.delta_time)

    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        if app.context == app.Context.SCENE:
            app.cur_map_context.camera.process_keyboard(Camera.Camera.Movement.LEFT, app.io.delta_time)

    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        if app.context == app.Context.SCENE:
            app.cur_map_context.camera.process_keyboard(Camera.Camera.Movement.RIGHT, app.io.delta_time)

    if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
        if app.context == app.Context.SCENE:
            app.cur_map_context.camera.process_keyboard(Camera.Camera.Movement.UP, app.io.delta_time)

    if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
        if app.context == app.Context.SCENE:
            app.cur_map_context.camera.process_keyboard(Camera.Camera.Movement.DOWN, app.io.delta_time)

    if app.context == app.Context.SCENE:
        app.update_view()


def mouse_button_callback(window, button, action, mods):
    app = glfw.get_window_user_pointer(window)
    if action == glfw.PRESS:
        app.mouse_btn_pressed = mouse_btn_str(button)
        if button == glfw.MOUSE_BUTTON_RIGHT:
            app.change_context(app.Context.SCENE)

    elif action == glfw.RELEASE:
        app.mouse_btn_released = mouse_btn_str(button)
        if button == glfw.MOUSE_BUTTON_RIGHT:
            app.change_context(app.Context.EDITOR)


class App:
    DEFAULT_MAP_DIR = "Resources/Map/"
    DEFAULT_MAP_NAME = "test_map.txt"

    class Context(enum.Enum):
        EDITOR = 0,
        SCENE = 1,

    def __init__(self):
        self.has_error = False
        self.impl = None
        self.width = 1280
        self.height = 720
        self.window_name = ("\"Within those eyes burned a lust for the female body, "
                            "stained with the same carnal desire that men possessed for women\"")
        self.clear_color = glm.vec4(0.2, 0.3, 0.3, 1.0)
        self.io = None
        self.key_pressed = None
        self.key_released = None
        self.mouse_btn_pressed = "None"
        self.mouse_btn_released = "None"
        self.mouse_scroll = glm.vec2(0, 0)
        self.mousePos = glm.vec2(-1, -1)
        self.window = self.impl_glfw_init()
        self.shader_manager = ShaderManager.ShaderManager()
        self.projection = glm.perspective(glm.radians(45), float(self.width) / self.height, 0.1, 500.0)
        self.mouse_first_time_enter = True
        self.context = None

        self.opened_map = {}
        self.map_contexts = {}
        self.cur_world_name = None
        self.cur_map_context = None

        # imgui modal state
        self.current_error_message = "None"
        self.show_inp_map_size_modal = False

        # imgui input state
        self.map_inp_changed_i0 = True
        self.map_inp_changed_i1 = True
        self.widgets_basic_i0 = 25
        self.widgets_basic_i1 = 25

    def prepare(self):
        pass

    def draw_spec(self):
        # fps
        imgui.set_next_window_position(0, 50)
        imgui.set_next_window_size(200, 20)
        imgui.begin("FPS", True,
                    imgui.WINDOW_NO_TITLE_BAR |
                    imgui.WINDOW_NO_RESIZE |
                    imgui.WINDOW_NO_MOVE |
                    imgui.WINDOW_NO_COLLAPSE)

        # input
        imgui.text("%.1f" % (1 / self.io.delta_time) + " FPS (%.6f " % self.io.delta_time + "ms)")
        imgui.end()

        imgui.set_next_window_position(0, 80)
        imgui.set_next_window_size(200, 150)
        imgui.begin("Input", False, imgui.WINDOW_NO_RESIZE |
                    imgui.WINDOW_NO_MOVE)
        imgui.text("Mouse pos: " + str(self.mousePos.x) + " " + str(self.mousePos.y))
        imgui.text(
            "Mouse delta: " + str(imgui.get_mouse_drag_delta().x) + " " + str(imgui.get_mouse_drag_delta().y))
        imgui.text("Mouse down:" + str(self.mouse_btn_pressed))
        imgui.text("Mouse released:" + str(self.mouse_btn_released))
        imgui.text("Mouse scroll: " + str(self.mouse_scroll.x) + " " + str(self.mouse_scroll.y))
        imgui.text("Key pressed: " + str(self.key_pressed))
        imgui.text("Key released: " + str(self.key_released))
        imgui.end()
        pass

    def change_context(self, context):
        self.context = context

        if self.context == self.Context.SCENE:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
            self.mouse_first_time_enter = True
            # disable imgui mouse
            imgui.get_io().config_flags = imgui.get_io().config_flags | imgui.CONFIG_NO_MOUSE
            # disable imgui keyboard
            imgui.get_io().config_flags = imgui.get_io().config_flags | imgui.CONFIG_NAV_NO_CAPTURE_KEYBOARD
        else:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)
            # enable imgui mouse
            imgui.get_io().config_flags = imgui.get_io().config_flags & ~imgui.CONFIG_NO_MOUSE
            # enable imgui keyboard
            imgui.get_io().config_flags = imgui.get_io().config_flags & ~imgui.CONFIG_NAV_NO_CAPTURE_KEYBOARD

        pass

    def on_create(self):
        self.init_map(open_existed_map(self.DEFAULT_MAP_DIR + "map1.txt"))
        pass

    def start_scene(self, map_name=None, asked_user_map_size=False):
        if map_name is None:
            return

        if not asked_user_map_size:
            self.init_map(Map(map_name))
            return

        self.show_inp_map_size_modal = asked_user_map_size
        pass

    def on_update(self, dt):
        esper.process(dt)
        pass

    def update_projection(self):
        for e, render_component in esper.get_component(RenderComponent.RenderComponent):
            cur_shader = render_component.shader
            self.update_proj_mat(cur_shader, "projection")
        pass

    def update_view(self):
        self.update_view_mat(self.cur_map_context.grid_shader, "view")
        pass

    def run(self):
        self.init()

        self.init_system()

        self.on_create()

        gl.glClearColor(self.clear_color.x, self.clear_color.y, self.clear_color.z, self.clear_color.w)

        while not glfw.window_should_close(self.window):
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
            glfw.poll_events()
            self.impl.process_inputs()

            process_input(self.window)

            self.on_update(self.io.delta_time)

            imgui.new_frame()

            self.on_imgui_render()

            show_test_window()

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
        # glfw.set_char_mods_callback(self.window, self.impl.char_callback)
        # set current context
        glfw.set_window_user_pointer(self.window, self)
        # ENABLE ALPHA BLENDING
        gl.glEnable(gl.GL_BLEND)

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

    def draw_menu(self):
        imgui.begin_main_menu_bar()
        if imgui.begin_menu("File", True):
            clicked_new_map, selected_new_map = imgui.menu_item("New Map", None, False, True)
            clicked_save_map, selected_save_map = imgui.menu_item("Save Map", None, False, True)
            clicked_save_map_as, selected_save_map_as = imgui.menu_item("Save Map As", None, False, True)
            clicked_load_map, selected_load_map = imgui.menu_item("Open Map", None, False, True)
            clicked_close_map, selected_close_map = imgui.menu_item("Close This Map", None, False,
                                                                    esper.list_worlds().__len__() > 1)
            clicked_quit, selected_quit = imgui.menu_item("Quit", None, False, True)

            if clicked_new_map:
                self.start_scene(self.get_new_world_name(), True)
            if clicked_save_map:
                dy.log.info("Save map")
            if clicked_save_map_as:
                dy.log.info("Save map as")
            if clicked_load_map:
                # reference: https://stackoverflow.com/questions/31122704/specify-file-path-in-tkinter-file-dialog
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename(
                    initialdir=os.path.join(os.getcwd(), Source.Map.Map.DEFAULT_MAP_DIR))
                if file_path != "":
                    # remove this switch world in the future (I'm too lazy rn):
                    new_map = Source.Map.Map.open_existed_map(file_path)
                    if new_map.name not in esper.list_worlds():
                        self.init_map(new_map)
                    else:
                        dy.log.warning("Map \'" + new_map.name + "\' is already opened!")
            if clicked_close_map:
                if esper.list_worlds().__len__() > 1:
                    cur_world = self.cur_world_name
                    for next_world in esper.list_worlds():
                        if next_world != cur_world:
                            self.load_map(next_world)
                            break
                    esper.delete_world(cur_world)
                    self.opened_map.pop(cur_world)
                    self.map_contexts.pop(cur_world)

            if clicked_quit:
                glfw.set_window_should_close(self.window, True)

            imgui.end_menu()
        imgui.end_main_menu_bar()
        pass

    def draw_editor_window(self):
        imgui.set_next_window_position(self.width - 400, 50)
        imgui.set_next_window_size(400, 200)
        imgui.begin("Editor", False, imgui.WINDOW_NO_RESIZE |
                    imgui.WINDOW_NO_MOVE)
        imgui.text("Debug")
        checked, self.cur_map_context.camera.will_print_camera_using_imgui = imgui.checkbox("Show camera info",
                                                                                            self.cur_map_context.camera.will_print_camera_using_imgui)
        if self.cur_map_context.camera.will_print_camera_using_imgui:
            imgui.set_next_window_position(self.width / 2 - 200,
                                           self.height / 2 - 200,
                                           imgui.FIRST_USE_EVER)
            imgui.begin("Camera Info", False)
            imgui.text("Position: " + str(self.cur_map_context.camera.pos))
            imgui.text("Direction: " + str(self.cur_map_context.camera.dir))
            imgui.text("Up: " + str(self.cur_map_context.camera.up))
            imgui.text("Right: " + str(self.cur_map_context.camera.right))
            imgui.text("Yaw: " + str(self.cur_map_context.camera.yaw))
            imgui.text("Pitch: " + str(self.cur_map_context.camera.pitch))
            imgui.text("FOV: " + str(self.cur_map_context.camera.fov))
            imgui.end()
        imgui.end()
        pass

    def on_imgui_render(self):
        self.draw_spec()

        self.draw_menu()

        self.draw_editor_window()

        self.draw_map_tab()

        if self.has_error:
            imgui.open_popup("Error!")

        if self.show_inp_map_size_modal:
            imgui.open_popup("Creat a new map")

        self.draw_modal()

    def draw_modal(self):
        if imgui.begin_popup_modal(
                title="Error!", visible=True, flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE
        )[0]:
            imgui.text(self.current_error_message)
            imgui.separator()
            if imgui.button(label="OK", width=120, height=0):
                imgui.close_current_popup()
                self.has_error = False
            imgui.set_item_default_focus()
            imgui.same_line()
            imgui.end_popup()
        else:
            # enable modal 'x' button to close
            imgui.close_current_popup()
            self.has_error = False

        if imgui.begin_popup_modal(
                title="Creat a new map", visible=True, flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE
        )[0]:
            imgui.text("Input map size")
            self.map_inp_changed_i0, self.widgets_basic_i0 = imgui.input_int("width", self.widgets_basic_i0, 1, 100)
            self.map_inp_changed_i1, self.widgets_basic_i1 = imgui.input_int("height", self.widgets_basic_i1, 1, 100)

            if self.map_inp_changed_i0:
                self.widgets_basic_i0 = max(10, self.widgets_basic_i0)
                self.widgets_basic_i0 = min(50, self.widgets_basic_i0)

            if self.map_inp_changed_i1:
                self.widgets_basic_i1 = max(10, self.widgets_basic_i1)
                self.widgets_basic_i1 = min(50, self.widgets_basic_i1)

            imgui.separator()
            if imgui.button(label="OK", width=120, height=0):
                imgui.close_current_popup()
                self.show_inp_map_size_modal = False
                self.init_map(Map(self.get_new_world_name(), self.widgets_basic_i0, self.widgets_basic_i1))

            imgui.set_item_default_focus()
            imgui.same_line()
            imgui.end_popup()
        else:
            # enable modal 'x' button to close
            imgui.close_current_popup()
            self.show_inp_map_size_modal = False

    def draw_map_tab(self):
        imgui.set_next_window_position(0, 20)
        imgui.set_next_window_size(self.width, 20)
        if imgui.begin("Map tab bar", True,
                       imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE |
                       imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_TITLE_BAR):
            with imgui.begin_tab_bar("MyTabBar") as tab_bar:
                if tab_bar.opened:

                    for (name) in esper.list_worlds():
                        with imgui.begin_tab_item(name) as item:
                            if item.selected and self.cur_world_name != name:
                                self.load_map(name)
                                pass
        imgui.end()

    def init_system(self):
        # cooking shaders
        self.shader_manager.hard_load_all_shaders()

        # change to EDITOR context (default)
        self.change_context(self.Context.EDITOR)

        pass

    def get_new_world_name(self):
        count = 0
        new_name = "map" + str(count) + '.txt'
        while new_name in esper.list_worlds() or Map.is_map_name_existed(new_name):
            count += 1
            new_name = "map" + str(count) + '.txt'

        return new_name

    def pop_up_error(self, message="None"):
        self.current_error_message = message
        self.has_error = True

    def init_map(self, target_map):
        # Note: each world has
        # + exactly one map component
        # + exactly one camera component (but rn we don't have camera component)
        # + exactly one grid component
        # + exactly one map context

        self.cur_map_context = MapContext.MapContext(target_map)
        # create new map context
        self.cur_map_context.camera.pos.x = target_map.width / 2
        self.cur_map_context.camera.update_camera_vectors()
        self.cur_map_context.grid_shader = self.shader_manager.get_shader(ShaderManager.ShaderType.GRID_SHADER)
        self.map_contexts[target_map.name] = self.cur_map_context

        # ===== add processors =====
        esper.add_processor(RenderProcessor.RenderProcessor(self))

        # ===== create a grid entity =====
        new_grid_entity = esper.create_entity()
        esper.add_component(new_grid_entity,
                            ECS.Component.GridComponent.GridComponent(target_map.width, target_map.height))
        esper.add_component(new_grid_entity, RenderComponent.RenderComponent(
            self.cur_map_context.grid_shader,
            ShaderManager.ShaderType.GRID_SHADER
        ))
        self.update_proj_mat(self.cur_map_context.grid_shader, "projection")
        self.update_view_mat(self.cur_map_context.grid_shader, "view")
        self.cur_map_context.grid_shader.use()
        self.cur_map_context.grid_shader.set_float("gridWidth", target_map.width)
        self.cur_map_context.grid_shader.set_float("gridHeight", target_map.height)
        self.cur_map_context.grid_shader.stop()
        # ==================================

        # load map data
        if not target_map.is_draft:
            dy.log.info("Loading \'" + target_map.name + "\' data")
            target_map.load(ShaderManager.ShaderType.SHAPE_SHADER, self.shader_manager.get_shader(
                ShaderManager.ShaderType.SHAPE_SHADER
            ))

        # create a new world with the name of the target map
        # self.load_map("default")
        pass

    def load_map(self, world_name):
        pass

    def update_view_mat(self, shader, uniform_name):
        shader.use()
        shader.set_mat4(uniform_name, self.cur_map_context.camera.view)
        shader.stop()

    def update_proj_mat(self, shader, uniform_name):
        shader.use()
        shader.set_mat4(uniform_name, self.projection)
        shader.stop()
