import numpy as np
from model import dy_train_model
 


#random-seed pku 3388302431
#random-seed msr 2374973769

if __name__ == "__main__":
      dy_train_model(
            max_epochs = 40,
            batch_size = 256,
            char_dims = 100,
            word_dims = 50,
            nhiddens = 50,
            dropout_rate = 0.2,
            max_word_len = 4,
            load_params = None, # None for train mode, otherwise please specify the parameter file.   
            margin_loss_discount = 0.2,
            max_sent_len = 60,
            shuffle_data = True,
            train_file = '../data/zh-train',
            dev_file = '../data/zh-test',   # dev/test in train/test mode.
            pre_trained = None,
            lr = 0.1,
            edecay = 0.05, #msr,pku 0.2,0.1
            momentum = 0.5,           
            word_proportion= 0.5       
            )
