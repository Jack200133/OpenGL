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

gomu_gomu_shader ='''
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

out vec3 fNormal;
out vec3 fPosition;
const float pi=3.14159;
out vec3 modelX;
out vec3 modelN;
out vec3 rawX;

vec2 Rotate2D(vec2 vec_in, float angle)
{
  vec2 vec_out;
  vec_out.x=cos(angle)*vec_in.x-sin(angle)*vec_in.y;
  vec_out.y=sin(angle)*vec_in.x+cos(angle)*vec_in.y;
  return vec_out;
}

void main()
{
  pos = (modelMatrix * vec4(position + (normals* sin(time*3))/10, 1.0)).xyz;
  modelX=pos;
  rawX=pos;
  modelN=normals;  
  UVs = texcoords;

  modelX.x = modelX.x + sin(modelX.y + time*3)/2;
  modelX.z = modelX.z + cos(modelX.y + time*3)/2;
  norms = normals;

  vec4 pos = viewMatrix * vec4(modelX, 1.0);
  fPosition = pos.xyz;
  gl_Position = projectionMatrix * pos;
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
in vec3 norms;
in vec2 UVs;
uniform sampler2D tex;
in vec3 pos;

void main()
{
	float intensity;
	vec4 color;
	intensity = dot(normalize(pointLight-pos),norms);

	if (intensity > 0.8)
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

siren_shader = '''
#version 450 core

out vec4 fragColor;

in vec2 UVs;
in vec3 norms;
in vec3 pos;

uniform vec3 pointLight;
uniform vec2 theta;

void main()
{
	vec3 dir1 = vec3(cos(theta.x),0,sin(theta.x)); 
	vec3 dir2 = vec3(sin(theta.x),0,cos(theta.x));

	float diffuse1 = pow(dot(norms,dir1),2.0);
	float diffuse2 = pow(dot(norms,dir2),2.0);

	vec3 col1 = diffuse1 * vec3(1,0,0);
	vec3 col2 = diffuse2 * vec3(0,0,1);

	fragColor = vec4((col1 + col2), 1.0);
}


'''