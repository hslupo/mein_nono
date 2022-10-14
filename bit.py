from itertools import combinations
import numpy as np



class NonogramSolver:
    def __init__(self, spalten_kopf=[[3], [5], [3, 2, 1], [5, 1, 1], [12], [3, 7], [4, 1, 1, 1], [3, 1, 1], [4], [2]],
                 zeilen_kopf=[[2], [4], [6], [4, 3], [5, 4], [2, 3, 2], [3, 5], [5], [3], [2], [2], [6]],
                 raster=50, savepath = ''):
        self.board = []
        self.animation = []
        self.animation_counter = 0

        self.zeilen_kopf = zeilen_kopf
        self.zeilen_zahl = len(zeilen_kopf)
        self.rows_changed = [0] * self.zeilen_zahl
        self.rows_done = [0] * self.zeilen_zahl

        self.spalten_kopf = spalten_kopf
        self.spalten_zahl = len(spalten_kopf)
        self.cols_changed = [0] * self.spalten_zahl
        self.cols_done = [0] * self.spalten_zahl

        self.solved = False
        self.shape = (self.zeilen_zahl, self.spalten_zahl)
        # self.board = [[0 for c in range(self.spalten_zahl)] for r in range(self.zeilen_zahl)]
        self.board_neu()
        self.savepath = savepath
        if self.savepath != '': self.n = 0
        self.raster = raster

        self.rows_possibilities = self.create_possibilities(zeilen_kopf, self.spalten_zahl)
        self.cols_possibilities = self.create_possibilities(spalten_kopf, self.zeilen_zahl)

        self.spaltenkopf_max_anzahl, self.spalten_kopf_matrix = self.kopfmatrix(self.spalten_kopf)
        self.zeilenkopf_max_anzahl, self.zeilen_kopf_matrix = self.kopfmatrix(self.zeilen_kopf, True)

        self.spaltenX = self.zeilenkopf_max_anzahl * self.raster
        self.zeilenY = self.spaltenkopf_max_anzahl * self.raster
        self.screen_size = ((self.zeilenkopf_max_anzahl + self.spalten_zahl + 1) * self.raster,
                            (self.spaltenkopf_max_anzahl + self.zeilen_zahl + 1) * self.raster)

        print(f'Eingelesenes Rätsel: {self.spalten_zahl}x{self.zeilen_zahl} (Spalten x Zeilen)')
        print(f'Spaltenkopfmatrix: {len(self.spalten_kopf_matrix)}x{len(self.spalten_kopf_matrix[0])}')
        print(f'Zeilenkopfmatrix: {len(self.zeilen_kopf_matrix)}x{len(self.zeilen_kopf_matrix[0])}')

        self.ab_hier_lösen()  # direkt lösen

    def board_neu(self):
        self.board = [[0 for c in range(self.spalten_zahl)] for r in range(self.zeilen_zahl)]
        return self.board


    def raster_delta(self, delta):
        self.raster += delta if self.raster + delta > 0 else 5
        self.spaltenX = self.zeilenkopf_max_anzahl * self.raster  # + self.raster//2
        self.zeilenY = self.spaltenkopf_max_anzahl * self.raster  # + self.raster//2
        self.screen_size = ((self.zeilenkopf_max_anzahl + self.spalten_zahl + 1) * self.raster,
                            (self.spaltenkopf_max_anzahl + self.zeilen_zahl + 1) * self.raster)


    def kopfmatrix(self, ko, trans = False):
        ret = []
        koza = max([len(x) for x in ko])
        for k in ko:
            ret.append([0 for _ in range(koza - len(k))] + k)
        if trans:  # transponieren für Spalten/Zeilen Ausrichtung des Zeilenkopfs
            ret = [[row[i] for row in ret] for i in range(len(ret[0]))]
        return koza, ret


    def ab_hier_lösen(self):
        while not self.solved:
            # step 2: Order indici by lowest
            self.lowest_rows = self.select_index_not_done(self.rows_possibilities, 1)
            self.lowest_cols = self.select_index_not_done(self.cols_possibilities, 0)
            self.lowest = sorted(self.lowest_rows + self.lowest_cols, key=lambda element: element[1])
            unverändert = True
            # print(f'In Lösung NOT SOLVED')

            # Schritt 3: Nur Nullen oder nur Einsen der niedrigsten Möglichkeit erhalten
            for ind1, _, row_ind in self.lowest:
                if not self.check_done(row_ind, ind1):
                    if row_ind:
                        values = self.rows_possibilities[ind1]
                    else:
                        values = self.cols_possibilities[ind1]
                    same_ind = self.get_only_one_option(values)
                    for ind2, val in same_ind:
                        if row_ind:
                            ri, ci = ind1, ind2
                        else:
                            ri, ci = ind2, ind1
                        if self.board[ri][ci] == 0:
                            self.board[ri][ci] = val
                            unverändert = False
                            self.animation.append((ri, ci, val))
                            if row_ind:
                                self.cols_possibilities[ci] = self.remove_possibilities(self.cols_possibilities[ci], ri, val)
                                # print(f'Spalte {ci}: {self.cols_possibilities[ci]}')
                            else:
                                # print(f'vorher Zeile {ri}: {self.rows_possibilities[ri]}')
                                self.rows_possibilities[ri] = self.remove_possibilities(self.rows_possibilities[ri], ci, val)
                                # print(f'danach Zeile {ri}: {self.rows_possibilities[ri]}')

                    self.update_done(row_ind, ind1)
                #if self.savepath != '':
                    # self.save_board()
                    # self.n += 1
            self.check_solved()
            print(self.  solved, unverändert)
            if unverändert:   # nicht eindeutig lösbar
                return

    def create_possibilities(self, values, no_of_other):
        possibilities = []
        # print(f'Reihen: {values} no_of_others: {no_of_other}')
        # maxi = 0
        for v in values:
            # print(f'Für den Kopf: {v} no_of_others: {no_of_other}')
            groups = len(v)
            no_empty = no_of_other - sum(v) - groups + 1
            ones = [[1] * x for x in v]
            res = self._create_possibilities(no_empty, groups, ones)
            # print(f'\tv: {v} - no_empty: {no_empty} - groups: {groups} - ones: {ones}\n\tres: {res}\n')
            # maxi = max(maxi, len(v))
            possibilities.append(res)

        return possibilities  #, maxi

    def _create_possibilities(self, n_empty, groups, ones):
        res_opts = []
        # print(f'\tKombinationen:(range({groups + n_empty}), {groups}) -> ',
        #       *combinations(range(groups + n_empty), groups),
        #       '\n\tVariable: ', n_empty, groups, ones)
        for p in combinations(range(groups + n_empty), groups):
            selected = [-1] * (groups + n_empty)
            ones_idx = 0
            for val in p:
                # print(f'\t\t\tval: {val} - selected: {selected} - ones_idx: {ones_idx}')
                selected[val] = ones_idx
                ones_idx += 1
                # print(f'\t\t\tval: {val} - selected: {selected} - ones_idx: {ones_idx}')
            res_opta = [ones[val] + [-1] if val > -1 else [-1] for val in selected]
            res_opt = [item for sublist in res_opta for item in sublist][:-1]
            # print(f'\t\tp: {p} - res_opta: {res_opta} - res_opt: {res_opt}')
            res_opts.append(res_opt)
        return res_opts

    def select_index_not_done(self, possibilities, row_ind):
        s = [len(i) for i in possibilities]
        if row_ind:
            return [(i, n, row_ind) for i, n in enumerate(s) if self.rows_done[i] == 0]
        else:
            return [(i, n, row_ind) for i, n in enumerate(s) if self.cols_done[i] == 0]

    def get_only_one_option(self, values):
        return [(n, np.unique(i)[0]) for n, i in enumerate(np.array(values).T) if len(np.unique(i)) == 1]

    def remove_possibilities(self, possibilities, i, val):
        return [p for p in possibilities if p[i] == val]

    def update_done(self, row_ind, idx):
        if row_ind:
            vals = self.board[idx]
        else:
            vals = [row[idx] for row in self.board]
        if 0 not in vals:
            if row_ind:
                self.rows_done[idx] = 1
            else:
                self.cols_done[idx] = 1

    def check_done(self, row_ind, idx):
        if row_ind:
            return self.rows_done[idx]
        else:
            return self.cols_done[idx]

    def check_solved(self):
        if 0 not in self.rows_done and 0 not in self.cols_done:
            self.solved = True


if __name__ == '__main__':

    a = [[4], [2, 1], [1, 1], [2], [2]]
    b = [[4], [2, 2], [1], [1], [3]]

    spiel = NonogramSolver()
