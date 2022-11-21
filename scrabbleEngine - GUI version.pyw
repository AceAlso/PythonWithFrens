import itertools, os, time, sys, pyperclip, tkinter as tk
# Program mający na celu stworzenie słowa które da najwięcej punktów z dostępnych liter w grze scrabble
# Co powinien robić program?
# 1 wklepujesz posiadane litery oraz litery które możesz wykorzystać z planszy
#DONE
# 2 program tworzy wszystkie możliwe kombinacje liter
# https://docs.python.org/3/library/itertools.html#itertools.permutations
# muszę zrobić to tak by stworzył możliwe kombinacje od 2 do liczby dostepnych liter
#DONE
# 3 program zostawia tylko te kombinacje które są słowami które można wykorzystać w grach słownych.
#https://sjp.pl/slownik/growy/
#DONE
# 4 program przypisze tym słowom punkty
#DONE
# 5 program wyświetli do 10 opcji dających największą ilość punktów oraz podane dostępne litery
#DONE
# 6 dodatkowo teraz program bierze pod uwagę możliwe do wykorzystania płytki z planszy
#DONE
# 6.5 naprawa błędu nie odpalania programu jeśli nie ma pliku slowa.txt
# 7 program bierze pod uwagę blanka
# 8 optymalizacja
pnkt = {'a': 1,'ą': 5,'b': 3,'c': 2,'ć': 6,'d': 2,'e': 1,'ę': 5,'f': 5,'g': 3,'h': 3,'i': 1,'j': 3,'k': 2,'l': 2,'ł': 3,'m': 2,'n': 1,'ń': 7,'o': 1,'ó': 5,'p': 2,'r': 1,'s': 1,'ś': 5,'t': 2,'u': 3,'w': 1,'y': 2,'z': 1,'ź': 9,'ż': 5}

#stała lista z punktami dla danej litery
czas = None
POLISH_WORDS = None
def update_status(tekst):
    status["text"]=tekst
def loadDictionary():
    file = 'slowa.txt'
    if not os.path.exists(file):
        polishWords = ''
        return polishWords
    else:
        dictionaryFile = open(file, encoding="utf-8")
        polishWords = {}
        for word in dictionaryFile.read().split('\n'):
            polishWords[word] = None
        dictionaryFile.close()
        return polishWords
def censor_gang_signs(linia):
    wypad=('')
    for h in range(len(linia)):
        if linia[h] not in pnkt:
            if linia[h] not in wypad:
                wypad=(wypad) + (linia[h])
    for i in range(len(wypad)):
        linia=linia.replace(wypad[i], '')
    return linia
def main():
    litery = None
    plansza = None
    while litery == None:
        litery = ent_litery.get()
        litery = litery.lower()
        litery = censor_gang_signs(litery)
        iteracje = list()
        if litery == '':
            litery = None
            update_status('Proszę podaj swoje litery (maks 7)')
            break
        elif len(litery) >= 8:
            litery = None
            update_status('Za dużo liter! Proszę podaj do 7 liter.')
            break
        else:
            plansza = ent_plansza.get()
            plansza = plansza.lower()
            czas = time.time()
            if plansza == '':
                for r in range(2, len(litery)+1):
                    niteracje = list(itertools.permutations(litery,r))
                    iteracje.extend(niteracje)
            else:
                plansza = censor_gang_signs(plansza)
                for p in range (len(plansza)):
                    for r in range(2, len(litery)+2):
                        listoplansza = str()
                        listoplansza = listoplansza + str(plansza[p])
                        listoplansza = listoplansza + litery
                        niteracje = list(itertools.permutations(listoplansza,r))
                        iteracje.extend(niteracje)
    else:
        listaIter = list()#lista z słowami z iteracji
        #poniżej kod odpowiedzialny za tworzenie, odsiew słów i przyznawanie im punktów
        listaPNKT = list()#lista z liczbą punktów za dane słowo z listy iteracje (punkty mają ten sam indeks co słowo)
        listaPolskieSlowa = list()#lista z odfiltrowanymi słowami
        listaPnktPl = list()#lista z punktami dla odfiltrowanych słów
        iteracje = list(dict.fromkeys(iteracje))
        for lista in iteracje:
            listaI = list()
            listaII = list() #robocze listy do przerzucania danych
            for litera in lista:
                listaI.append(pnkt[litera])
                listaII.append(litera)
            listaPNKT.append(sum(listaI))
            listaIter.append(''.join(listaII))
        for i in range(len(listaIter)):
            if listaIter[i] in POLISH_WORDS:
                listaPolskieSlowa.append(listaIter[i])
                listaPnktPl.append(listaPNKT[i])
        if not bool(listaPolskieSlowa):
            update_status('Nie da się ułożyć żadnego słowa z podanych liter.')
        else:
            wynik = zip(listaPnktPl, listaPolskieSlowa)
            wynik = list(dict.fromkeys(wynik))
            wynik.sort(reverse = True)
            out=('Najwyżej punktowane słowa \nktóre da się utworzyć z w twoich liter (%s) to: \n\npnkt słowo' % (litery))
            if len(wynik) <= 10:
                for i in range(len(wynik)):
                    out=out+"\n"+str((wynik[i]))
            else:
                for i in range(10):
                    out=out+"\n"+str((wynik[i]))
            czas = time.time() - czas
            out=out+('\n\n Cały proces zajął %s sekund(y)' % (czas))
            update_status(out)

#GUI do SE
#Okno
window = tk.Tk()
window.title("ScrabbleEngine")
#Frames
frm_entry = tk.Frame(master=window, width=900, height=200, borderwidth=5, relief=tk.GROOVE)
frm_entry.pack()
statuz = tk.Frame(master=window, width=900, borderwidth=5, relief=tk.GROOVE)
statuz.pack()
start = tk.Frame(master=window, width=900, height=200)
start.pack()
#pola na wpisywanie i opisy pól
label_litery = tk.Label(master=frm_entry, text="Podaj swoje litery.")
label_litery.pack()
ent_litery = tk.Entry(master=frm_entry, width=10)
ent_litery.pack()
label_plansza = tk.Label(master=frm_entry, text="Podaj litery z planszy z których możesz skorzystać.")
label_plansza.pack()
ent_plansza = tk.Entry(master=frm_entry, width=10)
ent_plansza.pack()
#status programu
status = tk.Label(master=statuz, text= "")
status.pack()
#przycisk odpalenia procesu
btn_start = tk.Button(master=start, text="Szukaj słów", borderwidth=5, relief=tk.RAISED, command=main)
btn_start.pack()
while POLISH_WORDS == None:
        POLISH_WORDS = loadDictionary()
        if POLISH_WORDS == '':
            update_status('Brakuje pliku slowa.txt w folderze programu.\nWrzuć plik slowa.txt z https://sjp.pl/slownik/growy/\nLink skopiowano do schowka.\nZamykam program...')
            POLISH_WORDS = None
            pyperclip.copy('https://sjp.pl/slownik/growy/')
            break
        else:
            update_status('Słownik wczytany')
window.mainloop()
#Odpalanie programu