import time
import copy
import pygame, sys
import statistics

ADANCIME_MAX = 0
TIMP_JOC = 0
TIMP_START = 0


def elem_identice(lista):
    if len(set(lista)) == 1:  # face o multime (fara dubluri); daca e de lungime 1, inseamna ca e o diagonala completata
        # cu 0/x, deci jucatorul respectiv primeste un punct
        jucator = lista[0]
        if jucator != Joc.GOL:
            return jucator
    return False


def verificare_vecini1(tabla_curenta, l1, l2, c):
    '''Functie care verifica daca o mutare de tip 1(pe verticala) este valida, adica daca printre cei 10 vecini
    se gasesc cate un x si 0
    '''
    x = False
    o = False
    if l1 > l2:
        l1, l2 = l2, l1  # l1 va fi linia de sus, l2 cea de jos
    if l1 == 0 and c == 0:  # colt stanga sus
        if ('x' in tabla_curenta.matr[(l2 + 1) * Joc.NR_COLOANE: (l2 + 1) * Joc.NR_COLOANE + 2]) or \
                ('x' in tabla_curenta.matr[1: l2 * Joc.NR_COLOANE + 2:Joc.NR_COLOANE]):
            x = True
        if ('0' in tabla_curenta.matr[(l2 + 1) * Joc.NR_COLOANE: (l2 + 1) * Joc.NR_COLOANE + 2]) or \
                ('0' in tabla_curenta.matr[1: l2 * Joc.NR_COLOANE + 2:Joc.NR_COLOANE]):
            o = True
        if x and o:
            return True
        return False
    if l1 == 0 and c == 9:  # colt dreapta sus
        if ('x' in tabla_curenta.matr[(l2 + 1) * Joc.NR_COLOANE + 8: (l2 + 1) * Joc.NR_COLOANE + 10]) or \
                ('x' in tabla_curenta.matr[8: l2 * Joc.NR_COLOANE + 9:Joc.NR_COLOANE]):
            x = True
        if ('0' in tabla_curenta.matr[(l2 + 1) * Joc.NR_COLOANE + 8: (l2 + 1) * Joc.NR_COLOANE + 10]) or \
                ('0' in tabla_curenta.matr[8: l2 * Joc.NR_COLOANE + 9:Joc.NR_COLOANE]):
            o = True
        if x and o:
            return True
        return False
    if l2 == 9 and c == 0:  # colt stanga jos
        if ('x' in tabla_curenta.matr[(l1 - 1) * Joc.NR_COLOANE: (l1 - 1) * Joc.NR_COLOANE + 2]) or \
                ('x' in tabla_curenta.matr[l1 * Joc.NR_COLOANE + 1: l2 * Joc.NR_COLOANE + 2:Joc.NR_COLOANE]):
            x = True
        if ('0' in tabla_curenta.matr[(l1 - 1) * Joc.NR_COLOANE: (l1 - 1) * Joc.NR_COLOANE + 2]) or \
                ('0' in tabla_curenta.matr[
                        l1 * Joc.NR_COLOANE + 1: l2 * Joc.NR_COLOANE + 2:Joc.NR_COLOANE]):
            o = True
        if x and o:
            return True
        return False
    if l2 == 9 and c == 9:  # colt dreapta jos
        if ('x' in tabla_curenta.matr[(l1 - 1) * Joc.NR_COLOANE + 8: (l1 - 1) * Joc.NR_COLOANE + 10]) or \
                ('x' in tabla_curenta.matr[l1 * Joc.NR_COLOANE + 8: l2 * Joc.NR_COLOANE + 9:Joc.NR_COLOANE]):
            x = True
        if ('0' in tabla_curenta.matr[(l1 - 1) * Joc.NR_COLOANE + 8: (l1 - 1) * Joc.NR_COLOANE + 10]) or \
                ('0' in tabla_curenta.matr[
                        l1 * Joc.NR_COLOANE + 8: l2 * Joc.NR_COLOANE + 9:Joc.NR_COLOANE]):
            o = True
        if x and o:
            return True
        return False
    if l2 == 9 and c != 0 and c != 9:  # ultima linie
        if ('x' in tabla_curenta.matr[
                   (l1 - 1) * Joc.NR_COLOANE + (c - 1): (l1 - 1) * Joc.NR_COLOANE + (c + 2)]) or \
                ('x' in tabla_curenta.matr[
                        l1 * Joc.NR_COLOANE + (c - 1): l2 * Joc.NR_COLOANE + c:Joc.NR_COLOANE]) or \
                ('x' in tabla_curenta.matr[
                        l1 * Joc.NR_COLOANE + (c + 1): l2 * Joc.NR_COLOANE + (c + 2):Joc.NR_COLOANE]):
            x = True
        if ('0' in tabla_curenta.matr[
                   (l1 - 1) * Joc.NR_COLOANE + (c - 1): (l1 - 1) * Joc.NR_COLOANE + (c + 2)]) or \
                ('0' in tabla_curenta.matr[
                        l1 * Joc.NR_COLOANE + (c - 1): l2 * Joc.NR_COLOANE + c:Joc.NR_COLOANE]) or \
                ('0' in tabla_curenta.matr[
                        l1 * Joc.NR_COLOANE + (c + 1): l2 * Joc.NR_COLOANE + (c + 2):Joc.NR_COLOANE]):
            o = True
        if x and o:
            return True
        return False
    if l1 == 0 and c != 0 and c != 9:  # prima linie
        if ('x' in tabla_curenta.matr[
                   (l2 + 1) * Joc.NR_COLOANE + (c - 1): (l2 + 1) * Joc.NR_COLOANE + (c + 2)]) or \
                ('x' in tabla_curenta.matr[(c - 1): l2 * Joc.NR_COLOANE + c:Joc.NR_COLOANE]) or \
                ('x' in tabla_curenta.matr[(c + 1): l2 * Joc.NR_COLOANE + (c + 2):Joc.NR_COLOANE]):
            x = True
        if ('0' in tabla_curenta.matr[
                   (l2 + 1) * Joc.NR_COLOANE + (c - 1): (l2 + 1) * Joc.NR_COLOANE + (c + 2)]) or \
                ('0' in tabla_curenta.matr[(c - 1): l2 * Joc.NR_COLOANE + c:Joc.NR_COLOANE]) or \
                ('0' in tabla_curenta.matr[(c + 1): l2 * Joc.NR_COLOANE + (c + 2):Joc.NR_COLOANE]):
            o = True
        if x and o:
            return True
        return False
    if c == 0 and l1 != 0 and l2 != 9:  # extrema stanga
        if ('x' in tabla_curenta.matr[(l1 - 1) * Joc.NR_COLOANE: (l1 - 1) * Joc.NR_COLOANE + 2]) or \
                ('x' in tabla_curenta.matr[(l2 + 1) * Joc.NR_COLOANE: (l2 + 1) * Joc.NR_COLOANE + 2]) or \
                ('x' in tabla_curenta.matr[
                        l1 * Joc.NR_COLOANE + 1: l2 * Joc.NR_COLOANE + 2:Joc.NR_COLOANE]):
            x = True
        if ('0' in tabla_curenta.matr[(l1 - 1) * Joc.NR_COLOANE: (l1 - 1) * Joc.NR_COLOANE + 2]) or \
                ('0' in tabla_curenta.matr[(l2 + 1) * Joc.NR_COLOANE: (l2 + 1) * Joc.NR_COLOANE + 2]) or \
                ('0' in tabla_curenta.matr[
                        l1 * Joc.NR_COLOANE + 1: l2 * Joc.NR_COLOANE + 2:Joc.NR_COLOANE]):
            o = True
        if x and o:
            return True
        return False
    if c == 9 and l1 != 0 and l2 != 9:  # extrema dreapta
        if ('x' in tabla_curenta.matr[(l1 - 1) * Joc.NR_COLOANE + 8: (l1 - 1) * Joc.NR_COLOANE + 10]) or \
                ('x' in tabla_curenta.matr[(l2 + 1) * Joc.NR_COLOANE + 8:(l2 + 1) * Joc.NR_COLOANE + 10]) or \
                ('x' in tabla_curenta.matr[
                        l1 * Joc.NR_COLOANE + 8: l2 * Joc.NR_COLOANE + 9:Joc.NR_COLOANE]):
            x = True
        if ('0' in tabla_curenta.matr[(l1 - 1) * Joc.NR_COLOANE + 8: (l1 - 1) * Joc.NR_COLOANE + 10]) or \
                ('0' in tabla_curenta.matr[(l2 + 1) * Joc.NR_COLOANE + 8:(l2 + 1) * Joc.NR_COLOANE + 10]) or \
                ('0' in tabla_curenta.matr[
                        l1 * Joc.NR_COLOANE + 8: l2 * Joc.NR_COLOANE + 9:Joc.NR_COLOANE]):
            o = True
        if x and o:
            return True
        return False
    if l1 != 0 and l2 != 9 and c != 9 and c != 0:  # mutare "neincoltita"
        if ('x' in tabla_curenta.matr[
                   (l1 - 1) * Joc.NR_COLOANE + (c - 1): (l1 - 1) * Joc.NR_COLOANE + (c + 2)]) or \
                ('x' in tabla_curenta.matr[
                        (l2 + 1) * Joc.NR_COLOANE + (c - 1): (l2 + 1) * Joc.NR_COLOANE + (c + 2)]) or \
                ('x' in tabla_curenta.matr[
                        l1 * Joc.NR_COLOANE + (c - 1): l2 * Joc.NR_COLOANE + c:Joc.NR_COLOANE]) or \
                ('x' in tabla_curenta.matr[
                        l1 * Joc.NR_COLOANE + (c + 1): l2 * Joc.NR_COLOANE + (c + 2):Joc.NR_COLOANE]):
            x = True
        if ('0' in tabla_curenta.matr[
                   (l1 - 1) * Joc.NR_COLOANE + (c - 1): (l1 - 1) * Joc.NR_COLOANE + (c + 2)]) or \
                ('0' in tabla_curenta.matr[
                        (l2 + 1) * Joc.NR_COLOANE + (c - 1): (l2 + 1) * Joc.NR_COLOANE + (c + 2)]) or \
                ('0' in tabla_curenta.matr[
                        l1 * Joc.NR_COLOANE + (c - 1): l2 * Joc.NR_COLOANE + c:Joc.NR_COLOANE]) or \
                ('0' in tabla_curenta.matr[
                        l1 * Joc.NR_COLOANE + (c + 1): l2 * Joc.NR_COLOANE + (c + 2):Joc.NR_COLOANE]):
            o = True
        if x and o:
            return True
        return False


