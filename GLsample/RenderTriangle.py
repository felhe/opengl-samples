import math
import os
from random import random

import numpy as np
from OpenGL.GL import *
from numpy import float32, int32

from Render import Render
from ShaderProgram import ShaderProgram


class RenderTriangle(Render):
    index_list = np.array([
        0, 4, 1,
        0, 9, 4,
        9, 5, 4,
        4, 5, 8,
        4, 8, 1,
        8, 10, 1,
        8, 3, 10,
        5, 3, 8,
        5, 2, 3,
        2, 7, 3,
        7, 10, 3,
        7, 6, 10,
        7, 11, 6,
        11, 0, 6,
        0, 1, 6,
        6, 1, 10,
        9, 0, 11,
        9, 11, 2,
        9, 2, 5,
        7, 2, 11,
    ], dtype=int32)

    x = 0.52573111212
    z = 0.85065080835
    vertex_list = np.array([
        -x, 0, z,
        x, 0, z,
        -x, 0, -z,
        x, 0, -z,
        0, z, x,
        0, z, -x,
        0, -z, x,
        0, -z, -x,
        z, x, 0,
        -z, x, 0,
        z, -x, 0,
        -z, -x, 0,
    ], dtype=float32)

    color_data = []

    def __init__(self):
        self.model_view_matrix = []
        self.projection_matrix = []
        self.fbo = 0
        self.vao = 0
        self.vbo_indices = 0
        self.vbo_coords = 0
        self.color_attrib_position = 0
        self.vertex_attrib_position = 0
        self.model_view_matrix_id = 0
        self.rot_y_value = 0.0
        self.rot_x_value = 0.0
        self.trans_z_value = -10.0
        self.projection_matrix_id = 0
        self.far_distance = 15.0
        self.height_angle = 0.4
        self.near_distance = 5.0
        self.width = 800
        self.height = 600
        self.shader_program = ShaderProgram()

        # vertex shader program
        with open(os.path.join(os.path.dirname(__file__), 'shaders/triangle.vert'), 'r') as file:
            self.vertex_shader_src = file.read()

        # fragment shader program
        with open(os.path.join(os.path.dirname(__file__), 'shaders/triangle.frag'), 'r') as file:
            self.fragment_shader_src = file.read()

        self.generate_color()

    def set_window_size(self, width: int, height: int):
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)
        self.render_camera()

    def init_gl(self):
        # create program and link
        self.shader_program.add_shader(self.vertex_shader_src, GL_VERTEX_SHADER)
        self.shader_program.add_shader(self.fragment_shader_src, GL_FRAGMENT_SHADER)
        self.shader_program.link_shaders()

        # determine bindings with shader
        self.vertex_attrib_position = glGetAttribLocation(self.shader_program.get_program_id(), "in_Position")
        self.color_attrib_position = glGetAttribLocation(self.shader_program.get_program_id(), "color")
        self.projection_matrix_id = glGetUniformLocation(self.shader_program.get_program_id(), "cProjectionMatrix")
        self.model_view_matrix_id = glGetUniformLocation(self.shader_program.get_program_id(), "cModelviewMatrix")

        # create object

        # create vertex array object
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # create buffer object for indices
        self.vbo_indices = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbo_indices)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.index_list.size * self.index_list.itemsize, self.index_list,
                     GL_STATIC_DRAW)

        # create coords object
        self.vbo_coords = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_coords)
        glBufferData(GL_ARRAY_BUFFER, self.vertex_list.size * self.vertex_list.itemsize, self.vertex_list,
                     GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.vertex_attrib_position)
        glVertexAttribPointer(self.vertex_attrib_position, 3, GL_FLOAT, GL_FALSE, 0, None)

        # color
        self.fbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.fbo)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(self.color_data), self.color_data, GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.color_attrib_position)
        glVertexAttribPointer(self.color_attrib_position, 4, GL_FLOAT, GL_FALSE, 0, None)

        # init GL
        # set background color to black
        glClearColor(0.5, 0.5, 0.5, 0.5)
        # set depth buffer to far plane
        glClearDepth(1.0)
        # enable depth test with the z-buffer
        glEnable(GL_DEPTH_TEST)

        # fill the polygon
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # do not use culling
        glDisable(GL_CULL_FACE)

        # initialize the camera
        self.render_camera()

    def uninit_gl(self):
        # delete buffer objects
        glDeleteBuffers(1, self.vbo_indices)
        glDeleteBuffers(1, self.vbo_coords)

        # destroy vertex array object
        glDeleteVertexArrays(1, self.vao)

    def render_camera(self):
        top: float = self.near_distance * math.tan(self.height_angle / 2.0)
        right: float = top * self.width / self.height
        bottom: float = -top
        left: float = -right

        self.projection_matrix = [0.0 for _ in range(16)]
        self.projection_matrix[0] = (2.0 * self.near_distance) / (right - left)
        self.projection_matrix[5] = (2.0 * self.near_distance) / (top - bottom)
        self.projection_matrix[8] = (right + left) / (right - left)
        self.projection_matrix[9] = (top + bottom) / (top - bottom)
        self.projection_matrix[10] = -(self.far_distance + self.near_distance) / (
                    self.far_distance - self.near_distance)
        self.projection_matrix[11] = -1.0
        self.projection_matrix[14] = -2.0 * self.far_distance * self.near_distance / (
                    self.far_distance - self.near_distance)
        glUniformMatrix4fv(self.projection_matrix_id, 1, False, self.projection_matrix)

        # setup modelview matrix
        ang_x = self.rot_x_value * 3.14159265 / 180.0
        ang_y = self.rot_y_value * 3.14159265 / 180.0
        self.model_view_matrix = [0.0 for _ in range(16)]

        self.model_view_matrix[0] = math.cos(ang_y)
        self.model_view_matrix[2] = -math.sin(ang_y)
        self.model_view_matrix[4] = math.sin(ang_x) * math.sin(ang_y)
        self.model_view_matrix[5] = math.cos(ang_x)
        self.model_view_matrix[6] = math.sin(ang_x) * math.cos(ang_y)
        self.model_view_matrix[8] = math.cos(ang_x) * math.sin(ang_y)
        self.model_view_matrix[9] = -math.sin(ang_x)
        self.model_view_matrix[10] = math.cos(ang_x) * math.cos(ang_y)
        self.model_view_matrix[14] = self.trans_z_value
        self.model_view_matrix[15] = 1.0
        glUniformMatrix4fv(self.model_view_matrix_id, 1, False, self.model_view_matrix)

    def render(self):
        # clear frame and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # render vertex array
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.index_list.size, GL_UNSIGNED_INT, None)

    def rot_x(self, angle: float):
        self.rot_x_value += angle

    def rot_y(self, angle: float):
        self.rot_y_value += angle

    def trans_z(self, z: float):
        self.trans_z_value += z

    def divide_polygons(self):
        def calculate_mid_vert(vert1, vert2):
            mid = np.array([(vert1[0] + vert2[0]) / 2, (vert1[1] + vert2[1]) / 2, (vert1[2] + vert2[2]) / 2],
                            dtype=float32)
            distance_vert = math.sqrt(vert1[0]*vert1[0] + vert1[1]*vert1[1] + vert1[2]*vert1[2])
            distance_mid = math.sqrt(mid[0]*mid[0] + mid[1]*mid[1] + mid[2]*mid[2])
            mid = mid * distance_vert / distance_mid
            return mid

        polygons = [self.index_list[i:i + 3] for i in range(0, len(self.index_list), 3)]
        vertices = [self.vertex_list[i:i + 3] for i in range(0, len(self.vertex_list), 3)]
        self.index_list = np.array([], dtype=int32)

        for polygon in polygons:
            vert_index1 = polygon[0]
            vert_index2 = polygon[1]
            vert_index3 = polygon[2]
            vert1 = vertices[vert_index1]
            vert2 = vertices[vert_index2]
            vert3 = vertices[vert_index3]
            mid1 = calculate_mid_vert(vert1, vert2)
            mid2 = calculate_mid_vert(vert2, vert3)
            mid3 = calculate_mid_vert(vert1, vert3)
            mid_index1 = len(self.vertex_list)//3
            mid_index2 = len(self.vertex_list)//3 + 1
            mid_index3 = len(self.vertex_list)//3 + 2
            self.vertex_list = np.concatenate((self.vertex_list, mid1, mid2, mid3))
            self.index_list = np.concatenate((
                self.index_list,
                np.array([vert_index1, mid_index1, mid_index3], dtype=int32),
                np.array([mid_index1, vert_index2, mid_index2], dtype=int32),
                np.array([mid_index1, vert_index2, mid_index2], dtype=int32),
                np.array([mid_index2, vert_index3, mid_index3], dtype=int32),
                np.array([mid_index1, mid_index2, mid_index3], dtype=int32)
            ))

        self.generate_color()

        # create buffer object for indices
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbo_indices)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.index_list.size * self.index_list.itemsize, self.index_list,
                     GL_STATIC_DRAW)

        # create coords object
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_coords)
        glBufferData(GL_ARRAY_BUFFER, self.vertex_list.size * self.vertex_list.itemsize, self.vertex_list,
                     GL_STATIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, self.fbo)
        glBufferData(GL_ARRAY_BUFFER, self.color_data.size * self.color_data.itemsize, self.color_data, GL_STATIC_DRAW)

    def generate_color(self):
        num_polygons: int = len(self.index_list) // 3
        self.color_data = np.array([random() for _ in range(num_polygons * 4)], dtype=float32)
        self.color_data[3::4] = [1.0] * num_polygons
