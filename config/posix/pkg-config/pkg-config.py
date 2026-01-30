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

  for flag in flags:
    if flag.startswith("-l"):
      libs.append(flag[2:])
    else:
      cflags.append(flag)

  result = json.dumps({ 
    "cflags": cflags, 
    "libs": libs,
    "error": error
  })
  print(result)

if __name__ == "__main__":
  main()