import esper

import Source.Util.dy as dy
import glm

import Source.ECS.Component.ShapeComponent as ShapeComponent
import Source.ECS.Component.RenderComponent as RenderComponent
import Source.ECS.Component.NameTagComponent as NameTagComponent
import Source.ECS.Component.OutliningComponent as OutliningComponent
import Source.ECS.Component.StartPointComponent as StartPointComponent
import Source.ECS.Component.GoalPointComponent as GoalPointComponent
import Source.Manager.ShaderManager as ShaderManager
import Source.ECS.Component.TransformComponent as TransformComponent
import Source.ECS.Component.CubeComponent as CubeComponent
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
        self.look_up = np.array([[[0 for _ in range(0, l+1)] for _ in range(0, h+1)] for _ in range(0, w+1)])
        self.is_draft = True
        self.goal_ent = -1
        self.start_ent = -1
        self.app = None
        self.passing_points = []

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

            self.look_up = np.array([[[0 for _ in range(0, self.length + 1)] for _ in range(0, self.height + 1)] for _ in range(0, self.width + 1)])

            self.create_start_point(glm.ivec3(int(lines[1].split(",")[0]), int(lines[1].split(",")[1]), 0))
            self.create_goal_point(glm.ivec3(int(lines[1].split(",")[2]), int(lines[1].split(",")[3]), 0))


            shape_count = int(lines[2].split(",")[0])

            for i in range(0, shape_count):
                line = lines[i + 3].strip()
                shape_data = line.split(",")
                if len(shape_data) == 0 or len(shape_data) % 2 != 0:
                    raise ValueError("Invalid shape data: " + line)
                pivots = []
                for j in range(0, len(shape_data), 2):
                    pivots.append(glm.ivec3(int(shape_data[j]), int(shape_data[j + 1]), 0))

                new_shape_ent = esper.create_entity()
                shape_comp = ShapeComponent.ShapeComponent(new_shape_ent, pivots, self)
                outline_comp = OutliningComponent.OutliningComponent(ShaderManager.ShaderType.SHAPE_OUTLINING_SHADER, shader_manager.get_shader(ShaderManager.ShaderType.SHAPE_OUTLINING_SHADER))
                shape_comp.gl_init()
                render_comp = RenderComponent.RenderComponent(ShaderManager.ShaderType.SHAPE_SHADER, shader_manager.get_shader(ShaderManager.ShaderType.SHAPE_SHADER))
                esper.add_component(new_shape_ent, shape_comp)
                esper.add_component(new_shape_ent, render_comp)
                esper.add_component(new_shape_ent, NameTagComponent.NameTagComponent("shape"))
                esper.add_component(new_shape_ent, outline_comp)


                for pos in shape_comp.cube_position:
                    self.look_up[pos.x][pos.y][pos.z] = 1

        except Exception as e:
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
        texture = self.app.texture_manager.get_texture(TextureManager.TextureType.START_CUBE)
        shader.use()
        shader.set_mat4("model", transform_comp.get_world_transform())
        shader.stop()
        start_point_component = StartPointComponent.StartPointComponent(texture)

        esper.add_component(self.start_ent, transform_comp)
        esper.add_component(self.start_ent, render_comp)
        esper.add_component(self.start_ent, NameTagComponent.NameTagComponent("start"))
        esper.add_component(self.start_ent, start_point_component)
        pass

    def create_goal_point(self, pos):
        self.goal = pos
        self.goal_ent = esper.create_entity()

        transform_comp = TransformComponent.TransformComponent(pos)
        shader = self.app.shader_manager.get_shader(ShaderManager.ShaderType.GOAL_POINT_SHADER)
        render_comp = RenderComponent.RenderComponent(ShaderManager.ShaderType.GOAL_POINT_SHADER, shader)
        texture = self.app.texture_manager.get_texture(TextureManager.TextureType.GOAL_CUBE)
        shader.use()
        shader.set_mat4("model", transform_comp.get_world_transform())
        shader.stop()
        goal_point_comp = GoalPointComponent.GoalPointComponent(texture)

        esper.add_component(self.goal_ent, transform_comp)
        esper.add_component(self.goal_ent, render_comp)
        esper.add_component(self.goal_ent, NameTagComponent.NameTagComponent("goal"))
        esper.add_component(self.goal_ent, goal_point_comp)
        pass

    def switch_context(self):
        transform_comp = esper.component_for_entity(self.start_ent, TransformComponent.TransformComponent)
        shader = self.app.shader_manager.get_shader(ShaderManager.ShaderType.GOAL_POINT_SHADER)
        shader.use()
        shader.set_mat4("model", transform_comp.get_world_transform())
        shader.stop()

        transform_comp = esper.component_for_entity(self.goal_ent, TransformComponent.TransformComponent)
        shader = self.app.shader_manager.get_shader(ShaderManager.ShaderType.START_POINT_SHADER)
        shader.use()
        shader.set_mat4("model", transform_comp.get_world_transform())
        shader.stop()

    def is_wall(self, pos: glm.ivec3):

        if pos.x < 1 or pos.y < 1 or pos.z < 0 or pos.x > self.width or pos.y > self.height or pos.z >= self.length:
            return True

        return self.look_up[pos.x][pos.y][pos.z] == 1

    def update_look_up(self):
        self.clear_look_up()

        for ent, (cube_comp) in esper.get_component(CubeComponent.CubeComponent):
            transform = esper.component_for_entity(ent, TransformComponent.TransformComponent)
            look_up_pos = glm.ivec3(transform.position)
            self.look_up[look_up_pos.x][look_up_pos.y][look_up_pos.z] = 1

        pass

    def clear_look_up(self):
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.length):
                    self.look_up[x][y][z] = 0
        pass
