import json
import os
import uuid
from datetime import date, datetime
from typing import List, Union, Dict

# Dateinamen für Kunden- und Artikeldaten
KUNDEN_DATEI = "kunden.json"
ARTIKEL_DATEI = "artikel.json"


# ---- Artikel-Verwaltung ----

class Artikel:
    def __init__(self, name: str, nummer: str, preis: float, bestand: int):
        self.name = name
        self.nummer = nummer
        self.preis = preis
        self.bestand = bestand

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "nummer": self.nummer,
            "preis": self.preis,
            "bestand": self.bestand,
        }

    @staticmethod
    def from_dict(d: dict) -> "Artikel":
        return Artikel(
            name=d["name"],
            nummer=d["nummer"],
            preis=d["preis"],
            bestand=d["bestand"]
        )


def lade_artikel() -> List[Artikel]:
    """Lädt alle Artikel aus der JSON-Datei."""
    if not os.path.exists(ARTIKEL_DATEI):
        return []
    with open(ARTIKEL_DATEI, "r", encoding="utf-8") as f:
        daten = json.load(f)
    return [Artikel.from_dict(e) for e in daten]


def speichere_artikel(liste: List[Artikel]):
    """Speichert die Artikel-Liste zurück in die JSON-Datei."""
    with open(ARTIKEL_DATEI, "w", encoding="utf-8") as f:
        json.dump([a.to_dict() for a in liste], f, ensure_ascii=False, indent=2)


def vorrat_anzeigen(artikel_liste: List[Artikel]):
    """Gibt den aktuellen Lagerbestand mit Preisen aus."""
    if not artikel_liste:
        print("Keine Artikel im Lager.")
        return

    print("\nAktueller Artikel-Vorrat:")
    for art in artikel_liste:
        gesamtwert = art.preis * art.bestand
        print(
            f"• {art.name} (Nr. {art.nummer}): "
            f"Preis {art.preis:.2f} € | "
            f"Bestand {art.bestand} | "
            f"Gesamtwert {gesamtwert:.2f} €"
        )


# ---- Bestell- und Kundendaten ----

class Bestellung:
    # artikelliste: Liste von Positionen mit {"nummer": str, "menge": int}
    def __init__(
        self,
        artikelliste: List[Dict[str, Union[str, int]]],
        rechnungsbetrag: float,
        bestelldatum: date = None
    ):
        self.bestellnummer = str(uuid.uuid4())
        self.artikelliste = artikelliste
        self.bestelldatum = bestelldatum or date.today()
        self.rechnungsbetrag = rechnungsbetrag

    def __str__(self):
        pos_str = ", ".join([f"Nr {p['nummer']} x {p['menge']}" for p in self.artikelliste])
        return (
            f"Bestellung {self.bestellnummer}: "
            f"[{pos_str}] | "
            f"Datum: {self.bestelldatum} | "
            f"Betrag: {self.rechnungsbetrag:.2f} €"
        )

    def to_dict(self) -> dict:
        return {
            "bestellnummer": self.bestellnummer,
            "artikelliste": self.artikelliste,
            "bestelldatum": self.bestelldatum.isoformat(),
            "rechnungsbetrag": self.rechnungsbetrag
        }

    @staticmethod
    def from_dict(d: dict) -> "Bestellung":
        datum = datetime.fromisoformat(d["bestelldatum"]).date()
        # artikelliste hat bereits das richtige Format (Liste von Dicts)
        b = Bestellung(d["artikelliste"], d["rechnungsbetrag"], datum)
        b.bestellnummer = d["bestellnummer"]
        return b


class Kunde:
    def __init__(self, typ: str, nachname: str, vorname: str, geburtsdatum: date):
        self.typ = typ
        self.nachname = nachname
        self.vorname = vorname
        self._kundennummer = str(uuid.uuid4())
        self.bestellungen: List[Bestellung] = []
        self.geburtsdatum = geburtsdatum

    @property
    def kundennummer(self) -> str:
        return self._kundennummer

    def add_bestellung(self, bestellung: Bestellung):
        self.bestellungen.append(bestellung)

    def __str__(self):
        return (
            f"{self.vorname} {self.nachname} "
            f"(Geb.: {self.geburtsdatum}) "
            f"KNR: {self.kundennummer} "
            f"Typ: {self.typ}"
        )

    def to_dict(self) -> dict:
        return {
            "typ": self.typ,
            "nachname": self.nachname,
            "vorname": self.vorname,
            "geburtsdatum": self.geburtsdatum.isoformat(),
            "kundennummer": self.kundennummer,
            "bestellungen": [b.to_dict() for b in self.bestellungen]
        }

    @staticmethod
    def from_dict(d: dict) -> "Kunde":
        geb = datetime.fromisoformat(d["geburtsdatum"]).date()
        typ = d.get("typ", "normal")
        k = Kunde(typ, d["nachname"], d["vorname"], geb)
        k._kundennummer = d["kundennummer"]
        for bd in d.get("bestellungen", []):
            k.bestellungen.append(Bestellung.from_dict(bd))
        return k


