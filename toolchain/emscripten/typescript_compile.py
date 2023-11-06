import os
import sys
import subprocess

def main()->None:
    #The last portion of the path supplied by GN doesn't exist. Get rid of it.
    last_slash_pos:int = sys.argv[1].rfind("/");
    dir_path:str = sys.argv[1][:last_slash_pos]
    os.chdir(dir_path) #Change execution directory to the one that contains webpack.config.js
    result:int = subprocess.call(sys.argv[2:])
    return result

if __name__ == "__main__":
    sys.exit(main())
