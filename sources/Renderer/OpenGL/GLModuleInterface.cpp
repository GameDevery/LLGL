/*
 * GLModuleInterface.h
 *
 * Copyright (c) 2015 Lukas Hermanns. All rights reserved.
 * Licensed under the terms of the BSD 3-Clause license (see LICENSE.txt).
 */

#include "../ModuleInterface.h"
#include "GLRenderSystem.h"
#include "Profile/GLProfile.h"


#if defined(LLGL_OPENGLES3)
LLGL_IMPLEMENT_RENDERER_MODULE(OpenGLES3, LLGL::GLProfile::GetRendererName(), LLGL::GLProfile::GetRendererID(), LLGL::GLRenderSystem, 100);
#elif defined(LLGL_WEBGL)
LLGL_IMPLEMENT_RENDERER_MODULE(WebGL, LLGL::GLProfile::GetRendererName(), LLGL::GLProfile::GetRendererID(), LLGL::GLRenderSystem, 100);
#else
LLGL_IMPLEMENT_RENDERER_MODULE(OpenGL, LLGL::GLProfile::GetRendererName(), LLGL::GLProfile::GetRendererID(), LLGL::GLRenderSystem, 100);
#endif



// ================================================================================
