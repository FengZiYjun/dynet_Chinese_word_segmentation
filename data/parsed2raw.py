"""
convert the parsed text file into raw file
raw text: no word seg + no sentence seg

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

string = ""
for line in lines:
    line = line.decode("utf8")
    string += "".join(line.strip().split())

with open(output_file, "w") as f:
    f.write(string.encode("utf8"))

