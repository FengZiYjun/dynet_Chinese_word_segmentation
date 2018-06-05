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


with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

tokens = []
string = ""
for line in lines:
    if line[0] == '#':
        continue
    if line == "\n":
        string += (" ".join(tokens) + "\n")
        tokens = []
        continue
    tokens.append(line.split()[1])


with open(output_file, "w", encoding="utf-8") as f:
    f.write(string)
