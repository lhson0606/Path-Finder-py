#version 330 core
// https://learnopengl.com/Advanced-OpenGL/Cubemaps
layout (location = 0) in vec3 aPos;

uniform mat4 projection;
uniform mat4 view;

out vec3 textCoords;

void main()
{
    textCoords = aPos;
    vec4 pos = projection * view *vec4(aPos, 1.0);
    gl_Position = pos.xyww;
}