import MeCab


m = MeCab.Tagger ("-Ochasen")
sentence = "今日は晴れです"


def nlp30(sentence):
    words = m.parse(sentence)
    morphemes = []
    for word in words.split('\n'):
        node = word.split("\t")
        if len(node) != 6:
            continue
        morpheme = {
            'surface': node[0],
            'base': node[2],
            'pos': node[3] if len(node[3].split("-")) == 1 else node[3].split("-")[0],
            'pos1': '*' if len(node[3].split("-")) == 1 else node[3].split("-")[1]
        }
        morphemes.append(morpheme)
    return morphemes


def nlp31(fpath):
    verbs = []
    with open(fpath, 'r') as fr:
        for row in fr:
            morphemes = nlp30(row)
            for morpheme in morphemes:
                if morpheme["pos"] == '動詞':
                    verbs.append(morpheme['surface'])
    return set(verbs)

def nlp32(fpath):
    verbs = []
    with open(fpath, 'r') as fr:
        for row in fr:
            morphemes = nlp30(row)
            for morpheme in morphemes:
                if morpheme["pos"] == '動詞':
                    verbs.append(morpheme['base'])
    return set(verbs)


def nlp33(fpath):
    verbs = []
    with open(fpath, 'r') as fr:
        for row in fr:
            morphemes = nlp30(row)
            for morpheme in morphemes:
                if morpheme["pos"] == '名詞' and morpheme["pos1"] == 'サ変接続':
                    verbs.append(morpheme['surface'])
    return set(verbs)


def nlp34(fpath):
    noun_phrases = []

    with open(fpath, 'r') as fr:
        for row in fr:
            morphemes = nlp30(row)
            for i, morpheme in enumerate(morphemes):
                if len(morphemes) <= i + 2:
                    break
                if morpheme["pos"] == '名詞' and morphemes[i + 1]["surface"] == 'の' and morphemes[i+2]["pos"] == '名詞':
                    noun_phrases.append(morpheme['surface'] + morphemes[i+1]['surface'] + morphemes[i+2]['surface'])
    return set(noun_phrases)


def nlp35(fpath):
    noun_phrases = []

    with open(fpath, 'r') as fr:
        nouns = ''
        for row in fr:
            morphemes = nlp30(row)
            for morpheme in morphemes:
                if morpheme['pos'] == '名詞':
                    nouns += morpheme['surface']
                elif nouns != '':
                    noun_phrases.append(nouns)
                    nouns = ''
            if nouns != '':
                noun_phrases.append(nouns)
                nouns = ''

    return set(noun_phrases)


def nlp36(fpath):
    words = {}

    with open(fpath, 'r') as fr:
        for row in fr:
            morphemes = nlp30(row)
            for morpheme in morphemes:
                word = morpheme['base']
                words[word] = 1 if word not in words.keys() else words[word] + 1
    return sorted(words.items(), key=lambda x: -x[1])

import matplotlib.pyplot as plt
import matplotlib

def nlp37(fpath):
    words = nlp36(fpath)[0:10]
    label = [word[0] for word in words]
    value = [word[1] for word in words]
    print(label)
    print(matplotlib.rcParams['font.family'])
    plt.bar(list(range(len(value))), height=value, tick_label=label)
    plt.xlabel("単語")
    plt.ylabel("頻度")
    plt.show()


def nlp38(fpath):
    words = nlp36(fpath)
    label = [word[0] for word in words]
    value = [word[1] for word in words]
    print(value)
    plt.hist(value, bins=20, range=(0, 100))
    # plt.xlabel("単語")
    # plt.ylabel("頻度")
    plt.show()


from scipy import stats
import numpy as np


def nlp39(fpath):
    words = nlp36(fpath)
    # label = [word[0] for word in words]
    value = np.array([word[1] for word in words])
    print(value)

    dic = {}
    for v in value:
        dic[str(v)] = 1 if str(v) not in dic.keys() else dic[str(v)] + 1




    rank = stats.rankdata(np.array(list(dic.values())), method='dense')
    print(rank)
    plt.xscale("log")
    plt.yscale("log")
    plt.hist(rank, 40)
    # # plt.xlabel("単語")
    # # plt.ylabel("頻度")
    plt.show()



if __name__ == '__main__':
# print(30, nlp30('今日は晴れでした'))
    # print(31, nlp31('./neko.txt'))
    # print(32, nlp32('./neko.txt'))
    # print(33, nlp33('./neko.txt'))
    # print(34, nlp34('./neko.txt'))
    # print(35, nlp35('./neko.txt'))
    # print(36, nlp36('./neko.txt'))
    # print(37, nlp37('./neko.txt'))
    # print(38, nlp38('./neko.txt'))
    print(39, nlp39('./neko.txt'))