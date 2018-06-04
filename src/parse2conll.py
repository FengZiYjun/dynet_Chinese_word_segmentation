# -*- coding: UTF-8 -*-

"""
convert parsed text to conll format file (first two columns)

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

string = ""

for line in lines:
    tokens = line.split()
    for idx, token in enumerate(tokens):
        string += (str(idx + 1) + "\t" + token + "\n")
    string += "\n"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(string)
