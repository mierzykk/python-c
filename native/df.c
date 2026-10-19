#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include <math.h>

int min(int a, int b){
    return a < b ? a : b;
}

int max(int a, int b){
    return a > b ? a : b;
}

static void rsif(double sredniawzrost, double sredniaspadek, double *wynik){
    if (sredniaspadek == 0.0) {
        *wynik = 100.0;
        return;
    }
    double rs = sredniawzrost / sredniaspadek;
    *wynik = 100.0 - (100.0 / (1.0 + rs));
}

//wskaznik do tablicy, size ilosc elementow
__declspec(dllexport)
double srednia(const double *tab, int size){
    double wynik = 0;
    for (int i=0; i<size;i++){
        wynik += *(tab+i);
    }
    wynik = wynik / size;
    return wynik;
}

__declspec(dllexport)
uint8_t sma(const double *tab, int size, int okres, double *wynik){
    if (okres<=0 || size<=0) return 1;
    else if(okres > size) return 2;
    double temp = 0;
    for(int i = 0; i<okres;i++){
        temp += *(tab+i);
    }
    *wynik = (temp/ okres);
    for(int h = 0; h<(size - okres);h++){
        temp -= *(tab + h);
        temp += *(tab + h + okres);
        *(wynik + h + 1) = (temp/ okres);
    }
    return 0;
}

__declspec(dllexport)
uint8_t ema(const double *tab, int size, int okres, double *wynik){
    if (okres<=0 || size<=0) return 1;
    else if(okres > size) return 2;
    double a = 2.0/(okres+1);
    *wynik = *tab;
    for(int i = 1; i<size;i++){
        *(wynik + i) = a * *(tab + i) + (1-a) * *(wynik + i -1);
    }
    return 0;
}

__declspec(dllexport)
uint8_t rsi(const double *zmiany, int size, int okres, double *wynik){
    if (okres <= 0 || size <= 0) return 1;
    else if (okres > size) return 2;

    double wzrostsuma = 0;
    double spadeksuma = 0;

    for (int i = 0; i < okres; i++) {
        double val = *(zmiany + i);
        if (val > 0) wzrostsuma += val;
        else spadeksuma -= val;
    }

    double sredniawzrost = wzrostsuma / okres;
    double sredniaspadek = spadeksuma / okres;

    rsif(sredniawzrost, sredniaspadek, wynik);

    for (int i = okres; i < size; i++) {
        double val = *(zmiany + i);
        double cur_wzrost = (val > 0) ? val : 0.0;
        double cur_spadek = (val < 0) ? -val : 0.0;

        sredniawzrost = (sredniawzrost * (okres - 1) + cur_wzrost) / okres;
        sredniaspadek = (sredniaspadek * (okres - 1) + cur_spadek) / okres;

        rsif(sredniawzrost, sredniaspadek, wynik + i - okres + 1);
    }

    return 0;
}

__declspec(dllexport)
uint8_t change(const double *tab, int size, double *wynik){
    if(size<=1) return 1;
    for(int i = 1; i<size;i++){
        *(wynik + i - 1) = *(tab + i) - *(tab +(i - 1));
    }
    return 0;
}

__declspec(dllexport)
uint8_t wma(const double *tab, int size, int okres, double *wynik){
    if (okres <= 0 || size <= 0) return 1;
    else if (okres > size) return 2;

    double suma_wag = (double)(okres * (okres + 1)) / 2.0;
    double wma_suma = 0.0;
    double okno_suma = 0.0;

    for (int g = 0; g < okres; g++) {
        double val = *(tab + g);
        okno_suma += val;
        wma_suma += val * (g + 1);
    }

    *wynik = wma_suma / suma_wag;

    for (int i = 0; i < size - okres; i++) {
        double wycinany = *(tab + i);
        double nowy = *(tab + i + okres);

        wma_suma = wma_suma - okno_suma + nowy * okres;
        okno_suma = okno_suma - wycinany + nowy;

        *(wynik + i + 1) = wma_suma / suma_wag;
    }

    return 0;
}

