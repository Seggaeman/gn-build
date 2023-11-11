#!/usr/bin/env python
import subprocess
import sys

def main()->None:
    return subprocess.call(sys.argv[1:])

if __name__ == "__main__":
    sys.exit(main())