from typing import Literal
from market.market import stock, init
import market.market as m
import inter
import inspect

def inspektklasa(cls):
    klasy = []
    # Pobranie wszystkich atrybutów klasy głównej
    for name, obj in inspect.getmembers(cls):
        if name.startswith("__"):
            continue

        # Wypisanie podklas
        if inspect.isclass(obj):
            klasy.append(name)
    return klasy

def inspektpole(klasy, klasa_glowna):
    pola = []
    for obj in klasy:
        pola_klasy = []
        for sub_name, sub_obj in inspect.getmembers(getattr(klasa_glowna, obj)):
            if sub_name.startswith("__"):
                continue
            if not inspect.isclass(sub_obj):
                pola_klasy.append(sub_name)  # lub sub_obj jeśli potrzebna jest wartość
        pola.append(pola_klasy)
    return pola

def helpcli():


    klasy = inspektklasa(stock)
    pola = inspektpole(klasy, stock)

    print("wybierz klase z listy (numer od 0 do ilosci klas -1): ")
    print(klasy)
    while True:
        liczba = int(input(">"))
        if liczba < 0 or liczba >= len(klasy):
            print("Nieprawidłowy numer klasy.")
            continue
        break

    wybranaklasa =klasy[liczba]
    print(pola[liczba])
    while True:
        liczbaklasa = input(f"wybierz pole z listy (numer od 0 do ilosci pol -1 albo nazwa) (maksymalna liczba: {len(pola[liczba])-1}): ")
        try:
            liczbaklasa = int(liczbaklasa)
            if liczbaklasa < 0 or liczbaklasa >= len(pola[liczba]):
                print("Nieprawidłowy numer pola.")
                continue
        except ValueError:
            if liczbaklasa not in pola[liczba]:
                print("Nieprawidłowa nazwa pola.")
                continue
            liczbaklasa = pola[liczba].index(liczbaklasa)  # Zamiana nazwy na indeks
        break

    print(f"Wybrano klasę: {wybranaklasa}, pole: {pola[liczba][liczbaklasa]}")
    print(getattr(getattr(stock, wybranaklasa), pola[liczba][liczbaklasa]))  # Wywołanie wybranego pola klasy
    wybor = inter.TrueorFalse("czy chcesz zobaczyc jaka liczbe wzraca to pole?\n>")
    if wybor:
        element = getattr(
        getattr(m.market, wybranaklasa),
        pola[liczba][liczbaklasa]
    )
        if callable(element):
            element = element()
        print(element)

def help(podklasa: Literal["ticker", "df", "chain"], pole: str):
    return getattr(getattr(stock, podklasa), pole)

if __name__ == "__main__":
    m.init(input("podaj ticket np AAPL>"))
    helpcli()
