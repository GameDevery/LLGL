/*
 * ModuleInterface.h
 *
 * Copyright (c) 2015 Lukas Hermanns. All rights reserved.
 * Licensed under the terms of the BSD 3-Clause license (see LICENSE.txt).
 */

#ifndef LLGL_MODULE_INTERFACE_H
#define LLGL_MODULE_INTERFACE_H


// Define base macro used by LLGL_IMPLEMENT_RENDERER_MODULE() in StaticModuleInterface.h and DynamicModuleInterface.h.
#define LLGL_IMPLEMENT_RENDERER_MODULE_BASE(MODULE, NAME, ID, RENDERSYSTEM) \
    namespace LLGL                                                          \
    {                                                                       \
        namespace Module ## MODULE                                          \
        {                                                                   \
            int GetRendererID()                                             \
            {                                                               \
                return (ID);                                                \
            }                                                               \
            const char* GetRendererName()                                   \
            {                                                               \
                return (NAME);                                              \
            }                                                               \
            RenderSystem* AllocRenderSystem(                                \
                const LLGL::RenderSystemDescriptor* renderSystemDesc)       \
            {                                                               \
                return new RENDERSYSTEM{ *renderSystemDesc };               \
            }                                                               \
        }                                                                   \
    } // /namespace LLGL

#if LLGL_BUILD_STATIC_LIB
#   include "StaticModuleInterface.h"
#else
#   include "DynamicModuleInterface.h"
#endif


#endif



// ================================================================================
