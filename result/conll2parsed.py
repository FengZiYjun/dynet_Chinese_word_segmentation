"""
build parsed text from conllu files

"""

with open("zh.conllu", "r", encoding="utf-8") as f:
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


with open("test_gold", "w", encoding="utf-8") as f:
    f.write(string)