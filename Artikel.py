import json
import os

DATEI_NAME = "artikel.json"

class Artikel:
    def __init__(self, name, nummer, preis, bestand):
        self.name = name
        self.nummer = nummer
        self.preis = preis
        self.bestand = bestand

    def berechne_gesamtwert(self):
        return self.preis * self.bestand

    def to_dict(self):
        return {
            "name": self.name,
            "nummer": self.nummer,
            "preis": self.preis,
            "bestand": self.bestand
        }

    @staticmethod
    def from_dict(d):
        return Artikel(d["name"], d["nummer"], d["preis"], d["bestand"])


def lade_artikel():
    if not os.path.exists(DATEI_NAME):
        return []
    with open(DATEI_NAME, "r", encoding="utf-8") as f:
        daten = json.load(f)
    return [Artikel.from_dict(e) for e in daten]


def speichere_artikel(liste):
    with open(DATEI_NAME, "w", encoding="utf-8") as f:
        json.dump([a.to_dict() for a in liste], f, ensure_ascii=False, indent=2)


def main():
    artikel_liste = lade_artikel()

    while True:
        print("\n1. Neuer Artikel")
        print("2. Übersicht über Bestand und Gesamtwert")
        print("3. Artikel löschen")
        print("4. Beenden")

        wahl = input("Auswahl (1-4): ").strip()
        if wahl == "1":
            artikel = neuer_artikel()
            artikel_liste.append(artikel)
            speichere_artikel(artikel_liste)
            print(f"Artikel '{artikel.name}' hinzugefügt und gespeichert.")

        elif wahl == "2":
            vorrat_anzeigen(artikel_liste)

        elif wahl == "3":
            if not artikel_liste:
                print("Keine Artikel zum Löschen vorhanden.")
                continue

            nummer = input("Artikelnummer zum Löschen: ").strip()
            # Artikel mit dieser Nummer suchen
            to_delete = next((a for a in artikel_liste if a.nummer == nummer), None)
            if to_delete:
                artikel_liste.remove(to_delete)
                speichere_artikel(artikel_liste)
                print(f"Artikel '{to_delete.name}' (Nr. {nummer}) gelöscht.")
            else:
                print(f"Kein Artikel mit Nummer {nummer} gefunden.")

        elif wahl == "4":
            speichere_artikel(artikel_liste)
            print("Programm beendet. Aktueller Stand wurde gespeichert.")
            break

        else:
            print("Ungültige Auswahl. Bitte 1, 2, 3 oder 4 eingeben.")


def neuer_artikel():
    name = input("Name des Artikels: ").strip()
    nummer = input("Artikelnummer: ").strip()

    while True:
        try:
            preis = float(input("Preis (z.B. 12.50): ").strip().replace(',', '.'))
            break
        except ValueError:
            print("Ungültiger Preis. Bitte erneut eingeben.")

    while True:
        try:
            bestand = int(input("Bestand (ganzzahlig): ").strip())
            break
        except ValueError:
            print("Ungültiger Bestand. Bitte ganzzahligen Wert eingeben.")

    return Artikel(name, nummer, preis, bestand)


def vorrat_anzeigen(artikel_liste):
    if not artikel_liste:
        print("Keine Artikel im Lager.")
        return

    print("\nAktueller Lagerbestand:")
    for art in artikel_liste:
        gesamtwert = art.berechne_gesamtwert()
        print(
            f"• {art.name} (Nr. {art.nummer}): "
            f"{art.bestand} × {art.preis:.2f} € = {gesamtwert:.2f} €"
        )


if __name__ == "__main__":
    main()
