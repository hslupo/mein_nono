"""
    Lösung von Nono-Rätseln
    von hslupo Stand 10.10.

"""
from bit import NonogramSolver as NS
import pygame as pg
# from pygame.locals import *  # für handisch änderbares Fenster
import tkinter as tk
from tkinter.filedialog import askopenfilename as aof
from time import perf_counter as pfc


def lese(datei):
    with open(datei, encoding="utf-8") as f:
        s, z = [x for x in f.read().split('\n')]
        rs = [[int(z) for z in x.split()] for x in s.split(',')]
        rz = [[int(z) for z in x.split()] for x in z.split(',')]
        return rs, rz

def calc_xy(sp, ze, dx = 0, dy = 0):
    x = spiel.raster
    return (sp * x + dx + spiel.raster//2, ze * x + dy + spiel.raster//2, x, x)

def zeichne_text(text, pos, farbe):
    x, y, b, h = pos
    font_size = int(b // 1.6)
    mitte = x + b // 2, y + h // 2
    t = pg.font.SysFont('Arial', font_size).render(str(text), False, farbe)
    t_rect = t.get_rect(center=mitte)
    screen.blit(t, t_rect)


def zeichne_spiel():
    def matrix(kopf, x, y):
        for zi, ze in enumerate(kopf):
            for si, sp in enumerate(ze):
                pos = calc_xy(zi, si, x, y)
                pg.draw.rect(screen, 'lightgray', pos)
                pg.draw.rect(screen, 'black', pos, 1)
                if sp:
                    zeichne_text(sp, pos, 'black')

    matrix(spiel.spalten_kopf_matrix, spiel.spaltenX, 0)
    matrix(spiel.zeilen_kopf_matrix, 0, spiel.zeilenY)


    farben = "white gray black".split()
    for zi, ze in enumerate(spiel.board):
        for si, sp in enumerate(ze):
            pos = calc_xy(si, zi, spiel.spaltenX, spiel.zeilenY)
            farbe = farben[sp + 1]
            # print(si, zi, pos, f'*** {sp} ***')
            # pg.draw.rect(screen,'lightgray',pos)
            pg.draw.rect(screen, farbe, pos)
            pg.draw.rect(screen, 'black', pos, 1)
            # zeichne_text(sp, pos, 'black')



def animiere():
    if pause:
        return
    if spiel.animation_counter < len(spiel.animation) :
        ri, ci, val = spiel.animation[spiel.animation_counter]
        spiel.board[ri][ci] = val
        # print( timer_time, spiel.animation_counter, ' -> ',spiel.animation[spiel.animation_counter])
    elif spiel.animation_counter < len(spiel.animation) + 3:
        pass
    else:
        spiel.board_neu()
        spiel.animation_counter = - 1  # damit es wieder bei 0 losgeht

    spiel.animation_counter += 1

def hole_dateiname():
    tk.Tk().withdraw()  # part of the import if you are not using other tkinter functions
    return aof(filetypes=[("Nonorätsel", ".bsp")])


fn = hole_dateiname()
while fn:    # Schleife, solange ein Nono-Beispiel gewählt wird
    spalten, zeilen = lese(fn)
    # print(f'{spalten}\n{zeilen}')

    if sum(map(sum, spalten)) != sum(map(sum, zeilen)):
        print(f'{fn} ist ein ungültiges Rätsel!')
        continue
    else:
        print(f'{fn} mit eine Dimension von {len(spalten)} x {len(zeilen)} Spalten/Zeilen')

    spiel = NS(spalten, zeilen, 30, '')
    # Klasse de Nonogram-Solvers


    pg.init()
    screen = pg.display.set_mode(spiel.screen_size)  # +, RESIZABLE)
    pg.display.set_caption(f"Nanorätsel ({fn})")

    # für die Automatik Lösung wird z.Z. nicht unterstützt
    weitermachen = True
    automatik = False

    # für die Animation des Ergebnisses
    Animation = pg.USEREVENT + 1
    timer_time = 100
    pause = False

    clock = pg.time.Clock()

    while weitermachen:
        clock.tick(40)
        if automatik:  # wird zur Zeit nicht aktiviert

            if spiel.anzahl_möglichkeiten:
                spiel.nächste_spalte_zeile()
            else:
                automatik = False

        for ereignis in pg.event.get():
            if ereignis.type == pg.QUIT:
                weitermachen = False
            elif ereignis.type == Animation:
                animiere()
            elif ereignis.type == pg.KEYDOWN:  # and ereignis.key in richtungen:
                if ereignis.key == pg.K_a:
                    if spiel.animation:   # ist das Rätsel schon gelöst
                        spiel.board_neu() # Anzeige löschen
                        pause = False
                        spiel.animation_counter = 0
                        pg.time.set_timer(Animation, timer_time)
                elif ereignis.key == pg.K_KP_PLUS:
                    spiel.raster_delta(+5)
                    screen = pg.display.set_mode(spiel.screen_size)  # , RESIZABLE)
                elif ereignis.key == pg.K_KP_MINUS:
                    spiel.raster_delta(-5)
                    screen = pg.display.set_mode(spiel.screen_size)  # , RESIZABLE)
                elif ereignis.key == pg.K_SPACE:
                    pause = not pause
                elif ereignis.key == pg.K_UP:  # schnellere Animation
                    if timer_time > 1:
                        timer_time //= 2
                        pg.time.set_timer(Animation, timer_time)
                elif ereignis.key == pg.K_DOWN:  # langsamere Animation
                    if timer_time > 1:
                        timer_time *= 2
                        pg.time.set_timer(Animation, timer_time)


        hg = (20, 20,220) if spiel.solved else (220, 20, 20)
        screen.fill(hg)
        zeichne_spiel()

        pg.display.flip()
    pg.time.set_timer(Animation, 0)
    fn = hole_dateiname()

pg.quit()
