# greedyCWS

### Updated from contributor FengZiYjun

0. Upgrade to Python 3.
1. Change the scoring script. Use "BMES" labels as critarion.
2. Introduce dev set. Save model and predict on test set only when dev set gets higher accuracy, if test set specified during training.
3. Train/Dev input is in *conllu* format. Test input is a raw text.
4. The final result of test output will be converted into the first two columns of a *conllu* file.
5. Specify the train/dev/test file as command line parameters `--train`, `--dev`, and `--test`. `--epoch <int>` sets the maximum epochs for training.
6. Add inference mode for deployment. Set `--infer_model <saved_model>` to turn on inference mode, otherwise training mode. `--test` and `--train` must be specified for inference.

Choose a GPU run by dynet. `--dynet-devices GPU: 0`

Training command:
```cmd
cd src
python train.py --epoch 40 --train ../data/zh-ud-train.conllu --dev ../data/zh-ud-dev.conllu  --dynet-devices GPU:0 
```

Testing command:
```cmd
cd src
python train.py --infer_model ../result/model/best_cws_model  --test ../data/zh_test_raw  --train ../data/train_parsed
```


**-------------- original README.md ---------------------------**

Hi, this code is easy to use!

Please check the `src/train.py` for all hyper-parameter and IO settings.

You can modify the `src/train.py` to speficy your own model settings or datasets.


- For training, use the command line `python train.py`. Training details will be printed on the screen and the tuned parameters will be saved in your disk per epoch. Those files saving the paramters will be named such as `epoch1`, `epoch2`, `...`, and placed in the same directory as `train.py`.

- For test, use the same command line `python train.py`. The segmented result will be saved in `src/result`

The **only difference** between training and test is that whether you specified a parameter file or not, through the function argument `load_params` in `train.py`. In addition, please tell the program your test file by setting `dev_file` (Yes, when test, consider it as "test_file").


## Citation
This code implements an efficient and effective neural word segmenter proposed in the following paper.

Deng Cai, Hai Zhao, etc., Fast and Accurate Neural Word Segmentation for Chinese. ACL 2017.

If you find it useful, please cite the [paper](http://aclweb.org/anthology/P17-2096).
```
@InProceedings{cai-EtAl:2017:Short,
  author    = {Cai, Deng  and  Zhao, Hai  and  Zhang, Zhisong  and  Xin, Yuan  and  Wu, Yongjian  and  Huang, Feiyue},
  title     = {Fast and Accurate Neural Word Segmentation for Chinese},
  booktitle = {Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)},
  month     = {July},
  year      = {2017},
  address   = {Vancouver, Canada},
  publisher = {Association for Computational Linguistics},
  pages     = {608--615},
  url       = {http://aclweb.org/anthology/P17-2096}
}
```

## Contact
Drop me (Deng Cai) an email at thisisjcykcd (AT) gmail.com if you have any question.


