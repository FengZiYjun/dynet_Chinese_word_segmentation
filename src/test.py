# -*- coding: UTF-8 -*-
import re
from tools import prepareData

def test(cws,filename,output_path, character_idx_map):

    def seg(char_seq,text):
        lens = cws.forward(char_seq)
        res, begin =[], 0
        for wlen in lens:
            res.append(''.join(text[begin:begin+wlen]))
            begin+=wlen
        return res

    char_seqs = prepareData(character_idx_map,filename,test=True)
    fo = open(output_path,'w', encoding="utf-8")
    seq_idx = 0 
    for line in open(filename, "r", encoding="utf-8").readlines():
        sent = (line).split()
        Left = 0
        output_sent = []
        for idx,word in enumerate(sent):
            if len(re.sub('\W','',word,flags=re.U))==0:
                if idx>Left:
                    words =seg(char_seqs[seq_idx],list(''.join(sent[Left:idx])))
                    seq_idx += 1
                    output_sent.extend(words)
                Left = idx+1
                output_sent.append(word)
        if Left!=len(sent):
            words = seg(char_seqs[seq_idx],list(''.join(sent[Left:])))
            seq_idx += 1
            output_sent.extend(words)
        output_sent = '  '.join(output_sent) + '\r\n'
        fo.write(output_sent)
    fo.close()
