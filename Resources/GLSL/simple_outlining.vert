#version 330 core

// ref: https://www.youtube.com/watch?v=ngF9LWWxhd0

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoords;
layout (location = 2) in vec3 aNormal;

uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * vec4(aPos + aNormal*0.08, 1.0);
}