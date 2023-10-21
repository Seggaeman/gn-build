import sys

def main()->None:
    output_file = open(sys.argv[len(sys.argv)-1], "w")
    lines_to_write = sys.argv[1:len(sys.argv)-1]
    output_file.write("\n".join(lines_to_write))
    output_file.close()
    return 0

if __name__ == "__main__":
    sys.exit(main());