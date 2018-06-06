import random as rnd


def nlp000(s: str) -> str:
    return s[::-1]


def nlp001(s: str) -> str:
    return s[1::2]


def nlp002(s1: str, s2: str):
    return ''.join([s1[i] + s2[i] for i in range(len(s1))])


def nlp003(s: str) -> list[int]:
    return [len(word) for word in s.split(" ")]


def nlp004(s: str) -> dict:
    one_list = [1, 5, 6, 7, 8, 9, 15, 16, 19]
    return {word[0:1] if i + 1 in one_list else word[0:2]: i for i, word in enumerate(s.split(" "))}


def nlp005(s: str, n: int = 2) -> dict:
    words = [word for word in s.split(" ")]
    return {'word-bigram': [words[i:i + n] for i in range(len(words) - n + 1)],
            'character-bigram': [s[i:i + n] for i in range(len(s) - n + 1)]}


def nlp006(x: str, y: str) -> dict:
    X, Y = set(x), set(y)
    return {
        'union': X.union(Y),
        'intersection': X.intersection(Y),
        'difference': X.difference(Y),
        'include_se_X': x.find("se") > -1,
        'include_"se"_y': y.find("se") > -1
    }


def nlp007(x: int, y: str, z: float) -> str:
    return "{}時の{}は{}".format(x, y, z)


def cipher(s: str) -> str:
    return ''.join([chr(219 - ord(s[i])) if (ord('a') <= ord(s[i]) <= ord('z')) else s[i] for i in range(len(s))])


def nlp008(s: str) -> dict:
    return {'encode': cipher(s), 'decode': cipher(cipher(s))}


def nlp009(s: str) -> str:
    words = s.split(" ")
    return " ".join([word[0] + ''.join(rnd.sample(list(word[1:-1]), len(word[1: -1]))) + word[-1] if len(word) > 4
                     else word for word in words])



if __name__ == '__main__':
    print(0, nlp000("stressed"))
    print(1, nlp001("パタトクカシーー"))
    print(2, nlp002("パトカー", "タクシー"))
    print(3, nlp003("Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."))
    print(4, nlp004(
        "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."))
    print(5, nlp005("I am an NLPer"))
    print(6, nlp006("paraparaparadise", "paragraph"))
    print(7, nlp007(12, "気温", 22.4))
    print(8, nlp008("I am 18 years old"))
    print(9, nlp009("I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."))
