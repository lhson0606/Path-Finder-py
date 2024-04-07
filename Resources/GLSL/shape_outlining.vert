#version 330 core

// ref: https://www.youtube.com/watch?v=ngF9LWWxhd0

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoords;
layout (location = 2) in vec3 aNormal;
layout (location = 3) in vec4 col0;
layout (location = 4) in vec4 col1;
layout (location = 5) in vec4 col2;
layout (location = 6) in vec4 col3;

uniform mat4 view;
uniform mat4 projection;

void main()
{
    mat4 instanceMatrix = mat4(col0, col1, col2, col3);
    gl_Position = projection * view * instanceMatrix * vec4(aPos + aNormal*0.08, 1.0);
}