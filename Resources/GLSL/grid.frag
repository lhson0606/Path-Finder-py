#version 330 core
// referenced:
//  + https://www.reddit.com/r/opengl/comments/mnap5m/drawing_a_game_engine_style_grid_plane/
//  + https://www.shadertoy.com/view/XtBfzz

const float N = 69.0; // grid ratio
float gridTextureGradBox( in vec2 p, in vec2 ddx, in vec2 ddy )
{
	// filter kernel
    vec2 w = max(abs(ddx), abs(ddy)) + 0.12;

	// analytic (box) filtering
    vec2 a = p + 0.5*w;
    vec2 b = p - 0.5*w;

	float T = N;

	if(abs(round(p.x/5) - p.x/5)<0.005 ||  abs(round(p.y/5) - p.y/5)<0.005)
	{
		T = 10;
	}


    vec2 i = (floor(a)+min(fract(a)*T,1.0)-
              floor(b)-min(fract(b)*T,1.0))/(T*w);
    //pattern
    return (1.0-i.x)*(1.0-i.y);
}

in vec2 textCoords;

out vec4 fragColor;

void main()
{
	vec2 uv = textCoords;

	// calc texture sampling footprint
	vec2 ddx_uv = dFdx( uv );
	vec2 ddy_uv = dFdy( uv );

	vec3 col = vec3(0.9);
	vec3 mate = vec3(1.0);

	mate = vec3(0.2, 0.3, 0.3)*gridTextureGradBox( uv*50, ddx_uv, ddy_uv );
	col = mate ;

	fragColor = vec4( col, 1 );
}