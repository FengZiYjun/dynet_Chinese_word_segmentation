# -*- coding: UTF-8 -*-
import random,time,os
from collections import Counter, namedtuple

import numpy as np
import dynet as dy

from tools import initCemb, prepareData
from test import test

"""
File converts: 
test input: continued text ---(sentence_cut.py)---> test_cut
train/dev input: conll file ---(conll2parse.py)---> parsed text
this model input: parsed text/test_cut -------> word seg text
word seg text ---(parse2conll.py)---> conll file

Evaluation over dev:
dev parsed text ---(parse2cws.py)---> cws format file(dev_truth)
dev pred text ---(parse2cws.py)---> cws format file(dev_pred)
cws format files(dev_truth & dev_pred) ---(compare.py)---> tmp file(a float)
this model reads the float from tmp file
"""


np.random.seed(970)

Sentence = namedtuple('Sentence',['score','score_expr','LSTMState','y','prevState','wlen','golden'])


class CWS (object):
    def __init__(self, Cemb, options):
        #model = dy.Model()
        model = dy.ParameterCollection()
        #self.trainer = dy.MomentumSGDTrainer(model,options['lr'],options['momentum'],options['edecay']) # we use Momentum SGD
        self.trainer = dy.MomentumSGDTrainer(model,options['lr'],options['momentum'])# we use Momentum SGD
        self.params = self.initParams(model,Cemb,options)
        self.options = options
        self.model = model
        #self.character_idx_map = character_idx_map
        self.known_words = None
    
    def load(self,filename):
        self.model.populate(filename)

    def save(self,filename):
        self.model.save(filename)

    def use_word_embed(self,known_words):
        self.known_words = known_words
        self.params['word_embed'] = self.model.add_lookup_parameters((len(known_words),self.options['word_dims']))

    def initParams(self,model,Cemb,options):
        # initialize the model parameters  
        params = dict()
        params['embed'] = model.add_lookup_parameters(Cemb.shape)
        for row_num,vec in enumerate(Cemb):
            params['embed'].init_row(row_num, vec)
        params['lstm'] = dy.LSTMBuilder(1,options['word_dims'],options['nhiddens'],model)
        
        params['reset_gate_W'] = []
        params['reset_gate_b'] = []
        params['com_W'] = []
        params['com_b'] = []

        params['word_score_U'] = model.add_parameters(options['word_dims'])
        params['predict_W'] = model.add_parameters((options['word_dims'],options['nhiddens']))
        params['predict_b'] = model.add_parameters(options['word_dims'])
        for wlen in xrange(1,options['max_word_len']+1):
            params['reset_gate_W'].append(model.add_parameters((wlen*options['char_dims'],wlen*options['char_dims'])))
            params['reset_gate_b'].append(model.add_parameters(wlen*options['char_dims']))
            params['com_W'].append(model.add_parameters((options['word_dims'],wlen*options['char_dims'])))
            params['com_b'].append(model.add_parameters(options['word_dims']))
        params['<BoS>'] = model.add_parameters(options['word_dims'])
        return params
    
    def renew_cg(self):
        # renew the compute graph for every single instance
        dy.renew_cg()

        param_exprs = dict()
        param_exprs['U'] = dy.parameter(self.params['word_score_U'])
        param_exprs['pW'] = dy.parameter(self.params['predict_W'])
        param_exprs['pb'] = dy.parameter(self.params['predict_b'])
        param_exprs['<bos>'] = dy.parameter(self.params['<BoS>'])

        self.param_exprs = param_exprs
    
    def word_repr(self, char_seq, cembs):
        # obtain the word representation when given its character sequence

        wlen = len(char_seq)
        if 'rgW%d'%wlen not in self.param_exprs:
            self.param_exprs['rgW%d'%wlen] = dy.parameter(self.params['reset_gate_W'][wlen-1])
            self.param_exprs['rgb%d'%wlen] = dy.parameter(self.params['reset_gate_b'][wlen-1])
            self.param_exprs['cW%d'%wlen] = dy.parameter(self.params['com_W'][wlen-1])
            self.param_exprs['cb%d'%wlen] = dy.parameter(self.params['com_b'][wlen-1])

        chars = dy.concatenate(cembs)
        reset_gate = dy.logistic(self.param_exprs['rgW%d'%wlen] * chars + self.param_exprs['rgb%d'%wlen])
        word = dy.tanh(self.param_exprs['cW%d'%wlen] * dy.cmult(reset_gate,chars) + self.param_exprs['cb%d'%wlen])
        if self.known_words is not None and tuple(char_seq) in self.known_words:
            return (word + dy.lookup(self.params['word_embed'],self.known_words[tuple(char_seq)]))/2.
        return word

    def greedy_search(self, char_seq, truth = None, mu =0.):
        init_state = self.params['lstm'].initial_state().add_input(self.param_exprs['<bos>'])
        init_y = dy.tanh(self.param_exprs['pW'] * init_state.output() + self.param_exprs['pb'])
        init_score = dy.scalarInput(0.)
        init_sentence = Sentence(score=init_score.scalar_value(),score_expr=init_score,LSTMState =init_state, y= init_y , prevState = None, wlen=None, golden=True)
        
        if truth is not None:
            cembs = [ dy.dropout(dy.lookup(self.params['embed'],char),self.options['dropout_rate']) for char in char_seq ]
        else:
            cembs = [dy.lookup(self.params['embed'],char) for char in char_seq ]

        start_agenda = init_sentence
        agenda = [start_agenda]
        
        # add 1 line
        golden_sent = None

        for idx, _ in enumerate(char_seq,1): # from left to right, character by character
            now = None
            for wlen in xrange(1,min(idx,self.options['max_word_len'])+1): # generate word candidate vectors
                # join segmentation sent + word
                word = self.word_repr(char_seq[idx-wlen:idx], cembs[idx-wlen:idx])
                sent = agenda[idx-wlen]

                if truth is not None:
                    word = dy.dropout(word,self.options['dropout_rate'])
                
                word_score = dy.dot_product(word,self.param_exprs['U'])

                if truth is not None:
                    golden =  sent.golden and truth[idx-1]==wlen
                    margin = dy.scalarInput(mu*wlen if truth[idx-1]!=wlen else 0.)
                    score = margin + sent.score_expr + dy.dot_product(sent.y, word) + word_score
                else:
                    golden = False
                    score = sent.score_expr + dy.dot_product(sent.y, word) + word_score


                good = (now is None or now.score < score.scalar_value())
                if golden or good:
                    new_state = sent.LSTMState.add_input(word)
                    new_y = dy.tanh(self.param_exprs['pW'] * new_state.output() + self.param_exprs['pb'])
                    new_sent = Sentence(score=score.scalar_value(),score_expr=score,LSTMState=new_state,y=new_y, prevState=sent, wlen=wlen, golden=golden)
                    if good:
                        now = new_sent
                        # add 2 lines
                        if golden_sent == None:
                            golden_sent = new_sent
                    if golden:
                        golden_sent = new_sent

            agenda.append(now)
            if truth is not None and truth[idx-1]>0 and (not now.golden):
                return (now.score_expr - golden_sent.score_expr)

        if truth is not None:
            return (now.score_expr - golden_sent.score_expr)

        return agenda

    def forward(self, char_seq):
        self.renew_cg()
        agenda = self.greedy_search(char_seq)
        now = agenda[-1]
        ans = []
        while now.prevState is not None:
            ans.append(now.wlen)
            now = now.prevState
        return reversed(ans)


    def backward(self, char_seq, truth):
        self.renew_cg()
        loss = self.greedy_search(char_seq,truth,self.options['margin_loss_discount'])
        res = loss.scalar_value()
        loss.backward()
        return res

