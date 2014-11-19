# -*- coding: utf-8 -*-
import csv
import bisect

def load_data(path):
    """
    Funkcja która ładuje dane z pliku zawierającego ngramy. Plik ten jest
    plikiem csv zawierającym n-gramy.

    Tak w ogóle tutaj możecie "zaszaleć" i np. nie zwracać list a jakieś
    generatory żeby mniej pamięci zużywać.

    Do testów tej funkcji i tam wynik tej funkcji zostanie potraktowany tak:

    >>> data = load_data('foo')
    >>> data = [list(data[0]), list(data[1])]

    :param str path: Ścieżka
    :return: Lista dwuelementowych krotek, pierwszym elementem jest ngram, drugim
    ilość wystąpień ngramu
    """
    file=open(path,"r",encoding='utf-8')
    r=csv.reader(file,dialect=csv.unix_dialect)
    ngram=[]
    cz=[]
    for line in r:
        ngram.append(line[0])
        cz.append(int(line[1]))
    return (ngram,cz)
        
def binary_search(seq, t):
    min = 0
    max = len(seq) - 1
    while True:
        if max < min:
            return -1
        m = (min + max) // 2
        if seq[m] < t:
            min = m + 1
        elif seq[m] > t:
            max = m - 1
        else:
            return m


def suggester(input, data):
    """
    Funkcja która sugeruje następną literę ciągu ``input`` na podstawie n-gramów
    zawartych w ``data``.

    :param str input: Ciąg znaków o długości 6 znaków lub mniejszej
    :param list data: Data jest krotką zawierającą dwie listy, w pierwszej liście
                      zawarte są n-gramy w drugiej ich częstotliwości.
                      Częstotliwość n-gramu data[0][0] jest zawarta w data[0][1]

    :return: Listę która zawiera krotki. Pierwszym elementem krotki jest litera,
             drugim prawdopodobieństwo jej wystąpienia. Lista jest posortowana
             względem prawdopodobieństwa tak że pierwszym elementem listy
             jest krotka z najbardziej prawdopodobną literą.

    Przykład implementacji
    ----------------------

    By wygenerować częstotliwości należy:

    Dla ustalenia uwagi zakładamy ze input zawiera ciąg znaków `foo`

    1. Odnaleźć pierwsze wystąpienie ngramu rozpoczynającego się od wartości
       ``foo``. Tutaj polecam algorytm przeszukiwania binarnego i moduł
       ``bisect``.
    2. Znaleźć ostatnie wystąpienie ngramu. Tutaj można albo ponownie przeszukać 
       binarnie, albo założyć po prostu przeszukać kolejene elementy listy.

       .. note::

            Kroki 1 i 2 można zastąpić mało wydajnym przeszukiwaniem naiwnym,
            tj. przeiterować się po liście i jeśli ciąg znakóœ rozpoczyna się od
            'foo' (patrz: https://docs.python.org/3.4/library/stdtypes.html#str.startswith)
            zapamiętujemy go

    3. Stworzyć słownik który odwzorowuje następną literę (tą po `foo`) na
       ilość wystąpień. Pamiętaj że w data może mieć taką zawartość 
       ``[['fooabcd', 300], ['fooa    ', 300]]`` --- co w takim wypadku w słowniku tym
       powinno być {'a': 600}.

    4. Z tego słownika wyznaczyć prawdopodobieństwo wystąpienia kolejnej litery.

    Przykład zastosowania:

    >>> data = load_data("path")
    >>> suggester('ąęćś', data)
    []
    >>> suggester('pytho', data)
    [('n', 1.0)]
    >>> suggester('pyth', data)
    [('o', 0.7794117647058824),
     ('a', 0.1323529411764706),
     ('e', 0.07352941176470588),
     ('i', 0.014705882352941176)]
    """
    start=bisect.bisect_left(data[0],input)
    #stop=bisect.bisect_right(data[0],input)
    flag=True
    n=start
    stop=n
    l=len(input)
    while flag:
        stop=n
        n+=1
        if data[0][n][0:l]!=input:
            flag=False
    w={}
    suma=0
    if(start==stop): return []
    for i in range(start,stop+1):
        if data[0][i][l] in w.keys():
            w[data[0][i][l]]+=data[1][i]
        else:
            w[data[0][i][l]]=data[1][i]
        suma+=data[1][i]
        
    for key in w.keys():
        #print(w[key])
        #print()
        #print(suma)
        w[key]=w[key]/suma

    sorted_list=sorted(w.items(),key=lambda x:x[1], reverse=True)
    return sorted_list
        
#path="enwiki-20140903-pages-articles_part_3.xml.csv"
#wynik=load_data(path)
#w=suggester("ąęćś", wynik)
#print(w)
    
    
