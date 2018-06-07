"""
    Each line is a segmented sentence.
    compare two files with "BMES" labels.
"""
import argparse


def labeling(sent):
    char_label = []  # list of tuple of (char, label)
    tokens = sent.strip().split()
    for token in tokens:
        if len(token) == 1:
            char_label.append((token, "S"))
        else:
            char_label.append((token[0], "B"))
            for x in range(1, len(token) - 1):
                char_label.append((token[x], "M"))
            char_label.append((token[-1], "E"))
    return char_label


def compare_seg(file1, file2):
    with open(file1, "r", encoding="utf-8") as f:
        lines1 = f.readlines()
    with open(file2, "r", encoding="utf-8") as f:
        lines2 = f.readlines()
    if len(lines1) != len(lines2):
        print("number of sentences not equal")
        return

    total = 0
    correct = 0
    for sent1, sent2 in zip(lines1, lines2):
        labels1 = labeling(sent1)
        labels2 = labeling(sent2)
        if len(labels1) != len(labels2):
            print("label sequence length differ")
            return
        for char1, char2 in zip(labels1, labels2):
            if char1[0] != char2[0]:
                print("char not the same")
                return
            else:
                total += 1
                if char1[1] == char2[1]:
                    correct += 1
    return correct / total


if __name__ == "__name__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--f1", type=str)
    parser.add_argument("--f2", type=str)
    args = parser.parse_args()

    x = compare_seg(args.f1, args.f2)
    print("BMES label similarity=", x)
