from src.model import dy_train_model


def from_dynet(path_to_model, train_file, test_file):
    return dy_train_model(
        infer_mode=True,
        max_epochs=40,
        batch_size=128,
        char_dims=50,
        word_dims=50,
        nhiddens=50,
        dropout_rate=0.2,
        max_word_len=4,
        load_params=path_to_model,
        margin_loss_discount=0.2,
        max_sent_len=60,
        shuffle_data=True,
        train_file=train_file,
        dev_file=None,
        test_file=test_file,
        test_output=None,
        pre_trained=None,
        lr=0.1,
        edecay=0.05,  # msr,pku 0.2,0.1
        momentum=0.5,
        word_proportion=0.5
    )


if __name__ == "__main__":
    x = from_dynet(path_to_model="./result/model/best_cws_model", train_file="./data/zh_gsd-ud-train.conllu",
               test_file="./data/dev_raw")
    print(x)
