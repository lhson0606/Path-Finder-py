import glm
import OpenGL.GL as gl
from OpenGL.GLU import *
import numpy


VERTICES = numpy.array([
        # width         #height
        0,      0,      0,
        1,      0,      0,
        1,      0,      1,
        0,      0,      1,
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


def get_vertices(width, height):
    return numpy.array([
        0, 0, 0,
        width, 0, 0,
        width, 0, height,
        0, 0, height,
    ], dtype=numpy.float32)


class GridComponent:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.vao = gl.glGenVertexArrays(1)
        self.vbo_pos = gl.glGenVertexArrays(1)
        self.vbo_text_coords = gl.glGenVertexArrays(1)
        self.ebo = gl.glGenBuffers(1)

        gl.glGenBuffers(1)
        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_pos)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, get_vertices(self.width, self.height), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_text_coords)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, TEXT_COORDS, gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(1)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, INDICES, gl.GL_STATIC_DRAW)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    def resize(self, width, height):
        self.width = width
        self.height = height

        gl.glBindVertexArray(self.vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_pos)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, get_vertices(self.width, self.height), gl.GL_STATIC_DRAW)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    def clear(self, x, y):

        self.vao = -1
        self.vbo_pos = -1
        self.vbo_text_coords = -1
        self.ebo = -1

        gl.glDeleteVertexArrays(1, [self.vao])
        gl.glDeleteBuffers(1, [self.vbo_pos])
        gl.glDeleteBuffers(1, [self.vbo_text_coords])
        gl.glDeleteBuffers(1, [self.ebo])
        pass