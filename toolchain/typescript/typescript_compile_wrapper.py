from enum import Enum
import os
import shutil
import subprocess
import sys

class CommandParseState(Enum):
    NO_COMMAND = 1
    HTML_COMMAND = 2
    OUTPUTDIR_COMMAND = 3
    TYPESCRIPT_COMMAND = 4

def main()->None:
    result:int = 0
    html_command:list[str] = []
    typescript_command:list[str] = []
    command_parse_state:CommandParseState = CommandParseState.NO_COMMAND
    output_directory:str = ""

    for i in range(1, len(sys.argv)): #Start at one because we don't need the script path
        if sys.argv[i].startswith("/"):
            if sys.argv[i] == "/outDir":
                command_parse_state = CommandParseState.OUTPUTDIR_COMMAND
            if sys.argv[i] == "/html":
                command_parse_state = CommandParseState.HTML_COMMAND
            elif sys.argv[i] == "/typescript":
                command_parse_state = CommandParseState.TYPESCRIPT_COMMAND
        else:
            match command_parse_state:
                case CommandParseState.HTML_COMMAND:
                    html_command.append(sys.argv[i])
                case CommandParseState.OUTPUTDIR_COMMAND:
                    output_directory = sys.argv[i]
                case CommandParseState.TYPESCRIPT_COMMAND:
                    typescript_command.append(sys.argv[i])

    for html_file in html_command:
        dest_file_path:str = f"{output_directory}/{os.path.basename(html_file)}"
        shutil.copy(html_file, dest_file_path)

    if len(typescript_command) > 0:
        result = subprocess.call(typescript_command)

    return result

if __name__ == "__main__":
    sys.exit(main())