__declspec(dllexport)
uint8_t roc(const double *tab, int size, int okres, double *wynik){
    if (okres <= 0 || size <= 0) return 1;
    else if (okres > size) return 2;

    for(int i = 0; i<size-okres;i++){
        *(wynik + i) = ((*(tab + okres + i) / *(tab + i)) -1) *100;
    }
    return 0;
}
__declspec(dllexport)
uint8_t macd(const double *tab, int size, int szybki, int wolny, int sygnal, double *macd, double *signallist, double *histogram){
    double *wynikszybki = calloc(size, sizeof(double));
    double *wynikwolny = calloc(size, sizeof(double));
    if(wynikszybki == NULL || wynikwolny == NULL) return 3;
    if(ema(tab,size,wolny,wynikwolny) != 0|| ema(tab,size,szybki,wynikszybki) != 0) if(wolny > size || szybki > size) return 2; else return 1;
    for(int i = 0; i<size;i++){
        *(macd + i) = *(wynikszybki + i) - *(wynikwolny + i);
    }
    if(ema(macd,size,sygnal,signallist) != 0)if(sygnal > size) return 2; else return 1;
    for(int i = 0; i<size;i++){
        *(histogram + i) = *(macd + i) - *(signallist + i);
    }
    free(wynikszybki);
    free(wynikwolny);
    return 0;
}

__declspec(dllexport)
uint8_t momentum(const double *tab, int size, int okres, double *wynik){
    if (okres <= 0 || size <= 0) return 1;
    else if (okres > size) return 2;
    for(int i = 0; i<size-okres; i++){
        *(wynik + i) = *(tab+okres+i) - *(tab + i);
    }
    return 0;
}

__declspec(dllexport)
uint8_t williams(const double *high, const double *low, const double *close, int size, int okres, double *wynik){
    if (okres <= 0 || size <= 0) return 1;
    else if (okres > size) return 2;
    double lowest = DBL_MAX;
    double highest = -DBL_MAX;

    for(int i = 0;i<size - okres + 1;i++){
        for(int h = 0; h<okres;h++){
           if(*(high + i + h)>highest) highest = *(high + i + h);
           if(*(low + i + h)<lowest) lowest = *(low + i + h);
        }
        if(highest == lowest) return 4;
        *(wynik + i) = ((highest - *(close + i))/(highest-lowest)) * -100;
        highest = -DBL_MAX;
        lowest = DBL_MAX;
    }
    return 0;
}

__declspec(dllexport)
uint8_t variance(const double *tab, int size, int okres, double *wynik){
    if (okres <= 0 || size <= 0) return 1;
    else if (okres > size) return 2;
    double sredniaa;
    double suma=0;
    for(int i = 0; i<size - okres+1;i++){
        sredniaa = srednia(tab + i,okres);
        for(int j = 0; j<okres; j++){
            suma += (tab[i+j]-sredniaa)*(tab[i+j]-sredniaa);
        }
        *(wynik+i) = suma/okres;
        suma = 0;
    }
    return 0;    
}

__declspec(dllexport)
uint8_t stddev(const double *tab, int size, int okres, double *wynik){
    if (okres <= 0 || size <= 0) return 1;
    else if (okres > size) return 2;
    double sredniaa;
    double suma=0;
    for(int i = 0; i<size - okres+1;i++){
        sredniaa = srednia(tab + i,okres);
        for(int j = 0; j<okres; j++){
            suma += (tab[i+j]-sredniaa)*(tab[i+j]-sredniaa);
        }
        *(wynik+i) = sqrt(suma/okres);
        suma = 0;
    }
    return 0;
}

__declspec(dllexport)
uint8_t bollinger(const double *tab, int size, int okres, double mnoznik, double *upper, double *middle, double *lower){
    if (okres <= 0 || size <= 0) return 1;
    else if (okres > size) return 2;
    double *sd = calloc(size-okres+1,sizeof(double));
    if (sd == NULL) return 3;
    stddev(tab,size,okres,sd);
    for(int i = 0; i<size-okres+1;i++){
        //midle band
        *(middle + i) = srednia(tab+i,okres);
        //upper
        *(upper + i) = *(middle + i) + (mnoznik * *(sd + i));
        //lower
        *(lower + i) = *(middle + i) - (mnoznik * *(sd + i));
    }
    free(sd);
    return 0;
}

