#!/usr/bin/env python3

import json
import subprocess
import sys

def main():
  pkg_name = sys.argv[1]
  command = [ "pkg-config", "--libs", "--cflags", pkg_name]
  result = subprocess.run(command, capture_output=True, text=True)
  error = result.stderr
  flags = result.stdout.split()
  cflags = []
  libs = []
  lib_dirs = []

  for flag in flags:
    if flag.startswith("-l"):
      libs.append(flag[2:])
    elif flag.startswith("-L"):
      lib_dirs.append(flag[2:])
    else:
      cflags.append(flag)

  result = json.dumps({ 
    "cflags": cflags, 
    "libs": libs,
    "lib_dirs": lib_dirs,
    "error": error
  })
  print(result)

if __name__ == "__main__":
  main()

'''Examples
Originally in file: //build/config/posix/pkg-config/BUILD.gn

config("gtk4") {
  cflags_and_libs = exec_script("pkg-config.py", ["gtk4"], "json")
  cflags = cflags_and_libs.cflags
  #Prefer libs instead of ldflags if these must be passed to dependents
  libs = cflags_and_libs.libs
}

config("gtkmm-4.0") {
  cflags_and_libs = exec_script("pkg-config.py", ["gtkmm-4.0"], "json")
  cflags = cflags_and_libs.cflags
  #Prefer libs instead of ldflags if these must be passed to dependents
  libs = cflags_and_libs.libs
}

Usage: In gtk_target, set
configs = [ ""//build/config/posix/pkg-config:gtk4", "//build/config/posix/pkg-config:gtkmm-4.0" ]

---------------------------------------------------
Originally in file: //build/config/posix/pkg-config/pkg-config.gni

# Config template example

template("pkg_config_single") { # Hyphens in name aren't allowed
  config(target_name) {
    cflags_and_libs = exec_script("//build/config/posix/pkg-config/pkg-config.py", [ target_name ], "json")
    cflags = cflags_and_libs.cflags
    #Prefer libs instead of ldflags if these must be passed to dependents
    libs = cflags_and_libs.libs
  }

  not_needed(invoker, "*")
}

Usage:
1. import("//build/config/posix/pkg-config/pkg-config.gni")
2. Before target:
pkg_config_single("lib-json-1.0") { }
pkg_config_single("some-other-lib") { }
pkg_config_single("yet-another-lib") { }
.....
3. In target:
configs = [ ":lib-json-1.0", ":some-other-lib", ":yet-another-lib", ... ]

------------------------------------------------------
In file: //build/toolchain/posix/gtk/gtk_target.gni

if(defined(invoker.packages)) {
  foreach(package, invoker.packages) {
    config(package) {
      cflags_and_libs = exec_script("//build/config/posix/pkg-config/pkg-config.py", [ package ], "json")
      cflags = cflags_and_libs.cflags
      #Prefer libs instead of ldflags if these must be passed to dependents
      libs = cflags_and_libs.libs
      if (len(cflags_and_libs.error) > 0) {
        print(cflags_and_libs.error)
        assert(len(cflags_and_libs.error) == 0)
      }
    }
  }
}

Usage:
1. See target definition in "gtk_target" template.
2. 
gtk_target("your_target") {
...
packages = [ "package_1", "package_2", ... , "package_n"]
}
3. No colon at start of the package name.
'''