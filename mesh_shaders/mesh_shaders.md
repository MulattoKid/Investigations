# Mesh Shaders

#### Disclaimer
This is based on the Nvidia extension VK_NV_mesh_shader, and current Nvidia HW (RTX 2080). The limits are also
based on this.

## What and How?
Mesh shaders are designed to replace the current geometry pipeline (tessellation, vertex and geometry) with a
more flexible alternative. Performance should however not suffer due to the increased flexibility (so long as
used "correctly").

Focusing on the vertex stage, a draw call is essentially replaced by a compute dispatch. The difference from
a normal compute dispatch is that the output data from the mesh shader is used by the rasterizer to generate
fragment which in turn run through the fragment stage.

## Meshlet
There are limitations on how many vertices (256) and primitives (512) a mesh shader group can output. This
means it cannot work on an entire mesh. This means that to render an entire mesh it needs to be split into
smaller pieces; meshlets.

A meshlet is subset of a mesh with at most 256 vertices and 512 primitives (Nvidia recommends 64 vertices and 126
primitives). An array of descriptions of meshlets is provided to the mesh shaders, to that each mesh shader group
knows which meshlet to shade. The description could be anything, but for general use Nvidia recommends the
following:
```
struct MeshletDescription
{
    uint32_t vertexIndexBufferOffset; // Offset to meshlet's vertices in vertex index buffer
    uint32_t vertexCount;             // Number of vertices in meshlet
    uint32_t primitiveBufferOffset;   // Offset to meshlet's primitive in primitive index buffer
    uint32_t primitiveCount;          // Number of primitives in meshlet
};
```

The vertex buffer is essentially the same as in a regular indexed draw call, with vertices that local in space
hopefully being local in memory.
```
vec3 vertices[] = { v0, v1, v2, v3, v4, v5, v6, v7, ... };
```

The vertex index buffer is a level of indirection that's needed for a few reasons:
- A vertex is only present once in the vertex buffer, so the vertices for a meshlet aren't guaranteed to be stored
contiguously in memory. This means that simply having an offset and a count into the vertex buffer isn't sufficient
to determine which vertices make up a meshlet.
- While the primitive index buffer could point directly into the vertex buffer, this would result in a vertex being
used more than once within a meshlet being shaded multiple times for said meshlet.

With the vertex index buffer it's possible to only shade each vertex that's part of a meshlet once per mesh shader
group, and still allow for vertex reuse within a meshlet. Also, depending on the number of vertices in the complete
mesh, it's possible for these indices to be e.g. `uint16_t` or `uint8_t`.
```
uint32_t vertexIndexBuffer[] = {
    0, 3, 4, 5, 6, 7, 1, // Meshlet #0
    2, 3, 0, 1, 4, 5,    // Meshlet #1
    ...
};
```

Finally, there's the primitive index buffer, which is used to contruct primitives after the vertices are shaded for
a meshlet. Since the number of output primitives is relatively limitied (maximum 512), it's possible to use fewer
than 32 bits per index to reduce the memory footprint for each meshlet's primitive list. These indices point into
the vertex index buffer.
```
uint32_t primitiveIndexBuffer[] = {
    0, 1, 2,  2, 3, 0,  3, 5, 6,  4, 0, 1, // Meshlet #0
    0, 2, 3,  4, 5, 0,  1, 2, 3            // Meshlet #1
};
```

## Shader Stages
Mesh shading consists of two shader stages
1) Task shader
2) Mesh shader

in that order. To have the functionality of just vertex shading, theoretically only the mesh shader stage is needed.
However, to support a more flexible mesh shader, and also tessellation, a pre-mesh shader stage is added. This acts
as a "amplification" shader, and allows for generating more vertices than in the original mesh. The task shader stage
is also optional.

### Mesh Shader
The mesh shader stage is the mandatory shader stage, and is what outputs transformed vertices and primitives to the
rasterizer. The main difference compared to a regular vertex shader is that a mesh shader is run in groups of N
threads (i.e. a work group) which works on a single meshlet, while a vertex shader runs on all vertices submitted
in the vertex buffer (+ index buffer).

As mentioned, a mesh shader group (MSG) has a limit on how many vertices (256) and primitives (512) it can output, so
meshlets must be guaranteed to not exceed these limits. Furthermore, a MSG has a limit on how many invocations
(threads) it can have (32). This means that if a MSG output more than 32 vertices or 32 primitives, at least one
thread must output more than 1.

