/*
 * VKModuleInterface.h
 *
 * Copyright (c) 2015 Lukas Hermanns. All rights reserved.
 * Licensed under the terms of the BSD 3-Clause license (see LICENSE.txt).
 */

#include "../ModuleInterface.h"
#include "VKRenderSystem.h"


LLGL_IMPLEMENT_RENDERER_MODULE(Vulkan, "Vulkan", LLGL::RendererID::Vulkan, LLGL::VKRenderSystem, 200);



// ================================================================================
