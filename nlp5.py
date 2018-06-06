import re
from nltk import stem
from bs4 import BeautifulSoup


class Token():
    def __init__(self, token):
        self.id = token.get('id')
        self.word = token.word.string
        self.lemma = token.lemma.string
        self.characteroffsetbegin = token.characteroffsetbegin.string
        self.characteroffsetend = token.characteroffsetend.string
        self.pos = token.pos.string
        self.ner = token.ner.string
        self.speaker = token.speaker.string if token.speaker is not None else None
        # self.to_string()

    def toString(self):
        return (self.id, self.word, self.lemma, self.characteroffsetbegin, self.characteroffsetend, self.pos, self.ner,
                self.speaker)

    def toStringTag(self):
        return '{}\t{}\t{}'.format(self.word, self.lemma, self.pos)


class Sentence():
    def __init__(self, sentence):
        self.id = sentence.get('id')
        self.tokens = [Token(token) for token in sentence.find_all('token') if token is not None]


class Mention:
    def __init__(self, mention):
        self.representative = mention.get('representative') is not None
        self.sentence = mention.sentence.string
        self.start = mention.start.string
        self.end = mention.end.string
        self.head = mention.head.string
        self.text = mention.find('text').text
        # print(self.to_string())

    def to_string(self):
        return '{}\t{}\t{}\t{}\t{}\t{}'.format(self.representative, self.sentence, self.start,
                                               self.end, self.head, self.text)


class Coreference:
    def __init__(self, coreference):
        self.mentions = [Mention(mention) for mention in coreference.find_all('mention') if mention is not None]


class Dep:
    def __init__(self, dep):
        self.type = dep.get('type')
        self.governor_idx = dep.governor.get('idx')
        self.governor = dep.governor.string
        self.dependent_idx = dep.dependent.get('idx')
        self.dependent = dep.dependent.string
        # print(dep)
        # print(self.to_string())

    def to_string(self):
        return '{}\t{}\t{}\t{}\t{}'.format(self.type, self.governor_idx, self.governor, self.dependent_idx, self.dependent)


class Dependency:
    def __init__(self, dependency):
        self.dependency = [Dep(dep) for dep in dependency.find_all('dep') if dep is not None]


class Document:
    def __init__(self, path: str) -> None:
        xml = ''
        with open(path, 'r') as fr:
            xml = BeautifulSoup('\n'.join(fr.readlines()), 'html.parser')
        self.coreferences = [Coreference(coreference) for tmp in xml.find_all('coreference') for coreference in
                             tmp.find_all('coreference') if coreference is not None]
        self.sentences = [Sentence(sentence) for sentence in
                          xml.find('sentences').find_all('sentence') if sentence is not None]
        self.dependencies = [Dependency(dependency) for dependency in
                             xml.find_all('dependencies') if dependency is not None]


def nlp50(path: str) -> list:
    with open(path) as fr:
        res = list()
        for row in fr:
            sentences = re.sub('([\.;:\?\!]) ([A-Z])', '\\1<kugiri>\\2', row.replace('\n', '')).split('<kugiri>')
            if len(sentences) == 1 and sentences[0] == '':
                continue
            res.extend(sentences)
    return res


def nlp51(sentences: list) -> list:
    return [sentence.replace(' ', '\n') + '\n' for sentence in sentences]


def nlp52(sentences: list) -> list:
    stemmer = stem.PorterStemmer()
    return ['\n'.join([stemmer.stem(word) for word in sentence.split('\n')]) for sentence in sentences]


def nlp53(path: str) -> list:
    return [[token.word for token in sentence.tokens] for sentence in Document(path).sentences]


def nlp54(path: str) -> list:
    return [[token.toStringTag() for token in sentence.tokens] for sentence in Document(path).sentences]


def nlp55(path: str) -> list:
    return [token.word for sentence in Document(path).sentences for token in sentence.tokens if token.ner == 'PERSON']


def nlp56(path: str) -> list:
    return [coreference for coreference in Document(path).coreferences]
    # 未完了



if __name__ == '__main__':
    # sentences = nlp50('nlp.txt')
    # print(50, sentences)
    # sentences2 = nlp51(sentences)
    # print(51, sentences2)
    # print(52, nlp52(sentences2))
    # print(53, nlp53('nlp.xml'))
    # print(54, nlp54('nlp.xml'))
    # print(55, nlp55('nlp.xml'))
    # print(56, nlp56('nlp.xml'))
    print(57, nlp56('nlp.xml'))
