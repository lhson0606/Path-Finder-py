import Source.Render.Shader as Shader
import Source.Manager.ShaderManager as ShaderManager


class RenderComponent:

    def __init__(self, shader: Shader.Shader, shader_type: ShaderManager.ShaderType):
        self.shader = shader
        self.type = shader_type
