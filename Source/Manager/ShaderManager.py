from enum import Enum
import Source.Render.Shader as Shader
import Source.Util.dy as dy

TEST_SHADER_VERT_PATH = "Resources/GLSL/test_shader.vert"
TEST_SHADER_FRAG_PATH = "Resources/GLSL/test_shader.frag"
GRID_SHADER_VERT_PATH = "Resources/GLSL/grid.vert"
GRID_SHADER_FRAG_PATH = "Resources/GLSL/grid.frag"
SHAPE_SHADER_VERT_PATH = "Resources/GLSL/shape.vert"
SHAPE_SHADER_FRAG_PATH = "Resources/GLSL/shape.frag"


class ShaderType(Enum):
    SELF_TEST_SHADER = 0
    CUBE_SHADER = 1
    GRID_SHADER = 2
    SHAPE_SHADER = 3

class ShaderManager:

    def __init__(self):
        self.shaders = {}

    def load_shaders(self, shader_type, vertex_path, fragment_path):
        self.shaders[shader_type] = Shader.Shader(vertex_path, fragment_path)

    def get_shader(self, shader_type):
        if shader_type not in self.shaders:
            dy.log.error(f"Shader not found: {shader_type}")
            raise Exception("Shader not found")

        return self.shaders[shader_type]

    def hard_load_all_shaders(self):
        self.load_shaders(ShaderType.SELF_TEST_SHADER, TEST_SHADER_VERT_PATH, TEST_SHADER_FRAG_PATH)
        self.load_shaders(ShaderType.GRID_SHADER, GRID_SHADER_VERT_PATH, GRID_SHADER_FRAG_PATH)
        self.load_shaders(ShaderType.SHAPE_SHADER, SHAPE_SHADER_VERT_PATH, SHAPE_SHADER_FRAG_PATH)
