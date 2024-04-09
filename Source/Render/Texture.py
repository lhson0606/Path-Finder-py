from PIL import Image
import OpenGL.GL as gl
import Source.Render.Shader as Shader


class Texture:
    def __init__(self, tex_id: int):
        self.tex_id = int(tex_id)

    def bind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.tex_id)

    def load_to_slot(self, slot: int):
        gl.glActiveTexture(gl.GL_TEXTURE0 + slot)

    def unbind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def delete(self):
        gl.glDeleteTextures(self.tex_id)
