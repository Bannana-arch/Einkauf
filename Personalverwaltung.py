personen_liste = []

def start():
    while True:
        print("Personalverwaltung")
        print("1. Neue Person erstellen")
        print("2. Alle Personen anzeigen")
        print("3. Beenden")

        auswahl = input("Bitte wählen (1-3): ")

        if auswahl == "1":
                neue_person_erstellen()
        elif auswahl == "2":
                personen_anzeigen()
        elif auswahl == "3":
            print("Programm beendet. ")
            break
        else:
            print("Ungültige Eingabe. Bitte erneut versuchen.\n")

def neue_person_erstellen():
    print("\n--- Neue Person erstellen ---")
    vorname = input("Vorname: ")
    nachname = input("Nachname: ")
    geburtsdatum = input("Geburtsdatum (TT.MM.JJJJ): ")
    adresse = input("Wohnadresse: ")
    email = input("E-Mail-Adresse: ")

    person = {
        "Vorname": vorname,
        "Nachname": nachname,
        "Geburtsdatum": geburtsdatum,
        "Adresse": adresse,
        "E-Mail": email
    }

    personen_liste.append(person)
    print("Person erfolgreich hinzugefügt!\n")


def personen_anzeigen():
    print("\n--- Alle gespeicherten Personen ---")
    if not personen_liste:
        print("Keine Personen gespeichert.\n")
        return

    for i, person in enumerate(personen_liste, start=1):
        print(f"Person {i}:")
        print(f"  Name: {person['Vorname']} {person['Nachname']}")
        print(f"  Geburtsdatum: {person['Geburtsdatum']}")
        print(f"  Adresse: {person['Adresse']}")
        print(f"  E-Mail: {person['E-Mail']}")
        print("-" * 30)
    print()

if __name__ == "__main__":
    start()