__declspec(dllexport)
uint8_t atr(const double *high, const double *low, const double *close, int size, int okres, double *wynik){
    if (okres <= 0 || size <= 0) return 1;
    else if (size < okres) return 2;
    double *tr = calloc(size, sizeof(double));
    if (tr == NULL) return 3;
    *tr = *high - *low;
    for(int i = 1; i< size; i++){
        *(tr + i) = fmax(*(high + i) - *(low + i),fmax(fabs(*(high + i) - *(close + i - 1)),fabs(*(low + i) - *(close + i - 1))));
    }
    *wynik = 0;
    for(int i = 0; i<okres;i++){
        *wynik += *(tr + i);
    }
    *wynik = *wynik/okres;
    for(int i = 1; i< size - okres + 1;i++){
        *(wynik + i) = (*(wynik + i - 1) * (okres - 1) + *(tr + okres + i- 1)) / okres;
    }
    
    free(tr);
    return 0;
}

__declspec(dllexport)
uint8_t stochastic(const double *high, const double *low, const double *close, int size, int okres, double *wynik){
    if (okres <= 0 || size <= 0) return 1;
    else if (size < okres) return 2;
    double lowest = DBL_MAX;
    double highest = -DBL_MAX;
    for(int i = 0; i < size - okres + 1; i++){
        for(int h = 0; h<okres;h++){
           if(*(high + i + h)>highest) highest = *(high + i + h);
           if(*(low + i + h)<lowest) lowest = *(low + i + h);
        }
        if(highest == lowest) return 4;
        *(wynik + i) = ((*(close + okres + i - 1) - lowest) / (highest - lowest)) *100;
        highest = -DBL_MAX;
        lowest = DBL_MAX;
    }
    return 0;
}

__declspec(dllexport)
uint8_t adx(const double *high, const double *low, const double *close, int size, int okres, double *wynik){
    if (okres <= 0 || size <= 0) return 1;
    else if (size < 2 * okres) return 2;
    double upmove;
    double downmove;
    double *dx = calloc(size, sizeof(double));
    double trsmooth = 0;
    double plusdmsmooth = 0;
    double minusdmsmooth = 0;
    double *plusdm = calloc(size, sizeof(double));
    double *minudm = calloc(size, sizeof(double));
    double *tr = calloc(size, sizeof(double));
    if (tr == NULL || minudm == NULL || plusdm == NULL || dx == NULL) return 3;
    *tr = *high - *low;
    for(int i = 1; i< size; i++){
        *(tr + i) = fmax(*(high + i) - *(low + i),fmax(fabs(*(high + i) - *(close + i - 1)),fabs(*(low + i) - *(close + i - 1))));
        upmove = *(high + i) - *(high + i -1);
        downmove = *(low + i -1 ) - *(low + i);
        if(upmove>downmove) {if(upmove > 0) *(plusdm + i) = upmove;}
        else if(downmove>0 && upmove!=downmove) *(minudm + i) = downmove;
        }
    for (int i = 0; i < okres; i++) {
        trsmooth += *(tr + i);
        plusdmsmooth += *(plusdm + i);
        minusdmsmooth += *(minudm + i);
    }
    for (int i = okres; i < size; i++){
        trsmooth = trsmooth - (trsmooth/okres) +*(tr+i);
        plusdmsmooth = plusdmsmooth - (plusdmsmooth/okres) +*(plusdm+i);
        minusdmsmooth = minusdmsmooth - (minusdmsmooth/okres) +*(minudm+i);
        if (trsmooth == 0) return 4;
        else if (minusdmsmooth == 0 && plusdmsmooth == 0) return 4;
        *(dx +i - okres) = 100 * ((fabs((100 * (plusdmsmooth/trsmooth)) - (100 * (minusdmsmooth/trsmooth)))) / ((100 * (plusdmsmooth/trsmooth)) + (100 * (minusdmsmooth/trsmooth))));
    }
    *wynik = 0;
    for(int i = 0; i<okres;i++){
        *wynik += *(dx+i);
    }
    *wynik = *wynik/okres;
    for(int i = 1; i<size - (2 * okres) + 1;i++){
        *(wynik + i) = (*(wynik + i - 1) * (okres - 1) + *(dx + i +okres - 1))/okres;
    }

    free(tr);
    free(minudm);
    free(plusdm);
    free(dx);
    return 0;
}

