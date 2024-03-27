#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoords;
layout (location = 2) in vec3 aNormal;
layout (location = 3) in mat4 instanceMatrix;

out vec3 normal;
out vec2 texCoords;

uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * instanceMatrix * vec4(aPos, 1.0);
    normal = mat3(transpose(inverse(instanceMatrix))) * aNormal;
    texCoords = aTexCoords;
}