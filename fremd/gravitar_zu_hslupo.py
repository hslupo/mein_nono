"""
Gravitar Text Zeilen/Spalten mehrere in einer Datei
AA C E E AA AA BB CA E
B D H DC BB A C C


Übergabeformat Spalten/Zeilen
[[2], [4], [8], [4, 3], [2, 2], [1], [3], [3]]
[[1, 1], [3], [5], [5], [1, 1], [1, 1], [2, 2], [3, 1], [5]]

hslupo: Dateiformat *.bsp Spalten/Zeilen
2,4,8,4 3,2 2,1,3,3
1 1,3,5,5,1 1,1 1,2 2,3 1,5

"""

def datei_einlesen(datei):
  with open(datei) as f:
    return [[[[ord(buchst)-64 for buchst in zf]
               for zf in zeile.split()]
               for zeile in nonogramm.split('\n')]
               for nonogramm in f.read().split('\n\n')]

nonogramme = datei_einlesen('gravitar.txt')
ZEILEN, SPALTEN = 0, 1

for i, nogra in enumerate(nonogramme):
    print(i, '\n\t',nogra[SPALTEN], '\n\t',nogra[ZEILEN])
    # Annäherung
    # sp = ','.join(str(' '.join(str(y) for y in x)) for x in nogra[SPALTEN])
    # ze = ','.join(str(' '.join(str(y) for y in x)) for x in nogra[ZEILEN])
    # print(sp, '\n', ze)
    ziel = f'gravitar{i}-({len(nogra[SPALTEN])}x{len(nogra[ZEILEN])}).bsp'
    spze = '\n'.join(str(','.join(str(' '.join(str(y) for y in x)) for x in sz)) for sz in nogra[::-1])
    print(f'{ziel}\n{spze}')
    with open(ziel,'w') as f:
        f.write(spze)