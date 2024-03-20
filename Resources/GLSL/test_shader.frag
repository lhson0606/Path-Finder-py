#version 330 core

in vec3 textCoords;

out vec4 fragColor;

void main()
{
	fragColor = vec4(textCoords, 1);
}