def dy_train_model(
    infer_mode = False,
    max_epochs = 30,
    batch_size = 256,
    char_dims = 50,
    word_dims = 100,
    nhiddens = 50,
    dropout_rate = 0.2,
    margin_loss_discount = 0.2,
    max_word_len = 4,
    load_params = None,
    max_sent_len = 60,
    shuffle_data = True,
    train_file = '../data/train',
    dev_file = '../data/dev',
    test_file = '../data/test',
    lr = 0.5,
    edecay = 0.1,
    momentum = 0.5,
    pre_trained = '../w2v/char_vecs_100',
    word_proportion = 0.5
):
    if infer_mode is False:
        # convert conll files into parsed text with conll2parse.py
        os.system("python ../result/conll2parsed.py --input %s --output ../data/train_parsed" % train_file)
        os.system("python ../result/conll2parsed.py --input %s --output ../data/dev_parsed" % dev_file)

        # replace dev_file & train_file with new file paths
        train_file = "../data/train_parsed"
        dev_file = "../data/dev_parsed"
        #print 'converted conllu input to word seg input'

        # sentence segmentation
        os.system("python ../result/sent_seg.py --input %s --output ../data/test_cut" % test_file)
        test_file = "../data/test_cut"
        #print 'finished sentence seg over test set'

    options = {"lr": lr, "momentum": momentum, "word_dims": word_dims, "char_dims": char_dims, 
            "nhiddens": nhiddens, "max_word_len": max_word_len, "dropout_rate": dropout_rate, 
            "margin_loss_discount": margin_loss_discount}
    #options = locals().copy()
    #print 'Model options:'
    #for kk,vv in options.iteritems():
        #print '\t',kk,'\t',vv

    print("char_embs={}, train_file={}, pre_train={}".format(char_dims, train_file, pre_trained))
    Cemb, character_idx_map = initCemb(char_dims,train_file,pre_trained)

    cws = CWS(Cemb, options)


    char_seq, _ , truth = prepareData(character_idx_map,train_file)
    
    if max_sent_len is not None:
        survived = []
        for idx,seq in enumerate(char_seq):
            if len(seq)<=max_sent_len and len(seq)>1:
                survived.append(idx)
        char_seq =  [ char_seq[idx]  for idx in survived]
        truth = [ truth[idx] for idx in survived]
    
    if word_proportion > 0:
        word_counter = Counter()
        for chars,labels in zip(char_seq,truth):
            word_counter.update(tuple(chars[idx-label:idx]) for idx,label in enumerate(labels,1))
        known_word_count  = int(word_proportion*len(word_counter))
        known_words =  dict(word_counter.most_common()[:known_word_count])
        idx = 0
        for word in known_words:
            known_words[word] = idx
            idx+=1
        cws.use_word_embed(known_words)

    n = len(char_seq)
    #print 'Total number of training instances:',n


    if infer_mode:
        if load_params is not None:
            cws.load(load_params)
            test(cws, test_file, "../result/test_result", character_idx_map)
            exit()
        else:
            print("Please provide load_params")
            exit()

    #print 'Start training model'
    start_time = time.time()
    nsamples = 0


    best_accuracy = 0.0

    # Main training loop
    for eidx in xrange(max_epochs):
        idx_list = range(n)
        if shuffle_data:
            np.random.shuffle(idx_list)

        for idx in idx_list:
            loss = cws.backward(char_seq[idx],truth[idx])
            if np.isnan(loss):
                #print 'somthing went wrong, loss is nan.'
                return
            nsamples += 1
            if nsamples % batch_size == 0:
                cws.trainer.update()

        #cws.trainer.update_epoch(1.)  # update to latest dynet
        end_time = time.time()
        #print 'Trained %s epoch(s) (%d samples) took %.lfs per epoch'%(eidx+1,nsamples,(end_time-start_time)/(eidx+1))       

        # predict on dev set
        test(cws, dev_file, '../result/dev_result%d'%(eidx+1), character_idx_map)

        # convert dev parsed text into CWS BMES format
        os.system("python ../result/parsed2cws.py --input ../result/dev_result%d " 
                  " --output ../result/dev_result%d_cws " % (eidx + 1, eidx + 1))

        # prepare dev ground truth
        if not os.path.exists("../result/dev_gold_cws"):
            os.system("python ../result/parsed2cws.py --input %s --output ../result/dev_gold_cws" % dev_file)

        # compare dev prediction & ground truth
        os.system("python ../result/compare.py --f1 ../result/dev_result%d_cws --f2 ../result/dev_gold_cws"
                  " --output ../result/tmp" % (eidx + 1))

        with open("../result/tmp", "r") as f:
            accuracy = f.read()
        accuracy = float(accuracy)

        os.system("rm ../result/tmp")

        print('Accuracy = %s' % (accuracy))

        # predict on test set if dev gets better accuracy
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            # predict on test file
            print("Testing on test set.")
            test(cws, test_file, '../result/pred_test', character_idx_map)

            #os.system('python score.py %s %d %d'%(dev_file,eidx+1,eidx+1))
            cws.save("../result/model/best_cws_model")
            print('Current model saved')


    # main loop ends

    # convert final pred_test into conll format
    os.system("python ../result/parse2conll.py --input ../result/pred_test --output ../result/test.conll")
