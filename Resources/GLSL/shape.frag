#version 330 core

// GLASS
#define REFRACTION_RATIO 0.65789436

in vec3 position;
in vec3 normal;
in vec2 texCoords;

uniform vec3 cameraPos;
uniform samplerCube skybox;

out vec4 fragColor;

void main()
{
    vec3 I = normalize(position - cameraPos);
    vec3 R = refract(I, normalize(normal), REFRACTION_RATIO);
    fragColor = vec4(texture(skybox, R).rgb, 1.0);
}