import esper

import Source.Util.dy as dy
import glm

import Source.ECS.Component.ShapeComponent as ShapeComponent
import Source.ECS.Component.RenderComponent as RenderComponent
import Source.ECS.Component.NameTagComponent as NameTagComponent
import Source.ECS.Component.OutliningComponent as OutliningComponent
import Source.ECS.Component.StartPointComponent as StartPointComponent
import Source.ECS.Component.GoalPointComponent as GoalPointComponent
import Source.ECS.Component.MotionComponent as MotionComponent
import Source.Manager.ShaderManager as ShaderManager
import Source.ECS.Component.TransformComponent as TransformComponent
import Source.ECS.Component.CubeComponent as CubeComponent
import Source.ECS.Component.PassingPointsComponent as PassingPointsComponent
import Source.Render.Shader as Shader
import Source.Manager.TextureManager as TextureManager
import numpy as np

DEFAULT_MAP_DIR = "Resources/Map/"
DEFAULT_MAP_NAME = "map"


def get_map_name(full_path):
    return full_path.split("/")[-1]


def open_existed_map(full_path):
    if not dy.file_exists(full_path):
        raise FileNotFoundError("File not found: " + full_path)

    a_map = Map(get_map_name(full_path))
    a_map.is_draft = False
    a_map.full_path = full_path
    return a_map


