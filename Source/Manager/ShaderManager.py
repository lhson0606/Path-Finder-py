from enum import Enum
import Source.Render.Shader as Shader
import Source.Util.dy as dy

TEST_SHADER_VERT_PATH = "Resources/GLSL/test_shader.vert"
TEST_SHADER_FRAG_PATH = "Resources/GLSL/test_shader.frag"
GRID_SHADER_VERT_PATH = "Resources/GLSL/grid.vert"
GRID_SHADER_FRAG_PATH = "Resources/GLSL/grid.frag"
SHAPE_SHADER_VERT_PATH = "Resources/GLSL/shape.vert"
SHAPE_SHADER_FRAG_PATH = "Resources/GLSL/shape.frag"
PICKING_DATA_SHADER_VERT_PATH = "Resources/GLSL/picking_data.vert"
PICKING_DATA_SHADER_FRAG_PATH = "Resources/GLSL/picking_data.frag"
TEMP_SHAPE_SHADER_VERT_PATH = "Resources/GLSL/temp_shape.vert"
TEMP_SHAPE_SHADER_FRAG_PATH = "Resources/GLSL/temp_shape.frag"
SKY_BOX_SHADER_VERT_PATH = "Resources/GLSL/sky_box.vert"
SKY_BOX_SHADER_FRAG_PATH = "Resources/GLSL/sky_box.frag"
SHAPE_OUTLINING_SHADER_VERT_PATH = "Resources/GLSL/shape_outlining.vert"
SHAPE_OUTLINING_SHADER_FRAG_PATH = "Resources/GLSL/shape_outlining.frag"
START_POINT_SHADER_VERT_PATH = "Resources/GLSL/start_point.vert"
START_POINT_SHADER_FRAG_PATH = "Resources/GLSL/start_point.frag"
GOAL_POINT_SHADER_VERT_PATH = "Resources/GLSL/goal_point.vert"
GOAL_POINT_SHADER_FRAG_PATH = "Resources/GLSL/goal_point.frag"
PATH_POINT_SHADER_VERT_PATH = "Resources/GLSL/path_point.vert"
PATH_POINT_SHADER_FRAG_PATH = "Resources/GLSL/path_point.frag"
PASSING_POINT_SHADER_VERT_PATH = "Resources/GLSL/passing_point.vert"
PASSING_POINT_SHADER_FRAG_PATH = "Resources/GLSL/passing_point.frag"


class ShaderType(Enum):
    SELF_TEST_SHADER = 0
    CUBE_SHADER = 1
    GRID_SHADER = 2
    SHAPE_SHADER = 3
    PICKING_DATA_SHADER = 4
    TEMP_SHAPE_SHADER = 5
    SKY_BOX_SHADER = 6
    SHAPE_OUTLINING_SHADER = 7
    START_POINT_SHADER = 8
    GOAL_POINT_SHADER = 9
    PATH_POINT_SHADER = 10
    PASSING_POINT_SHADER = 11

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
        self.load_shaders(ShaderType.PICKING_DATA_SHADER, PICKING_DATA_SHADER_VERT_PATH, PICKING_DATA_SHADER_FRAG_PATH)
        self.load_shaders(ShaderType.TEMP_SHAPE_SHADER, TEMP_SHAPE_SHADER_VERT_PATH, TEMP_SHAPE_SHADER_FRAG_PATH)
        self.load_shaders(ShaderType.SKY_BOX_SHADER, SKY_BOX_SHADER_VERT_PATH, SKY_BOX_SHADER_FRAG_PATH)
        self.load_shaders(ShaderType.SHAPE_OUTLINING_SHADER, SHAPE_OUTLINING_SHADER_VERT_PATH, SHAPE_OUTLINING_SHADER_FRAG_PATH)
        self.load_shaders(ShaderType.START_POINT_SHADER, START_POINT_SHADER_VERT_PATH, START_POINT_SHADER_FRAG_PATH)
        self.load_shaders(ShaderType.GOAL_POINT_SHADER, GOAL_POINT_SHADER_VERT_PATH, GOAL_POINT_SHADER_FRAG_PATH)
        self.load_shaders(ShaderType.PATH_POINT_SHADER, PATH_POINT_SHADER_VERT_PATH, PATH_POINT_SHADER_FRAG_PATH)
        self.load_shaders(ShaderType.PASSING_POINT_SHADER, PASSING_POINT_SHADER_VERT_PATH, PASSING_POINT_SHADER_FRAG_PATH)
