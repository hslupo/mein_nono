


spako = [[3], [5], [3, 2, 1], [5, 1, 1], [12], [3, 7], [4, 1, 1, 1], [3, 1, 1], [4], [2]]
zeiko = [[2], [4], [6], [4, 3], [5, 4], [2, 3, 2], [3, 5], [5], [3], [2], [2], [6]]

spaza = len(spako)
zeiza = len(zeiko)

def kopf(ko):
    ret = []
    koza = max([len(x) for x in ko])
    for k in  ko:
        ret.append([0 for _ in range(koza - len(k))] + k)
    return koza, ret



spakozei, spako1 = kopf(spako)
zeikospa, zeiko1 = kopf(zeiko)
zeiko1 = [[row[i] for row in zeiko1] for i in range(len(zeiko1[0]))]   # transponieren
# [[row[i] for row in l1] for i in range(len(l1[0]))]
# list(map(list, zip(*zeiko1)))
print(spakozei, zeikospa)