class Map:

    def __init__(self, name, w=25, h=25, l=1):
        self.name = name
        self.width = w
        self.height = h
        self.length = l
        self.is_dirty = False
        self.start = glm.ivec2(0, 0)
        self.goal = glm.ivec2(0, 0)
        self.shape_count = 0
        self.full_path = DEFAULT_MAP_DIR + name
        self.look_up = np.array([[[0 for _ in range(0, l + 1)] for _ in range(0, h + 1)] for _ in range(0, w + 1)])
        self.is_draft = True
        self.goal_ent = -1
        self.start_ent = -1
        self.app = None
        self.passing_point_positions = []
        self.shape_entities = []
        self.passing_points_ent = -1

    def create(self):
        count = 0

        pass

    def load(self, app):
        self.app = app
        shader_manager = app.shader_manager
        texture_manager = app.texture_manager
        with open(self.full_path) as file:
            lines = file.readlines()

        try:
            for i in range(len(lines)):
                lines[i] = lines[i].replace("\n", "")
                lines[i] = lines[i].replace("\r", "")
                lines[i] = lines[i].replace(" ", "")

            if lines[0].split(",").__len__() != 2:
                raise ValueError("Not implemented map format: " + lines[0])
            self.width = int(lines[0].split(",")[0])
            self.height = int(lines[0].split(",")[1])

            self.look_up = np.array(
                [[[0 for _ in range(0, self.length + 1)] for _ in range(0, self.height + 1)] for _ in
                 range(0, self.width + 1)])

            second_line_data = lines[1].split(",")

            self.create_start_point(glm.ivec3(int(second_line_data[0]), int(second_line_data[1]), 0))
            self.create_goal_point(glm.ivec3(int(second_line_data[2]), int(second_line_data[3]), 0))

            # check for passing points
            if len(second_line_data) > 4:
                for i in range(4, len(second_line_data), 2):
                    pos = glm.ivec3(int(second_line_data[i]), int(second_line_data[i + 1]), 0)
                    self.passing_point_positions.append(pos)
                self.create_passing_points(self.passing_point_positions)

            shape_count = int(lines[2].split(",")[0])

            for i in range(0, shape_count):
                line = lines[i + 3].strip()
                shape_data = line.split(",")
                if len(shape_data) == 0 or len(shape_data) % 2 != 0:
                    raise ValueError("Invalid shape data: " + line)
                pivots = []
                for j in range(0, len(shape_data), 2):
                    pivots.append(glm.ivec3(int(shape_data[j]), int(shape_data[j + 1]), 0))

                self.create_shape(pivots)

        except Exception as e:
            dy.log.error("Invalid map file: " + str(self.full_path) + " " + str(e))
            raise ValueError("Invalid map file: " + str(self.full_path) + " " + str(e))
        pass

    def save(self):
        pass

    @staticmethod
    def get_new_map_name(directory=DEFAULT_MAP_DIR):
        count = 0

        while dy.file_exists(directory + DEFAULT_MAP_NAME + str(count) + ".txt"):
            count += 1

        return DEFAULT_MAP_NAME + str(count) + ".txt"

    @staticmethod
    def is_map_name_existed(name, directory=DEFAULT_MAP_DIR):
        return dy.file_exists(directory + name)

    def create_start_point(self, pos):
        self.start = pos
        self.start_ent = esper.create_entity()

        transform_comp = TransformComponent.TransformComponent(pos)
        shader = self.app.shader_manager.get_shader(ShaderManager.ShaderType.START_POINT_SHADER)
        render_comp = RenderComponent.RenderComponent(ShaderManager.ShaderType.START_POINT_SHADER, shader)
        outlining_comp = OutliningComponent.OutliningComponent(ShaderManager.ShaderType.SIMPLE_OUTLINING_SHADER,
                                                               self.app.shader_manager.get_shader(
                                                                   ShaderManager.ShaderType.SIMPLE_OUTLINING_SHADER))
        name_tag_comp = NameTagComponent.NameTagComponent("start")

        texture = self.app.texture_manager.get_texture(TextureManager.TextureType.START_CUBE)
        shader.use()
        shader.set_mat4("model", transform_comp.get_world_transform())
        shader.stop()
        start_point_component = StartPointComponent.StartPointComponent(texture)

        esper.add_component(self.start_ent, transform_comp)
        esper.add_component(self.start_ent, render_comp)
        esper.add_component(self.start_ent, NameTagComponent.NameTagComponent("start"))
        esper.add_component(self.start_ent, start_point_component)
        esper.add_component(self.start_ent, outlining_comp)
        esper.add_component(self.start_ent, name_tag_comp)

        pass

    def create_goal_point(self, pos):
        self.goal = pos
        self.goal_ent = esper.create_entity()

        transform_comp = TransformComponent.TransformComponent(pos)
        shader = self.app.shader_manager.get_shader(ShaderManager.ShaderType.GOAL_POINT_SHADER)
        render_comp = RenderComponent.RenderComponent(ShaderManager.ShaderType.GOAL_POINT_SHADER, shader)
        outlining_comp = OutliningComponent.OutliningComponent(ShaderManager.ShaderType.SIMPLE_OUTLINING_SHADER,
                                                               self.app.shader_manager.get_shader(
                                                                   ShaderManager.ShaderType.SIMPLE_OUTLINING_SHADER))
        name_tag_comp = NameTagComponent.NameTagComponent("goal")

        texture = self.app.texture_manager.get_texture(TextureManager.TextureType.GOAL_CUBE)
        shader.use()
        shader.set_mat4("model", transform_comp.get_world_transform())
        shader.stop()
        goal_point_comp = GoalPointComponent.GoalPointComponent(texture)

        esper.add_component(self.goal_ent, transform_comp)
        esper.add_component(self.goal_ent, render_comp)
        esper.add_component(self.goal_ent, NameTagComponent.NameTagComponent("goal"))
        esper.add_component(self.goal_ent, goal_point_comp)
        esper.add_component(self.goal_ent, outlining_comp)
        esper.add_component(self.goal_ent, name_tag_comp)

        pass

    def switch_context(self):
        if self.start_ent == -1 or self.goal_ent == -1:
            return

        transform_comp = esper.component_for_entity(self.start_ent, TransformComponent.TransformComponent)
        shader = self.app.shader_manager.get_shader(ShaderManager.ShaderType.START_POINT_SHADER)
        shader.use()
        shader.set_mat4("model", transform_comp.get_world_transform())
        shader.stop()

        transform_comp = esper.component_for_entity(self.goal_ent, TransformComponent.TransformComponent)
        shader = self.app.shader_manager.get_shader(ShaderManager.ShaderType.GOAL_POINT_SHADER)
        shader.use()
        shader.set_mat4("model", transform_comp.get_world_transform())
        shader.stop()

    def is_wall(self, pos: glm.ivec3):
        if pos.x < 1 or pos.y < 1 or pos.z < 0 or pos.x > self.width or pos.y > self.height or pos.z >= self.length:
            return False

        return self.look_up[pos.x][pos.y][pos.z] == 1

    def is_moveable(self, cur_pos: glm.ivec3, next_pos: glm.ivec3):

        if next_pos.x < 1 or next_pos.y < 1 or next_pos.z < 0 or next_pos.x > self.width or next_pos.y > self.height or next_pos.z >= self.length:
            return False

        if self.look_up[next_pos.x][next_pos.y][next_pos.z] == 1:
            return False

        if cur_pos.x == next_pos.x and cur_pos.y == next_pos.y and cur_pos.z == next_pos.z:
            return False

        # prevent from going inside the shape
        if cur_pos.x == next_pos.x:
            off_set = glm.ivec2(next_pos.y - cur_pos.y, next_pos.z - cur_pos.z)
            if self.is_wall(glm.ivec3(cur_pos.x, cur_pos.y, cur_pos.z + off_set.y)) and self.is_wall(
                    glm.ivec3(cur_pos.x, cur_pos.y + off_set.x, cur_pos.z)):
                return False

        if cur_pos.y == next_pos.y:
            off_set = glm.ivec2(next_pos.x - cur_pos.x, next_pos.z - cur_pos.z)
            if self.is_wall(glm.ivec3(cur_pos.x, cur_pos.y, cur_pos.z + off_set.y)) and self.is_wall(
                    glm.ivec3(cur_pos.x + off_set.x, cur_pos.y, cur_pos.z)):
                return False

        if cur_pos.z == next_pos.z:
            off_set = glm.ivec2(next_pos.x - cur_pos.x, next_pos.y - cur_pos.y)
            if self.is_wall(glm.ivec3(cur_pos.x + off_set.x, cur_pos.y, cur_pos.z)) and self.is_wall(
                    glm.ivec3(cur_pos.x, cur_pos.y + off_set.y, cur_pos.z)):
                return False

        return True

    def update_look_up(self):
        self.clear_look_up()

        for ent, (cube_comp) in esper.get_component(CubeComponent.CubeComponent):
            transform = esper.component_for_entity(ent, TransformComponent.TransformComponent)
            look_up_pos = glm.ivec3(transform.position)
            try:
                self.look_up[look_up_pos.x][look_up_pos.y][look_up_pos.z] = 1
            except:
                dy.log.error("Invalid cube position: " + str(look_up_pos))
                raise ValueError("Invalid cube position: " + str(look_up_pos))

        pass

    def clear_look_up(self):
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.length):
                    self.look_up[x][y][z] = 0
        pass

    def is_valid_position(self, pos: glm.ivec3):
        return pos.x >= 1 and pos.y >= 1 and pos.z >= 0 and pos.x <= self.width and pos.y <= self.height and pos.z < self.length

    def get_neighbors(self, current):
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if i == 0 and j == 0 and k == 0:
                        continue

                    if not self.is_moveable(current, glm.ivec3(current.x + i, current.y + j, current.z + k)):
                        continue

                    neighbors.append(glm.ivec3(current.x + i, current.y + j, current.z + k))

        return neighbors

    def create_passing_points(self, passing_point_positions):
        self.passing_points_ent = esper.create_entity()
        passing_points_comp = PassingPointsComponent.PassingPointsComponent(self)
        passing_points_comp.build_path(passing_point_positions)
        render_comp = RenderComponent.RenderComponent(ShaderManager.ShaderType.PASSING_POINT_SHADER,
                                                      self.app.shader_manager.get_shader(
                                                          ShaderManager.ShaderType.PASSING_POINT_SHADER))
        tag = NameTagComponent.NameTagComponent("passing points")
        esper.add_component(self.passing_points_ent, passing_points_comp)
        esper.add_component(self.passing_points_ent, render_comp)
        esper.add_component(self.passing_points_ent, tag)
        pass

    def create_shape(self, pivots):
        new_shape_ent = esper.create_entity()
        transform = TransformComponent.TransformComponent(glm.vec3(0, 0, 0))
        esper.add_component(new_shape_ent, transform)
        shape_comp = ShapeComponent.ShapeComponent(new_shape_ent, pivots, self)
        outline_comp = OutliningComponent.OutliningComponent(ShaderManager.ShaderType.SHAPE_OUTLINING_SHADER,
                                                             self.app.shader_manager.get_shader(
                                                                 ShaderManager.ShaderType.SHAPE_OUTLINING_SHADER))
        shape_comp.gl_init()
        render_comp = RenderComponent.RenderComponent(ShaderManager.ShaderType.SHAPE_SHADER,
                                                      self.app.shader_manager.get_shader(
                                                          ShaderManager.ShaderType.SHAPE_SHADER))

        motion_comp = MotionComponent.MotionComponent()

        esper.add_component(new_shape_ent, shape_comp)
        esper.add_component(new_shape_ent, render_comp)
        esper.add_component(new_shape_ent, NameTagComponent.NameTagComponent("shape"))
        esper.add_component(new_shape_ent, outline_comp)
        esper.add_component(new_shape_ent, motion_comp)

        self.shape_entities.append(new_shape_ent)

        for pos in shape_comp.cube_position:
            self.look_up[pos.x][pos.y][pos.z] = 1
        pass

    def clean_up(self):
        for ent in self.shape_entities:
            shape_comp = esper.component_for_entity(ent, ShapeComponent.ShapeComponent)
            shape_comp.clean_up()
            esper.delete_entity(ent, True)

        if self.start_ent != -1:
            esper.delete_entity(self.start_ent, True)

        if self.goal_ent != -1:
            esper.delete_entity(self.goal_ent, True)

        if self.passing_points_ent != -1:
            passing_points_comp = esper.component_for_entity(self.passing_points_ent, PassingPointsComponent.PassingPointsComponent)
            passing_points_comp.clean_up()
            esper.delete_entity(self.passing_points_ent, True)
        pass

    def reset_shapes_position(self):
        for ent in self.shape_entities:
            shape_comp = esper.component_for_entity(ent, ShapeComponent.ShapeComponent)
            shape_comp.reset_shape_position()
        pass