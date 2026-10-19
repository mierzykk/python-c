import yfinance as yf

market = None

class create:
    def __init__(self, ticker, period="1y", interval="1d"):
        self.ticker = yf.Ticker(ticker=ticker)
        self.df = self.ticker.history(period=period, interval=interval)
        self.chain = self.ticker.option_chain(self.ticker.options[0]) #niezbedny features

class stock:

    class ticker:
        """Opisy tego, co można pobrać z yf.Ticker."""

        info = (
            "Zwraca ogólne informacje o spółce, takie jak nazwa, "
            "sektor, branża, kapitalizacja i podstawowe wskaźniki."
        )

        fast_info = (
            "Zwraca najważniejsze i szybko dostępne informacje rynkowe "
            "o instrumencie."
        )

        history = (
            "Zwraca historyczne dane cenowe OHLCV dla wybranego okresu "
            "i interwału."
        )

        dividends = (
            "Zwraca historię wypłaconych dywidend wraz z datami."
        )

        splits = (
            "Zwraca historię splitów akcji oraz ich współczynniki."
        )

        actions = (
            "Zwraca historię działań korporacyjnych, takich jak "
            "dywidendy i splity."
        )

        capital_gains = (
            "Zwraca historię wypłat zysków kapitałowych, głównie "
            "dla funduszy i ETF-ów."
        )

        income_stmt = (
            "Zwraca roczny rachunek zysków i strat spółki."
        )

        quarterly_income_stmt = (
            "Zwraca kwartalny rachunek zysków i strat spółki."
        )

        balance_sheet = (
            "Zwraca roczny bilans spółki obejmujący aktywa, "
            "zobowiązania i kapitał własny."
        )

        quarterly_balance_sheet = (
            "Zwraca kwartalny bilans spółki."
        )

        cashflow = (
            "Zwraca roczny rachunek przepływów pieniężnych spółki."
        )

        quarterly_cashflow = (
            "Zwraca kwartalny rachunek przepływów pieniężnych."
        )

        financials = (
            "Zwraca podstawowe roczne dane finansowe spółki."
        )

        quarterly_financials = (
            "Zwraca podstawowe kwartalne dane finansowe spółki."
        )

        ttm_income_stmt = (
            "Zwraca rachunek zysków i strat za ostatnie 12 miesięcy."
        )

        ttm_cashflow = (
            "Zwraca przepływy pieniężne za ostatnie 12 miesięcy."
        )

        ttm_financials = (
            "Zwraca dane finansowe spółki za ostatnie 12 miesięcy."
        )

        earnings = (
            "Zwraca roczne dane dotyczące wyników i zysków spółki."
        )

        quarterly_earnings = (
            "Zwraca kwartalne wyniki finansowe spółki."
        )

        earnings_dates = (
            "Zwraca daty publikacji wyników finansowych."
        )

        earnings_history = (
            "Zwraca historyczne wyniki EPS i porównanie ich z prognozami."
        )

        earnings_estimate = (
            "Zwraca prognozy analityków dotyczące przyszłego EPS."
        )

        revenue_estimate = (
            "Zwraca prognozy analityków dotyczące przyszłych przychodów."
        )

        eps_revisions = (
            "Zwraca zmiany prognoz EPS dokonywane przez analityków."
        )

        eps_trend = (
            "Zwraca trend prognozowanego EPS w kolejnych okresach."
        )

        growth_estimates = (
            "Zwraca prognozy dotyczące przyszłego wzrostu spółki."
        )

        recommendations = (
            "Zwraca historyczne rekomendacje analityków dotyczące spółki."
        )

        recommendations_summary = (
            "Zwraca podsumowanie rekomendacji analityków."
        )

        upgrades_downgrades = (
            "Zwraca historię podwyższeń i obniżeń rekomendacji analityków."
        )

        analyst_price_targets = (
            "Zwraca cele cenowe analityków, w tym minimalny, średni "
            "i maksymalny."
        )

        major_holders = (
            "Zwraca informacje o głównych udziałowcach spółki."
        )

        institutional_holders = (
            "Zwraca informacje o instytucjach posiadających akcje spółki."
        )

        mutualfund_holders = (
            "Zwraca informacje o funduszach posiadających akcje spółki."
        )

        insider_roster_holders = (
            "Zwraca listę insiderów oraz informacje o ich udziałach."
        )

        insider_transactions = (
            "Zwraca historię transakcji kupna i sprzedaży akcji przez insiderów."
        )

        insider_purchases = (
            "Zwraca informacje o zakupach akcji dokonywanych przez insiderów."
        )

        shares = (
            "Zwraca informacje dotyczące liczby akcji spółki."
        )

        shares_full = (
            "Zwraca szczegółową historię liczby akcji spółki."
        )

        sustainability = (
            "Zwraca dostępne dane dotyczące zrównoważonego rozwoju i ESG."
        )

        news = (
            "Zwraca wiadomości powiązane z danym instrumentem."
        )

        sec_filings = (
            "Zwraca dostępne dokumenty i zgłoszenia spółki składane do SEC."
        )

        calendar = (
            "Zwraca zaplanowane wydarzenia dotyczące spółki."
        )

        options = (
            "Zwraca listę dostępnych terminów wygaśnięcia opcji."
        )

        option_chain = (
            "Zwraca dane wszystkich opcji CALL i PUT dla wybranego terminu."
        )

        funds_data = (
            "Zwraca dane charakterystyczne dla ETF-ów i funduszy."
        )


    class df:
        """Opisy danych znajdujących się w historycznym DataFrame."""

        history = (
            "Historyczne dane giełdowe zawierające między innymi "
            "Open, High, Low, Close i Volume."
        )

        Open = (
            "Cena otwarcia instrumentu w danym okresie."
        )

        High = (
            "Najwyższa cena instrumentu w danym okresie."
        )

        Low = (
            "Najniższa cena instrumentu w danym okresie."
        )

        Close = (
            "Cena zamknięcia instrumentu w danym okresie."
        )

        Volume = (
            "Liczba akcji lub jednostek instrumentu będących przedmiotem obrotu."
        )

        Dividends = (
            "Wartość dywidendy przypadająca na akcję w danym okresie."
        )

        Stock_Splits = (
            "Informacja o splitach akcji występujących w danym okresie."
        )


    class chain:
        """Opisy danych z option chain."""

        calls = (
            "Zwraca dane dotyczące opcji CALL dla wybranego terminu."
        )

        puts = (
            "Zwraca dane dotyczące opcji PUT dla wybranego terminu."
        )

        contractSymbol = (
            "Symbol identyfikujący konkretny kontrakt opcyjny."
        )

        lastPrice = (
            "Ostatnia dostępna cena kontraktu opcyjnego."
        )

        bid = (
            "Najwyższa cena, jaką kupujący oferuje za kontrakt."
        )

        ask = (
            "Najniższa cena, po której sprzedający oferuje kontrakt."
        )

        volume = (
            "Liczba kontraktów opcyjnych będących przedmiotem obrotu."
        )

        openInterest = (
            "Liczba otwartych kontraktów opcyjnych."
        )

        impliedVolatility = (
            "Implikowana zmienność wynikająca z aktualnej ceny opcji."
        )

        strike = (
            "Cena wykonania kontraktu opcyjnego."
        )

        expiration = (
            "Data wygaśnięcia kontraktu opcyjnego."
        )


def init(ticker="AAPL", period="1y", interval="1d"):
    global market
    market = create(ticker, period, interval)

def reset(ticker, period="1y", interval="1d"):
    if not market:
        raise ValueError("Market is not initialized. Call init() first.")
    market.ticker = yf.Ticker(ticker)
    market.df = market.ticker.history(period=period, interval=interval)
    market.chain = market.ticker.option_chain(market.ticker.options[0])
