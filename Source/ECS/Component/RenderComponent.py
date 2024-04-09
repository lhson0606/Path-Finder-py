import Source.Render.Shader as Shader
import Source.Manager.ShaderManager as ShaderManager


class RenderComponent:

    def __init__(self, shader_type: ShaderManager.ShaderType, shader: Shader.Shader):
        self.shader = shader
        self.shader_type = shader_type
