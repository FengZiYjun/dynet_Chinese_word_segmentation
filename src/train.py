import numpy as np
from model import dy_train_model
import argparse 


#random-seed pku 3388302431
#random-seed msr 2374973769

if __name__ == "__main__":
      
    parser = argparse.ArgumentParser()
    parser.add_argument("--train")
    parser.add_argument("--dev")
    parser.add_argument("--test")
    parser.add_argument("--dynet-devices")
    args = parser.parse_args()
    train = args.train
    dev = args.dev
    test = args.test
    
    dy_train_model(
            max_epochs = 30,
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
            train_file = train,
            dev_file = dev,
            test_file = test,
            pre_trained = None,
            lr = 0.1,
            edecay = 0.05, #msr,pku 0.2,0.1
            momentum = 0.5,           
            word_proportion= 0.5       
            )
