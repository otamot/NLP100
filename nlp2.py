from operator import itemgetter
import json
import re
import urllib.request


def nlp20(fpath):
    with open(fpath, 'r') as fr:
        for row in fr:
            js_dict = json.loads(row)
            if js_dict['title'] == 'イギリス':
                return js_dict['text']
    return None


def nlp21(s):
    return '\n'.join([line for line in s.split('\n') if line.find('Category') > -1])


def nlp22(s):
    return '\n'.join([re.match(r'.*Category:([^\|\]]+)', line).group(1) for line in s.split('\n') if
                      re.match(r'.*Category:([^\|\]]+)', line)])


def nlp23(s):
    return {re.match(r'(=+)([^=]+)(=+)', line).group(2): len(re.match(r'(=+)([^=]+)(=+)', line).group(1)) - 1 for
            line in s.split('\n') if re.match(r'(=+)([^=]+)(=+)', line)}


def nlp24(s):
    return '\n'.join([re.match(r'.*(http[^ <\|\n\t]+)', line).group(1) for line in s.split('\n') if
                      re.match(r'.*(http[^ \n\t]+)', line)])



def nlp25(s):
    return {re.match(r'\|([^ ]+) = (.+)', line).group(1): re.match(r'\|([^ ]+) = (.+)', line).group(2) for line in s.split('\n') if
                      re.match(r'\|([^ ]+) = (.+)', line)}


def nlp26(dic):
    return {k: re.sub(r"'+([^']+)'+", r"\1", v) if re.match(r".*'+([^']+)'+", v) else v for k, v in dic.items()}


def remove_link(s):
    while re.match(r".*\[\[([^]]+)\]\]", s):
        s = re.sub(r"\[\[([^\|]+\|)*([^]]+)\]\]", r"\2", s)
    return s


def nlp27(dic):
    return {k: remove_link(v) for k, v in dic.items()}


def remove_markup(s):
    while re.match(r".*(|([]+))([^]]+)[]+", s):
        s = re.sub(r"\[\[([^\|]+\|)*([^]]+)\]\]", r"\2", s)
    return s


def nlp28(dic):
    return {k: remove_link(v) for k, v in dic.items()}


def get_img_url(s):
    url = 'https://commons.wikimedia.org/w/api.php?action=query&titles=File:{}&prop=imageinfo&iiprop=url&format=json'.format(s)
    url = url.replace(' ', '+')
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))
    pages = data["query"]["pages"]
    for k in pages.keys():
        if "imageinfo" in pages[k].keys():
            return pages[k]["imageinfo"][0]["url"]


def nlp29(dic):
    return get_img_url(dic["国旗画像"])






if __name__ == '__main__':
    eng_wiki = nlp20('./jawiki-country.json')
    print(20, eng_wiki)
    print(21, nlp21(eng_wiki))
    print(22, nlp22(eng_wiki))
    print(23, nlp23(eng_wiki))
    print(24, nlp24(eng_wiki))
    template_dic = nlp25(eng_wiki)
    print(25, template_dic)
    template_dic2 = nlp26(template_dic)
    print(26, template_dic2)
    template_dic3 = nlp27(template_dic2)
    print(27, template_dic3)
    template_dic4 = nlp28(template_dic3)
    print(28, template_dic4)
    template_dic5 = nlp29(template_dic)
    print(29, template_dic5)