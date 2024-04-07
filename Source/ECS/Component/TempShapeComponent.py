import OpenGL.GL as gl
import ctypes
import glm
import numpy as np

import Source.ECS.Component.CubeComponent as CubeComponent

# VERTICES = np.array([
#     # Front face
#     [-0.5, -0.5, 0.5], [0, -0.5, 0.5], [0, 0, 1], [-1, 0, 1],
#     # Back face
#     [-1, -1, 0], [-1, 0, 0], [0, 0, 0], [0, -1, 0],
#     # Top face
#     [-1, 0, 0], [-1, 0, 1], [0, 0, 1], [0, 0, 0],
#     # Bottom face
#     [-1, -1, 0], [0, -1, 0], [0, -1, 1], [-1, -1, 1],
#     # Right face
#     [0, -1, 0], [0, 0, 0], [0, 0, 1], [0, -1, 1],
#     # Left face
#     [-1, -1, 0], [-1, -1, 1], [-1, 0, 1], [-1, 0, 0]
# ], dtype=np.float32)



class TempShapeComponent:
    def __init__(self, positions):
        self.vao = -1
        self.vbo_pos = -1
        self.vbo_model_col_0 = -1
        self.vbo_model_col_1 = -1
        self.vbo_model_col_2 = -1
        self.vbo_model_col_3 = -1
        self.ebo = -1
        self.positions = positions
        self.vertex_count = len(positions) * 36
        self.load()

    def load(self):
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
        gl.glVertexAttribPointer(1, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_model_col_1)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.get_batch_transform_data(1), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(2, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(2)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_model_col_2)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.get_batch_transform_data(2), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(3, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(3)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_model_col_3)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.get_batch_transform_data(3), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(4, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(4)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.get_batch_indices_data(), gl.GL_STATIC_DRAW)

        gl.glBindVertexArray(0)
        pass

    def get_batch_position_data(self):
        position = np.array([], dtype=np.float32)

        for i in range(len(self.positions)):
            position = np.append(position, CubeComponent.VERTICES)

        return position

    def get_batch_transform_data(self, col: int):
        transforms = np.array([], dtype=np.float32)
        for pos in self.positions:
            trans_mat = glm.translate(glm.mat4(1), glm.vec3(pos))
            for j in range(24):
                transforms = np.append(transforms, trans_mat[col])

        return transforms

    def get_batch_indices_data(self):
        indices = np.array([], dtype=np.uint32)
        count = 0

        for i in range(len(self.positions)):
            indices = np.append(indices, CubeComponent.INDICES + 24 * count)
            count += 1

        return indices

    def clean_up(self):
        gl.glDeleteVertexArrays(1, self.vao)
        gl.glDeleteBuffers(1, self.vbo_pos)
        gl.glDeleteBuffers(1, self.vbo_model_col_0)
        gl.glDeleteBuffers(1, self.vbo_model_col_1)
        gl.glDeleteBuffers(1, self.vbo_model_col_2)
        gl.glDeleteBuffers(1, self.vbo_model_col_3)
        gl.glDeleteBuffers(1, self.ebo)
        pass

