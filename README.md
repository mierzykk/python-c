# python-c

Projekt biblioteki do analizy giełdowej napisanej w Pythonie i C.

## Funkcje

- Obliczanie wskaźników analizy technicznej.
- Implementacja obliczeń w C.
- Integracja C z Pythonem za pomocą bibliotek DLL.
- Pobieranie i analiza danych giełdowych.

### Dostępne wskaźniki

SMA, EMA, WMA, HMA, KAMA, RSI, MACD, ROC, ATR, ADX, Bollinger Bands, Stochastic, CCI, OBV, VWAP, MFI, Ichimoku i wiele innych.

## Technologie

- Python
- C

## Status

Projekt jest w trakcie rozwoju. Nie wszystkie funkcje zostały w pełni przetestowane.

## Uruchomienie

na Windowsie przejdź do katalogu `native` i uruchom:

```bat
make.bat
```

Skrypt kompiluje kod C do bibliotek DLL używanych przez Python.

## Cel projektu

Stworzenie biblioteki do analizy giełdowej

## jak uzywac
1. pip install numpy pandas yfinance matplotlib
2. python help.py
glowne funckcje sa opisane w main.py 

## dysclaimer
to nie porada inwestycyjna btw
plik opisy.json jest przydatny ale moze zawierac drobne bledy tak samo help.py
