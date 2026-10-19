from ctypes import c_double, c_int, POINTER, c_uint8
import numpy as np
import json
import copy
try:
    from analysis import log
except ImportError:
    import log
try:
    from analysis import analist
except ImportError:
    import analist


erorcode = ["okres albo size jest mniejszy lub równy zero", #C
            "okres jest większy niz rozmiar danych wejsciowych", #C
            "calloc nie przyznal pamieci", #C
            "blad dzielenia przez 0", #C
            "bledna wielkosc tablicy", #python 
            "blad przygotowania tablicy" #python
            ]
dll = None
def iferror(status, name, wywal_gdy_blad, print_log:bool = False, message = ""):
    if status <= len(erorcode) and status>0 and not message:
        message = erorcode[status-1]
    elif not message: message ="nieznany blad"
    log.write_log(status,name,print_log,message)
    if wywal_gdy_blad:
        raise ValueError(message)





class df:
    def __init__(self):

        self.dll = analist.loaddll().dlldf

        self.dll.srednia.argtypes = [POINTER(c_double), c_int]
        self.dll.srednia.restype = c_double

        self.dll.sma.argtypes = [POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.sma.restype = c_uint8

        self.dll.ema.argtypes = [POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.ema.restype = c_uint8

        self.dll.rsi.argtypes = [POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.rsi.restype = c_uint8

        self.dll.change.argtypes = [POINTER(c_double), c_int, POINTER(c_double)]
        self.dll.change.restype = c_uint8

        self.dll.wma.argtypes = [POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.wma.restype = c_uint8

        self.dll.roc.argtypes = [POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.roc.restype = c_uint8

        self.dll.macd.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
        self.dll.macd.restype = c_uint8

        self.dll.momentum.argtypes = [POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.momentum.restype = c_uint8

        self.dll.williams.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.williams.restype = c_uint8

        self.dll.variance.argtypes = [POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.variance.restype = c_uint8

        self.dll.stddev.argtypes = [POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.stddev.restype = c_uint8

        self.dll.bollinger.argtypes = [POINTER(c_double), c_int, c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
        self.dll.bollinger.restype = c_uint8

        self.dll.atr.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.atr.restype = c_uint8

        self.dll.stochastic.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.stochastic.restype = c_uint8

        self.dll.adx.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.adx.restype = c_uint8

        self.dll.cci.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.cci.restype = c_uint8

        self.dll.obv.argtypes = [POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double)]
        self.dll.obv.restype = c_uint8

        self.dll.vwap.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double)]
        self.dll.vwap.restype = c_uint8

        self.dll.mfi.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.mfi.restype = c_uint8

        self.dll.psar.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_double, c_double, POINTER(c_double)]
        self.dll.psar.restype = c_uint8

        self.dll.ichimoku.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
        self.dll.ichimoku.restype = c_uint8

        self.dll.aroon.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, POINTER(c_double), POINTER(c_double)]
        self.dll.aroon.restype = c_uint8

        self.dll.keltner.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
        self.dll.keltner.restype = c_uint8

        self.dll.donchian.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
        self.dll.donchian.restype = c_uint8

        self.dll.cmf.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.cmf.restype = c_uint8

        self.dll.williamsad.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double)]
        self.dll.williamsad.restype = c_uint8

        self.dll.trix.argtypes = [POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.trix.restype = c_uint8

        self.dll.forceindex.argtypes = [POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double)]
        self.dll.forceindex.restype = c_uint8

        self.dll.ultimateoscillator.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, POINTER(c_double)]
        self.dll.ultimateoscillator.restype = c_uint8

        self.dll.awesomeoscillator.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, POINTER(c_double)]
        self.dll.awesomeoscillator.restype = c_uint8

        self.dll.eom.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double)]
        self.dll.eom.restype = c_uint8

        self.dll.kama.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, POINTER(c_double)]
        self.dll.kama.restype = c_uint8

        self.dll.hma.argtypes = [POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.hma.restype = c_uint8

        self.dll.dpo.argtypes = [POINTER(c_double), c_int, c_int, POINTER(c_double)]
        self.dll.dpo.restype = c_uint8

    @staticmethod
    def help(tryb = 0, nazwafunkcji = None):
        
        if tryb == 0: return """help przyjmuje tryb od 1 do 5 i dla trybu 5 przyjmuje nazwafunkcji tryby:
1 wyswietla wszystkie funkcje
2 wyswietla funkcje ktore wywoluje sie wspolne(close,okres, nazwa funckji utd)
3 wyswietla funkcje ktore wywoluje sie wspolnehlc(high, low, close, okres, funkcja itd)
4 wyswietla funkcje ktore maja specjalne wrappery 
5 wymaga nazwy funkcji i opisuje ta funkcje
0 opisuje help"""
        elif tryb == 1: return "ema, sma, wma, rsi, roc, momentum, variance, stddev, bollinger, atr, stochastic, change, macd, williams, adx, cci, obv, vwap, mfi, psar, ichimoku, aroon, keltner, donchian, cmf, williamsad, trix, forceindex, ultimateoscillator, awesomeoscillator, eom, kama, hma, dpo"
        elif tryb == 2: return "ema, sma, wma, roc, momentum, variance, stddev, trix, hma, dpo"
        elif tryb == 3: return "atr, stochastic, williams, adx, cci"
        elif tryb == 4: return "bollinger, change, macd, rsi, obv, vwap, mfi, psar, ichimoku, aroon, keltner, donchian, cmf, williamsad, forceindex, ultimateoscillator, awesomeoscillator, eom, kama"
        elif tryb == 5:
            if not nazwafunkcji: return "nie podano nazwy funkcji"
            try:
                with open("opisy.json", encoding="utf-8") as j:
                    teksty = json.load(j)
            except FileNotFoundError:
                with open(r"analysis\opisy.json", encoding="utf-8") as j:
                    teksty = json.load(j)
            try: return teksty[str(nazwafunkcji).lower()]
            except: return "niepoprawna nazwa funckji"
        else:
            return "tryb musi byc od 0 do 5"


    def wspolne(self, close, okres, funkcja, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            tab = np.ascontiguousarray(close, dtype=np.float64)
            if str(funkcja) == "trix": wynik = np.zeros(tab.size - 1, dtype=np.float64)
            elif str(funkcja) == "roc" or str(funkcja) == "momentum": wynik = np.zeros(tab.size - okres, dtype=np.float64)
            elif str(funkcja) == "hma": wynik = np.zeros(tab.size - okres - int(np.sqrt(okres)) + 2, dtype=np.float64)
            elif str(funkcja) == "dpo": wynik = np.zeros(tab.size - okres // 2, dtype=np.float64)
            elif str(funkcja) == "ema": wynik = np.zeros(tab.size, dtype=np.float64)
            else: wynik = np.zeros(tab.size - okres + 1, dtype=np.float64)
        except ValueError:
            status = 6

        if status !=0:
            iferror(status, funkcja, wywal_gdy_blad, print_log)
            if zwroc_kod:
                return np.zeros(1, dtype=np.float64), status
            return np.zeros(1, dtype=np.float64)
        
        metoda = getattr(self,str(funkcja))
        status = metoda(okres, tab, wynik)

        if status != 0:
            iferror(status, funkcja, wywal_gdy_blad, print_log)
        if zwroc_kod:
            return wynik, status
        return wynik

    def rsi(self,okres, tab, wynik):
        status = self.dll.rsi( #type:ignore
            tab.ctypes.data_as(POINTER(c_double)),
            tab.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status

    def ema(self,okres, tab, wynik):
        status = self.dll.ema( #type:ignore
            tab.ctypes.data_as(POINTER(c_double)),
            tab.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status

    def sma(self,okres, tab, wynik):
        status = self.dll.sma( #type:ignore
            tab.ctypes.data_as(POINTER(c_double)),
            tab.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status

    def wma(self,okres, tab, wynik):
        status = self.dll.wma( #type:ignore
            tab.ctypes.data_as(POINTER(c_double)),
            tab.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status

    def roc(self,okres, tab, wynik):
        status = self.dll.roc( #type:ignore
            tab.ctypes.data_as(POINTER(c_double)),
            tab.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status

    def momentum(self, okres, tab, wynik):
        status = self.dll.momentum( #type:ignore
            tab.ctypes.data_as(POINTER(c_double)),
            tab.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status

    def variance(self, okres, tab, wynik):
        status = self.dll.variance( #type:ignore
            tab.ctypes.data_as(POINTER(c_double)),
            tab.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status

    def stddev(self, okres, tab, wynik):
        status = self.dll.stddev( #type:ignore
            tab.ctypes.data_as(POINTER(c_double)),
            tab.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status

    def trix(self, okres, tab, wynik):
        status = self.dll.trix( #type:ignore
            tab.ctypes.data_as(POINTER(c_double)),
            tab.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status

    def hma(self, okres, tab, wynik):
        status = self.dll.hma( #type:ignore
            tab.ctypes.data_as(POINTER(c_double)),
            tab.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status

    def dpo(self, okres, tab, wynik):
        status = self.dll.dpo( #type:ignore
            tab.ctypes.data_as(POINTER(c_double)),
            tab.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status

    def wspolnehlc(self, high, low, close, okres, funkcja, print_log:bool = True, wywal_gdy_blad=True, zwroc_kod=False):
        status = 0
        try:
            t_high = np.ascontiguousarray(high, dtype=np.float64)
            t_low = np.ascontiguousarray(low, dtype=np.float64)
            t_close = np.ascontiguousarray(close, dtype=np.float64)
            if funkcja == "adx": wynik = np.zeros(t_high.size - 2 * okres+1, dtype=np.float64)
            else: wynik = np.zeros(t_high.size - okres + 1, dtype=np.float64)
            if not t_high.size == t_low.size == t_close.size: status = 5
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, funkcja, wywal_gdy_blad, print_log)
            if zwroc_kod:
                return np.zeros(1, dtype=np.float64), status
            return np.zeros(1, dtype=np.float64)
        
        metoda = getattr(self,str(funkcja))
        status = metoda(okres, t_high, t_low, t_close, wynik)

        if status != 0:
            iferror(status, funkcja, wywal_gdy_blad, print_log)

        if zwroc_kod:
            return wynik, status
        return wynik

    def atr(self, okres, t_high, t_low, t_close, wynik):
        status = self.dll.atr( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_close.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status

    def stochastic(self, okres, t_high, t_low, t_close, wynik):
        status = self.dll.stochastic( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_close.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status
    

    def williams(self, okres, t_high, t_low, t_close, wynik):  
        status = self.dll.williams( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_close.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status

    def adx(self, okres, t_high, t_low, t_close, wynik):
        status = self.dll.adx( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_close.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status
    
    def cci(self, okres, t_high, t_low, t_close, wynik):
        status = self.dll.cci( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_close.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )
        return status

    def bollinger(self, close, okres, mnoznik=2.0, print_log:bool = True, wywal_gdy_blad=True, zwroc_kod=False):
        status = 0
        try:
            tab = np.ascontiguousarray(close, dtype=np.float64)
            upper = np.zeros(tab.size - okres + 1, dtype=np.float64)
            middle = np.zeros(tab.size - okres + 1, dtype=np.float64)
            lower = np.zeros(tab.size - okres + 1, dtype=np.float64)
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, "bollinger", wywal_gdy_blad, print_log)
            puste = np.zeros(1, dtype=np.float64)
            if zwroc_kod:
                return puste, copy.deepcopy(puste), copy.deepcopy(puste), status
            return puste, copy.deepcopy(puste), copy.deepcopy(puste)
        
        status = self.dll.bollinger( #type:ignore
            tab.ctypes.data_as(POINTER(c_double)),
            tab.size,
            okres,
            mnoznik,
            upper.ctypes.data_as(POINTER(c_double)),
            middle.ctypes.data_as(POINTER(c_double)),
            lower.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "bollinger", wywal_gdy_blad, print_log)

        if zwroc_kod:
            return upper, middle, lower, status
        return upper, middle, lower

    def macd(self, close, szybki, wolny, sygnal, print_log:bool = True, wywal_gdy_blad=True, zwroc_kod=False):
        status = 0
        try:
            tab = np.ascontiguousarray(close, dtype=np.float64)
            macd_wynik = np.zeros(tab.size, dtype=np.float64)
            signal_wynik = np.zeros(tab.size, dtype=np.float64)
            histogram_wynik = np.zeros(tab.size, dtype=np.float64)
        except ValueError:
            status = 6
        if status !=0:
            iferror(status, "macd", wywal_gdy_blad, print_log)
            puste = np.zeros(1, dtype=np.float64)
            if zwroc_kod:
                return puste, copy.deepcopy(puste), copy.deepcopy(puste), status
            return puste, copy.deepcopy(puste), copy.deepcopy(puste)
        status = self.dll.macd(
            tab.ctypes.data_as(POINTER(c_double)),
            tab.size,
            szybki,
            wolny,
            sygnal,
            macd_wynik.ctypes.data_as(POINTER(c_double)),
            signal_wynik.ctypes.data_as(POINTER(c_double)),
            histogram_wynik.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "macd", wywal_gdy_blad, print_log)

        if zwroc_kod:
            return macd_wynik, signal_wynik, histogram_wynik, status

        return macd_wynik, signal_wynik, histogram_wynik

    def change(self, close, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            tab = np.ascontiguousarray(close, dtype=np.float64)
            wynik = np.zeros(tab.size - 1, dtype=np.float64)
        except ValueError:
            status = 6
        
        if status  !=0:
            iferror(status, "change", wywal_gdy_blad, print_log)
            if zwroc_kod:
                return np.zeros(1, dtype=np.float64), status
            return np.zeros(1, dtype=np.float64)
        
        status = self.dll.change( #type:ignore
            tab.ctypes.data_as(POINTER(c_double)),
            tab.size,
            wynik.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "change", wywal_gdy_blad, print_log)

        if zwroc_kod:
            return wynik, status
        return wynik

    def obv(self,close, volume, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            t_close = np.ascontiguousarray(close, dtype=np.float64)
            t_volume = np.ascontiguousarray(volume, dtype=np.float64)
            wynik = np.zeros(t_close.size, dtype=np.float64)
            if t_close.size != t_volume.size:
                status = 5
        except ValueError:
            status = 6
        
        if status != 0:
            iferror(status, "obv", wywal_gdy_blad, print_log)
            if zwroc_kod:
                return np.zeros(1, dtype=np.float64), status
            return np.zeros(1, dtype=np.float64)


        status = self.dll.obv(
            t_close.ctypes.data_as(POINTER(c_double)),
            t_volume.ctypes.data_as(POINTER(c_double)),
            t_close.size,
            wynik.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "obv", wywal_gdy_blad, print_log)

        if zwroc_kod:
            return wynik, status
        return wynik

    def vwap(self, high, low, close, volume, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            t_high = np.ascontiguousarray(high, dtype=np.float64)
            t_low = np.ascontiguousarray(low, dtype=np.float64)
            t_close = np.ascontiguousarray(close, dtype=np.float64)
            t_volume = np.ascontiguousarray(volume, dtype=np.float64)
            wynik = np.zeros(t_high.size, dtype=np.float64)
            if not t_high.size == t_low.size == t_close.size == t_volume.size: status = 5
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, "vwap", wywal_gdy_blad, print_log)
            if zwroc_kod:
                return np.zeros(1, dtype=np.float64), status
            return np.zeros(1, dtype=np.float64)

        status = self.dll.vwap( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_close.ctypes.data_as(POINTER(c_double)),
            t_volume.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            wynik.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "vwap", wywal_gdy_blad, print_log)
        if zwroc_kod:
            return wynik, status
        return wynik

    def mfi(self, high, low, close, volume, okres, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            t_high = np.ascontiguousarray(high, dtype=np.float64)
            t_low = np.ascontiguousarray(low, dtype=np.float64)
            t_close = np.ascontiguousarray(close, dtype=np.float64)
            t_volume = np.ascontiguousarray(volume, dtype=np.float64)
            wynik = np.zeros(t_high.size - okres, dtype=np.float64)
            if not t_high.size == t_low.size == t_close.size == t_volume.size: status = 5
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, "mfi", wywal_gdy_blad, print_log)
            if zwroc_kod:
                return np.zeros(1, dtype=np.float64), status
            return np.zeros(1, dtype=np.float64)

        status = self.dll.mfi( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_close.ctypes.data_as(POINTER(c_double)),
            t_volume.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "mfi", wywal_gdy_blad, print_log)
        if zwroc_kod:
            return wynik, status
        return wynik

    def psar(self, high, low, step=0.02, max_step=0.2, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            t_high = np.ascontiguousarray(high, dtype=np.float64)
            t_low = np.ascontiguousarray(low, dtype=np.float64)
            wynik = np.zeros(t_high.size, dtype=np.float64)
            if t_high.size != t_low.size: status = 5
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, "psar", wywal_gdy_blad, print_log)
            if zwroc_kod:
                return np.zeros(1, dtype=np.float64), status
            return np.zeros(1, dtype=np.float64)

        status = self.dll.psar( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            step,
            max_step,
            wynik.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "psar", wywal_gdy_blad, print_log)
        if zwroc_kod:
            return wynik, status
        return wynik

    def ichimoku(self, high, low, close, tenkan, kijun, senkou, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            t_high = np.ascontiguousarray(high, dtype=np.float64)
            t_low = np.ascontiguousarray(low, dtype=np.float64)
            t_close = np.ascontiguousarray(close, dtype=np.float64)
            output_size = max(t_high.size, t_high.size - senkou + kijun + 1)
            tenkan_w = np.zeros(output_size, dtype=np.float64)
            kijun_w = np.zeros(output_size, dtype=np.float64)
            senkou_a = np.zeros(output_size, dtype=np.float64)
            senkou_b = np.zeros(output_size, dtype=np.float64)
            chikou = np.zeros(output_size, dtype=np.float64)
            if not t_high.size == t_low.size == t_close.size: status = 5
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, "ichimoku", wywal_gdy_blad, print_log)
            puste = np.zeros(1, dtype=np.float64)
            if zwroc_kod:
                return puste, copy.deepcopy(puste), copy.deepcopy(puste), copy.deepcopy(puste), copy.deepcopy(puste), status
            return puste, copy.deepcopy(puste), copy.deepcopy(puste), copy.deepcopy(puste), copy.deepcopy(puste)

        status = self.dll.ichimoku( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_close.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            tenkan,
            kijun,
            senkou,
            tenkan_w.ctypes.data_as(POINTER(c_double)),
            kijun_w.ctypes.data_as(POINTER(c_double)),
            senkou_a.ctypes.data_as(POINTER(c_double)),
            senkou_b.ctypes.data_as(POINTER(c_double)),
            chikou.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "ichimoku", wywal_gdy_blad, print_log)
        if zwroc_kod:
            return tenkan_w, kijun_w, senkou_a, senkou_b, chikou, status
        return tenkan_w, kijun_w, senkou_a, senkou_b, chikou

    def aroon(self, high, low, okres, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            t_high = np.ascontiguousarray(high, dtype=np.float64)
            t_low = np.ascontiguousarray(low, dtype=np.float64)
            up = np.zeros(t_high.size - okres + 1, dtype=np.float64)
            down = np.zeros(t_high.size - okres + 1, dtype=np.float64)
            if t_high.size != t_low.size: status = 5
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, "aroon", wywal_gdy_blad, print_log)
            puste = np.zeros(1, dtype=np.float64)
            if zwroc_kod:
                return puste, copy.deepcopy(puste), status
            return puste, copy.deepcopy(puste)

        status = self.dll.aroon( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            okres,
            up.ctypes.data_as(POINTER(c_double)),
            down.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "aroon", wywal_gdy_blad, print_log)
        if zwroc_kod:
            return up, down, status
        return up, down

    def keltner(self, high, low, close, okres, mnoznik=2.0, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            t_high = np.ascontiguousarray(high, dtype=np.float64)
            t_low = np.ascontiguousarray(low, dtype=np.float64)
            t_close = np.ascontiguousarray(close, dtype=np.float64)
            upper = np.zeros(t_high.size - okres + 1, dtype=np.float64)
            middle = np.zeros(t_high.size - okres + 1, dtype=np.float64)
            lower = np.zeros(t_high.size - okres + 1, dtype=np.float64)
            if not t_high.size == t_low.size == t_close.size: status = 5
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, "keltner", wywal_gdy_blad, print_log)
            puste = np.zeros(1, dtype=np.float64)
            if zwroc_kod:
                return puste, copy.deepcopy(puste), copy.deepcopy(puste), status
            return puste, copy.deepcopy(puste), copy.deepcopy(puste)

        status = self.dll.keltner( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_close.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            okres,
            mnoznik,
            upper.ctypes.data_as(POINTER(c_double)),
            middle.ctypes.data_as(POINTER(c_double)),
            lower.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "keltner", wywal_gdy_blad, print_log)
        if zwroc_kod:
            return upper, middle, lower, status
        return upper, middle, lower

    def donchian(self, high, low, okres, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            t_high = np.ascontiguousarray(high, dtype=np.float64)
            t_low = np.ascontiguousarray(low, dtype=np.float64)
            upper = np.zeros(t_high.size - okres + 1, dtype=np.float64)
            lower = np.zeros(t_high.size - okres + 1, dtype=np.float64)
            middle = np.zeros(t_high.size - okres + 1, dtype=np.float64)
            if t_high.size != t_low.size: status = 5
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, "donchian", wywal_gdy_blad, print_log)
            puste = np.zeros(1, dtype=np.float64)
            if zwroc_kod:
                return puste, copy.deepcopy(puste), copy.deepcopy(puste), status
            return puste, copy.deepcopy(puste), copy.deepcopy(puste)

        status = self.dll.donchian( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            okres,
            upper.ctypes.data_as(POINTER(c_double)),
            lower.ctypes.data_as(POINTER(c_double)),
            middle.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "donchian", wywal_gdy_blad, print_log)
        if zwroc_kod:
            return upper, lower, middle, status
        return upper, lower, middle

    def cmf(self, high, low, close, volume, okres, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            t_high = np.ascontiguousarray(high, dtype=np.float64)
            t_low = np.ascontiguousarray(low, dtype=np.float64)
            t_close = np.ascontiguousarray(close, dtype=np.float64)
            t_volume = np.ascontiguousarray(volume, dtype=np.float64)
            wynik = np.zeros(t_high.size - okres + 1, dtype=np.float64)
            if not t_high.size == t_low.size == t_close.size == t_volume.size: status = 5
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, "cmf", wywal_gdy_blad, print_log)
            if zwroc_kod:
                return np.zeros(1, dtype=np.float64), status
            return np.zeros(1, dtype=np.float64)

        status = self.dll.cmf( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_close.ctypes.data_as(POINTER(c_double)),
            t_volume.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            okres,
            wynik.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "cmf", wywal_gdy_blad, print_log)
        if zwroc_kod:
            return wynik, status
        return wynik

    def williamsad(self, high, low, close, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            t_high = np.ascontiguousarray(high, dtype=np.float64)
            t_low = np.ascontiguousarray(low, dtype=np.float64)
            t_close = np.ascontiguousarray(close, dtype=np.float64)
            wynik = np.zeros(t_high.size, dtype=np.float64)
            if not t_high.size == t_low.size == t_close.size: status = 5
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, "williamsad", wywal_gdy_blad, print_log)
            if zwroc_kod:
                return np.zeros(1, dtype=np.float64), status
            return np.zeros(1, dtype=np.float64)

        status = self.dll.williamsad( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_close.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            wynik.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "williamsad", wywal_gdy_blad, print_log)
        if zwroc_kod:
            return wynik, status
        return wynik

    def forceindex(self, close, volume, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            t_close = np.ascontiguousarray(close, dtype=np.float64)
            t_volume = np.ascontiguousarray(volume, dtype=np.float64)
            wynik = np.zeros(t_close.size - 1, dtype=np.float64)
            if t_close.size != t_volume.size: status = 5
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, "forceindex", wywal_gdy_blad, print_log)
            if zwroc_kod:
                return np.zeros(1, dtype=np.float64), status
            return np.zeros(1, dtype=np.float64)

        status = self.dll.forceindex( #type:ignore
            t_close.ctypes.data_as(POINTER(c_double)),
            t_volume.ctypes.data_as(POINTER(c_double)),
            t_close.size,
            wynik.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "forceindex", wywal_gdy_blad, print_log)
        if zwroc_kod:
            return wynik, status
        return wynik

    def ultimateoscillator(self, high, low, close, okres1, okres2, okres3, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            t_high = np.ascontiguousarray(high, dtype=np.float64)
            t_low = np.ascontiguousarray(low, dtype=np.float64)
            t_close = np.ascontiguousarray(close, dtype=np.float64)
            wynik = np.zeros(t_high.size - max(okres1, okres2, okres3), dtype=np.float64)
            if not t_high.size == t_low.size == t_close.size: status = 5
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, "ultimateoscillator", wywal_gdy_blad, print_log)
            if zwroc_kod:
                return np.zeros(1, dtype=np.float64), status
            return np.zeros(1, dtype=np.float64)

        status = self.dll.ultimateoscillator( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_close.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            okres1,
            okres2,
            okres3,
            wynik.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "ultimateoscillator", wywal_gdy_blad, print_log)
        if zwroc_kod:
            return wynik, status
        return wynik

    def awesomeoscillator(self, high, low, okres1, okres2, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            t_high = np.ascontiguousarray(high, dtype=np.float64)
            t_low = np.ascontiguousarray(low, dtype=np.float64)
            wynik = np.zeros(t_high.size - max(okres1, okres2) + 1, dtype=np.float64)
            if t_high.size != t_low.size: status = 5
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, "awesomeoscillator", wywal_gdy_blad, print_log)
            if zwroc_kod:
                return np.zeros(1, dtype=np.float64), status
            return np.zeros(1, dtype=np.float64)

        status = self.dll.awesomeoscillator( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            okres1,
            okres2,
            wynik.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "awesomeoscillator", wywal_gdy_blad, print_log)
        if zwroc_kod:
            return wynik, status
        return wynik

    def eom(self, high, low, volume, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            t_high = np.ascontiguousarray(high, dtype=np.float64)
            t_low = np.ascontiguousarray(low, dtype=np.float64)
            t_volume = np.ascontiguousarray(volume, dtype=np.float64)
            wynik = np.zeros(t_high.size - 1, dtype=np.float64)
            if not t_high.size == t_low.size == t_volume.size: status = 5
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, "eom", wywal_gdy_blad, print_log)
            if zwroc_kod:
                return np.zeros(1, dtype=np.float64), status
            return np.zeros(1, dtype=np.float64)

        status = self.dll.eom( #type:ignore
            t_high.ctypes.data_as(POINTER(c_double)),
            t_low.ctypes.data_as(POINTER(c_double)),
            t_volume.ctypes.data_as(POINTER(c_double)),
            t_high.size,
            wynik.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "eom", wywal_gdy_blad, print_log)
        if zwroc_kod:
            return wynik, status
        return wynik

    def kama(self, close, okres, fast, slow, print_log:bool = True, wywal_gdy_blad = True, zwroc_kod = False):
        status = 0
        try:
            t_close = np.ascontiguousarray(close, dtype=np.float64)
            wynik = np.zeros(t_close.size - okres, dtype=np.float64)
        except ValueError:
            status = 6

        if status != 0:
            iferror(status, "kama", wywal_gdy_blad, print_log)
            if zwroc_kod:
                return np.zeros(1, dtype=np.float64), status
            return np.zeros(1, dtype=np.float64)

        status = self.dll.kama( #type:ignore
            t_close.ctypes.data_as(POINTER(c_double)),
            t_close.size,
            okres,
            fast,
            slow,
            wynik.ctypes.data_as(POINTER(c_double))
        )

        if status != 0:
            iferror(status, "kama", wywal_gdy_blad, print_log)
        if zwroc_kod:
            return wynik, status
        return wynik