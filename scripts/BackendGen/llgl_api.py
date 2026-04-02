#
# llgl_api.py
#
# Copyright (c) 2015 Lukas Hermanns. All rights reserved.
# Licensed under the terms of the BSD 3-Clause license (see LICENSE.txt).
#

import os


def count_path_segments(path):
    # 1. Replace backslashes with forward slashes for uniformity
    # 2. Strip trailing/leading slashes so 'A/B/' becomes 'A/B'
    # 3. Split by '/' and count the resulting list
    normalized = path.replace('\\', '/').strip('/')
    return len(normalized.split('/')) if normalized else 0


class LLGLInterfaceInfo:
    def __init__(self, name, sub_dir=None, has_inl:bool=True, has_default_ctor:bool=False, private_decls=None, private_defs=None, forward_decls=None, additional_include_files=[]):
        self.name = name # Interface name, e.g. "Buffer"
        self.sub_dir = sub_dir
        self.has_inl:bool = has_inl # Does this interface have any Backend/<NAME>.inl files?
        self.private_decls = private_decls
        self.private_defs = private_defs
        self.forward_decls = forward_decls
        self.has_default_ctor:bool = has_default_ctor # Should a default constructor be generated? Requires <NAME>Descriptor struct for this interface, e.g. "BufferDescriptor".
        self.additional_include_files = additional_include_files
    
    def get_dest_dir(self, root):
        return os.path.join(root, self.sub_dir) if self.sub_dir is not None else root
    
    def print_assert_include_directive(self):
        sub_dir_count = count_path_segments(self.sub_dir) if self.sub_dir is not None else 0
        return f"#include \"{'../' * (sub_dir_count + 2)}Core/Assertion.h\""


class LLGLFunctionSignature:
    def __init__(self, ret_type: str, class_name: str, func_name: str, args: str, is_const=False):
        self.ret_type = ret_type
        self.class_name = class_name
        self.func_name = func_name
        self.args = args
        self.is_const = is_const

    def __str__(self):
        const_suffix = " const" if self.is_const else ""
        args = "" if self.args == "void" else self.args
        return f"{self.ret_type} {self.class_name}::{self.func_name}({args}){const_suffix}"
    
    def has_pointer_ret_type(self):
        return '*' in self.ret_type
    
    def has_void_ret_type(self):
        return self.ret_type == 'void'
    
    def has_bool_ret_type(self):
        return self.ret_type == 'bool'
    
    def has_sint_ret_type(self):
        return self.ret_type in ['int', 'long', 'std::int8_t', 'std::int16_t', 'std::int32_t', 'std::int64_t']
    
    def has_uint_ret_type(self):
        return self.ret_type in ['unsigned', 'unsigned int', 'unsigned long', 'std::uint8_t', 'std::uint16_t', 'std::uint32_t', 'std::uint64_t']
    
    def has_format_ret_type(self):
        return self.ret_type == 'Format'
    
    def has_dummy_body(self):
        return False

    def print_default_return(self):
        if self.has_pointer_ret_type():
            return 'nullptr'
        if self.has_bool_ret_type():
            return 'false'
        if self.has_sint_ret_type():
            return '0'
        if self.has_uint_ret_type():
            return '0u'
        if self.has_format_ret_type():
            return 'Format::Undefined'
        if not self.has_void_ret_type():
            return '{}'
        return None


COMMAND_BUFFER_FORWARD_DECLS="""using {prefix}VirtualCommandBuffer = VirtualCommandBuffer<{prefix}Opcode>;

"""

COMMAND_BUFFER_FIELDS="""// Allocates only an opcode for empty commands.
        void AllocOpcode(const {prefix}Opcode opcode);

        // Allocates a new command and stores the specified opcode.
        template <typename TCommand>
        TCommand* AllocCommand(const {prefix}Opcode opcode, std::size_t payloadSize = 0);

    private:

        {prefix}VirtualCommandBuffer buffer_;
"""

COMMAND_BUFFER_PRIVATE_DEFS="""void {prefix}CommandBuffer::AllocOpcode(const {prefix}Opcode opcode)
{{
    buffer_.AllocOpcode(opcode);
}}

template <typename TCommand>
TCommand* {prefix}CommandBuffer::AllocCommand(const {prefix}Opcode opcode, std::size_t payloadSize)
{{
    return buffer_.AllocCommand<TCommand>(opcode, payloadSize);
}}"""

