#version 330 core
// https://learnopengl.com/Advanced-OpenGL/Cubemaps
out vec4 fragColor;

in vec3 textCoords;

uniform samplerCube skybox;

void main()
{
    fragColor = texture(skybox, textCoords);
}