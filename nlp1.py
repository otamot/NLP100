from operator import itemgetter


def nlp010(fpath):
    with open(fpath, 'r') as f:
        return len(f.readlines())


def nlp011(fpath):
    output = 'nlp011-out.txt'
    with open(fpath, 'r') as fr:
        with open(output, 'w') as fw:
            for row in fr:
                fw.write(row.replace('\t', ' '))
    return output


def nlp012(fpath):
    output1 = 'nlp012-col1.txt'
    output2 = 'nlp012-col2.txt'
    with open(fpath, 'r') as fr:
        with open(output1, 'w') as fw1:
            with open(output2, 'w') as fw2:
                for row in fr:
                    cols = row.split("\t")
                    fw1.write('{}\n'.format(cols[0]))
                    fw2.write('{}\n'.format(cols[1]))
    return output1, output2


def nlp013(fpath1, fpath2):
    output = 'nlp013-out.txt'
    with open(fpath1, 'r') as fr1:
        with open(fpath2, 'r') as fr2:
            with open(output, 'w') as fw:
                for row1, row2 in zip(fr1, fr2):
                    fw.write('{}\t{}\n'.format(row1.replace('\n', ''), row2.replace('\n', '')))
    return output


def nlp014(fpath, n=10):
    with open(fpath, 'r') as fr:
        return ''.join(fr.readlines()[0:n])



def nlp015(fpath, n=10):
    with open(fpath, 'r') as fr:
        return ''.join(fr.readlines()[-n:])


def nlp016(fpath, n=3):
    with open(fpath, 'r') as fr:
        lines = fr.readlines()
        n_lines = len(lines)
        div = n_lines // n
        mod = n_lines % n
        outputs = ['nlp016-out-{}.txt'.format(i) for i in range(n)]
        for i, fpath in enumerate(outputs):
            with open(fpath, 'w') as fw:
                fw.write(''.join(lines[div*i+min(i, mod): div*(i+1)+min(i+1, mod)]))
    return outputs


def nlp017(fpath):
    with open(fpath, 'r') as fr:
        return set(fr.readlines()[0].replace('\n', '').split('\t'))


def nlp018(fpath):
    with open(fpath, 'r') as fr:
        lines = [row.split('\t') for row in fr.readlines()]
        lines.sort(key=itemgetter(2), reverse=True)
        return ''.join(['\t'.join(words) for words in lines])


def nlp019(fpath):
    with open(fpath, 'r') as fr:
        words = [row.split('\t')[0] for row in fr.readlines()]
        dic = {}
        for word in words:
            dic[word] = dic[word] + 1 if word in dic.keys() else 1
        dic_list = sorted(dic.items(), key=lambda x:-x[1])
        return '\n'.join(['{}\t{}'.format(k, v) for k, v in dic_list])




if __name__ == '__main__':
    print(10, nlp010('./hightemp.txt'))
    print(11, nlp011('./hightemp.txt'))
    print(12, nlp012('./hightemp.txt'))
    print(13, nlp013('nlp012-col1.txt', 'nlp012-col2.txt'))
    print(14, nlp014('./hightemp.txt'))
    print(15, nlp015('./hightemp.txt'))
    print(16, nlp016('./hightemp.txt',5))
    print(17, nlp017('./hightemp.txt'))
    print(18, nlp018('./hightemp.txt'))
    print(19, nlp019('./hightemp.txt'))