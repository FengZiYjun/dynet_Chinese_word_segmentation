# coding=utf-8

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input")
parser.add_argument("--output")
args = parser.parse_args()
input_file = args.input
output_file = args.output

cut_list = "."
NUM = "0123456789"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

tokens = []
str_list = list()
start = 0
end = 0
for i in range(len(content)):
    if content[i] in cut_list and content[i-1] not in NUM:
        end = i
        str_list.append(content[start:end+1] + "\n")
        start = i+1

with open(output_file, "w", encoding="utf-8") as f:
    f.write("".join(str_list))
