/*
 * D3D12ModuleInterface.h
 *
 * Copyright (c) 2015 Lukas Hermanns. All rights reserved.
 * Licensed under the terms of the BSD 3-Clause license (see LICENSE.txt).
 */

#include "../ModuleInterface.h"
#include "D3D12RenderSystem.h"


LLGL_IMPLEMENT_RENDERER_MODULE(Direct3D12, "Direct3D 12", LLGL::RendererID::Direct3D12, LLGL::D3D12RenderSystem, 1012);



// ================================================================================
