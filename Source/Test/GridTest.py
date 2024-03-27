import glm
import OpenGL.GL as gl
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy

import Source.Render.Shader as Shader


class GridTest:
    VERTICES = numpy.array([
        0,    0,  0,
        50,   0,  0,
        50,   0,  50,
        0,    0,  50,
    ], dtype=numpy.float32)

    TEXT_COORDS = numpy.array([
        0, 0,
        1, 0,
        1, 1,
        0, 1,
    ], dtype=numpy.float32)

    INDICES = numpy.array([
        0, 3, 2,
        0, 2, 1,
    ], dtype=numpy.uint)

    def __init__(self):
        self.vao = -1
        self.vbo_pos = -1
        self.vbo_text_coords = -1
        self.ebo = -1

    def create(self):
        self.vao = gl.glGenVertexArrays(1)
        self.vbo_pos = gl.glGenBuffers(1)
        self.vbo_text_coords = gl.glGenBuffers(1)
        self.ebo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_pos)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.VERTICES, gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_text_coords)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.TEXT_COORDS, gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(1)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.INDICES, gl.GL_STATIC_DRAW)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    def load_projection_matrix(self, shader: Shader, inp_projection: glm.mat4):
        shader.use()
        shader.set_mat4("projection", inp_projection)
        shader.stop()

    def load_view_matrix(self, shader: Shader, view: glm.mat4):
        shader.use()
        shader.set_mat4("view", view)
        shader.stop()

    def render(self, shader: Shader):
        shader.use()
        gl.glBindVertexArray(self.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT,  ctypes.c_void_p(0))
        gl.glBindVertexArray(0)
        shader.stop()

    def clean_up(self):
        gl.glDeleteVertexArrays(1, [self.vao])
        gl.glDeleteBuffers(1, [self.vbo_pos])
        gl.glDeleteBuffers(1, [self.vbo_text_coords])
        gl.glDeleteBuffers(1, [self.ebo])
        pass