def verificare_vecini2(tabla_curenta, l, c1, c2):
    '''Functie care verifica daca o mutare de tip 2(pe orizontala) este valida, adica daca printre cei 10 vecini
    se gasesc cate un x si 0
    '''
    x = False
    o = False
    if c1 > c2:
        c1, c2 = c2, c1  # c1 este coloana din stanga, c2 din dreapta

    if l == 0 and c1 == 0:  # colt stanga sus
        if ('x' in tabla_curenta.matr[Joc.NR_COLOANE: Joc.NR_COLOANE + 3]) or \
                ('x' in tabla_curenta.matr[2]):
            x = True
        if ('0' in tabla_curenta.matr[Joc.NR_COLOANE: Joc.NR_COLOANE + 3]) or \
                ('0' in tabla_curenta.matr[2]):
            o = True
        if x and o:
            return True
        return False
    if l == 0 and c2 == 9:  # colt dreapta sus
        if ('x' in tabla_curenta.matr[Joc.NR_COLOANE + 7: Joc.NR_COLOANE + 10]) or \
                ('x' in tabla_curenta.matr[7]):
            x = True
        if ('0' in tabla_curenta.matr[Joc.NR_COLOANE + 7: Joc.NR_COLOANE + 10]) or \
                ('0' in tabla_curenta.matr[7]):
            o = True
        if x and o:
            return True
        return False
    if l == 9 and c1 == 0:  # colt stanga jos
        if ('x' in tabla_curenta.matr[8 * Joc.NR_COLOANE: 8 * Joc.NR_COLOANE + 3]) or \
                ('x' in tabla_curenta.matr[9 * Joc.NR_COLOANE + 2]):
            x = True
        if ('0' in tabla_curenta.matr[8 * Joc.NR_COLOANE: 8 * Joc.NR_COLOANE + 3]) or \
                ('0' in tabla_curenta.matr[9 * Joc.NR_COLOANE + 2]):
            o = True
        if x and o:
            return True
        return False
    if l == 9 and c2 == 9:  # colt dreapta jos
        if ('x' in tabla_curenta.matr[8 * Joc.NR_COLOANE + 7: 8 * Joc.NR_COLOANE + 10]) or \
                ('x' in tabla_curenta.matr[9 * Joc.NR_COLOANE + 7]):
            x = True
        if ('0' in tabla_curenta.matr[8 * Joc.NR_COLOANE + 7: 8 * Joc.NR_COLOANE + 10]) or \
                ('0' in tabla_curenta.matr[9 * Joc.NR_COLOANE + 7]):
            o = True
        if x and o:
            return True
        return False
    if l == 9 and c1 != 0 and c2 != 9:  # utima linie
        if ('x' in tabla_curenta.matr[8 * Joc.NR_COLOANE + (c1 - 1): 8 * Joc.NR_COLOANE + (c2 + 2)]) or \
                ('x' in tabla_curenta.matr[9 * Joc.NR_COLOANE + (c1 - 1)]) or \
                ('x' in tabla_curenta.matr[9 * Joc.NR_COLOANE + (c2 + 1)]):
            x = True
        if ('0' in tabla_curenta.matr[8 * Joc.NR_COLOANE + (c1 - 1): 8 * Joc.NR_COLOANE + (c2 + 2)]) or \
                ('0' in tabla_curenta.matr[9 * Joc.NR_COLOANE + (c1 - 1)]) or \
                ('0' in tabla_curenta.matr[9 * Joc.NR_COLOANE + (c2 + 1)]):
            o = True
        if x and o:
            return True
        return False
    if l == 0 and c1 != 0 and c2 != 9:  # prima linie
        if ('x' in tabla_curenta.matr[Joc.NR_COLOANE + (c1 - 1): Joc.NR_COLOANE + (c2 + 2)]) or \
                ('x' in tabla_curenta.matr[(c1 - 1)]) or \
                ('x' in tabla_curenta.matr[(c2 + 1)]):
            x = True
        if ('0' in tabla_curenta.matr[Joc.NR_COLOANE + (c1 - 1): Joc.NR_COLOANE + (c2 + 2)]) or \
                ('0' in tabla_curenta.matr[(c1 - 1)]) or \
                ('0' in tabla_curenta.matr[(c2 + 1)]):
            o = True
        if x and o:
            return True
        return False
    if c1 == 0 and l != 0 and l != 9:  # extrema stanga
        if ('x' in tabla_curenta.matr[(l - 1) * Joc.NR_COLOANE: (l - 1) * Joc.NR_COLOANE + (c2 + 2)]) or \
                ('x' in tabla_curenta.matr[(l + 1) * Joc.NR_COLOANE: (l + 1) * Joc.NR_COLOANE + (c2 + 2)]) or \
                ('x' in tabla_curenta.matr[l * Joc.NR_COLOANE + (c2 + 1)]):
            x = True
        if ('0' in tabla_curenta.matr[(l - 1) * Joc.NR_COLOANE: (l - 1) * Joc.NR_COLOANE + (c2 + 2)]) or \
                ('0' in tabla_curenta.matr[(l + 1) * Joc.NR_COLOANE: (l + 1) * Joc.NR_COLOANE + (c2 + 2)]) or \
                ('0' in tabla_curenta.matr[l * Joc.NR_COLOANE + (c2 + 1)]):
            o = True
        if x and o:
            return True
        return False
    if c2 == 9 and l != 0 and l != 9:  # extrema dreapta
        if ('x' in tabla_curenta.matr[(l - 1) * Joc.NR_COLOANE + 7: (l - 1) * Joc.NR_COLOANE + 10]) or \
                ('x' in tabla_curenta.matr[(l + 1) * Joc.NR_COLOANE + 7: (l + 1) * Joc.NR_COLOANE + 10]) or \
                ('x' in tabla_curenta.matr[l * Joc.NR_COLOANE + (c1 - 1)]):
            x = True
        if ('0' in tabla_curenta.matr[(l - 1) * Joc.NR_COLOANE + 7: (l - 1) * Joc.NR_COLOANE + 10]) or \
                ('0' in tabla_curenta.matr[(l + 1) * Joc.NR_COLOANE + 7: (l + 1) * Joc.NR_COLOANE + 10]) or \
                ('0' in tabla_curenta.matr[l * Joc.NR_COLOANE + (c1 - 1)]):
            o = True
        if x and o:
            return True
        return False
    if l != 0 and l != 9 and c1 != 0 and c2 != 9:  # mutare "neincoltita"
        if ('x' in tabla_curenta.matr[(l - 1) * Joc.NR_COLOANE +
                                      (c1 - 1): (l - 1) * Joc.NR_COLOANE + (c2 + 2)]) or \
                ('x' in tabla_curenta.matr[(l + 1) * Joc.NR_COLOANE +
                                           (c1 - 1): (l + 1) * Joc.NR_COLOANE + (c2 + 2)]) or \
                ('x' in tabla_curenta.matr[l * Joc.NR_COLOANE + (c1 - 1)]) or \
                ('x' in tabla_curenta.matr[l * Joc.NR_COLOANE + (c2 + 1)]):
            x = True
        if ('0' in tabla_curenta.matr[(l - 1) * Joc.NR_COLOANE +
                                      (c1 - 1): (l - 1) * Joc.NR_COLOANE + (c2 + 2)]) or \
                ('0' in tabla_curenta.matr[(l + 1) * Joc.NR_COLOANE +
                                           (c1 - 1): (l + 1) * Joc.NR_COLOANE + (c2 + 2)]) or \
                ('0' in tabla_curenta.matr[l * Joc.NR_COLOANE + (c1 - 1)]) or \
                ('0' in tabla_curenta.matr[l * Joc.NR_COLOANE + (c2 + 1)]):
            o = True
        if x and o:
            return True
        return False


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 10
    JMIN = None
    JMAX = None
    GOL = '#'

    def __init__(self, tabla=None):  # Joc()
        if tabla is not None:
            self.matr = tabla
            self.scor = 0
            self.scor_opus = 0
        else:
            self.scor = 0
            self.scor_opus = 0
            self.matr = [Joc.GOL] * self.NR_COLOANE ** 2
            self.matr[4 * self.NR_COLOANE + 4] = 'x'
            self.matr[5 * self.NR_COLOANE + 4] = 'x'
            self.matr[4 * self.NR_COLOANE + 5] = '0'
            self.matr[5 * self.NR_COLOANE + 5] = '0'

    @classmethod
    def jucator_opus(cls, jucator):
        if jucator == cls.JMIN:
            return cls.JMAX
        else:
            return cls.JMIN

    # TO DO 5
    def final(self):
        """
        Functie care verifica daca jocul s-a terminat
        :return: "plin" daca tabla nu are suficiente spatii goale
        :return: False daca mai sunt spatii goale valide pentru o mutare
        :return: True daca mai sunt spatii goale,dar acestea nu sunt valide pt. mutari (sunt departate, etc)
        """
        poz_libere = []
        for i in range(len(self.matr)):
            if self.matr[i] == '#':
                poz_libere.append(i)
        if len(poz_libere) == 0 or len(poz_libere) == 1:
            return "plin"  # tabla nu mai are spatii goale suficiente
        else:
            for i in range(0, len(poz_libere) - 1):
                if poz_libere[i] + 1 == poz_libere[i + 1]:  # spatiile goale sunt consectv pt. mutare de tip 2/oriz
                    if i > 10:
                        l = int(i / 10)
                        c1 = i % 10
                        c2 = c1 + 1
                    else:
                        l = 0  # i < 10 => se afla pe prima linie
                        c1 = i
                        c2 = c1 + 1
                    if verificare_vecini2(self, l, c1, c2):
                        return False  # jocul nu e terminat, mai sunt locuri posibile pt mutari, cel putin 1 orizontal
            for i in range(0, len(poz_libere)):
                for j in range(i, len(poz_libere)):
                    if poz_libere[i] + 10 == poz_libere[j]:  # spatiile goale sunt una sub alta(distanta de 10= o linie)
                        if poz_libere[i] > 10:
                            l1 = int(poz_libere[i] / 10)
                            l2 = int(poz_libere[j] / 10)
                            c = poz_libere[i] % 10
                        else:
                            l1 = 0  # i < 10 => se afla pe prima si a doua linie (indicii 0 si 1)
                            l2 = 1
                            c = poz_libere[i]
                        if verificare_vecini1(self, l1, l2, c):
                            return False  # jocul nu e terminat,mai sunt locuri posibile pt mutari, cel putin 1 vertical
            return True  # jocul s-a terminat, chiar daca mai ale spatii goale, nu mai exista mutari valide

    def mutari(self, jucator):  # jucator = simbolul jucatorului care muta
        l_mutari = []
        for i in range(len(self.matr) - 1):  # creez copiile tablei de joc cu mutari de tip 2(orizontale)
            if self.matr[i] == Joc.GOL and self.matr[i + 1] == Joc.GOL and (i + 1) % 10 != 0:  # 2 spatii consec. goale,
                #  care nu se despart la capatul liniei(c1=9,c2=0)
                if i < 10:
                    l = 0  # i < 10 => se afla pe prima linie
                    c1 = i
                    c2 = c1 + 1
                else:
                    l = int(i / 10)
                    c1 = i % 10
                    c2 = c1 + 1
                if verificare_vecini2(self, l, c1, c2):
                    # daca mutarea e valida(are veciii x si o) copiez tabla cu mutarea:
                    copie_matr = copy.deepcopy(self.matr)
                    copie_matr[i] = jucator
                    copie_matr[i + 1] = jucator
                    l_mutari.append(Joc(copie_matr))
        for i in range(0, len(self.matr) - 10):  # creez copiile tablei de joc cu mutari de tip 1(verticale)
            if self.matr[i] == Joc.GOL and self.matr[i + 10] == Joc.GOL:  # 2 spatii unul sub altul goale
                if i < 10:
                    l1 = 0  # i < 10 => se afla pe prima linie
                    l2 = 1
                    c = i
                else:
                    l1 = int(i / 10)
                    l2 = l1 + 1
                    c = i % 10
                if verificare_vecini1(self, l1, l2, c):
                    # daca mutarea e valida(are veciii x si o) copiez tabla cu mutarea:
                    copie_matr = copy.deepcopy(self.matr)
                    copie_matr[i] = jucator
                    copie_matr[i + 10] = jucator
                    l_mutari.append(Joc(copie_matr))
        return l_mutari

    def calculeaza_scor(self):
        self.scor = 0
        self.scor_opus = 0
        for i in range(len(self.matr) - 20):
            if i % 10 >= 2:
                # caut diagonale formate in stanga jos si adun la scor in functie de ce simbol e
                if elem_identice(self.matr[i: i + 19: 9]):  # am gasit o diagonala completata
                    if self.matr[i] == Joc.JMAX:
                        self.scor += 1
                    else:
                        self.scor_opus += 1
            if i % 10 <= 7:
                # caut diagonale formate in dreapta jos si adun la scor in functie de ce simbol e
                if elem_identice(self.matr[i: i + 23: 11]):  # am gasit o diagonala completata
                    if self.matr[i] == Joc.JMAX:
                        self.scor += 1
                    else:
                        self.scor_opus += 1

    def diagonala_deschisa_dreapta(self, lista, jucator):
        # verific daca pornind de pe prima linie din lista de 3 linii din matrice data pot face o diagonala
        # in dreapta jos (adica daca am deja 2 simboluri puse in diagonala)
        #      0 1 2 3 4 5 6 7 8 9
        # ------------------------
        # 0 |  x # # # # # # x # #
        # 1 |  # x # # # # # # x #
        # 2 |  # # # # # # # # # #
        estimare = 0
        for j in range(0, 8):
            if lista[j] == jucator and lista[j + 11] == jucator:
                if lista[j + 22] == self.GOL:
                    estimare += 1
        return estimare

    def diagonala_deschisa_stanga(self, lista, jucator):
        # verific daca pornind de pe prima linie din lista de 3 linii din matrice data pot face o diagonala
        # in stanga jos (adica daca am deja 2 simboluri puse in diagonala)
        #      0 1 2 3 4 5 6 7 8 9
        # ------------------------
        # 0 |  # # x # # # # x # #
        # 1 |  # x # # # # x # # #
        # 2 |  # # # # # # # # # #
        estimare = 0
        for j in range(2, 10):
            if lista[j] == jucator and lista[j + 9] == jucator:
                if lista[j + 18] == self.GOL:
                    estimare += 1
        return estimare

    def linii_deschise(self, jucator):  # transmit liste a cate 3 linii din matr pt a verifica diagonale posibile
        estimare = 0
        for i in range(self.NR_COLOANE - 2):
            estimare += self.diagonala_deschisa_stanga(self.matr[i * 10: (i + 3) * 10], jucator)
            estimare += self.diagonala_deschisa_dreapta(self.matr[i * 10: (i + 3) * 10], jucator)
        return estimare

    def estimeaza_scor(self, adancime, scor, scor_opus):
        t_final = self.final()
        # if (adancime==0):
        if t_final:
            if scor > scor_opus:
                return 99 + adancime
            elif scor < scor_opus:
                return -99 - adancime
            else:
                return 0
        else:
            #return self.linii_deschise(self.__class__.JMAX) - self.linii_deschise(self.__class__.JMIN)
            self.calculeaza_scor()
            return self.scor - self.scor_opus

    def __str__(self):
        sir = "  |"
        for i in range(self.NR_COLOANE):
            sir += str(i) + " "
        sir += "\n"
        sir += "-" * (self.NR_COLOANE + 1) * 2 + "\n"
        for i in range(self.NR_COLOANE):  # itereaza prin linii
            sir += str(i) + " |" + " ".join(
                [str(x) for x in self.matr[self.NR_COLOANE * i: self.NR_COLOANE * (i + 1)]]) + "\n"
        # [0,1,2,3,4,5,6,7,8]
        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    O instanta din clasa stare este un nod din arborele minimax
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile
    posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent
        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile (tot de tip Stare) din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        # e de tip Stare (cel mai bun succesor)
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)  # lista de informatii din nodurile succesoare
        juc_opus = Joc.jucator_opus(self.j_curent)

        # mai jos calculam lista de noduri-fii (succesori)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari


    def __str__(self):
        sir = str(self.tabla_joc) + "(Jucator curent: " + self.j_curent + ")\nScor: " \
              + Joc.JMAX + " -> " + str(self.tabla_joc.scor) + "\n" + Joc.JMIN + " -> " + str(self.tabla_joc.scor_opus) + "\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    # daca sunt la o frunza in arborele minimax sau la o stare finala
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.tabla_joc.scor, stare.tabla_joc.scor_opus)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(x) for x in
                        stare.mutari_posibile]  # expandez(constr subarb) fiecare nod x din mutari posibile

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)

    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.tabla_joc.scor, stare.tabla_joc.scor_opus)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)  # aici construim subarborele pentru stare_noua

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')
        # completati cu rationament similar pe cazul stare.j_curent==Joc.JMAX
        for mutare in stare.mutari_posibile:
            # calculeaza estimarea
            stare_noua = alpha_beta(alpha, beta, mutare)  # aici construim subarborele pentru stare_noua

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break

    stare.estimare = stare.stare_aleasa.estimare

    return stare


