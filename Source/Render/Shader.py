import glm
import OpenGL.GL as gl
import Source.Util.dy as dy


class Shader:
    def __init__(self, vertex_path, fragment_path):
        self.id = 0
        self.vertex_path = vertex_path
        self.fragment_path = fragment_path
        self.__compile_shader(self.vertex_path, self.fragment_path)
        self.uni_cache = {}

    def __compile_shader(self, vertex_path, fragment_path):
        vertex_code = dy.read_text(vertex_path)
        fragment_code = dy.read_text(fragment_path)

        vertex = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(vertex, vertex_code)
        gl.glCompileShader(vertex)
        if not gl.glGetShaderiv(vertex, gl.GL_COMPILE_STATUS):
            info_log = gl.glGetShaderInfoLog(vertex)
            dy.log.error("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n", info_log)
            raise Exception("Vertex shader compilation failed")

        fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(fragment, fragment_code)
        gl.glCompileShader(fragment)
        if not gl.glGetShaderiv(fragment, gl.GL_COMPILE_STATUS):
            info_log = gl.glGetShaderInfoLog(fragment)
            dy.log.error("ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n", info_log)
            raise Exception("Fragment shader compilation failed")

        self.id = gl.glCreateProgram()
        gl.glAttachShader(self.id, vertex)
        gl.glAttachShader(self.id, fragment)
        gl.glLinkProgram(self.id)
        if not gl.glGetProgramiv(self.id, gl.GL_LINK_STATUS):
            info_log = gl.glGetProgramInfoLog(self.id)
            dy.log.error("ERROR::SHADER::PROGRAM::LINKING_FAILED\n", info_log)
            raise Exception("Shader linking failed")
        gl.glDeleteShader(vertex)
        gl.glDeleteShader(fragment)

        dy.log.info(f"Shader compiled: {vertex_path} | {fragment_path}")

    def use(self):
        gl.glUseProgram(self.id)

    def stop(self):
        gl.glUseProgram(0)

    def get_uniform_location(self, name):
        if name in self.uni_cache:
            return self.uni_cache[name]
        location = gl.glGetUniformLocation(self.id, name)
        if location == -1:
            dy.log.error(f"Uniform {name} not found in " + self.vertex_path + " | " + self.fragment_path)

        self.uni_cache[name] = location
        return location

    def set_bool(self, name, value):
        gl.glUniform1i(self.get_uniform_location(name), value)

    def set_int(self, name, value):
        gl.glUniform1i(self.get_uniform_location(name), value)

    def set_float(self, name, value):
        gl.glUniform1f(self.get_uniform_location(name), value)

    def set_vec2(self, name, value):
        gl.glUniform2fv(self.get_uniform_location(name), 1, glm.value_ptr(value))

    def set_vec3(self, name, value):
        gl.glUniform3fv(self.get_uniform_location(name), 1, glm.value_ptr(value))

    def set_vec4(self, name, value):
        gl.glUniform4fv(self.get_uniform_location(name), 1, glm.value_ptr(value))

    def set_mat4(self, name, value):
        gl.glUniformMatrix4fv(self.get_uniform_location(name), 1, gl.GL_FALSE, glm.value_ptr(value))

