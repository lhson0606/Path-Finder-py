import glm
import esper
import numpy as np
import OpenGL.GL as gl
import ctypes

import Source.ECS.Component.CubeComponent as CubeComponent
import Source.ECS.Component.TransformComponent as TransformComponent

import Source.Algorithm.AStarNoWall as AStarNoWall


def add_cube(shape_entity, position: glm.vec3):
    new_cube_entity = esper.create_entity()
    esper.add_component(new_cube_entity, CubeComponent.CubeComponent(shape_entity))
    esper.add_component(new_cube_entity, TransformComponent.TransformComponent(position))
    return new_cube_entity
    pass


def build_cubes(shape_ent, pivots, cube_position):
    cubes = []

    if len(pivots) == 1:
        cubes.append(add_cube(shape_ent, pivots[0]))
    else:
        for i in range(0, len(pivots) - 1):
            nodes = AStarNoWall.a_star_search(pivots[i], pivots[i + 1])
            for node in nodes:
                if node not in cube_position:
                    cube_position.append(node)
                    cubes.append(add_cube(shape_ent, node))

        nodes = AStarNoWall.a_star_search(pivots[-1], pivots[0])
        for node in nodes:
            cubes.append(add_cube(shape_ent, node))

    return cubes
    pass


class ShapeComponent:
    def __init__(self, ent_id, pivots: list[glm.ivec3]):
        self.pivots = []
        self.ent_id = ent_id
        # store unique cube position
        self.cube_position = []
        self.cubes = build_cubes(self.ent_id, pivots, self.cube_position)
        self.vao = -1
        self.vbo_pos = -1
        self.vbo_tex = -1
        self.vbo_normal = -1
        self.vbo_model = -1
        self.ebo = -1
        self.vertex_count = len(self.cubes) * 36

    def gl_init(self):
        self.vao = gl.glGenVertexArrays(1)
        self.vbo_pos = gl.glGenBuffers(1)
        self.vbo_tex = gl.glGenBuffers(1)
        self.vbo_normal = gl.glGenBuffers(1)
        self.vbo_model = gl.glGenBuffers(1)
        self.ebo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_pos)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.get_batch_position_data(), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_tex)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.get_batch_tex_coord_data(), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_normal)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.get_batch_normal_data(), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(2, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(2)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_model)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.get_batch_transform_data(), gl.GL_STATIC_DRAW)
        for i in range(4):
            gl.glEnableVertexAttribArray(i + 3)

            # Specify the format of your mat4 data
            gl.glVertexAttribPointer(i + 3, 4, gl.GL_FLOAT, gl.GL_FALSE, 64, ctypes.c_void_p(i * 16))

            # Tell OpenGL that this is instanced data
            gl.glVertexAttribDivisor(i + 3, 1)
        gl.glEnableVertexAttribArray(3)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.get_batch_indices_data(), gl.GL_STATIC_DRAW)

        gl.glBindVertexArray(0)

    def get_batch_position_data(self):
        position = np.array([], dtype=np.float32)

        for cube in self.cubes:
            position = np.append(position, CubeComponent.VERTICES)

        return position

    def get_batch_tex_coord_data(self):
        tex_coords = np.array([], dtype=np.float32)

        for cube in self.cubes:
            tex_coords = np.append(tex_coords, CubeComponent.TEXTURE_COORDS)

        return tex_coords

    def get_batch_normal_data(self):
        normals = np.array([], dtype=np.float32)

        for cube in self.cubes:
            normals = np.append(normals, CubeComponent.NORMALS)

        return normals

    def get_batch_transform_data(self):
        transforms = np.array([], dtype=np.float32)

        for cube in self.cubes:
            cube_transform = esper.component_for_entity(cube,
                                                        TransformComponent.TransformComponent).get_world_transform()
            transforms = np.append(transforms, cube_transform)

        return transforms

    def get_batch_indices_data(self):
        indices = np.array([], dtype=np.uint32)

        for cube in self.cubes:
            indices = np.append(indices, CubeComponent.INDICES + len(indices))

        return indices

    def clean_up(self):
        gl.glDeleteVertexArrays(1, self.vao)
        gl.glDeleteBuffers(1, self.vbo_pos)
        gl.glDeleteBuffers(1, self.vbo_tex)
        gl.glDeleteBuffers(1, self.vbo_normal)
        gl.glDeleteBuffers(1, self.vbo_model)
        gl.glDeleteBuffers(1, self.ebo)