import time



def write_log(code, name, print_log:bool = False, message = "brak wiadomosci"):
    czas = time.localtime()
    with open("log.txt", "a") as a:
        a.write(f"rok: {czas.tm_year} miesiac: {czas.tm_mon} dzien: {czas.tm_mday} godzina: {czas.tm_hour} minuta: {czas.tm_min} sekunda: {czas.tm_sec} funkcja: {name} kod: {code} message: {message}\n")
    if print_log:
        print(f"LOG: godzina: {czas.tm_hour} minuta: {czas.tm_min} funkcja: {name} kod: {code} message: {message}")


