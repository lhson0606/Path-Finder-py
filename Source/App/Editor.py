import imgui

import Source.App.Command as Command
import enum
import Source.Util.dy as dy

import Source.ECS.Component.NameTagComponent as NameTagComponent
import Source.ECS.Component.CubeComponent as CubeComponent
import Source.ECS.Component.ShapeComponent as ShapeComponent
import Source.ECS.Component.TransformComponent as TransformComponent
import Source.App.MoveCubeCmd as MoveCubeCmd

import esper

import glm


class Mode(enum.Enum):
    NONE = 0
    SELECT_CUBE = 1
    SELECT_SHAPE = 2


class Editor:
    def __init__(self, app):
        self.history = []
        self.future = []
        self.mode = Mode.NONE
        self.app = app
        self.cur_cube = None
        self.is_new = False
        self.widgets_basic_vec3a = [0.0, 0.0, 0.0]

    def execute(self, command: Command):
        self.history.append(command)
        command.execute()
        self.future.clear()

    def undo(self):
        if len(self.history) > 0:
            command = self.history.pop()
            command.undo()
            self.future.append(command)

    def redo(self):
        if len(self.future) > 0:
            command = self.future.pop()
            command.execute()
            self.history.append(command)

    def handle_pick(self, picked_obj):
        if picked_obj.entity == -1:
            self.cur_cube = None
            self.mode = Mode.NONE
            return

        if self.cur_cube is not picked_obj.entity:
            self.is_new = True

        name_tag = esper.component_for_entity(picked_obj.entity, NameTagComponent.NameTagComponent)

        if name_tag.name == "cube":
            self.cur_cube = picked_obj.entity

        pass

    def on_imgui_render(self):
        if self.cur_cube is None:
            return

        cube_comp = esper.component_for_entity(self.cur_cube, CubeComponent.CubeComponent)
        transform_comp = esper.component_for_entity(self.cur_cube, TransformComponent.TransformComponent)

        if cube_comp.pivot_index == -1:
            return

        if self.is_new:
            imgui.set_next_window_position(self.app.mousePos.x, self.app.mousePos.y)
            self.is_new = False
        else:
            imgui.set_next_window_position(self.app.mousePos.x, self.app.mousePos.y, imgui.ONCE)
        imgui.set_next_window_size(300, 80, imgui.ONCE)

        imgui.begin("Cube: ", False,
                    imgui.WINDOW_NO_COLLAPSE)
        imgui.text("Entity: " + str(self.cur_cube))
        self.widgets_basic_vec3a = transform_comp.position
        imgui.text("Pivot index: " + str(cube_comp.pivot_index))
        changed, self.widgets_basic_vec3a = imgui.input_int3(
            "Position",
            *self.widgets_basic_vec3a
        )
        imgui.end()

        if changed:
            self.execute(MoveCubeCmd.MoveCubeCmd(self.cur_cube, glm.vec3(self.widgets_basic_vec3a)))
