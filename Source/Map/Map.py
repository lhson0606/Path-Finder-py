import esper

import Source.Util.dy as dy
import glm

import Source.ECS.Component.ShapeComponent as ShapeComponent
import Source.ECS.Component.RenderComponent as RenderComponent
import Source.ECS.Component.NameTagComponent as NameTagComponent
import Source.ECS.Component.OutliningComponent as OutliningComponent
import Source.Manager.ShaderManager as ShaderManager
import Source.Render.Shader as Shader
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
        self.look_up = np.array([[[0 for _ in range(l)] for _ in range(h)] for _ in range(w)])
        self.is_draft = True

    def create(self):
        count = 0

        pass

    def load(self, shader_type: ShaderManager.ShaderType, shape_shader: Shader, outlining_type: ShaderManager.ShaderType, outlining_shader: Shader):
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
            self.start = glm.ivec2(int(lines[1].split(",")[0]), int(lines[1].split(",")[1]))
            self.goal = glm.ivec2(int(lines[1].split(",")[2]), int(lines[1].split(",")[3]))


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
                shape_comp = ShapeComponent.ShapeComponent(new_shape_ent, pivots)
                outline_comp = OutliningComponent.OutliningComponent(outlining_type, outlining_shader)
                shape_comp.gl_init()
                render_comp = RenderComponent.RenderComponent(shape_shader, shader_type)
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
