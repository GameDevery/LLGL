/*
 * D3D11ModuleInterface.h
 *
 * Copyright (c) 2015 Lukas Hermanns. All rights reserved.
 * Licensed under the terms of the BSD 3-Clause license (see LICENSE.txt).
 */

#include "../ModuleInterface.h"
#include "D3D11RenderSystem.h"


LLGL_IMPLEMENT_RENDERER_MODULE(Direct3D11, "Direct3D 11", LLGL::RendererID::Direct3D11, LLGL::D3D11RenderSystem, 1011);



// ================================================================================