__declspec(dllexport)
uint8_t cci(const double *high, const double *low, const double *close, int size, int okres, double *wynik){
    if (okres <= 0 || size <= 0) return 1;
    else if (size < okres) return 2;
    for(int i = 0; i < size - okres + 1; i++){
        double sma = 0;
        for(int h = 0; h < okres; h++){
            sma += (*(high + i + h) + *(low + i + h) + *(close + i + h)) / 3.0;
        }
        sma /= okres;

        double md = 0;
        for(int h = 0; h < okres; h++){
            double tp = (*(high + i + h) + *(low + i + h) + *(close + i + h)) / 3.0;
            md += fabs(tp - sma);
        }
        md /= okres;

        double last_tp = (*(high + i + okres - 1) + *(low + i + okres - 1) + *(close + i + okres - 1)) / 3.0;
        *(wynik + i) = (last_tp - sma) / (0.015 * md);
    }
    return 0;
}

__declspec(dllexport)
uint8_t obv( const double *close, const double *volume, int size, double *wynik){
    if(size <= 0) return 1;
    *wynik = 0;
    for(int i =1; i<size;i++){
        if(*(close + i) > *(close+ i -1)) *(wynik + i) = *(wynik + i -1) + *(volume + i);
        else if(*(close + i) < *(close+ i -1)) *(wynik + i) = *(wynik + i -1) - *(volume + i);
        else *(wynik + i) = *(wynik + i -1);
    }
    return 0;
}

__declspec(dllexport)
uint8_t vwap(const double *high, const double *low, const double *close, const double *volume, int size, double *wynik){
    if(size <= 0) return 1;
    double sum1 = 0;
    double sum2 = 0;
    for(int i = 0; i<size; i++){
        sum1 += ((*(high + i) + *(low + i) + *(close + i)) /3) * *(volume + i);
        sum2 += *(volume + i);
        if (sum2 == 0) return 4;
        *(wynik + i) = sum1/sum2;
    }
    return 0;
}

__declspec(dllexport)
uint8_t mfi(const double *high, const double *low, const double *close, const double *volume, int size, int okres, double *wynik){
    if (okres <= 0 || size <= 0) return 1;
    else if (size < okres) return 2;
    double tp;
    double tppoprzednie = (*high + *low + *close) /3;
    double positive = 0;
    double negative = 0;
    for (int h = 1; h<size - okres + 1;h++){
        for(int i = h; i<h+okres; i++){
            tp = (*(high + i) + *(low + i) + *(close + i)) /3;
            if(tp>tppoprzednie) positive += tp * *(volume + i);
            else if(tp<tppoprzednie) negative += tp * *(volume + i);
            tppoprzednie = tp;
        }
        tppoprzednie = (*(high + h) + *(low + h) + *(close + h)) /3;
        if(negative == 0){
            if(positive>0) *(wynik + h -1) = 100;
            else if(positive == 0) *(wynik + h -1) = 50;
        }
        else *(wynik + h-1) = 100 - (100 / ( 1 + ( positive / negative)));
        positive = 0;
        negative = 0;
    }
    return 0;
}

__declspec(dllexport)
uint8_t psar(const double *high, const double *low, int size, double step, double max_step, double *wynik){
    if (step <= 0 || size <= 0 || max_step <= 0) return 1;
    else if (step>max_step) return 2;
    double sar = *low;
    double ep = *high;
    double af = step;
    char trend = 0;
    *wynik = sar;

    for(int i = 1; i<size;i++){
        sar = sar + af * (ep-sar);
        if (trend == 0){
            if (*(high + i)>ep){ 
                ep = *(high + i);
                if (af + step>max_step) af = max_step;
                else af += step;
            }
            if (i -2 >= 0) sar = fmin(sar, fmin(*(low + i - 1),*(low + i - 2)));
            else sar = fmin(sar, *(low + i - 1));

            if(*(low + i) < sar){ 
                trend = 1;
                sar = ep;
                ep = *(low + i);
                af = step;
            }
        }
        else{
            if (*(low + i)<ep){
                ep = *(low + i);
                if (af + step>max_step) af = max_step;
                else af += step;
            }
            if (i -2 >= 0) sar = fmax(sar, fmax(*(high + i - 1),*(high + i - 2)));
            else sar = fmax(sar, *(high + i - 1));
            
            if(*(high + i) > sar){ 
                trend = 0;
                sar = ep;
                ep = *(high + i);
                af = step;
            }
        }
        *(wynik + i) = sar;
    }
    return 0;
}

