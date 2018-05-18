"""
build parsed text from conllu files

"""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input")
parser.add_argument("--output")
args = parser.parse_args()
input_file = args.input
output_file = args.output


with open(input_file, "r") as f:
    lines = f.readlines()

tokens = []
string = ""
for line in lines:
    line = line.decode("utf8")
    if line[0] == '#':
        continue
    if line == "\n":
        string += (" ".join(tokens) + "\n")
        tokens = []
        continue
    tokens.append(line.split()[1])


with open(output_file, "w") as f:
    f.write(string.encode("utf8"))