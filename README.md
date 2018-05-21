# greedyCWS

### Updated from contributor FengZiYjun

1. Change the scoring script.
2. Introduce dev set.
3. Predict on test set only when dev set gets higher accuracy.
4. Deal with train/dev input with *conllu* format, and test input of raw text.
5. The final result of test output will be converted into the first two columns of a *conllu* file.

Specify the train/dev/test file as command line parameters `--train`, `--dev`, and `--test`.

Choose a GPU run by dynet. `--dynet-devices GPU: 0`

```cmd
cd src
python train.py --train ../data/zh-ud-train.conllu --dev ../data/zh-ud-dev.conllu --test ../data/zh_test_raw --dynet-devices GPU:4
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