def verif_timp(timp_curent, timp_start, timp_joc, stare_curenta):
    if timp_curent - timp_start >= timp_joc * 60:  # timp_joc transformat din minute in secunde
        print("TIME'S UP! ")
        return True
    return False


def afis_daca_final(stare_curenta, timp_curent, timp_start, timp_joc, nr_mutari_jmin, nr_mutari_jmax, timpi_calculator):
    final = stare_curenta.tabla_joc.final()  # final() returneaza "plin" daca nu mai sunt spatii goale suficiente,
    # False daca nu e stare finala adica mai exista mutari posibile valide, si True daca spatiile goale nu formeaza
    # mutari valide
    if final:
        if final == "plin":
            print("GAME OVER \nTabla nu mai are suficient spatiu pentru o mutare!")
        else:
            print("GAME OVER \nNu mai exista mutari valide pe tabla!")

    else:  # jocul nu este terminat, dar verificam daca s-a scurs timpul
        final = verif_timp(timp_curent, timp_start, timp_joc, stare_curenta)

    if final:  # in oricare dintre cazurile in care jocul s-a terminat, afisam scorul si castigaorul/remiza
        print("\nNumar mutari utilizator: ", nr_mutari_jmin, "\nNumar mutari calculator: ", nr_mutari_jmax)
        print("\nJocul a durat ", str(round(timp_curent - timp_start)), "secunde")
        stare_curenta.tabla_joc.calculeaza_scor()
        print("\nScor: " + Joc.JMAX + " -> " + str(stare_curenta.tabla_joc.scor) + "\n" +
              Joc.JMIN + " -> " + str(stare_curenta.tabla_joc.scor_opus) + "\n")
        if stare_curenta.tabla_joc.scor > stare_curenta.tabla_joc.scor_opus:
            print("Castigatorul este: ", Joc.JMAX)
        elif stare_curenta.tabla_joc.scor < stare_curenta.tabla_joc.scor_opus:
            print("Castigatorul este: ", Joc.JMIN)
        else:  # remiza
            print("REMIZA!")
        print("Statisticile jocului:\nTimpul de \"gandire\" minim: ", str(min(timpi_calculator)), "milisecunde",
              "\nTimpul de \"gandire\" maxim: ", str(max(timpi_calculator)), "milisecunde",
              "\nTimpul de \"gandire\" mediu: ",
              str((max(timpi_calculator) - min(timpi_calculator)) / len(timpi_calculator)), "milisecunde",
              "\nTimpul de \"gandire\" median: ", str(statistics.median(timpi_calculator)), "milisecunde")
        return True
    return False