class Premiumkunde(Kunde):
    def add_bestellung(self, bestellung: Bestellung):
        bestellung.rechnungsbetrag = round(bestellung.rechnungsbetrag * 0.95, 2)
        super().add_bestellung(bestellung)

    @staticmethod
    def from_dict(d: dict) -> "Premiumkunde":
        geb = datetime.fromisoformat(d["geburtsdatum"]).date()
        k = Premiumkunde("premium", d["nachname"], d["vorname"], geb)
        k._kundennummer = d["kundennummer"]
        for bd in d.get("bestellungen", []):
            k.bestellungen.append(Bestellung.from_dict(bd))
        return k


def parse_date(datum_str: str) -> date:
    return datetime.strptime(datum_str, "%Y-%m-%d").date()


def lade_kunden() -> List[Union[Kunde, Premiumkunde]]:
    if not os.path.exists(KUNDEN_DATEI):
        return []
    with open(KUNDEN_DATEI, "r", encoding="utf-8") as f:
        daten = json.load(f)
    kunden = []
    for e in daten:
        if e.get("typ") == "premium":
            kunden.append(Premiumkunde.from_dict(e))
        else:
            kunden.append(Kunde.from_dict(e))
    return kunden


def speichere_kunden(liste: List[Union[Kunde, Premiumkunde]]):
    with open(KUNDEN_DATEI, "w", encoding="utf-8") as f:
        json.dump([k.to_dict() for k in liste], f, ensure_ascii=False, indent=2)


def loesche_kunde(kundennummer: str, kunden_liste: List[Union[Kunde, Premiumkunde]]) -> bool:
    """Löscht einen Kunden aus der Liste und speichert die JSON."""
    for i, k in enumerate(kunden_liste):
        if k.kundennummer == kundennummer:
            kunden_liste.pop(i)
            speichere_kunden(kunden_liste)
            return True
    return False


# ---- Hilfsfunktionen für den Warenkorb ----

def finde_artikel(artikel_liste: List[Artikel], nr: str) -> Union[Artikel, None]:
    return next((a for a in artikel_liste if a.nummer == nr), None)


def zeige_warenkorb(cart: Dict[str, int], artikel_liste: List[Artikel]):
    if not cart:
        print("Warenkorb ist leer.")
        return
    print("Aktueller Warenkorb:")
    summe = 0.0
    for nr, menge in cart.items():
        art = finde_artikel(artikel_liste, nr)
        if not art:
            continue
        betrag = art.preis * menge
        summe += betrag
        print(f"  - {art.name} (Nr. {nr}) x {menge} = {betrag:.2f} €")
    print(f"Zwischensumme: {summe:.2f} €")


# ---- Hauptprogramm ----

