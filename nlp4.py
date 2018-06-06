from typing import List

import CaboCha
from cabocha.analyzer import CaboChaAnalyzer
from graphviz import Digraph

analyzer = CaboChaAnalyzer()
c = CaboCha.Parser()


class Morph:
    def __init__(self, token) -> None:
        feature = token.feature.split(',')
        self.surface: str = token.surface
        self.base: str = feature[6]
        self.pos: str = feature[0]
        self.pos1: str = feature[1]


class Chunk:
    def __init__(self, chunk: CaboCha.Tree.chunk) -> None:
        self.morphs: List[Morph] = [Morph(morph) for morph in chunk]
        self.dst = chunk.next_link_id
        self.srcs = chunk.prev_link_ids

    def join_morphs(self) -> str:
        return ''.join([morph.surface for morph in self.morphs if morph.pos != '記号'])

    def has_pos(self, pos: str) -> bool:
        return sum([morph.pos == pos for morph in self.morphs]) > 0

    def has_pos2(self, pos2: str) -> bool:
        return sum([morph.pos2 == pos2 for morph in self.morphs]) == 1

    def first_pos(self, pos: str) -> Morph:
        for morph in self.morphs:
            if morph.pos == pos:
                return morph

    def last_pos(self, pos: str) -> Morph:
        for morph in self.morphs[::-1]:
            if morph.pos == pos:
                return morph

    def first_pos2(self, pos2: str) -> Morph:
        for morph in self.morphs:
            if morph.pos2 == pos2:
                return morph


def get_morph_list(sentence: str) -> List[Morph]:
    tree = c.parse(sentence)
    morphs = [Morph(tree.token(i)) for i in range(tree.token_size())]
    return morphs


def get_chunk_list(sentence: str) -> List[Chunk]:
    tree = analyzer.parse(sentence)
    chunks = [Chunk(chunk) for chunk in tree.chunks]
    return chunks


def nlp40(sentence: str) -> List[Morph]:
    return get_morph_list(sentence)


def nlp41(sentence: str) -> List[Chunk]:
    return get_chunk_list(sentence)


def join_received_relates(chunks: List[Chunk], index: int) -> str:
    return chunks[index].join_morphs() + '\t' + chunks[chunks[index].dst].join_morphs()


def nlp42(sentence: str) -> str:
    chunks = get_chunk_list(sentence)
    print(type(chunks))
    return '\n'.join([join_received_relates(chunks, i) for i, chunk in enumerate(chunks) if chunk.dst != -1])


def nlp43(sentence: str) -> str:
    chunks = get_chunk_list(sentence)
    return '\n'.join([join_received_relates(chunks, i) for i, chunk in enumerate(chunks) if
                      chunk.dst != -1 and chunk.has_pos('名詞') and chunks[chunk.dst].has_pos('動詞')])


def nlp44(sentence: str) -> None:
    chunks = get_chunk_list(sentence)
    G = Digraph(format='png')
    G.attr('node', shape='circle')
    for i, chunk in enumerate(chunks):
        G.edge(chunk.join_morphs(), chunks[chunk.dst].join_morphs())
    G.render('cabocha_tree')
    return


def nlp45(sentence: str) -> str:
    chunks = get_chunk_list(sentence)
    res = []
    for chunk in chunks:
        kaku = []
        if chunk.has_pos('動詞'):
            kaku.append(chunk.first_pos('動詞').base)
            for src in chunk.srcs:
                prev_chunk = chunks[src]
                if prev_chunk.has_pos('助詞'):
                    kaku.append(prev_chunk.last_pos('助詞').surface)
        if len(kaku) > 1:
            res.append('\t'.join(kaku))
    return '\n'.join(res)


def nlp46(sentence: str) -> str:
    chunks = get_chunk_list(sentence)
    res = []
    for chunk in chunks:
        joshi = []
        setsu = []
        if chunk.has_pos('動詞'):
            for src in chunk.srcs:
                prev_chunk = chunks[src]
                if prev_chunk.has_pos('助詞'):
                    joshi.append(prev_chunk.last_pos('助詞').surface)
                    setsu.append(prev_chunk.join_morphs())
        if len(joshi) > 0:
            res.append('{}\t{}\t{}'.format(chunk.last_pos('動詞').base, '\t'.join(joshi), '\t'.join(setsu)))
    return '\n'.join(res)


def nlp47(sentence: str) -> str:
    chunks = get_chunk_list(sentence)
    res = []
    for i, chunk in enumerate(chunks):
        if len(chunk.morphs) == 2 and chunk.morphs[0].pos == '名詞' and chunk.morphs[0].pos1 == 'サ変接続' and \
                chunk.morphs[1].surface == 'を' and chunk.morphs[1].pos == '助詞':
            if chunks[chunk.dst].has_pos('動詞'):
                kinoudoushi = '{}{}{}'.format(chunk.morphs[0].surface, chunk.morphs[1].surface,
                                              chunks[chunk.dst].first_pos('動詞').base)
                srcs = chunks[chunk.dst].srcs
                joshi = []
                setsu = []
                for src in srcs:
                    if src == i:
                        continue
                    prev_link = chunks[src]
                    if prev_link.has_pos('助詞'):
                        joshi.append(prev_link.last_pos('助詞').surface)
                        setsu.append(prev_link.join_morphs())
                if len(joshi) > 0:
                    res.append('{}\t{}\t{}'.format(kinoudoushi, '\t'.join(joshi), '\t'.join(setsu)))
    return '\n'.join(res)


def nlp48(sentence: str) -> str:
    chunks = get_chunk_list(sentence)
    res = []
    for i, chunk in enumerate(chunks):
        if chunk.has_pos('名詞'):
            path = [chunk.join_morphs()]
            j = i
            while True:
                next = chunks[j].dst
                if next == -1:
                    break
                path.append(chunks[next].join_morphs())
                j = next
            if len(path) > 1:
                res.append(' -> '.join(path))
    return '\n'.join(res)


def nlp48(sentence: str) -> str:
    return ''


if __name__ == '__main__':
    # print(40, nlp40("太郎はこの本を渡した。"))
    # print(41, nlp41("太郎はこの本を渡した。"))
    # print(42, nlp42("太郎はこの本を渡した"))
    # print(43, nlp43("太郎はこの本を渡した"))
    # print(44, nlp44("太郎はこの本を渡した"))
    # print(45, nlp45('吾輩はここで始めて人間というものを見た'))
    # print(46, nlp46('吾輩はここで始めて人間というものを見た'))
    # print(47, nlp47('別段くるにも及ばんさと、主人は手紙に返事をする。'))
    # print(48, nlp48('吾輩はここで始めて人間というものを見た'))
    print(49, nlp49('吾輩はここで始めて人間というものを見た'))
    pass
