import Source.Map.Map as Map
import glm
import Source.ECS.Component.TransformComponent as TransformComponent
import Source.ECS.Component.NameTagComponent as NameTagComponent
import Source.App as App
import esper
import numpy as np
import OpenGL.GL as gl
import ctypes

translation_vector = np.array([-0.125, -0.125, 0.125], dtype=np.float32)

VERTICES = np.array([
    # Front face
    [-0.75, -0.75, 0.75], [0, -0.75, 0.75], [0, 0, 0.75], [-0.75, 0, 0.75],
    # Back face
    [-0.75, -0.75, 0], [-0.75, 0, 0], [0, 0, 0], [0, -0.75, 0],
    # Top face
    [-0.75, 0, 0], [-0.75, 0, 0.75], [0, 0, 0.75], [0, 0, 0],
    # Bottom face
    [-0.75, -0.75, 0], [0, -0.75, 0], [0, -0.75, 0.75], [-0.75, -0.75, 0.75],
    # Right face
    [0, -0.75, 0], [0, 0, 0], [0, 0, 0.75], [0, -0.75, 0.75],
    # Left face
    [-0.75, -0.75, 0], [-0.75, -0.75, 0.75], [-0.75, 0, 0.75], [-0.75, 0, 0]
], dtype=np.float32)

# Add the translation vector to each vertex
VERTICES = VERTICES + translation_vector

INDICES = np.array([
    # Front face
    0, 1, 2, 2, 3, 0,
    # Back face
    4, 5, 6, 6, 7, 4,
    # Top face
    8, 9, 10, 10, 11, 8,
    # Bottom face
    12, 13, 14, 14, 15, 12,
    # Right face
    16, 17, 18, 18, 19, 16,
    # Left face
    20, 21, 22, 22, 23, 20
], dtype=np.uint32)


class PassingPointsComponent:
    def __init__(self, map: Map):
        self.vao = -1
        self.vbo_pos = -1
        self.vbo_model_col_0 = -1
        self.vbo_model_col_1 = -1
        self.vbo_model_col_2 = -1
        self.vbo_model_col_3 = -1
        self.ebo = -1
        self.entities = []
        self.map = map
        self.vertex_count = 0

    def build_path(self, positions):
        self.clean_up()

        for pos in positions:
            self.create_passing_point(pos)

        self.vao = int(gl.glGenVertexArrays(1))
        self.vbo_pos = int(gl.glGenBuffers(1))
        self.vbo_model_col_0 = int(gl.glGenBuffers(1))
        self.vbo_model_col_1 = int(gl.glGenBuffers(1))
        self.vbo_model_col_2 = int(gl.glGenBuffers(1))
        self.vbo_model_col_3 = int(gl.glGenBuffers(1))
        self.ebo = int(gl.glGenBuffers(1))

        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_pos)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.get_batch_position_data(), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

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

        gl.glEnableVertexAttribArray(0)

        self.vertex_count = len(positions) * 36

        pass

    def create_passing_point(self, pos: glm.vec3):
        new_ent = esper.create_entity()
        self.entities.append(new_ent)
        transform = TransformComponent.TransformComponent(pos)
        tag = NameTagComponent.NameTagComponent("passing point")

        esper.add_component(new_ent, transform)
        esper.add_component(new_ent, tag)

        pass

    def clean_up(self):
        for ent in self.entities:
            esper.delete_entity(ent)

        gl.glDeleteVertexArrays(1, [self.vao])
        gl.glDeleteBuffers(1, [self.vbo_pos])
        gl.glDeleteBuffers(1, [self.vbo_model_col_0])
        gl.glDeleteBuffers(1, [self.vbo_model_col_1])
        gl.glDeleteBuffers(1, [self.vbo_model_col_2])
        gl.glDeleteBuffers(1, [self.vbo_model_col_3])
        gl.glDeleteBuffers(1, [self.ebo])

        self.vao = -1
        self.vbo_pos = -1
        self.ebo = -1

        pass

    def get_batch_position_data(self):
        position = np.array([], dtype=np.float32)

        for e in self.entities:
            position = np.append(position, VERTICES)

        return position

    def get_batch_indices_data(self):
        indices = np.array([], dtype=np.uint32)
        count = 0

        for e in self.entities:
            indices = np.append(indices, INDICES + 24 * count)
            count += 1

        return indices

    def get_batch_transform_data(self, col: int):
        transforms = np.array([], dtype=np.float32)
        for e in self.entities:
            cube_transform = esper.component_for_entity(e,
                                                        TransformComponent.TransformComponent).get_world_transform()
            for j in range(24):
                transforms = np.append(transforms, cube_transform[col])

        return transforms
