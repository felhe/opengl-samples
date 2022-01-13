from OpenGL.GL import *
from OpenGL.GL.shaders import glDeleteShader


class ShaderProgram:
    def __init__(self):
        self.program = glCreateProgram()
        self.shaders = []

    def __exit__(self, exc_type, exc_val, exc_tb):
        for shader in self.shaders:
            glDeleteShader(shader)
        if self.program:
            glDeleteProgram(self.program)

    def add_shader(self, shader_src, shader_type):
        shader = glCreateShader(shader_type)
        if shader == 0:
            raise RuntimeError('Shader compilation failed: %s')
        self.shaders.append(shader)
        glShaderSource(shader, [shader_src])
        glCompileShader(shader)
        compiled = glGetShaderiv(shader, GL_COMPILE_STATUS)
        if compiled != GL_TRUE:
            info = glGetShaderInfoLog(shader)
            raise RuntimeError('Shader compilation failed: %s' % info)
        glAttachShader(self.program, shader)

    def link_shaders(self):
        glLinkProgram(self.program)
        linked = glGetProgramiv(self.program, GL_LINK_STATUS)
        if linked != GL_TRUE:
            info = glGetProgramInfoLog(self.program)
            raise RuntimeError('Shader compilation failed: %s' % info)
        self.use_program()

    def use_program(self):
        glUseProgram(self.program)

    def get_program_id(self):
        return self.program
