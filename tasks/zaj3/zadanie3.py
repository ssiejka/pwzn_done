# -*- coding: utf-8 -*-


################################################################################
### Kod pomocniczy od prowadzącego
################################################################################

import io
import bz2
import re
import csv
from xml.dom.pulldom import parse, START_ELEMENT
from collections import OrderedDict

link_re = re.compile("\[\[([^\[\]\|]+)(?:\|[^\]]+)?\]\]")


def text_from_node(node):
    """
    Przyjmuje węzeł XML i zwraca kawałki zawartego w nim tekstu
    """
    for ch in node.childNodes:
        if ch.nodeType == node.TEXT_NODE:
            yield ch.data


def clean_page(page_contents):
    """
    Pobiera iterator tekstu i w (z dużymi błędami) usuwa z niego markup Wikipedii
    oraz normalizuje go.

    .. warning::

        Ten lgorytm czyszczenia markupu Wikipedii ma więcej wad niz zalet.
        W zasadzie zaletę ma jedną: nie wymaga instalacji parsera Wikipedii,
        i będzie tak samo działać na Windowsie co na Linuksie.

        Ogólnie jest tu duze pole do poprawy.
    """
    page = io.StringIO()
    for c in page_contents:
        page.write(c)

    page = page.getvalue()

    page = re.sub(r"[^a-zA-Z0-9\.\,\;\s]", " ", page, flags=re.UNICODE)
    page = re.sub("\s+", " ", page, flags=re.UNICODE | re.MULTILINE)

    return page


def iter_over_contents(IN):
    """
    Pobiera nazwę pliku i zwraca iterator który zwraca krotki
    (tytuł strony, wyczyszczona zawartość).

    Działa to na tyle sprytnie że nie ładuje całego XML do pamięci!
    :param IN:
    :return:
    """
    open_func = open
    if IN.endswith("bz2"):
        open_func = bz2.open
    with open_func(IN) as f:
        doc = parse(f)
        for event, node in doc:
            if event == START_ELEMENT and node.tagName == 'page':
                doc.expandNode(node)
                text = node.getElementsByTagName('text')[0]
                title = node.getElementsByTagName('title')[0]
                title = "".join(text_from_node(title))
                yield title, clean_page(text_from_node(text))

################################################################################
### Kod pomocniczy od prowadzącego === END
################################################################################


def generate_ngrams(contents, ngram_len=7):
    """
    Funkcja wylicza częstotliwość n-gramów w części wikipedii.
    N-gramy są posortowane względem zawartości n-grama.

    Testiowanie tej funkcji na pełnych danych może być uciążliwe, możecie
    np. po 1000 stron kończyć tą funkcję.

    :param generator contents: Wynik wywołania funkcji: ``iter_over_contents``,
        czyli generator który zwraca krotki: (tytuł, zawartość artykułu).
    :param int ngram_len: Długość generowanych n-gramów. Jeśli parametr ten
        przyjmie wartość 1 to wyznaczacie Państwo rozkład częstotliwości
        pojawiania się poszczególnyh liter w wikipedii

    :return: Funkcja zwraca słownik n-gram -> ilość wystąpień
    """
    result={}
    flag=0
    for tekst in contents.__next__():
        flag+=1
        if(flag%2==0):
            N=len(tekst)
            for i in range(N-ngram_len):
##                print(tekst[i:i+ngram_len])
                if(result.keys() is not tekst[i:i+ngram_len]):
                    result[tekst[i:i+ngram_len]]=1
                else:
                    result[tekst[i:i+ngram_len]]+=1
    return result


def save_ngrams(out_file, contents):
    """
    Funkcja działa tak jak `generate_ngrams` ale zapisuje wyniki do pliku
    out_file. Może wykorzystywać generate_ngrams!

    Plik ma format csv w dialekcie ``csv.unix_dialect`` i jest posortowany
    względem zawartości n-grama.

    :param dict ngram_dict: Słownik z n-gramami
    :param str out_file: Plik do którego n-gramy zostaną zapisane
    """
    wynik=generate_ngrams(contents)
    out=open(out_file,'w',encoding='utf-8')
    w=csv.writer(out,dialect=csv.unix_dialect)
    sorted_dict=OrderedDict(sorted(wynik.items()))
    for key in sorted_dict.keys():
        w.writerow([key,sorted_dict[key]])
    out.close()
    
    
    


#w=iter_over_contents("/home/angelika/Dokumenty/Python/tasks/zaj3/enwiki-20140903-pages-articles_part_0.xml.bz2")
#print(generate_ngrams(w,5))
#save_ngrams("/home/angelika/Dokumenty/Python/tasks/zaj3/wynik.csv",w)
