import time
start = time.perf_counter()
print("importowanie")
import market.market as m
from analysis.df import df
zaimportowanopo = time.perf_counter()
print(f'zaimportowano po: {zaimportowanopo - start}')
print("inicjalizowanie")
#inicjalizowanie ticketu powinno sie robic to raz na caly program
m.init("AAPL")
print(f'zainicjalizowano po: {time.perf_counter() - zaimportowanopo}')

#ladowanie close do osobne zmiennej
close = m.market.df["Close"]

#inicjalizacja df
df = df()

#wyswietla mozliwosci df
print(df.help())

#przykladowe uzycie
wynik = df.wspolne(close, 20, "sma")
print(wynik)
