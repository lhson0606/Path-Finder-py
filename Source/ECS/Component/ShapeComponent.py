import glm
import esper
import numpy as np
import OpenGL.GL as gl
import ctypes

import Source.ECS.Component.CubeComponent as CubeComponent
import Source.ECS.Component.TransformComponent as TransformComponent
import Source.ECS.Component.NameTagComponent as NameTagComponent

import Source.Algorithm.GreedyNoWall as GreedyNoWall

import Source.Map.Map as Map

import Source.Util.dy as dy


def get_new_cubes(shape_ent, new_pivot_pos: glm.ivec3):
    shape_comp = esper.component_for_entity(shape_ent, ShapeComponent)

    if len(shape_comp.pivots) == 1:
        return new_pivot_pos
    else:
        result = []
        temp = GreedyNoWall.a_star_search(shape_comp.pivots[-1], new_pivot_pos)
        result.extend(temp)
        temp = GreedyNoWall.a_star_search(new_pivot_pos, shape_comp.pivots[0])
        result.extend(temp)
        temp = set(result)
        result = list(temp)
        result.remove(shape_comp.pivots[0])
        result.remove(shape_comp.pivots[-1])
        return result
    pass

def add_cube(shape_entity, position: glm.vec3, pivot_index: int = -1):
    new_cube_entity = esper.create_entity()
    esper.add_component(new_cube_entity, CubeComponent.CubeComponent(shape_entity, pivot_index))
    esper.add_component(new_cube_entity, TransformComponent.TransformComponent(position))
    esper.add_component(new_cube_entity, NameTagComponent.NameTagComponent("cube"))
    return new_cube_entity
    pass


def build_cubes(shape_ent, pivots, cube_position):
    cubes = []

    if len(pivots) == 1:
        cubes.append(add_cube(shape_ent, pivots[0], 0))
    else:
        for i in range(0, len(pivots) - 1):
            nodes = GreedyNoWall.a_star_search(pivots[i], pivots[i + 1])
            for node in nodes:
                if node not in cube_position:
                    cube_position.append(node)
                    if node == pivots[i]:
                        cubes.append(add_cube(shape_ent, node, i))
                    else:
                        if node == pivots[i + 1]:
                            cubes.append(add_cube(shape_ent, node, i + 1))
                        else:
                            cubes.append(add_cube(shape_ent, node))

        nodes = GreedyNoWall.a_star_search(pivots[-1], pivots[0])
        for node in nodes:
            if node not in cube_position:
                cube_position.append(node)
                if node == pivots[0]:
                    cubes.append(add_cube(shape_ent, node, 0))
                else:
                    if node == pivots[-1]:
                        cubes.append(add_cube(shape_ent, node, len(pivots) - 1))
                    else:
                        cubes.append(add_cube(shape_ent, node))

    return cubes
    pass


