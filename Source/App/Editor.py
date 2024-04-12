import imgui

import Source.App.Command as Command
import enum
import Source.Util.dy as dy

import Source.ECS.Component.NameTagComponent as NameTagComponent
import Source.ECS.Component.CubeComponent as CubeComponent
import Source.ECS.Component.ShapeComponent as ShapeComponent
import Source.ECS.Component.TransformComponent as TransformComponent
import Source.ECS.Component.TempShapeComponent as TempShapeComponent
import Source.ECS.Component.RenderComponent as RenderComponent
import Source.ECS.Component.OutliningComponent as OutliningComponent
import Source.ECS.Component.MotionComponent as MotionComponent
import Source.ECS.Processor.PhysicProcessor as PhysicProcessor
import Source.ECS.Processor.VisualizingProcessor as VisualizingProcessor
import Source.App.MoveCubeCmd as MoveCubeCmd
import Source.Manager.ShaderManager as ShaderManager
import Source.App.AddPivotCmd as AddPivotCmd
import Source.Algorithm.VisualizedAStar as VisualizedAStar
import imgui

import esper

import glm

shape_inp_int3 = glm.vec3(0.0, 0.0, 0.0)
shape_inp_int = 0


class Mode(enum.Enum):
    NONE = 0
    SELECT_CUBE = 1
    SELECT_SHAPE = 2
    ADDING_PIVOT = 3
    IS_RUNNING_SIMULATION = 4


