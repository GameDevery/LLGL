// GLSL tessellation evaluation shader
#version 450 core

// Tessellation evaluation input configuration
layout(quads, fractional_odd_spacing, cw) in;

// Input constant data
layout(std140, binding = 1) uniform Scene
{
    mat4    vpMatrix;
    mat4    vMatrix;
    mat4    wMatrix;
    vec3    lightVec;
    float   texScale;
    float   tessLevelInner;
    float   tessLevelOuter;
    float   maxHeightFactor;
    float   shininessPower;
};

// Input and output attributes
layout(location = 0) in vec3 tcWorldPos[];
layout(location = 1) in vec3 tcNormal[];
layout(location = 2) in vec3 tcTangent[];
layout(location = 3) in vec3 tcBitangent[];
layout(location = 4) in vec2 tcTexCoord[];

layout(location = 0) out vec3 teViewPos;
layout(location = 1) out vec3 teNormal;
layout(location = 2) out vec3 teTangent;
layout(location = 3) out vec3 teBitangent;
layout(location = 4) out vec2 teTexCoord;

out gl_PerVertex
{
    vec4 gl_Position;
};

float InterpolateHeightAlongEdges(vec2 coord)
{
    vec2 t = vec2(1.0) - abs(coord*2.0 - 1.0);
    return smoothstep(0.0, 0.2, min(t.x, t.y));
}

#define INTERPOLATE_PATCH(COMP)             	\
    mix(                                    	\
        mix(COMP[0], COMP[1], gl_TessCoord.x),	\
        mix(COMP[2], COMP[3], gl_TessCoord.x),	\
        gl_TessCoord.y                         	\
    )

layout(binding = 2) uniform sampler linearSampler;
layout(binding = 6) uniform texture2D heightMap;

// Tessellation-evaluation shader main function
void main()
{
    // Interpolate world position
    vec3 interpolatedWorldPos = INTERPOLATE_PATCH(tcWorldPos);
    vec2 interpolatedTexCoord = INTERPOLATE_PATCH(tcTexCoord);
    vec2 scaledTexCoord = (interpolatedTexCoord - 0.5)*texScale + 0.5;

    // Sample height map and create bump by moving along the patch normal vector
    float bumpHeight = textureLod(sampler2D(heightMap, linearSampler), scaledTexCoord, 0.0).r * maxHeightFactor * InterpolateHeightAlongEdges(interpolatedTexCoord);

    interpolatedWorldPos += tcNormal[0] * bumpHeight;

    // Transform vertex by the view-projection matrix
    gl_Position = vpMatrix * vec4(interpolatedWorldPos, 1);
    teViewPos   = (vMatrix * vec4(interpolatedWorldPos, 1)).xyz;
    teNormal    = tcNormal[0];
    teTangent   = tcTangent[0];
    teBitangent	= tcBitangent[0];
    teTexCoord	= scaledTexCoord;
}