MSGs are dispatched with the following API call
```
void vkCmdDrawMeshTasksNV(
    VkCommandBuffer commandBuffer,
    uint32_t        taskCount,
    uint32_t        firstTask);
```
The `taskCount` is the number of MSGs to dispatch. This will start N MSGs. An example of a pretty straight forward
mesh shader could look like this
```
#version 450
#extension GL_NV_mesh_shader : require

struct VertexDescription
{
    vec3 position;
    vec3 normal;
    vec2 uv;
};

struct MeshletDescription
{
    uint vertex_index_buffer_offset;
    uint vertex_count;
    uint primitive_index_buffer_offset;
    uint primitive_count;
};

layout(std430, set=0, binding=0) buffer readonly Vertices
{
    VertexDescription vertices[];
};

layout(std430, set=0, binding=1) buffer readonly Meshlets
{
    MeshletDescription meshlets[];
};

layout(std430, set=0, binding=2) buffer readonly VertexIndices
{
    uint vertex_indices[];
};

layout(std430, set=0, binding=3) buffer readonly PrimitiveIndices
{
    uint primitive_indices[];
};

layout(std430, set=0, binding=4) push_constant PushConstant
{
    mat4 model_view_projection;
    mat4 model;
};

layout(triangles) out; // Specify the output primtives are trianlges
layout(max_vertices = 64, max_primitives = 126) out; // Specify the maximum amount output data

layout (location = 0) out PerVertexData
{
    vec3 normal;
    vec2 uv;
} vertices_out[64]; // Room for maximum number of output vertices

// This is a rather simple mesh shader with a known meshlet size:
//   32 output vertices
//   32 output primitives
// This makes it so that each thread will output a single vertex, and 1 primitive (3 indices)
layout(local_size_x=32) in; // 32 threads in a MSG
void main()
{
    uint group_id = gl_WorkGroupID.x; // We know both Y and Z are 1, and X is specified in the dispatch call
    uint thread_id = gl_LocalInvocationIndex.x; // We know that both Y and Z are 1, and X is specified in the qualifier

    // Retrieve the meshlet for the MSG
    MeshletDescription meshlet = meshlets[group_id];

    // We know this will pass for all threads, but it would be neccessary in other scenarios
    if (thread_id < meshlet.vertex_count)
    {
        uint vertex_index = vertex_indices[meshlet.vertex_index_buffer_offset + thread_id];
        VertexDescription vertex = vertices[vertex_index];
        vertices_out[thread_id].normal = vec4(model * vec4(vertex.normal, 1.0)).xyz;
        vertices_out[thread_id].uv = vertex.uv;
        gl_MeshVerticesNV[thread_id].gl_Position = model_view_projection * vec4(vertex.position, 1.0);
    }

    // We know this will pass for all threads, but it would be neccessary in other scenarios
    if (thread_id < meshlet.primitive_count)
    {
        gl_PrimitiveIndicesNV[(thread_id * 3) + 0] = primitive_indices[meshlet.primitive_index_buffer_offset + (thread_id * 3) + 0];
        gl_PrimitiveIndicesNV[(thread_id * 3) + 1] = primitive_indices[meshlet.primitive_index_buffer_offset + (thread_id * 3) + 1];
        gl_PrimitiveIndicesNV[(thread_id * 3) + 2] = primitive_indices[meshlet.primitive_index_buffer_offset + (thread_id * 3) + 2];
    }
    gl_PrimitiveCountNV = 32;
}
```

### Task Shader
TODO

## Links
- [Reinventing the Geometry Pipeline: Mesh Shaders in DirectX 12 | Shawn Hargreaves | DirectX Dev Day](https://youtu.be/CFXKTXtil34) (YouTube)
- [Introduction to Turing Mesh Shaders](https://developer.nvidia.com/blog/introduction-turing-mesh-shaders/) (Nvidia Article)
- [New Rendering Techniques for Real-Time Graphics: Turing - Mesh Shaders](https://on-demand.gputechconf.com/siggraph/2018/video/sig1811-3-christoph-kubisch-mesh-shaders.html) (Siggraph Video)
- [Quick Introduction to Mesh Shaders (OpenGL and Vulkan)](https://www.geeks3d.com/20200519/introduction-to-mesh-shaders-opengl-and-vulkan/) (Geeks3D Article)