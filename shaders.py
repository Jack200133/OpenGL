vertex_shader ='''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texcoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;

out vec2 UVs;
out vec3 norms;
out vec3 pos;

void main()
{
    UVs = texcoords;
    norms = normals;
    pos = (modelMatrix * vec4(position + (normals* sin(time*3))/10, 1.0)).xyz;


    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position+(normals*sin(time*3))/10, 1.0);
}
'''

fragment_shader ='''
#version 450 core

out vec4 fragColor;

in vec2 UVs;
in vec3 norms;
in vec3 pos;

uniform vec3 pointLight;

uniform sampler2D tex;

void main()
{
    float intensity = dot(norms, normalize(pointLight - pos));
    fragColor = texture(tex, UVs) * intensity;
}
'''


toon_shader = '''
uniform vec3 pointLight;
varying vec3 norms;
in vec2 UVs;
uniform sampler2D tex;

void main()
{
	float intensity;
	vec4 color;
	intensity = dot(pointLight,norms);

	if (intensity > 0.95)
		color = texture(tex, UVs) * 1;
	else if (intensity > 0.5)
		color =texture(tex, UVs) *0.6 ;
	else if (intensity > 0.25)
		color = texture(tex, UVs) * 0.3;
	else
		color = texture(tex, UVs) * 0.1;
	gl_FragColor = color;

}
'''


rainbow_shader = '''
#version 450 core

out vec4 fragColor;

in vec2 UVs;
in vec3 norms;
in vec3 pos;

uniform vec2 colorRaibow;

uniform vec3 pointLight;

uniform sampler2D tex;
uniform sampler2D tex1;

void main()
{
    float intensity = dot(norms, normalize(pointLight - pos));
    fragColor = texture(tex, UVs) * intensity * texture(tex1, colorRaibow);
}
'''