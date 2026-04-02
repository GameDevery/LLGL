/*
 * NullModuleInterface.h
 *
 * Copyright (c) 2015 Lukas Hermanns. All rights reserved.
 * Licensed under the terms of the BSD 3-Clause license (see LICENSE.txt).
 */

#include "../ModuleInterface.h"
#include "NullRenderSystem.h"


LLGL_IMPLEMENT_RENDERER_MODULE(Null, "Null", LLGL::RendererID::Null, LLGL::NullRenderSystem, 0);



// ================================================================================