def main():
    # initializare algoritm
    raspuns_valid = False

    # TO DO 1
    while not raspuns_valid:
        tip_algoritm = input("Algoritmul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    # initializare nivel joc
    raspuns_valid = False
    while not raspuns_valid:
        nivel = input("Alegeti nivelul? (raspundeti cu 1, 2 sau 3:)\n 1.Usor\n 2.Mediu\n 3.Dificil\n ")
        if nivel in ['1', '2', '3']:
            raspuns_valid = True
            if nivel == '1':
                ADANCIME_MAX = 3  # usor
            elif nivel == '2':
                ADANCIME_MAX = 5  # mediu
            else:
                ADANCIME_MAX = 7  # greu
        else:
            print("Nu ati ales o varianta corecta.")
    # Initializarea timpului :
    raspuns_valid = False
    while not raspuns_valid:
        try:
            timp_joc = float(input("Setati timpul de joc in minute: "))
            raspuns_valid = True
            TIMP_JOC = timp_joc
            print("Timp de jos setat: ", TIMP_JOC, " minute")
        except ValueError:
            print("Nu ati introdus un input valid! Se asteapta un float \n")
    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu x sau cu 0? ").lower()
        if (Joc.JMIN in ['x', '0']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie x sau 0.")
    Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'
    # expresie= val_true if conditie else val_false  (conditie? val_true: val_false)

    # initializare tabla
    tabla_curenta = Joc();  # apelam constructorul
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'x', ADANCIME_MAX)

    TIMP_START = time.time()
    timpi_calculator = []
    nr_mutari_jmin = 0
    nr_mutari_jmax = 0

    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul
            t_inainte = int(round(time.time() * 1000))
            raspuns_valid = False
            while not raspuns_valid:
                # alegerea tipului de mutare
                tip_mutare = input("Acum muta utilizatorul cu simbolul "
                                   + stare_curenta.j_curent
                                   + "\nMutarea trebuie sa fie de tipul:\n1. "
                                   + stare_curenta.j_curent
                                   + "\n   " + stare_curenta.j_curent
                                   + "\n\n2. " + stare_curenta.j_curent + " "
                                   + stare_curenta.j_curent
                                   + "\nAlegeti tipul mutarii: \n"
                                   + "\nDaca doriti sa parasiti jocul, tastati exit\n")
                if tip_mutare in ['1', '2']:
                    raspuns_valid = True
                elif tip_mutare == "exit":
                    print("Ati parasit jocul!")
                    return
                else:
                    print("Nu ati ales o varianta valida!\n")

            raspuns_valid = False
            while not raspuns_valid:
                try:
                    if tip_mutare == '1':
                        linie1 = int(input("linie1="))
                        linie2 = int(input("linie2="))
                        coloana = int(input("coloana="))

                        if (linie1 in range(Joc.NR_COLOANE) and linie2 in range(Joc.NR_COLOANE) and coloana in range(
                                Joc.NR_COLOANE) and abs(linie1 - linie2) == 1):
                            if (stare_curenta.tabla_joc.matr[linie1 * Joc.NR_COLOANE + coloana] == Joc.GOL and
                                    stare_curenta.tabla_joc.matr[linie2 * Joc.NR_COLOANE + coloana]):
                                # verific daca are vecini un x si un 0
                                if verificare_vecini1(stare_curenta.tabla_joc, linie1, linie2, coloana):
                                    raspuns_valid = True
                                else:
                                    print("\nMutarea trebuie sa aiba printre cei 10 vecini cel putin un x si un 0!\n\n")
                            else:
                                print("Exista deja un simbol in pozitia ceruta.")
                        else:
                            print("Linii sau coloana invalida (trebuie sa fie unul dintre numerele 0-9),"
                                  " iar liniile trebuie sa fie consecutive!")

                    else:
                        linie = int(input("linie="))
                        coloana1 = int(input("coloana1="))
                        coloana2 = int(input("coloana2="))

                        if (linie in range(Joc.NR_COLOANE) and coloana1 in range(Joc.NR_COLOANE) and coloana1 in range(
                                Joc.NR_COLOANE) and abs(coloana1 - coloana2) == 1):
                            if stare_curenta.tabla_joc.matr[linie * Joc.NR_COLOANE + coloana1] == Joc.GOL and \
                                    stare_curenta.tabla_joc.matr[linie * Joc.NR_COLOANE + coloana2] == Joc.GOL:
                                # verific daca are vecini un x si un 0
                                if verificare_vecini2(stare_curenta.tabla_joc, linie, coloana1, coloana2):
                                    raspuns_valid = True
                                else:
                                    print("\nMutarea trebuie sa aiba printre cei 10 vecini cel putin un x si un 0!\n\n")
                            else:
                                print("Exista deja un simbol in pozitia ceruta.")
                        else:
                            print("Linie sau coloana invalida (trebuie sa fie unul dintre numerele 0-9),"
                                  " iar liniile trebuie sa fie consecutive!")
                except ValueError:
                    print("Linia si coloana trebuie sa fie numere intregi")

            # dupa iesirea din while sigur am valide atat linia cat si coloana
            # deci pot plasa simbolul pe "tabla de joc"
            if tip_mutare == '1':
                stare_curenta.tabla_joc.matr[linie1 * Joc.NR_COLOANE + coloana] = Joc.JMIN
                stare_curenta.tabla_joc.matr[linie2 * Joc.NR_COLOANE + coloana] = Joc.JMIN
            if tip_mutare == '2':
                stare_curenta.tabla_joc.matr[linie * Joc.NR_COLOANE + coloana1] = Joc.JMIN
                stare_curenta.tabla_joc.matr[linie * Joc.NR_COLOANE + coloana2] = Joc.JMIN
            stare_curenta.tabla_joc.calculeaza_scor()
            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))
            nr_mutari_jmin += 1
            timp_curent = time.time()
            print("Utilizatorul a gandit timp de " + str(int(round(timp_curent * 1000)) - t_inainte)
                  + " milisecunde.")
            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if afis_daca_final(stare_curenta, timp_curent, TIMP_START, TIMP_JOC, nr_mutari_jmin,
                                                   nr_mutari_jmax, timpi_calculator):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            print("Acum muta calculatorul cu simbolul", stare_curenta.j_curent)
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))

            # stare actualizata e starea mea curenta in care am setat stare_aleasa (mutarea urmatoare)
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc  # aici se face de fapt mutarea !!!
            stare_curenta.tabla_joc.calculeaza_scor()
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))
            nr_mutari_jmax += 1
            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            timpi_calculator.append(t_dupa - t_inainte)
            timp_curent = time.time()
            if afis_daca_final(stare_curenta, timp_curent, TIMP_START, TIMP_JOC, nr_mutari_jmin,
                                                   nr_mutari_jmax, timpi_calculator):
                break

            # S-a realizat o mutare.  jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


if __name__ == "__main__":
    main()
