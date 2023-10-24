import sys
import subprocess

def main()->None:
    result:int = subprocess.call(sys.argv[1:])
    return result

if __name__ == "__main__":
    sys.exit(main())
