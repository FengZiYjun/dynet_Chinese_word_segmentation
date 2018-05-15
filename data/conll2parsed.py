"""
build parsed text from conllu files

"""

original_file = "zh-ud-train.conllu"
parsed_file = "zh-train"

with open(original_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

tokens = []
string = ""
for line in lines:
    if line[0] == '#':
        continue
    if line == "\n":
        string += ("  ".join(tokens) + "\n")
        tokens = []
        continue
    tokens.append(line.split()[1])


with open(parsed_file, "w", encoding="utf-8") as f:
    f.write(string)
