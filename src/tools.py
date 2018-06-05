# -*- coding: UTF-8 -*-
from collections import defaultdict

import numpy as np
import random
import gensim
import re


def initCemb(ndims, train_file, pre_trained, thr=5.):
    f = open(train_file, "r", encoding="utf-8")
    train_vocab = defaultdict(float)
    for line in f.readlines():
        sent = line.split()
        for word in sent:
            for character in word:
                train_vocab[character] += 1
    f.close()
    character_vecs = {}
    for character in train_vocab:
        if train_vocab[character]< thr:
            continue
        character_vecs[character] = np.random.uniform(-0.5/ndims, 0.5/ndims, ndims)
    if pre_trained is not None:
        pre_trained = gensim.models.Word2Vec.load(pre_trained)
        pre_trained_vocab = set([w for w in pre_trained.vocab.keys()])
        for character in pre_trained_vocab:
            character_vecs[character] = pre_trained[character]
    Cemb = np.zeros(shape=(len(character_vecs)+1, ndims))
    idx = 1
    character_idx_map = dict()
    for character in character_vecs:
        Cemb[idx] = character_vecs[character]
        character_idx_map[character] = idx
        idx += 1
    return Cemb, character_idx_map


def SMEB(lens):
    idxs = []
    for len in lens:
        for i in range(len-1):
            idxs.append(0)
        idxs.append(len)
    return idxs


def prepareData(character_idx_map, path, test=False):
    seqs, wlenss, idxss = [], [], []
    f = open(path, "r", encoding="utf-8")
    for line in f.readlines():
        sent = line.split()
        Left = 0
        for idx, word in enumerate(sent):
            if len(re.sub('\W', '', word, flags=re.U)) == 0:
                if idx > Left:
                    seqs.append(list(''.join(sent[Left:idx])))
                    wlenss.append([len(word) for word in sent[Left:idx]])
                Left = idx+1
        if Left != len(sent):
            seqs.append(list(''.join(sent[Left:])))
            wlenss.append([len(word) for word in sent[Left:]])
    seqs = [[character_idx_map[character] if character in character_idx_map else 0 for character in seq] for seq in seqs]
    f.close()
    if test:
        return seqs
    for wlens in wlenss:
        idxss.append(SMEB(wlens))
    return seqs, wlenss, idxss


def conll2seg(input_file, output_file):
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
    return string


def sent_seg(input_file, output_file):
    cut_list = "."
    NUM = "0123456789"
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()
    tokens = []
    str_list = list()
    start = 0
    end = 0
    for i in range(len(content)):
        if content[i] in cut_list and content[i - 1] not in NUM:
            end = i
            str_list.append(content[start:end + 1] + "\n")
            start = i + 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("".join(str_list))