__declspec(dllexport)
uint8_t ichimoku(const double *high, const double *low, const double *close, int size, int tenkan, int kijun, int senkou, double *tenkan_w, double *kijun_w, double *senkou_a, double *senkou_b, double *chikou){
    if (tenkan <= 0 || size <= 0 || senkou <= 0 || kijun <= 0) return 1;
    if(tenkan >= size || senkou >= size || kijun >= size) return 2;
    double max = -DBL_MAX;
    double imin = DBL_MAX;
    for (int i = 0; i <= size - tenkan; i++){
        for(int h = i; h<tenkan + i;h++){
            if(*(high+h)>max) max = *(high+h);
            if(*(low+h)<imin) imin = *(low+h);
        }
        *(tenkan_w + i + tenkan - 1) = (max + imin) / 2;
        imin = DBL_MAX;
        max = -DBL_MAX;
    }
    for (int i = 0; i <= size - kijun; i++){
        if (i < size - kijun) *(chikou + i) = *(close + i + kijun);
        for(int h = i; h<kijun + i;h++){
            if(*(high+h)>max) max = *(high+h);
            if(*(low+h)<imin) imin = *(low+h);
        }
        *(kijun_w + i + kijun - 1) = (max + imin) / 2;
        imin = DBL_MAX;
        max = -DBL_MAX;
    }

    for (int i =0;i<size - senkou + 1; i++){
        for(int h = i; h<senkou + i;h++){
            if(*(high+h)>max) max = *(high+h);
            if(*(low+h)<imin) imin = *(low+h);
        }
        *(senkou_b + i + kijun) = (max + imin) / 2;
        imin = DBL_MAX;
        max = -DBL_MAX;
    }
    int first_valid = (tenkan > kijun ? tenkan : kijun) - 1;
    int projected_size = size - senkou + kijun + 1;
    int output_size = size > projected_size ? size : projected_size;
    for(int i = first_valid; i < size && i + kijun < output_size; i++){
        *(senkou_a + i + kijun) = (*(tenkan_w + i) + *(kijun_w + i)) / 2;
    }
    return 0;
}

__declspec(dllexport)
uint8_t aroon(const double *high, const double *low, int size, int okres, double *up, double *down){
    if (okres <= 0 || size <= 0) return 1;
    else if (size < okres) return 2;
    double max = -DBL_MAX;
    double min = DBL_MAX;
    uint32_t indekslow; 
    uint32_t indekshigh; 
    for(int i = size - 1;i>okres - 2;i--){
        for(int h = i; h > i - okres; h--){
            if (*(high + h) > max){ max = *(high + h); indekshigh = h;}
            if (*(low + h) < min){ min = *(low + h); indekslow = h;}
        }
        *(up + size - i -1) = (1 - (double)(i - indekshigh) /okres) * 100;
        *(down + size - i -1) = (1 - (double)(i - indekslow) /okres) * 100;
        min = DBL_MAX;
        max = -DBL_MAX;
    }
    return 0;
}

__declspec(dllexport)
uint8_t keltner(const double *high, const double *low, const double *close, int size, int okres, double mnoznik, double *upper, double *middle, double *lower){
    if (okres <= 0 || size <= 0) return 1;
    if (size < okres) return 2;
    double *atrw = calloc(size, sizeof(double));
    double *emaw = calloc(size, sizeof(double));
    if (atrw == NULL || emaw == NULL) return 3;

    ema(close, size, okres, emaw);
    atr(high, low, close, size, okres, atrw);

    for (int i = 0; i < size - okres + 1; i++){
        int idx = i + okres - 1;

        *(middle + i) = *(emaw + idx);
        *(upper + i) = *(emaw + idx) + mnoznik * *(atrw + i);
        *(lower + i) = *(emaw + idx) - mnoznik * *(atrw + i);
    }
    free(atrw);
    free(emaw);

    return 0;
}

__declspec(dllexport)
uint8_t donchian(const double *high, const double *low, int size, int okres, double *upper, double *lower, double *middle){
    if (okres <= 0 || size <= 0) return 1;
    else if (size < okres) return 2;
    double max = -DBL_MAX;
    double min = DBL_MAX;
    for (int i =0;i < size - okres + 1; i++){
        for(int h = i; h<okres + i;h++){
            if(*(high+h)>max) max = *(high+h);
            if(*(low+h)<min) min = *(low+h);
        }
        *(middle + i) = (max + min) / 2;
        *(upper + i) = max;
        *(lower + i) = min;

        min = DBL_MAX;
        max = -DBL_MAX;
    }
    return 0;
}

