#
# llgl_cmake.py
#
# Copyright (c) 2015 Lukas Hermanns. All rights reserved.
# Licensed under the terms of the BSD 3-Clause license (see LICENSE.txt).
#

import os

def process_cmake(source_dir, dest_dir, name, prefix):
    cmake_path = os.path.join(source_dir, 'CMakeLists.txt')
    if not os.path.exists(cmake_path):
        return

    with open(cmake_path, 'r') as f:
        content = f.read()

    # Replace "Null" with the specific Name/Prefix patterns
    # Usually "Null" appears in target names and folder references
    new_content = content.replace('Null', prefix)
    new_content = new_content.replace('null', name.lower())

    with open(os.path.join(dest_dir, 'CMakeLists.txt'), 'w') as f:
        f.write(new_content)
