#version 150

uniform mat4  cProjectionMatrix;
uniform mat4  cModelviewMatrix;

in vec4 in_Position;
in vec4 color;

flat out vec4 vcolor;

void main()
{
    gl_Position = cProjectionMatrix * cModelviewMatrix * in_Position;
    vcolor = color;
}