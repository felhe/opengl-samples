#version 150

uniform mat4  cProjectionMatrix;
uniform mat4  cModelviewMatrix;

in vec4 in_Position;
in vec4 color;
in vec2 texture;

flat out vec4 vcolor;
out vec2 vtexture;

void main()
{
    gl_Position = cProjectionMatrix * cModelviewMatrix * in_Position;
    vcolor = color;
    vtexture = texture;
}