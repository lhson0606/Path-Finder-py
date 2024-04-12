#version 330 core

in vec3 normal;
in float entityID;

out vec4 fragColor;

void main()
{
    fragColor = vec4(normal, entityID);
}