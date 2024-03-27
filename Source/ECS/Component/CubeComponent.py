import glm
import numpy as np
import OpenGL.GL as gl
import ctypes
import esper

# Define vertices, texture coordinates, and normals for a unit cube
VERTICES = np.array([
    # Front face
    [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5],
    # Back face
    [-0.5, -0.5, -0.5], [-0.5, 0.5, -0.5], [0.5, 0.5, -0.5], [0.5, -0.5, -0.5],
    # Top face
    [-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, -0.5],
    # Bottom face
    [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, -0.5, 0.5], [-0.5, -0.5, 0.5],
    # Right face
    [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [0.5, 0.5, 0.5], [0.5, -0.5, 0.5],
    # Left face
    [-0.5, -0.5, -0.5], [-0.5, -0.5, 0.5], [-0.5, 0.5, 0.5], [-0.5, 0.5, -0.5]
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


class CubeComponent:
    def __init__(self, shape_entity):
        self.is_selected: bool = False
        self.shape_entity = shape_entity
