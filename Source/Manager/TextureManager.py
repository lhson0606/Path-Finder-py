import enum
from PIL import Image
import OpenGL.GL as gl
import Source.Render.Texture as Texture
import Source.Util.dy as dy

START_CUBE_TEXTURE_PATH = "Resources/Textures/start.png"
GOAL_CUBE_TEXTURE_PATH = "Resources/Textures/goal.png"

class TextureType(enum.Enum):
    START_CUBE = 0,
    GOAL_CUBE = 1,
    pass

PNG_FORMAT = "RGB"
JPEG_FORMAT = "RGBA"

class TextureManager:
    def __init__(self):
        self.textures = {}

    def get_texture(self, texture_type: TextureType):
        return self.textures[texture_type]

    def hard_load_all_textures(self):
        self.textures[TextureType.START_CUBE] = self.load_simple_texture(START_CUBE_TEXTURE_PATH, PNG_FORMAT)
        self.textures[TextureType.GOAL_CUBE] = self.load_simple_texture(GOAL_CUBE_TEXTURE_PATH, PNG_FORMAT)

    def load_simple_texture(self, path: str, format: str):
        img = Image.open(path)
        img = img.convert("RGB")
        img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        img_data = img.tobytes()

        tex_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex_id)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

        if format is JPEG_FORMAT:
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, img.width, img.height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img_data)
        else:
            if format is PNG_FORMAT:
                gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, img.width, img.height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img_data)
            else:
                dy.log.error("Unknown format")
                raise Exception("Unknown format")

        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

        dy.log.info("Texture loaded: %s", path)

        return Texture.Texture(tex_id)