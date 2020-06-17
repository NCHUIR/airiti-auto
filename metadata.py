import re

from risReader import RisReader


def get_metadata(ris: RisReader):
    return {
        "dc.contributor.author[zh_TW]": get_author(ris, parse_zht_name),
        "dc.contributor.author[en_US]": get_author(ris, parse_eng_name),
        "dc.title[zh_TW]": ris.get_ris_value_first("T1"),
        "dc.title[en_US]": ris.get_ris_value_first("TT"),
        "dc.date[zh_TW]": "",
        "contents": "",
        "dc.description.abstract[zh_TW]": get_abstract(ris, 0),
        "dc.description.abstract[en_US]": get_abstract(ris, 1),
        "dc.relation[zh_TW]": get_relation(ris),
        "dc.subject[zh_TW]": get_keywords(ris, 'zh_TW'),
        "dc.subject[en_US]": get_keywords(ris, 'en_US'),
        "dc.type[zh_TW]": "Journal Article",
    }


def get_abstract(ris: RisReader, index):
    abs = ris.get_ris_value('AB')
    if abs is None:
        return ''
    return abs[index]


def get_author(ris: RisReader, parse_func):
    authors = ris.get_ris_value('AU')
    ret = ''
    if authors is None:
        return ''
    for author in authors:
        name = parse_func(author)
        if name != '':
            ret += "||" + name
    if ret[0:2] == '||':
        ret = ret[2:]
    return ret


def parse_eng_name(name: str):
    s = re.search(r'\((.*?)\)', name).group()
    if s is not None:
        s = s.replace("(", "").replace(")", "")
        return s

    s = re.search(r'/[a-zA-Z]/', name).group()
    if s is None:
        return ''
    else:
        return name


def parse_zht_name(name: str):
    s = name.find('(')
    if s == -1:
        s = re.search(r'/[a-zA-Z]/', name).group()
        if s is None:
            return name
        else:
            return ''
    else:
        return name[0:s]


def get_relation(ris: RisReader):
    ret = ''
    if ris.v('JO') != '':
        ret += ris.v('JO')
    if ris.v('VL') != '':
        ret += ', Volume ' + ris.v('VL')
    if ris.v('IS') != '':
        ret += ', Issue ' + ris.v('IS')
    if ris.v('SP') != '' and ris.v('EP') != '':
        ret += ', Page(s) ' + ris.v('SP') + '-' + ris.v('EP')

    return ret


def get_keywords(ris: RisReader, lang):
    """ lang='zh_TW' or 'en_US' """
    kws = ris.get_ris_value('KW')
    ret = ''
    for kw in kws:
        has_chinese = len(re.findall(r'[\u4e00-\u9fff]+', kw)) > 0
        if lang == 'zh_TW' and has_chinese:
            ret += '||' + kw
        elif lang == 'en_US' and not has_chinese:
            ret += '||' + kw
        else:
            pass
    if ret[0:2] == '||':
        ret = ret[2:]
    return ret
