#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoords;

out vec2 textCoords;

uniform mat4 projection;
uniform mat4 view;

void main()
{
	gl_Position = projection*view*vec4(aPos, 1.0);
	textCoords = aTexCoords;
}