__declspec(dllexport)
uint8_t cmf(const double *high, const double *low, const double *close, const double *volume, int size, int okres, double *wynik){
    if (okres <= 0 || size <= 0) return 1;
    else if (size < okres) return 2;
    double mfv = 0; 
    double suma = 0;
    for(int i = 0;i<size - okres + 1;i++){
        for(int h = i; h<okres + i; h++){
            if(*(high + h) == *(low + h)) return 4;
            mfv += (((2 * *(close + h)) - *(low + h) - *(high + h)) / (*(high + h) - *(low + h))) * *(volume + h);
            suma += *(volume + h);
        }
        if (suma == 0) return 4;
        *(wynik + i) = mfv/suma;
        mfv = 0;
        suma = 0;
    }
    return 0;
}

__declspec(dllexport)
uint8_t williamsad(const double *high, const double *low, const double *close, int size, double *wynik){
    if(size <= 0) return 1;
    *wynik = 0;
    for(int i = 1; i<size; i++){
        if ( *(close + i)> *(close + i -1)) *(wynik + i) = *(wynik + i -1) + *(close + i) - fmin(*(low + i),*(close + i -1));
        else if ( *(close + i)< *(close + i -1)) *(wynik + i) = *(wynik + i -1) + *(close + i) - fmax(*(high + i),*(close + i -1));
        else *(wynik + i) = *(wynik + i - 1);
    }   
    return 0;
}

__declspec(dllexport)
uint8_t trix(const double *close, int size, int okres, double *wynik){
    if (okres <= 0 || size <= 0) return 1;
    else if (size < okres) return 2;
    double *ema1 = malloc(size * sizeof(double));
    double *ema2 = malloc(size * sizeof(double));
    if(ema1==NULL || ema2==NULL) return 3;

    ema(close,size,okres,ema1);
    ema(ema1,size,okres,ema2);
    ema(ema2,size,okres,ema1);
    free(ema2);

    for(int i =1; i<size;i++){
        if (*(ema1 + i - 1) == 0){ free(ema1); return 4;}
        *(wynik + i - 1) = (*(ema1 + i) / *(ema1 + i - 1) - 1) * 100;
    }
    free(ema1);
    return 0;
}

__declspec(dllexport)
uint8_t forceindex(const double *close, const double *volume, int size, double *wynik){
    if (size <= 0) return 1;
    for(int i = 1; i< size;i++){
        *(wynik + i -1) = (*(close + i) - *(close + i -1)) * *(volume + i);
    }
    return 0;
}

__declspec(dllexport)
uint8_t ultimateoscillator( const double *high, const double *low, const double *close, int size, int okres1, int okres2, int okres3, double *wynik){
    if (okres1 <= 0 || size <= 0 || okres2 <= 0 || okres3 <= 0) return 1;
    if(okres1 >= size || okres2 >= size || okres3 >= size) return 2;
    double avgbp1;
    double avgbp2;
    double avgbp3;
    double bp = 0;
    double tr = 0;

    for(int i = 1; i<size - max(okres1, max(okres2, okres3))+1;i++){
        for(int h =i; h<okres1 + i;h++){
            bp += *(close + h) - fmin(*(low + h), *(close + h-1));
            tr += fmax(*(high + h) - *(low + h),fmax(fabs(*(high + h) - *(close + h - 1)),fabs(*(low + h) - *(close + h - 1))));
        }
        if (tr == 0) return 4; 
        avgbp1 = bp/tr;
        bp = 0;
        tr = 0;
        for(int h =i; h<okres2 + i;h++){
            bp += *(close + h) - fmin(*(low + h), *(close + h-1));
            tr += fmax(*(high + h) - *(low + h),fmax(fabs(*(high + h) - *(close + h - 1)),fabs(*(low + h) - *(close + h - 1))));
        }
        if (tr == 0) return 4; 
        avgbp2 = bp/tr;
        bp = 0;
        tr = 0;
        for(int h =i; h<okres3 + i;h++){
            bp += *(close + h) - fmin(*(low + h), *(close + h-1));
            tr += fmax(*(high + h) - *(low + h),fmax(fabs(*(high + h) - *(close + h - 1)),fabs(*(low + h) - *(close + h - 1))));
        }
        if (tr == 0) return 4; 
        avgbp3 = bp/tr;
        bp = 0;
        tr = 0;

        *(wynik + i -1) = 100 * (((4 * avgbp1) + (2 * avgbp2) + avgbp3)/7);
    }
    return 0;
}

