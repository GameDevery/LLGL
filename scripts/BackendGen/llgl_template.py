#
# llgl_backend.py
#
# Copyright (c) 2015 Lukas Hermanns. All rights reserved.
# Licensed under the terms of the BSD 3-Clause license (see LICENSE.txt).
#

# Header template
# Variables: backend, interface, prefix, guard
HEADER_TEMPLATE = """/*
 * {file}.h
 *
 * Copyright (c) 2015 Lukas Hermanns. All rights reserved.
 * Licensed under the terms of the BSD 3-Clause license (see LICENSE.txt).
 */

#ifndef {guard}
#define {guard}


{include_directives}


namespace LLGL
{{


{content}


}} // /namespace LLGL


#endif



// ================================================================================
"""

# Source template
# Variables: backend, interface, prefix, functions
SOURCE_TEMPLATE = """/*
 * {file}.cpp
 *
 * Copyright (c) 2015 Lukas Hermanns. All rights reserved.
 * Licensed under the terms of the BSD 3-Clause license (see LICENSE.txt).
 */

#include "{file}.h"
{include_directives}


namespace LLGL
{{


{content}


}} // /namespace LLGL



// ================================================================================
"""

SOURCE_TEMPLATE_PRIVATE = """
/*
 * ======= Private: =======
 */

"""


HEADER_TEMPLATE_INTERFACE = """class {prefix}{interface} final : public {interface}
{{

    public:

        #include <LLGL/Backend/{interface}.inl>

    public:

        /* {prefix}{interface}(const {interface}Descriptor& desc); */

    private:

        {private_fields}

}};"""


HEADER_TEMPLATE_INTERFACE_MINIMAL = """class {prefix}{interface} final : public {interface}
{{

    public:

        /* {prefix}{interface}(const {interface}Descriptor& desc); */

    private:

        {private_fields}

}};"""


SOURCE_TEMPLATE_INTERFACE="""/* {prefix}{interface}::{prefix}{interface}(const {interface}Descriptor& desc) {{ ... }} */{functions}"""


HEADER_TEMPLATE_COMMAND="""/*struct {prefix}CmdDraw
{{
    ...
}};*/"""


HEADER_TEMPLATE_COMMAND_OPCODE="""enum {prefix}Opcode : std::uint8_t
{{
    // {prefix}OpcodeDraw = 1, ...
}};"""


HEADER_TEMPLATE_COMMAND_EXECUTOR="""// Executes all virtual commands from the specified command buffer.
void Execute{prefix}VirtualCommandBuffer(const {prefix}VirtualCommandBuffer& virtualCmdBuffer);"""


SOURCE_TEMPLATE_COMMAND_EXECUTOR="""/*static std::size_t Execute{prefix}Command(const {prefix}Opcode opcode, const void* pc)
{{
    switch (opcode)
    {{
        case {prefix}OpcodeDraw:
        {{
            auto cmd = static_cast<const {prefix}CmdDraw>(pc);
            ...
            return sizeof(cmd);
        }}
        default:
            return 0;
    }}
}}*/

void Execute{prefix}VirtualCommandBuffer(const {prefix}VirtualCommandBuffer& virtualCmdBuffer)
{{
    //virtualCmdBuffer.Run(Execute{prefix}Command);
}}"""


CMAKELISTS_TEMPLATE='''#
# CMakeLists.txt file for LLGL/{project} backend
#
# Copyright (c) 2015 Lukas Hermanns. All rights reserved.
# Licensed under the terms of the BSD 3-Clause license (see LICENSE.txt).
#

if (NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
    cmake_minimum_required(VERSION 3.12 FATAL_ERROR)
endif()

project(LLGL_{project})


# === Source files ===

# {project} renderer files
find_source_files(FilesRenderer{project}             CXX ${{PROJECT_SOURCE_DIR}})
find_source_files(FilesRenderer{project}Buffer       CXX ${{PROJECT_SOURCE_DIR}}/Buffer)
find_source_files(FilesRenderer{project}Command      CXX ${{PROJECT_SOURCE_DIR}}/Command)
find_source_files(FilesRenderer{project}RenderState  CXX ${{PROJECT_SOURCE_DIR}}/RenderState)
find_source_files(FilesRenderer{project}Shader       CXX ${{PROJECT_SOURCE_DIR}}/Shader)
find_source_files(FilesRenderer{project}Texture      CXX ${{PROJECT_SOURCE_DIR}}/Texture)

set(
    Files{project}
    ${{FilesRenderer{project}}}
    ${{FilesRenderer{project}Buffer}}
    ${{FilesRenderer{project}Command}}
    ${{FilesRenderer{project}RenderState}}
    ${{FilesRenderer{project}Shader}}
    ${{FilesRenderer{project}Texture}}
)


# === Source group folders ===

source_group("{project}"                 FILES ${{FilesRenderer{project}}})
source_group("{project}\\\\Buffer"         FILES ${{FilesRenderer{project}Buffer}})
source_group("{project}\\\\Command"        FILES ${{FilesRenderer{project}Command}})
source_group("{project}\\\\RenderState"    FILES ${{FilesRenderer{project}RenderState}})
source_group("{project}\\\\Shader"         FILES ${{FilesRenderer{project}Shader}})
source_group("{project}\\\\Texture"        FILES ${{FilesRenderer{project}Texture}})


# === Projects ===

if(LLGL_BUILD_RENDERER_{project_ucase})
    # {project} Renderer
    add_llgl_module(LLGL_{project} LLGL_BUILD_RENDERER_{project_ucase} "${{Files{project}}}")
    target_link_libraries(LLGL_{project} LLGL)
endif()

'''


MODULE_INTERFACE_SOURCE_TEMPLATE='''/*
 * {prefix}ModuleInterface.h
 *
 * Copyright (c) 2015 Lukas Hermanns. All rights reserved.
 * Licensed under the terms of the BSD 3-Clause license (see LICENSE.txt).
 */

#include "../ModuleInterface.h"
#include "{prefix}RenderSystem.h"


namespace LLGL
{{


namespace Module{project}
{{
    int GetRendererID()
    {{
        return RendererID::{project};
    }}

    const char* GetRendererName()
    {{
        return "{project}";
    }}

    RenderSystem* AllocRenderSystem(const LLGL::RenderSystemDescriptor* renderSystemDesc)
    {{
        return new {prefix}RenderSystem(*renderSystemDesc);
    }}
}} // /namespace Module{project}

LLGL_IMPLEMENT_RENDERER_MODULE({project}, {priority});


}} // /namespace LLGL

#ifndef LLGL_BUILD_STATIC_LIB

extern "C"
{{

LLGL_EXPORT int LLGL_RenderSystem_BuildID()
{{
    return LLGL_BUILD_ID;
}}

LLGL_EXPORT int LLGL_RenderSystem_RendererID()
{{
    return LLGL::Module{project}::GetRendererID();
}}

LLGL_EXPORT const char* LLGL_RenderSystem_Name()
{{
    return LLGL::Module{project}::GetRendererName();
}}

LLGL_EXPORT void* LLGL_RenderSystem_Alloc(const void* renderSystemDesc, int renderSystemDescSize)
{{
    if (renderSystemDesc != nullptr && static_cast<std::size_t>(renderSystemDescSize) == sizeof(LLGL::RenderSystemDescriptor))
    {{
        auto desc = static_cast<const LLGL::RenderSystemDescriptor*>(renderSystemDesc);
        return LLGL::Module{project}::AllocRenderSystem(desc);
    }}
    return nullptr;
}}

}} // /extern "C"

#endif // /LLGL_BUILD_STATIC_LIB



// ================================================================================
'''


