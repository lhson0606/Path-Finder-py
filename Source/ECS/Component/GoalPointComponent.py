import numpy as np
import glm
import OpenGL.GL as gl
import ctypes
import Source.Render.Texture as Texture

VERTICES = np.array([
    # Front face
    [-1, -1, 1], [0, -1, 1], [0, 0, 1], [-1, 0, 1],
    # Back face
    [-1, -1, 0], [-1, 0, 0], [0, 0, 0], [0, -1, 0],
    # Top face
    [-1, 0, 0], [-1, 0, 1], [0, 0, 1], [0, 0, 0],
    # Bottom face
    [-1, -1, 0], [0, -1, 0], [0, -1, 1], [-1, -1, 1],
    # Right face
    [0, -1, 0], [0, 0, 0], [0, 0, 1], [0, -1, 1],
    # Left face
    [-1, -1, 0], [-1, -1, 1], [-1, 0, 1], [-1, 0, 0]
], dtype=np.float32)

TEXTURE_COORDS = np.array([
    # Front face
    [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0],
    # Back face
    [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0],
    # Top face
    [0.0, 1.0], [0.0, 0.0], [1.0, 0.0], [1.0, 1.0],
    # Bottom face
    [1.0, 1.0], [0.0, 1.0], [0.0, 0.0], [1.0, 0.0],
    # Right face
    [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0],
    # Left face
    [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]
], dtype=np.float32)

NORMALS = np.array([
    # Front face
    [0.0, 0.0, 1.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0],
    # Back face
    [0.0, 0.0, -1.0], [0.0, 0.0, -1.0], [0.0, 0.0, -1.0], [0.0, 0.0, -1.0],
    # Top face
    [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0],
    # Bottom face
    [0.0, -1.0, 0.0], [0.0, -1.0, 0.0], [0.0, -1.0, 0.0], [0.0, -1.0, 0.0],
    # Right face
    [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 0.0, 0.0],
    # Left face
    [-1.0, 0.0, 0.0], [-1.0, 0.0, 0.0], [-1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]
], dtype=np.float32)

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


class GoalPointComponent:
    def __init__(self, texture: Texture):
        self.vao = int(gl.glGenVertexArrays(1))
        self.vbo_pos = int(gl.glGenBuffers(1))
        self.vbo_tex_coords = int(gl.glGenBuffers(1))
        self.ebo = int(gl.glGenBuffers(1))
        self.vertex_count = 36
        self.texture = texture

        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_pos)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, VERTICES, gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_tex_coords)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, TEXTURE_COORDS, gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(1)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, INDICES, gl.GL_STATIC_DRAW)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    def clean_up(self):
        gl.glDeleteVertexArrays(1, [self.vao])
        gl.glDeleteBuffers(1, [self.vbo_pos])
        gl.glDeleteBuffers(1, [self.vbo_tex_coords])
        gl.glDeleteBuffers(1, [self.ebo])
        pass


