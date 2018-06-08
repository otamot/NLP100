import random
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
import matplotlib.pyplot as plt
from sklearn.metrics import average_precision_score, precision_recall_curve
from sklearn.cross_validation import KFold

stemmer = nltk.PorterStemmer()
STOP_WORD = ['.', 'the', 'a', ',']


def nlp70(neg_path: str, pos_path: str, output_path: str) -> None:
    data = []
    data.extend(['{} {}'.format('+1', line) for line in open(neg_path, 'r', encoding='ISO-8859-1')])
    data.extend(['{} {}'.format('-1', line) for line in open(pos_path, 'r', encoding='ISO-8859-1')])
    random.shuffle(data)
    with open(output_path, 'w') as fw:
        fw.write(''.join(data))
    return


def nlp71(sentence: str):
    return len([word for word in sentence.split(' ') if word in STOP_WORD]) != 0


def nlp72(path: str):
    return [[word if i == 0 else stemmer.stem(word) for i, word in enumerate(line.split(' ')) if nlp71(word) == False]
            for line in open(path, 'r')]


def nlp73(path: str):
    data = nlp72(path)
    label = [line[0] for line in data]
    data = [' '.join(line[1:]) for line in data]
    count = CountVectorizer()
    bag = count.fit_transform(np.array(data))
    lr = LogisticRegression()
    train = bag.toarray()
    lr.fit(train, label)

    return lr, count, count.vocabulary_, train, label


def nlp74(sentence: str):
    words = ([stemmer.stem(word) for word in sentence.split(' ') if nlp71(word) == False])
    bow = np.zeros(len(vocab))
    for word in words:
        if word in vocab.keys():
            bow[vocab[word]] += 1
    return lr.predict_proba([bow]), lr.predict([bow])


def nlp75(lr, vocab):
    vocab_ = {v: k for k, v in vocab.items()}
    return [vocab_[index] for index in np.argsort(lr.coef_)[0][0:10]], [vocab_[index] for index in
                                                                        np.argsort(lr.coef_)[0][-10:]]


def nlp76(lr, label, train):
    return [[seikai, yosoku, kakuritsu] for seikai, yosoku, kakuritsu in
            zip(label, lr.predict(train), lr.predict_proba(train))]


def nlp77(lr, label, train):
    x = nlp76(lr, label, train)
    accuracy = sum([x_[0] == x_[1] for x_ in x]) / len(x)
    tp = sum([x_[0] == x_[1] == '+1' for x_ in x])
    fp = sum([x_[0] != x_[1] == '+1' for x_ in x])
    tn = sum([x_[0] == '+1' != x_[1] for x_ in x])
    fn = sum([x_[0] == x_[1] == '-1' for x_ in x])
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * recall * precision / (recall + precision)
    return 'accuracy:{}, precision:{}, recall:{}, F1:{}'.format(accuracy, precision, recall, f1)


def nlp78(train, label):
    lr = LogisticRegression()
    y = np.array(label)
    kekka = []
    for training, test in KFold(n=len(train), n_folds=5):
        train_x = train[training]
        train_y = y[training]
        test_x = train[test]
        test_y = y[test]
        lr.fit(train_x, train_y)
        x = [[seikai, yosoku, kakuritsu] for seikai, yosoku, kakuritsu in
             zip(test_y, lr.predict(test_x), lr.predict_proba(test_x))]
        accuracy = sum([x_[0] == x_[1] for x_ in x]) / len(x)
        tp = sum([x_[0] == x_[1] == '+1' for x_ in x])
        fp = sum([x_[0] != x_[1] == '+1' for x_ in x])
        tn = sum([x_[0] == '+1' != x_[1] for x_ in x])
        fn = sum([x_[0] == x_[1] == '-1' for x_ in x])
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * recall * precision / (recall + precision)
        kekka.append('accuracy:{}, precision:{}, recall:{}, F1:{}'.format(accuracy, precision, recall, f1))
    return kekka


def nlp79(train, label):
    lr = LogisticRegression()
    y = np.array(label)
    for training, test in KFold(n=len(train), n_folds=5):
        train_x = train[training]
        train_y = y[training]
        test_x = train[test]
        test_y = y[test]
        lr.fit(train_x, train_y)
        precision, recall, _ = precision_recall_curve([1 if line == '+1' else 0 for line in test_y],
                                                      np.array([line[0] for line in lr.predict_proba(test_x)]))
        plt.step(recall, precision, color='b', alpha=0.2, where='post')
        plt.fill_between(recall, precision, step='post', alpha=0.2, color='b')

        average_precision = average_precision_score([1 if line == '+1' else 0 for line in test_y],
                                                    np.array([line[0] for line in lr.predict_proba(test_x)]))

        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(average_precision))
        plt.show()
    return None


if __name__ == '__main__':
    # print(70, nlp70('rt-polaritydata/rt-polarity.neg', 'rt-polaritydata/rt-polarity.pos', 'sentiment.txt'))
    # print(71, nlp71('hi is the biggest man .'))
    # print(72, nlp72('sentiment.txt'))
    lr, count, vocab, train, label = nlp73('sentiment.txt')
    # print(74, nlp74('This is a pen'))
    # print(75, nlp75(lr, vocab))
    # print(nlp76(lr, label, train))
    # print(nlp77(lr, label, train))
    #     print(78, nlp78(train, label))
    print(79, nlp79(train, label))