__declspec(dllexport)
uint8_t awesomeoscillator(const double *high, const double *low, int size, int okres1, int okres2, double *wynik){
    if (okres1 <= 0 || size <= 0 || okres2 <= 0) return 1;
    if (okres1 >= size || okres2 >= size) return 2;
    double sma1 = 0;
    double sma2 = 0;
    int p = max(okres1, okres2);

    for(int i = 0; i < size - p + 1; i++){
        for(int h = p + i - okres1; h < p + i; h++){
            sma1 += (*(high + h) + *(low + h)) / 2;
        }
        sma1 = sma1 / okres1;
        for(int h = p + i - okres2; h < p + i; h++){
            sma2 += (*(high + h) + *(low + h)) / 2;
        }
        sma2 = sma2 / okres2;
        *(wynik + i) = sma1 - sma2;
        sma1 = sma2= 0;
    }
    return 0;
}

__declspec(dllexport)
uint8_t eom(const double *high, const double *low, const double *volume, int size, double *wynik){
    if(size <= 0) return 1;
    for(int i = 1; i<size;i++){
        if (*(volume + i) == 0) return 4;
        *(wynik + i -1) = ((*(high + i) + *(low + i))/2 - (*(high + i - 1) + *(low + i - 1))/2) * ((*(high + i) - *(low + i)) / *(volume + i));
    }
    return 0;
}

__declspec(dllexport)
uint8_t kama(const double *close, int size, int okres, int fast, int slow, double *wynik){
    if (okres <= 0 || size <= 0 || fast <= 0 || slow <= 0) return 1;
    if (okres >= size || fast >= size || slow >= size) return 2;
    double sum = 0;
    *wynik = *(close+okres);

    for (int i = okres + 1; i< size;i++){
        for(int h = i - okres + 1; h <= i; h++){
            sum += fabs(*(close + h) - *(close + h - 1));
        }
        if (sum == 0) return 4;
        *(wynik + i - okres) = *(wynik + i - okres - 1) + ((fabs(*(close + i) - *(close + i - okres))/ sum * (2.0 / (fast + 1) - 2.0 / (slow + 1)) + 2.0 / (slow + 1)) * (fabs(*(close + i) - *(close + i - okres))/ sum * (2.0 / (fast + 1) - 2.0 / (slow + 1)) + 2.0 / (slow + 1))) * (*(close + i) - *(wynik + i - okres - 1));
        sum = 0;
    }
    return 0;
}

__declspec(dllexport)
uint8_t hma(const double *close, int size, int okres, double *wynik){
    if (okres <= 1 || size <= 0) return 1;
    else if (size < okres || (int)(sqrt(okres))> size - okres + 1) return 2;
    int s = okres/2;
    double *wma1 = calloc(size - s + 1, sizeof(double));
    double *wma2 = calloc(size - okres + 1, sizeof(double));
    double *r = calloc(size - okres + 1, sizeof(double));
    if(wma1 == NULL || wma2 == NULL || r == NULL) return 3;


    wma(close,size,s,wma1);
    wma(close,size,okres,wma2);

    for (int i = 0; i<size - okres + 1;i++){
        *(r + i) = 2 * wma1[s + i] - *(wma2 + i);
    }
    wma(r, size - okres + 1, (int)(sqrt(okres)),wynik);
    
    free(wma1);
    free(wma2);
    free(r);
    return 0;
}

__declspec(dllexport)
uint8_t dpo(const double *close, int size, int okres, double *wynik){
    if (okres<=1 || size<=0) return 1;
    else if(okres > size) return 2;
    int k = okres / 2;
    double *b = calloc(size - k, sizeof(double));
    if(b == NULL) return 3;
    sma(close, size, k + 1,b);

    for(int i = 0; i<size - k;i++){
        *(wynik + i) = *(close + i + k) - *(b + i);
    }

    free(b);
    return 0;
}
