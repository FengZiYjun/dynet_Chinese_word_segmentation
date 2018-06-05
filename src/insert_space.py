

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input")
parser.add_argument("--output")
args = parser.parse_args()
input_file = args.input
output_file = args.output


with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

string = ""
for line in lines:
    char_list = []
    for char in line:
        char_list.append(char)
    string += (" ".join(char_list))

with open(output_file, "w", encoding="utf-8") as f:
    f.write(string)