RENDER_SYSTEM_FIELDS="""#include <LLGL/Backend/RenderSystem.Internal.inl>

    private:

        /* ----- Hardware object containers ----- */

        HWObjectContainer<{prefix}SwapChain>        swapChains_;
        HWObjectInstance<{prefix}CommandQueue>      commandQueue_;
        HWObjectContainer<{prefix}CommandBuffer>    commandBuffers_;
        HWObjectContainer<{prefix}Buffer>           buffers_;
        HWObjectContainer<{prefix}BufferArray>      bufferArrays_;
        HWObjectContainer<{prefix}Texture>          textures_;
        HWObjectContainer<{prefix}RenderPass>       renderPasses_;
        HWObjectContainer<{prefix}RenderTarget>     renderTargets_;
        HWObjectContainer<{prefix}Shader>           shaders_;
        HWObjectContainer<{prefix}PipelineLayout>   pipelineLayouts_;
        HWObjectContainer<{prefix}PipelineState>    pipelineStates_;
        HWObjectContainer<{prefix}ResourceHeap>     resourceHeaps_;
        HWObjectContainer<{prefix}Sampler>          samplers_;
        HWObjectContainer<{prefix}QueryHeap>        queryHeaps_;
        HWObjectContainer<{prefix}Fence>            fences_;

        HWObjectInstance<ProxyPipelineCache>  pipelineCacheProxy_;
"""


# Define the metadata for each interface
INTERFACES = [
    LLGLInterfaceInfo("Buffer", sub_dir="Buffer"),
    LLGLInterfaceInfo("BufferArray", sub_dir="Buffer"),
    LLGLInterfaceInfo(
        "CommandBuffer",
        sub_dir="Command",
        forward_decls=COMMAND_BUFFER_FORWARD_DECLS,
        private_decls=COMMAND_BUFFER_FIELDS,
        private_defs=COMMAND_BUFFER_PRIVATE_DEFS,
        additional_include_files=[
            '"{prefix}CommandOpcode.h"',
            '"../../VirtualCommandBuffer.h"'
        ]
    ),
    LLGLInterfaceInfo("CommandQueue", sub_dir="Command"),
    LLGLInterfaceInfo("Fence", sub_dir="RenderState"),
    #LLGLInterfaceInfo("PipelineCache", sub_dir="RenderState"),
    LLGLInterfaceInfo("PipelineLayout", sub_dir="RenderState"),
    LLGLInterfaceInfo("PipelineState", sub_dir="RenderState"),
    LLGLInterfaceInfo("QueryHeap", sub_dir="RenderState"),
    LLGLInterfaceInfo("RenderPass", sub_dir="RenderState"),
    LLGLInterfaceInfo(
        "RenderSystem",
        private_decls=RENDER_SYSTEM_FIELDS,
        has_default_ctor=True,
        additional_include_files=[
            '',
            '"{prefix}SwapChain.h"',
            '"Command/{prefix}CommandBuffer.h"',
            '"Command/{prefix}CommandQueue.h"',
            '',
            '"Buffer/{prefix}Buffer.h"',
            '"Buffer/{prefix}BufferArray.h"',
            '',
            '"RenderState/{prefix}Fence.h"',
            '"RenderState/{prefix}PipelineLayout.h"',
            '"RenderState/{prefix}PipelineState.h"',
            '"RenderState/{prefix}QueryHeap.h"',
            '"RenderState/{prefix}ResourceHeap.h"',
            '"RenderState/{prefix}RenderPass.h"',
            '',
            '"Shader/{prefix}Shader.h"',
            '',
            '"Texture/{prefix}Texture.h"',
            '"Texture/{prefix}RenderTarget.h"',
            '"Texture/{prefix}Sampler.h"',
            '',
            '"../ProxyPipelineCache.h"',
            '"../ContainerTypes.h"'
        ]
    ),
    LLGLInterfaceInfo("RenderTarget", sub_dir="Texture"),
    LLGLInterfaceInfo("ResourceHeap", sub_dir="RenderState"),
    LLGLInterfaceInfo("Sampler", sub_dir="Texture"),
    LLGLInterfaceInfo("Shader", sub_dir="Shader"),
    LLGLInterfaceInfo("SwapChain"),
    LLGLInterfaceInfo("Texture", sub_dir="Texture"),
]