class Editor:
    def __init__(self, app):
        self.history = []
        self.future = []
        self.mode = Mode.NONE
        self.app = app
        self.cur_entity = -1
        self.widgets_basic_vec3a = [0.0, 0.0, 0.0]
        # walk around for imgui bug
        self.prev_widgets_basic_vec3a = [0.0, 0.0, 0.0]
        self.should_update_position = False
        self.cur_obj = None
        self.pause_time = 0
        self.cur_shape = -1
        self.cur_temp_shape = -1
        self.new_pivot_pos = glm.ivec3(0)
        self.current_algorithm = None

    def execute(self, command: Command):
        try:
            if command.execute():
                self.history.append(command)
                self.app.cur_map_context.map.is_dirty = True
            else:
                self.app.pop_up_error("Command failed to execute, please check log for more information.")
                return
        except Exception as e:
            dy.log.error("Command failed to execute: %s", e)
            self.app.pop_up_error("Command failed to execute, please check log for more information.")
            return

        self.future.clear()

    def undo(self):
        self.quit_edit()
        if len(self.history) > 0:
            command = self.history.pop()
            command.undo()
            self.future.append(command)
            self.app.cur_map_context.map.is_dirty = True

        else:
            dy.log.warning("No command to undo")

    def redo(self):
        self.quit_edit()
        if len(self.future) > 0:
            command = self.future.pop()
            command.execute()
            self.history.append(command)
            self.app.cur_map_context.map.is_dirty = True
        else:
            dy.log.warning("No command to redo")

    def placing(self, obj):
        if self.mode == Mode.IS_RUNNING_SIMULATION:
            return

        if imgui.is_any_item_hovered() or imgui.is_any_item_active():
            return

        if obj.entity == 0 or self.cur_entity == obj.entity:
            return

        new_pivot_pos = glm.ivec3(0)

        if obj.entity == -1:

            ray_dir = dy.cast_ray(self.app.mousePos.x, self.app.mousePos.y, self.app.width, self.app.height,
                                  self.app.cur_map_context.camera.view, self.app.projection)
            ray_origin = self.app.cur_map_context.camera.pos
            if ray_dir.z == 0:
                return
            t = (0 - ray_origin.z) / ray_dir.z
            intersection = ray_origin + t * ray_dir
            intersection.x = dy.round_away_from_zero(intersection.x)
            intersection.y = dy.round_away_from_zero(intersection.y)
            intersection.z = dy.round_away_from_zero(intersection.z)
            new_pivot_pos = glm.ivec3(intersection)
        else:
            try:
                transform_comp = esper.component_for_entity(obj.entity, TransformComponent.TransformComponent)
                new_pivot_pos = glm.ivec3(transform_comp.position)
                off_set = glm.ivec3(obj.x, obj.y, obj.z)
                new_pivot_pos += off_set
                self.cur_entity = obj.entity
            except AttributeError:
                dy.log.warning("No transform component for entity: %s", obj.entity)

        if self.cur_temp_shape != -1:
            t_shape_comp = esper.component_for_entity(self.cur_temp_shape, TempShapeComponent.TempShapeComponent)
            t_shape_comp.clean_up()
            esper.delete_entity(self.cur_temp_shape, True)
            self.cur_temp_shape = -1

        # new_pivot_pos.x += 1
        # new_pivot_pos.y += 1
        # new_pivot_pos.z += 1
        # dy.log.info("New pivot pos: %s", new_pivot_pos)

        new_temp_cubes = ShapeComponent.get_new_cubes(self.cur_shape, new_pivot_pos)
        # dy.log.info("New temp cubes: %s", new_temp_cubes)
        temp_shape_comp = TempShapeComponent.TempShapeComponent(new_temp_cubes)
        temp_shape_comp.load()
        shader = self.app.shader_manager.get_shader(ShaderManager.ShaderType.TEMP_SHAPE_SHADER)
        render_comp = RenderComponent.RenderComponent(
            ShaderManager.ShaderType.TEMP_SHAPE_SHADER,
            shader)
        new_temp_shape_ent = esper.create_entity()
        esper.add_component(new_temp_shape_ent, temp_shape_comp)
        esper.add_component(new_temp_shape_ent, render_comp)
        self.cur_temp_shape = new_temp_shape_ent
        self.new_pivot_pos = new_pivot_pos
        pass

    def handle_pick(self, picked_obj):
        if self.mode == Mode.IS_RUNNING_SIMULATION:
            return

        if self.mode == Mode.ADDING_PIVOT:
            self.execute(AddPivotCmd.AddPivotCommand(self.cur_shape, self.new_pivot_pos))
            self.mode = Mode.NONE
            self.quit_edit()

            return

        if picked_obj.entity == -1:
            self.quit_edit()
            return

        tag_comp = esper.component_for_entity(picked_obj.entity, NameTagComponent.NameTagComponent)

        if tag_comp.name == "start":
            dy.log.info("Start picked")
            pass

        if tag_comp.name == "goal":
            dy.log.info("Goal picked")
            pass

        if tag_comp.name == "passing point":
            dy.log.info("Passing point picked")
            pass

        if tag_comp.name == "cube":

            cube_comp = esper.component_for_entity(picked_obj.entity, CubeComponent.CubeComponent)
            self.cur_obj = picked_obj

            if self.cur_entity != picked_obj.entity:
                self.should_update_position = True

            if not cube_comp.is_pivot():
                self.quit_edit()
                self.cur_entity = picked_obj.entity
                self.mode = Mode.SELECT_SHAPE
                # enable shape outlining
                outline_comp = esper.component_for_entity(cube_comp.shape_entity, OutliningComponent.OutliningComponent)
                outline_comp.set_draw_outline(True)
                self.cur_shape = cube_comp.shape_entity
            else:
                if self.cur_entity == picked_obj.entity:
                    self.quit_edit()
                    self.cur_entity = picked_obj.entity
                    self.mode = Mode.SELECT_SHAPE
                    self.should_update_position = True
                    # enable shape outlining
                    outline_comp = esper.component_for_entity(cube_comp.shape_entity, OutliningComponent.OutliningComponent)
                    outline_comp.set_draw_outline(True)
                    self.cur_shape = cube_comp.shape_entity
                else:
                    self.cur_entity = picked_obj.entity
                    self.mode = Mode.SELECT_CUBE
                    self.prev_widgets_basic_vec3a = glm.vec3(
                        esper.component_for_entity(self.cur_entity, TransformComponent.TransformComponent).position)

        pass

    def on_imgui_render(self):
        imgui.set_next_window_position(self.app.width - 400, 50)
        imgui.set_next_window_size(400, 350)
        imgui.begin("Editor", False, imgui.WINDOW_NO_RESIZE |
                    imgui.WINDOW_NO_MOVE)

        if self.mode == Mode.IS_RUNNING_SIMULATION:
            imgui.text("Simulation is running, please wait...")
            imgui.text("press ESC or \"Pause\" to stop")
            if imgui.button("Pause"):
                self.quit_edit()
            imgui.end()
            return

        imgui.text("Edit")

        if imgui.button("Add shape"):
            pass

        if imgui.button("Add passing point"):
            pass

        if self.app.cur_map_context.map.start_ent == -1:
            if imgui.button("Add start"):
                pass

        if self.app.cur_map_context.map.goal_ent == -1:
            if imgui.button("Add goal"):
                pass

        imgui.text("Visualize")

        if imgui.button("Clear path"):
            if self.current_algorithm is not None:
                self.current_algorithm.clean_up()
                self.current_algorithm = None
            pass

        if imgui.button("Run A Star"):
            if self.current_algorithm is not None:
                self.current_algorithm.clean_up()
                self.current_algorithm = None

            self.current_algorithm = VisualizedAStar.VisualizedAStar(self.app.cur_map_context.map, self.app)
            try:
                self.current_algorithm.solve_and_visualize()
            except Exception as e:
                self.handle_when_no_path_found()
            pass

        if imgui.button("Run greedy"):
            pass

        if imgui.button("Run BFS"):
            pass

        if imgui.button("Run in real time"):
            self.run_simulation()

        if imgui.button("Reset shapes position"):
            pass

        imgui.end()

        if self.mode == Mode.NONE:
            return

        if self.mode == Mode.SELECT_CUBE:
            self.render_cube_editor()

        if self.mode == Mode.SELECT_SHAPE:
            self.render_shape_editor()

    def render_cube_editor(self):
        if self.cur_entity == -1:
            return

        cube_comp = esper.component_for_entity(self.cur_entity, CubeComponent.CubeComponent)
        transform_comp = esper.component_for_entity(self.cur_entity, TransformComponent.TransformComponent)

        if cube_comp.pivot_index == -1:
            return

        if self.should_update_position:
            imgui.set_next_window_position(self.app.mousePos.x, self.app.mousePos.y)
            self.should_update_position = False
        else:
            imgui.set_next_window_position(self.app.mousePos.x, self.app.mousePos.y, imgui.ONCE)
        imgui.set_next_window_size(400, 80, imgui.ONCE)

        imgui.begin("Pivot: ", False,
                    imgui.WINDOW_NO_COLLAPSE)
        imgui.text("Entity: " + str(self.cur_entity))
        self.widgets_basic_vec3a = transform_comp.position
        imgui.text("Pivot index: " + str(cube_comp.pivot_index))
        changed, self.widgets_basic_vec3a = imgui.input_int3(
            "Position",
            *self.widgets_basic_vec3a
        )

        imgui.same_line()

        if changed:
            self.prev_widgets_basic_vec3a = glm.vec3(self.widgets_basic_vec3a)

        if imgui.button("ok"):
            self.execute(MoveCubeCmd.MoveCubeCmd(self.cur_entity, self.prev_widgets_basic_vec3a))
            pass

        imgui.end()

        pass

    def quit_edit(self):
        if self.mode == Mode.IS_RUNNING_SIMULATION:
            esper.get_processor(PhysicProcessor.PhysicProcessor).disable()
            esper.get_processor(VisualizingProcessor.VisualizingProcessor).disable()

        if self.cur_temp_shape != -1:
            t_shape_comp = esper.component_for_entity(self.cur_temp_shape, TempShapeComponent.TempShapeComponent)
            t_shape_comp.clean_up()
            esper.delete_entity(self.cur_temp_shape, True)
            self.cur_temp_shape = -1

        if self.cur_shape != -1:
            outline_comp = esper.component_for_entity(self.cur_shape, OutliningComponent.OutliningComponent)
            outline_comp.set_draw_outline(False)

        self.mode = Mode.NONE
        self.cur_entity = -1
        self.cur_obj = None
        self.cur_shape = -1
        self.cur_temp_shape = -1
        self.new_pivot_pos = glm.ivec3(0)
        pass

    def render_shape_editor(self):
        cube_comp = esper.component_for_entity(self.cur_entity, CubeComponent.CubeComponent)
        shape_ent = cube_comp.shape_entity
        shape_comp = esper.component_for_entity(shape_ent, ShapeComponent.ShapeComponent)
        motion_comp = esper.component_for_entity(shape_ent, MotionComponent.MotionComponent)

        if self.should_update_position:
            imgui.set_next_window_position(self.app.mousePos.x, self.app.mousePos.y)
            self.should_update_position = False
        else:
            imgui.set_next_window_position(self.app.mousePos.x, self.app.mousePos.y, imgui.ONCE)
        imgui.set_next_window_size(300, 150, imgui.ONCE)

        imgui.begin("Shape: ", False,
                    imgui.WINDOW_NO_COLLAPSE)
        imgui.text("Entity: " + str(shape_ent))

        if imgui.button("Add pivot"):
            self.mode = Mode.ADDING_PIVOT
            self.cur_shape = shape_ent
            pass

        shape_inp_int3 = glm.ivec3(int(motion_comp.velocity.x), int(motion_comp.velocity.y), int(motion_comp.velocity.z))

        changed, shape_inp_int3 = imgui.input_int3(
            "Velocity",
            *shape_inp_int3
        )

        if changed:
            motion_comp.set_velocity(glm.vec3(shape_inp_int3))

        changed, motion_comp.distance = imgui.input_int(
            "Distance",
            motion_comp.distance,
            1,
            0
        )

        if imgui.button("Translate"):
            pass

        if imgui.button("Delete"):
            pass

        imgui.end()
        pass

    def run_simulation(self):
        self.quit_edit()
        self.mode = Mode.IS_RUNNING_SIMULATION
        esper.get_processor(PhysicProcessor.PhysicProcessor).enable()
        esper.get_processor(VisualizingProcessor.VisualizingProcessor).enable(
            VisualizedAStar.VisualizedAStar(self.app.cur_map_context.map, self.app), self)
        pass

    def handle_when_no_path_found(self):
        self.quit_edit()
        self.app.pop_up_error("No path found")
        pass
