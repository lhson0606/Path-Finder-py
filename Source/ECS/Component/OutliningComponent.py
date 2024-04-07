import Source.Manager.ShaderManager as ShaderManager
import Source.Render.Shader as Shader


class OutliningComponent:
    def __init__(self, shader_type: ShaderManager.ShaderType, shader: Shader.Shader, should_draw_outline: bool = False):
        self._should_draw_outline = should_draw_outline
        self.shader_type = shader_type
        self.shader = shader

    def will_draw_outline(self):
        return self._should_draw_outline

    def set_draw_outline(self, should_draw_outline):
        self._should_draw_outline = should_draw_outline
        pass
