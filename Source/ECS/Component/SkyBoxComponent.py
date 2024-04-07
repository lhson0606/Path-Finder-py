import numpy as np
import OpenGL.GL as gl
import ctypes
from PIL import Image
import Source.Util.dy as dy
import glm

# https://learnopengl.com/code_viewer_gh.php?code=src/4.advanced_opengl/6.1.cubemaps_skybox/cubemaps_skybox.cpp


VERTICES = np.array([
    # positions
    -0.5, 0.5, -0.5,
    -0.5, -0.5, -0.5,
    0.5, -0.5, -0.5,
    0.5, -0.5, -0.5,
    0.5, 0.5, -0.5,
    -0.5, 0.5, -0.5,

    -0.5, -0.5, 0.5,
    -0.5, -0.5, -0.5,
    -0.5, 0.5, -0.5,
    -0.5, 0.5, -0.5,
    -0.5, 0.5, 0.5,
    -0.5, -0.5, 0.5,

    0.5, -0.5, -0.5,
    0.5, -0.5, 0.5,
    0.5, 0.5, 0.5,
    0.5, 0.5, 0.5,
    0.5, 0.5, -0.5,
    0.5, -0.5, -0.5,

    -0.5, -0.5, 0.5,
    -0.5, 0.5, 0.5,
    0.5, 0.5, 0.5,
    0.5, 0.5, 0.5,
    0.5, -0.5, 0.5,
    -0.5, -0.5, 0.5,

    -0.5, 0.5, -0.5,
    0.5, 0.5, -0.5,
    0.5, 0.5, 0.5,
    0.5, 0.5, 0.5,
    -0.5, 0.5, 0.5,
    -0.5, 0.5, -0.5,

    -0.5, -0.5, -0.5,
    -0.5, -0.5, 0.5,
    0.5, -0.5, -0.5,
    0.5, -0.5, -0.5,
    -0.5, -0.5, 0.5,
    0.5, -0.5, 0.5
], dtype=np.float32)

TEXTURES = [

    "Resources/Textures/skybox/right.jpg",
    "Resources/Textures/skybox/left.jpg",

    "Resources/Textures/skybox/front.jpg",
    "Resources/Textures/skybox/back.jpg",


    "Resources/Textures/skybox/top.jpg",
    "Resources/Textures/skybox/bottom.jpg",


]


def load_cube_map(textures):
    tex = int(gl.glGenTextures(1))
    gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, tex)

    for i in range(6):
        img = Image.open(textures[i])
        img = img.convert("RGB")
        img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        img_data = np.array(img, dtype=np.uint8)

        gl.glTexImage2D(gl.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, gl.GL_RGB, img.width, img.height, 0, gl.GL_RGB,
                        gl.GL_UNSIGNED_BYTE, img_data)
        pass

    gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP_TO_EDGE)

    return tex
    pass


def get_transformed_data(m: glm.mat4):
    res = np.zeros(VERTICES.shape, dtype=np.float32)
    for i in range(0, VERTICES.shape[0], 3):
        vec = glm.vec3(VERTICES[i], VERTICES[i + 1], VERTICES[i + 2])
        vec = glm.vec4(vec, 1) * m
        res[i] = vec.x
        res[i + 1] = vec.y
        res[i + 2] = vec.z
        pass
    return res
    pass


class SkyBoxComponent:
    def __init__(self):
        self.vao = int(gl.glGenVertexArrays(1))
        self.vbo = int(gl.glGenBuffers(1))
        self.texture = int(load_cube_map(TEXTURES))
        self.vertex_count = 36

        gl.glBindVertexArray(self.vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        # create a rotating matrix: 90 decrees along the x-axis
        # m = glm.rotate(glm.mat4(1), glm.radians(90), glm.vec3(1, 0, 0))
        # transformed_data = get_transformed_data(m)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, VERTICES.nbytes, VERTICES, gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)
        gl.glBindVertexArray(0)
        pass

    def clean_up(self):
        gl.glDeleteVertexArrays(1, self.vao)
        gl.glDeleteBuffers(1, self.vbo)
        gl.glDeleteTextures(1, self.texture)
        pass

    def __del__(self):
        pass