def main():
    # Daten aus beiden JSON-Dateien einlesen
    artikel_liste = lade_artikel()
    kunden_liste  = lade_kunden()
    kunden_dict   = {k.kundennummer: k for k in kunden_liste}

    while True:
        print("\n--- Kundenverwaltung ---")
        print("1. Neuen Kunden anlegen")
        print("2. Warenkorb ")
        print("3. Kundenliste anzeigen")
        print("4. Kunde löschen")
        print("5. Artikelliste anzeigen")
        print("6. Beenden")
        wahl = input("Auswahl: ").strip()

        if wahl == "1":
            typ_in = input("Normalkunde (n) oder Premiumkunde (p)? ").lower().strip()
            nachn = input("Nachname: ").strip()
            vorgn = input("Vorname: ").strip()
            geb   = parse_date(input("Geburtsdatum (YYYY-MM-DD): ").strip())

            if typ_in == "p":
                k = Premiumkunde("premium", nachn, vorgn, geb)
            else:
                k = Kunde("normal", nachn, vorgn, geb)

            kunden_liste.append(k)
            kunden_dict[k.kundennummer] = k
            speichere_kunden(kunden_liste)
            print(f"Kunde angelegt: {k}")

        elif wahl == "2":
            knr = input("Kundennummer: ").strip()
            k   = kunden_dict.get(knr)
            if not k:
                print("Kunde nicht gefunden.")
                continue

            # aktuellen Lagerbestand samt Preisen anzeigen
            vorrat_anzeigen(artikel_liste)

            # Warenkorb: nummer -> menge
            cart: Dict[str, int] = {}

            print("\nEingabe-Hinweise:")
            print("  + NR MENGE   : Artikel hinzufügen/erhöhen (z. B. + A100 3)")
            print("  - NR MENGE   : Menge reduzieren (z. B. - A100 1)")
            print("  del NR       : Artikel komplett entfernen (z. B. del A100)")
            print("  show         : Warenkorb anzeigen")
            print("  ok           : Bestellung speichern")
            print("  abbruch      : Vorgang abbrechen")

            while True:
                cmd = input("> ").strip()
                if not cmd:
                    continue

                parts = cmd.split()
                action = parts[0].lower()

                if action == "show":
                    zeige_warenkorb(cart, artikel_liste)
                    continue

                if action == "abbruch":
                    print("Bestellvorgang abgebrochen.")
                    cart.clear()
                    break

                if action == "ok":
                    if not cart:
                        print("Warenkorb ist leer.")
                        continue
                    # Bestand prüfen (final)
                    fehler = False
                    for nr, menge in cart.items():
                        art = finde_artikel(artikel_liste, nr)
                        if not art:
                            print(f"Artikel {nr} existiert nicht mehr.")
                            fehler = True
                            continue
                        if art.bestand < menge:
                            print(f"Zu wenig Bestand für {nr}. Verfügbar: {art.bestand}, gewünscht: {menge}.")
                            fehler = True
                    if fehler:
                        print("Bitte Warenkorb anpassen.")
                        continue

                    # Gesamtsumme berechnen
                    gesamtbetrag = 0.0
                    for nr, menge in cart.items():
                        art = finde_artikel(artikel_liste, nr)
                        gesamtbetrag += art.preis * menge

                    # Bestellung anlegen
                    positionen = [{"nummer": nr, "menge": menge} for nr, menge in cart.items()]
                    b = Bestellung(positionen, gesamtbetrag)
                    k.add_bestellung(b)

                    # Bestand abbuchen
                    for nr, menge in cart.items():
                        art = finde_artikel(artikel_liste, nr)
                        art.bestand -= menge

                    speichere_artikel(artikel_liste)
                    speichere_kunden(kunden_liste)

                    print("Bestellung gespeichert:")
                    print(b)
                    break  # raus aus Bestellvorgang

                # Bearbeitungsbefehle
                if action in ["+", "-"]:
                    if len(parts) != 3:
                        print("Format: + NR MENGE oder - NR MENGE")
                        continue
                    nr = parts[1]
                    try:
                        menge = int(parts[2])
                        if menge <= 0:
                            print("Menge muss > 0 sein.")
                            continue
                    except ValueError:
                        print("Menge muss eine Zahl sein.")
                        continue

                    art = finde_artikel(artikel_liste, nr)
                    if not art:
                        print(f"Artikel {nr} nicht gefunden.")
                        continue

                    aktuelle_menge = cart.get(nr, 0)
                    if action == "+":
                        # prüfen gegen vorhandenen Bestand
                        if menge + aktuelle_menge > art.bestand:
                            print(f"Nicht genug Bestand. Verfügbar: {art.bestand}, im Warenkorb: {aktuelle_menge}.")
                            continue
                        cart[nr] = aktuelle_menge + menge
                        print(f"Hinzugefügt: {nr} x {menge} (jetzt {cart[nr]} im Warenkorb).")
                    else:  # action == "-"
                        if menge >= aktuelle_menge:
                            cart.pop(nr, None)
                            print(f"Artikel {nr} aus Warenkorb entfernt.")
                        else:
                            cart[nr] = aktuelle_menge - menge
                            print(f"Reduziert: {nr} um {menge} (jetzt {cart[nr]} im Warenkorb).")
                    continue

                if action == "del":
                    if len(parts) != 2:
                        print("Format: del NR")
                        continue
                    nr = parts[1]
                    if nr in cart:
                        cart.pop(nr)
                        print(f"Artikel {nr} entfernt.")
                    else:
                        print(f"Artikel {nr} ist nicht im Warenkorb.")
                    continue

                print("Unbekannter Befehl. Nutze: +, -, del, show, ok, abbruch.")

        elif wahl == "3":
            if not kunden_liste:
                print("Keine Kunden vorhanden.")
            for kunde in kunden_liste:
                print(kunde)

        elif wahl == "4":
            knr = input("Zu löschende Kundennummer: ").strip()
            if loesche_kunde(knr, kunden_liste):
                kunden_dict.pop(knr, None)
                print("Kunde gelöscht:", knr)
            else:
                print("Kunde nicht gefunden:", knr)

        elif wahl == "5":
            vorrat_anzeigen(artikel_liste)

        elif wahl == "6":
            print("Programm beendet.")
            speichere_artikel(artikel_liste)
            speichere_kunden(kunden_liste)
            break

        else:
            print("Ungültige Auswahl. Bitte erneut versuchen.")


if __name__ == "__main__":
    main()