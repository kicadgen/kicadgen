# (C) 2023 Jerry Terra
# Use of this source code is governed by MIT license that can be found in the LICENSE file.

import os
import sys

from gen import *

if len(sys.argv) < 3:
    print("Usage: %s (library name) (dir)\n".format(sys.argv[0]))
    exit(-1)

libraryName = sys.argv[1]
libDir = sys.argv[2]

try:
    os.chdir(libDir)
except Exception as e:
    print(e)

walk = os.walk(libDir)

for path, dirs, files in walk:
    lib = Library(libraryName)
    for filename in files:
        s = filename.split(".")
        if len(s) < 2:
            exit(-1)

        name, ext = s[0], s[1]

        sym = Symbol(name, lib)

        if ext == "pin":
            try:
                parse_pin_description(sym, filename)
                print("Found pin description for", name)
            except Exception as e:
                print(e)
                exit(-1)
        elif ext == "kicad_sym":
            continue
        else:
            print("Skipped file with unknown extension name:", filename)

        lib.add_sym(sym)
    lib.generate(libraryName+".kicad_sym")

exit(0)
