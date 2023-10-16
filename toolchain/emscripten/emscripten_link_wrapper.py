#!/usr/bin/env python
import os
import subprocess
import sys
from enum import Enum
import typing

class CommandParseState(Enum):
    STANDARD_COMPILE = 1
    TYPESCRIPT_COMPILE = 2

def main()->None:
    result = -1
    command_parse_state:CommandParseState = CommandParseState.STANDARD_COMPILE
    standard_compile_command_line:list[str] = []
    #Typescript command line is embedded inside linker arguments as --typescript_compile_start <typescript_command_line> --typescript_compile_end
    typescript_compile_command_line:list[str] = []

    for i in range(1, len(sys.argv)): #Start at one because we don't need the script path
        if command_parse_state == CommandParseState.STANDARD_COMPILE:
            if sys.argv[i] == "--typescript_compile_start":
                command_parse_state = CommandParseState.TYPESCRIPT_COMPILE
            else:
                standard_compile_command_line.append(sys.argv[i])
        else: #commandParseState == CommandParseState.TYPESCRIPT_COMPILE
            if sys.argv[i] == "--typescript_compile_end":
                command_parse_state = CommandParseState.STANDARD_COMPILE
            else:
                typescript_compile_command_line.append(sys.argv[i])
    
    result = subprocess.call(standard_compile_command_line)   
    if result != 0:
        print("Error generating binaries, result=",result)
        return result

    # Compile typescript after generating the definition file, in case it references it
    if len(typescript_compile_command_line) > 0:
        result = subprocess.call(typescript_compile_command_line)
        if result != 0:
            print("Error compiling typescript file(s), result=",result)
    
    return result

if __name__ == "__main__":
    sys.exit(main())