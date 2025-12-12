import random

def nutzer_tipps():
    tipps = set()
    print("Bitte geben Sie Ihre 6 Lotto-Tipps ein (Zahlen zwischen 1 und 49, keine Wiederholungen).")

    while len(tipps) < 6:
        try:
            zahl = int(input(f"Tipp {len(tipps) + 1}: "))
            if 1 <= zahl <= 49:
                if zahl not in tipps:
                    tipps.add(zahl)
                else:
                    print("Diese Zahl wurde bereits getippt.")
            else:
                print("Zahl muss zwischen 1 und 49 liegen.")
        except ValueError:
            print("Bitte geben Sie eine ganze Zahl ein.")
    return tipps

def lotto_ziehung():
    return set(random.sample(range(1, 50), 6))

def main():
    tipps = nutzer_tipps()
    ziehung = lotto_ziehung()

    print("\nIhre Tipps:", sorted(tipps))
    print("Gezogene Lottozahlen:", sorted(ziehung))

    richtige = tipps & ziehung
    print(f"Richtige Treffer: {sorted(richtige)}")
    print(f"Anzahl Richtige: {len(richtige)}")

if __name__ == "__main__":
    main()