class ShapeComponent:
    def __init__(self, ent_id, pivots: list[glm.ivec3], m: Map):
        self.pivots = pivots
        self.ent_id = ent_id
        # store unique cube position
        self.cube_position = []
        self.cubes = []
        self.vao = -1
        self.vbo_pos = -1
        self.vbo_tex = -1
        self.vbo_normal = -1
        self.vbo_model_col_0 = -1
        self.vbo_model_col_1 = -1
        self.vbo_model_col_2 = -1
        self.vbo_model_col_3 = -1
        self.ebo = -1
        self.vertex_count = 0
        self.map = m

    def gl_init(self):
        self.vao = int(gl.glGenVertexArrays(1))
        self.vbo_pos = int(gl.glGenBuffers(1))
        self.vbo_tex = int(gl.glGenBuffers(1))
        self.vbo_normal = int(gl.glGenBuffers(1))
        self.vbo_model_col_0 = int(gl.glGenBuffers(1))
        self.vbo_model_col_1 = int(gl.glGenBuffers(1))
        self.vbo_model_col_2 = int(gl.glGenBuffers(1))
        self.vbo_model_col_3 = int(gl.glGenBuffers(1))
        self.ebo = int(gl.glGenBuffers(1))

        self.generate_cubes()
        self.update_data()

    def recreate_gl(self):
        self.vao = int(gl.glGenVertexArrays(1))
        self.vbo_pos = int(gl.glGenBuffers(1))
        self.vbo_tex = int(gl.glGenBuffers(1))
        self.vbo_normal = int(gl.glGenBuffers(1))
        self.vbo_model_col_0 = int(gl.glGenBuffers(1))
        self.vbo_model_col_1 = int(gl.glGenBuffers(1))
        self.vbo_model_col_2 = int(gl.glGenBuffers(1))
        self.vbo_model_col_3 = int(gl.glGenBuffers(1))
        self.ebo = int(gl.glGenBuffers(1))

        self.vao = gl.glGenVertexArrays(1)
        self.vbo_pos = gl.glGenBuffers(1)
        self.vbo_tex = gl.glGenBuffers(1)
        self.vbo_normal = gl.glGenBuffers(1)
        self.vbo_model_col_0 = gl.glGenBuffers(1)
        self.vbo_model_col_1 = gl.glGenBuffers(1)
        self.vbo_model_col_2 = gl.glGenBuffers(1)
        self.vbo_model_col_3 = gl.glGenBuffers(1)
        self.ebo = gl.glGenBuffers(1)
    pass



    def generate_cubes(self):
        new_cubes = build_cubes(self.ent_id, self.pivots, self.cube_position)
        for cube in new_cubes:
            self.cubes.append(cube)
        self.vertex_count = len(self.cubes) * 36

    def update_data(self):

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

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_model_col_0)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.get_batch_transform_data(0), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(3, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(3)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_model_col_1)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.get_batch_transform_data(1), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(4, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(4)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_model_col_2)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.get_batch_transform_data(2), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(5, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(5)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_model_col_3)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.get_batch_transform_data(3), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(6, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(6)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.get_batch_indices_data(), gl.GL_STATIC_DRAW)

        gl.glBindVertexArray(0)
        pass

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

    def get_batch_transform_data(self, col: int):
        transforms = np.array([], dtype=np.float32)
        for cube in self.cubes:
            cube_transform = esper.component_for_entity(cube,
                                                        TransformComponent.TransformComponent).get_world_transform()
            for j in range(24):
                transforms = np.append(transforms, cube_transform[col])

        return transforms

    def get_batch_indices_data(self):
        indices = np.array([], dtype=np.uint32)
        count = 0

        for cube in self.cubes:
            indices = np.append(indices, CubeComponent.INDICES + 24 * count)
            count += 1

        return indices

    def get_batch_picking_position(self):
        position = np.array([], dtype=np.float32)

        for cube in self.cubes:
            position = np.append(position, CubeComponent.VERTICES)

        return position

    def get_batch_picking_normal(self):
        normals = np.array([], dtype=np.float32)

        for cube in self.cubes:
            normals = np.append(normals, CubeComponent.NORMALS)

        return normals

    def get_batch_picking_id(self):
        ids = np.array([], dtype=np.float32)

        for cube in self.cubes:
            for i in range(24):
                ids = np.append(ids, np.float32(cube))

        return ids

    def get_batch_picking_transform(self, col):
        transforms = np.array([], dtype=np.float32)
        for cube in self.cubes:
            cube_transform = esper.component_for_entity(cube,
                                                        TransformComponent.TransformComponent).get_world_transform()
            for j in range(24):
                transforms = np.append(transforms, cube_transform[col])

        return transforms

    def get_batch_picking_indices(self):
        indices = np.array([], dtype=np.uint32)
        count = 0

        for cube in self.cubes:
            indices = np.append(indices, CubeComponent.INDICES + 24 * count)
            count += 1

        return indices

    def move_pivot(self, pivot_index, position):
        if pivot_index == -1:
            return

        if self.pivots[pivot_index] == position:
            return

        self.pivots[pivot_index] = glm.ivec3(position)

        self.clear_all_none_pivot_cubes()
        self.generate_cubes()
        self.update_data()

        self.map.update_look_up()

        pass

    def clear_all_none_pivot_cubes(self):
        # destroy all none-pivot cubes
        # copy new list of cubes
        pivots_cube = []
        for cube in self.cubes:
            cube_comp = esper.component_for_entity(cube, CubeComponent.CubeComponent)
            if cube_comp.is_pivot():
                pivots_cube.append(cube)

        for cube in self.cubes:
            if cube not in pivots_cube:
                esper.delete_entity(cube, True)
        self.cubes = pivots_cube
        self.cube_position.clear()

        for p in self.pivots:
            self.cube_position.append(p)
    pass

    def add_pivot(self, position):
        new_pos = glm.ivec3(position)
        self.pivots.append(new_pos)

        # create new entity for pivot
        pivot_entity = esper.create_entity()
        esper.add_component(pivot_entity, CubeComponent.CubeComponent(self.ent_id, len(self.pivots) - 1))
        esper.add_component(pivot_entity, TransformComponent.TransformComponent(glm.vec3(position)))
        esper.add_component(pivot_entity, NameTagComponent.NameTagComponent("cube"))

        self.cubes.append(pivot_entity)

        self.clear_all_none_pivot_cubes()
        self.generate_cubes()
        self.recreate_gl()
        self.update_data()

        self.map.update_look_up()

        return pivot_entity
        pass

    def remove_pivot(self, pivot_index, ent):
        self.pivots.remove(self.pivots[pivot_index])
        self.cubes.remove(ent)
        esper.delete_entity(ent, True)
        self.clear_all_none_pivot_cubes()
        self.generate_cubes()
        self.recreate_gl()
        self.update_data()
        self.map.update_look_up()
        pass

    def clean_up(self):
        gl.glDeleteVertexArrays(1, self.vao)
        gl.glDeleteBuffers(1, self.vbo_pos)
        gl.glDeleteBuffers(1, self.vbo_tex)
        gl.glDeleteBuffers(1, self.vbo_normal)
        gl.glDeleteBuffers(1, self.vbo_model_col_0)
        gl.glDeleteBuffers(1, self.vbo_model_col_1)
        gl.glDeleteBuffers(1, self.vbo_model_col_2)
        gl.glDeleteBuffers(1, self.vbo_model_col_3)
        gl.glDeleteBuffers(1, self.ebo)
