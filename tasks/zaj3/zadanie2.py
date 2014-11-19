# -*- coding: utf-8 -*-
import csv

def merge(path1, path2, out_file):
    """
    Funkcja pobiera nazwy dwóch plików z n-gramami (takie jak w poprzedmim
    zadaniu) i łączy zawartość tych plików i zapisuje do pliku w ścieżce ``out``.

    Pliki z n-gramami są posortowane względem zawartości n-grama.

    :param str path1: Ścieżka do pierwszego pliku
    :param str path2: Ścieżka do drugiego pliku
    :param str out_file:  Ścieżka wynikowa

    Testowanie tej funkcji na pełnych danych może być mało wygodne, możecie
    stworzyć inną funkcję która działa na dwóch listach/generatorach i testować
    ją.

    Naiwna implementacja polegałaby na stworzeniu dwóch słowników które
    zawierają mapowanie ngram -> ilość wystąpień i połączeniu ich.

    Lepsza implementacja ładuje jeden z plików do pamięci RAM (jako słownik
    bądź listę) a po drugim iteruje.

    Najlepsza implementacja nie wymaga ma złożoność pamięciową ``O(1)``.
    Podpowiedź: merge sort. Nie jest to trywialne zadanie, ale jest do zrobienia.
    """
    file1=open(path1,"r",encoding='utf-8')
    r=csv.reader(file1,dialect=csv.unix_dialect)
    dane1={}
    for line in r:
        dane1[line[0]]=int(line[1])
    file1.close()
    
    file2=open(path2,"r",encoding='utf-8')
    r2=csv.reader(file2,dialect=csv.unix_dialect)
    flag=False
    for line in r2:
        for key in dane1.keys():
            if(line[0]==key):
                dane1[key]+=int(line[1])
            else:
                flag=True
        if(flag):
            dane1[line[0]]=int(line[1])
            flag=False
    out=open(out_file,'w',encoding='utf-8')
    w=csv.writer(out,dialect=csv.unix_dialect)
    sorted_dict=OrderedDict(sorted(dane1.items(),key=lambda x:x[0]))
    for key in sorted_dict.keys():
        w.writerow([key,sorted_dict[key]])
    out.close()
    file2.close()
    

if __name__ == '__main__':

    merge(
        '/home/angelika/Dokumenty/Python/tasks/zaj3/enwiki-20140903-pages-articles_part_0.xmlascii.csv',
        '/home/angelika/Dokumenty/Python/tasks/zaj3/enwiki-20140903-pages-articles_part_1.xmlascii.csv',
        '/home/angelika/Dokumenty/Python/tasks/zaj3/mergeout.csv')
