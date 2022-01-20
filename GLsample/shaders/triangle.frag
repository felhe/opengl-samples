#version 150

uniform sampler2D ourTexture;

flat in vec4 vcolor;
in vec2 vtexture;

out vec4 out_color;

void main()
{
    out_color = texture(ourTexture, vtexture) + 0.1 * vcolor;
}