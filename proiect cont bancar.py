import os
import time
import random
from colorama import Fore, Style, init
from bank import sold_curent

init(autoreset=True)

G  = Fore.GREEN
Y  = Fore.YELLOW
C  = Fore.CYAN
R  = Fore.RED
W  = Fore.WHITE
M  = Fore.MAGENTA
DIM = Style.DIM
B   = Style.BRIGHT
RST = Style.RESET_ALL

tranzactii = []
undo_list  = []


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def type_print(text, delay=0.03, culoare=G):
    for ch in text:
        print(culoare + ch, end="", flush=True)
        time.sleep(delay)
    print()


def bara_incarcare(label="Initializare", culoare=G, pasi=30, delay=0.04):
    print(culoare + f"\n  {label}")
    print(culoare + "  [", end="", flush=True)
    for _ in range(pasi):
        time.sleep(delay)
        print(culoare + "█", end="", flush=True)
    print(culoare + "] DONE")


def loading():
    clear()
    bara_incarcare("Conectare la server...",   M, 20, 0.10)
    bara_incarcare("Verificare securitate...", R, 15, 0.10)
    bara_incarcare("Incarcare cont...",        C, 25, 0.10)
    time.sleep(0.3)
    type_print("\n  ✔  ACCES AUTORIZAT", delay=0.4, culoare=G)
    time.sleep(0.7)


def pauza():
    input(W + "\n  Apasa Enter pentru continuare...")


def mesaj_random():
    mesaje = [
        "💡 Fiecare leu conteaza.",
        "🔐 Crest Bank Terminal este securizat.",
        "📊 Urmareste-ti tranzactiile inteligent.",
        "💰 Un buget nu-ți limitează libertatea, un buget îți oferă libertate."
        ]
    print(Y + "\n  " + random.choice(mesaje))


def sold_curent():
    sold = 0
    for t in tranzactii:
        if t["tip"] == "intrare":
            sold += t["suma"]
        else:
            sold -= t["suma"]
    return sold


def citeste_zi():
    while True:
        try:
            zi = int(input(W + "  Ziua (1-31): "))
            if 1 <= zi <= 31:
                return zi
            print(R + "  Ziua trebuie sa fie intre 1 si 31.")
        except ValueError:
            print(R + "  Introdu un numar intreg.")


def citeste_suma():
    while True:
        try:
            suma = float(input(W + "  Suma: "))
            if suma > 0:
                return suma
            print(R + "  Suma trebuie sa fie pozitiva.")
        except ValueError:
            print(R + "  Introdu o suma valida.")


def citeste_tip():
    while True:
        tip = input(W + "  Tip (intrare/iesire): ").lower().strip()
        if tip in ["intrare", "iesire"]:
            return tip
        print(R + "  Tip invalid. Scrie intrare sau iesire.")


def afiseaza_tranzactii(lista=None):
    if lista is None:
        lista = tranzactii
    if not lista:
        print(R + "  ❌ Nu exista tranzactii.")
        return
    print(M + "\n  ╔════╦══════╦════════════╦══════════╗")
    print(M +   "  ║ Nr ║ Ziua ║    Suma    ║   Tip    ║")
    print(M +   "  ╠════╬══════╬════════════╬══════════╣")
    for i, t in enumerate(lista, 1):
        culoare = G if t["tip"] == "intrare" else R
        print(culoare + f"  ║ {i:<2} ║ {t['zi']:<4} ║ {t['suma']:<10.2f} ║ {t['tip']:<8} ║")
    print(M +   "  ╚════╩══════╩════════════╩══════════╝")


def adauga_tranzactie():
    undo_list.append([t.copy() for t in tranzactii])
    print(C + "\n  >> TRANZACTIE NOUA")
    zi   = citeste_zi()
    suma = citeste_suma()
    tip  = citeste_tip()
    tranzactii.append({"zi": zi, "suma": suma, "tip": tip})
    type_print("  ✔  Tranzactie inregistrata.", delay=0.03, culoare=G)


def actualizeaza_tranzactie():
    if not tranzactii:
        print(R + "  ❌ Nu ai nicio tranzactie.")
        return
    afiseaza_tranzactii()
    try:
        poz = int(input(W + "  Numarul tranzactiei de modificat: ")) - 1
        if not 0 <= poz < len(tranzactii):
            print(R + "  Pozitie invalida.")
            return
    except ValueError:
        print(R + "  Introdu un numar valid.")
        return
    undo_list.append([t.copy() for t in tranzactii])
    print(C + "\n  >> DATE NOI")
    tranzactii[poz]["zi"]   = citeste_zi()
    tranzactii[poz]["suma"] = citeste_suma()
    tranzactii[poz]["tip"]  = citeste_tip()
    type_print("  ✔  Tranzactie actualizata.", delay=0.03, culoare=G)


def sterge_dupa_zi():
    global tranzactii
    print(C + "\n  >> STERGE DUPA ZI")
    zi = citeste_zi()
    undo_list.append([t.copy() for t in tranzactii])
    inainte = len(tranzactii)
    tranzactii = [t for t in tranzactii if t["zi"] != zi]
    sterse = inainte - len(tranzactii)
    type_print(f"  ✔  {sterse} tranzactie(i) sterse din ziua {zi}.", delay=0.03, culoare=G)


def sterge_dupa_perioada():
    global tranzactii
    print(C + "\n  >> STERGE PERIOADA")
    print(W + "  Zi start:")
    zi1 = citeste_zi()
    print(W + "  Zi sfarsit:")
    zi2 = citeste_zi()
    if zi1 > zi2:
        zi1, zi2 = zi2, zi1
    undo_list.append([t.copy() for t in tranzactii])
    inainte = len(tranzactii)
    tranzactii = [t for t in tranzactii if not (zi1 <= t["zi"] <= zi2)]
    sterse = inainte - len(tranzactii)
    type_print(f"  ✔  {sterse} tranzactie(i) sterse din ziua {zi1} pana in {zi2}.", delay=0.03, culoare=G)


def sterge_dupa_tip():
    global tranzactii
    print(C + "\n  >> STERGE DUPA TIP")
    tip = citeste_tip()
    undo_list.append([t.copy() for t in tranzactii])
    inainte = len(tranzactii)
    tranzactii = [t for t in tranzactii if t["tip"] != tip]
    sterse = inainte - len(tranzactii)
    type_print(f"  ✔  {sterse} tranzactie(i) de tip '{tip}' sterse.", delay=0.03, culoare=G)


def cauta_suma_mai_mare():
    print(C + "\n  >> CAUTA DUPA SUMA")
    suma = citeste_suma()
    rezultat = [t for t in tranzactii if t["suma"] > suma]
    if not rezultat:
        print(R + f"  ❌ Nicio tranzactie cu suma mai mare decat {suma:.2f} lei.")
        return
    type_print(f"  {len(rezultat)} rezultat(e) gasite:", delay=0.02, culoare=Y)
    afiseaza_tranzactii(rezultat)


def cauta_inainte_zi_si_suma():
    print(C + "\n  >> CAUTA INAINTE DE ZI + SUMA")
    print(W + "  Inainte de ziua:")
    zi   = citeste_zi()
    print(W + "  Cu suma mai mare decat:")
    suma = citeste_suma()
    rezultat = [t for t in tranzactii if t["zi"] < zi and t["suma"] > suma]
    if not rezultat:
        print(R + "  ❌ Nicio tranzactie gasita.")
        return
    type_print(f"  {len(rezultat)} rezultat(e) gasite:", delay=0.02, culoare=Y)
    afiseaza_tranzactii(rezultat)


def cauta_dupa_tip():
    print(C + "\n  >> CAUTA DUPA TIP")
    tip = citeste_tip()
    rezultat = [t for t in tranzactii if t["tip"] == tip]
    if not rezultat:
        print(R + f"  ❌ Nicio tranzactie de tip '{tip}'.")
        return
    type_print(f"  {len(rezultat)} rezultat(e) gasite:", delay=0.02, culoare=Y)
    afiseaza_tranzactii(rezultat)


def suma_totala_tip():
    print(C + "\n  >> SUMA TOTALA PE TIP")
    tip   = citeste_tip()
    total = sum(t["suma"] for t in tranzactii if t["tip"] == tip)
    type_print(f"  💰 Suma totala {tip}: {total:.2f} lei", delay=0.03, culoare=Y)


def sold_la_zi():
    print(C + "\n  >> SOLD LA O ZI")
    zi   = citeste_zi()
    sold = 0
    for t in tranzactii:
        if t["zi"] <= zi:
            if t["tip"] == "intrare":
                sold += t["suma"]
            else:
                sold -= t["suma"]
    type_print(f"  💳 Sold la ziua {zi}: {sold:.2f} lei", delay=0.03, culoare=Y)


def tip_ordonat_suma():
    print(C + "\n  >> TIP ORDONAT DUPA SUMA")
    tip      = citeste_tip()
    rezultat = sorted([t for t in tranzactii if t["tip"] == tip], key=lambda x: x["suma"])
    if not rezultat:
        print(R + f"  ❌ Nicio tranzactie de tip '{tip}'.")
        return
    type_print(f"  {len(rezultat)} tranzactie(i) gasite:", delay=0.02, culoare=Y)
    afiseaza_tranzactii(rezultat)


def filtrare_tip():
    global tranzactii
    print(C + "\n  >> FILTRARE DUPA TIP")
    tip = citeste_tip()
    undo_list.append([t.copy() for t in tranzactii])
    inainte = len(tranzactii)
    tranzactii = [t for t in tranzactii if t["tip"] != tip]
    sterse = inainte - len(tranzactii)
    type_print(f"  ✔  {sterse} tranzactie(i) eliminate de tip '{tip}'.", delay=0.03, culoare=G)


def filtrare_suma_si_tip():
    global tranzactii
    print(C + "\n  >> FILTRARE DUPA SUMA SI TIP")
    print(W + "  Elimina tranzactiile cu suma mai mica decat:")
    suma = citeste_suma()
    tip  = citeste_tip()
    undo_list.append([t.copy() for t in tranzactii])
    inainte = len(tranzactii)
    tranzactii = [t for t in tranzactii if not (t["suma"] < suma and t["tip"] == tip)]
    sterse = inainte - len(tranzactii)
    type_print(f"  ✔  {sterse} tranzactie(i) eliminate.", delay=0.03, culoare=G)


def undo():
    global tranzactii
    if not undo_list:
        print(R + "  ❌ Nu exista operatii de anulat.")
        return
    tranzactii = undo_list.pop()
    type_print("  ✔  Ultima operatie anulata.", delay=0.03, culoare=G)


def login():
    clear()
    print(M + "\n    ╔══════════════════════════════════════════╗")
    print(M + "    ║         CREST BANK TERMINAL              ║")
    print(M + "    ║              -- LOGIN --                 ║")
    print(M + "    ╚══════════════════════════════════════════╝")

    utilizatori = {"admin": "1234", "user": "0000"}

    for _ in range(3):
        user = input(W + "\n  Utilizator: ").strip()
        parola = input(W + "  Parola: ").strip()

        if user in utilizatori and utilizatori[user] == parola:
            type_print(f"\n  ✔  Bun venit, {user}!", delay=0.05, culoare=G)
            time.sleep(0.8)
            return
        print(R + "  ❌ Date incorecte. Mai incearca.")

    print(R + "\n  ❌ Prea multe incercari. Iesire.")
    exit()


def meniu():
    while True:
        clear()
        mesaj_random()

        print(W + f"\n  💰 SOLD CURENT: {sold_curent():.2f} lei")
        print(W + f"  📌 TRANZACTII:  {len(tranzactii)}")

        print(M + "\n  ╔══════════════════════════════════════╗")
        print(M +   "  ║         CREST BANK TERMINAL v2.0     ║")
        print(M +   "  ╠══════════════════════════════════════╣")
        print(C +   "  ║  1. Adauga tranzactie                ║")
        print(C +   "  ║  2. Actualizeaza tranzactie          ║")
        print(C +   "  ║  3. Afiseaza toate tranzactiile      ║")
        print(Y +   "  ║  4. Sterge dupa zi                   ║")
        print(Y +   "  ║  5. Sterge dupa perioada             ║")
        print(Y +   "  ║  6. Sterge dupa tip                  ║")
        print(G +   "  ║  7. Cauta suma mai mare              ║")
        print(G +   "  ║  8. Cauta inainte de zi si suma      ║")
        print(G +   "  ║  9. Cauta dupa tip                   ║")
        print(C +   "  ║ 10. Suma totala pe tip               ║")
        print(C +   "  ║ 11. Sold la o zi                     ║")
        print(C +   "  ║ 12. Tip ordonat dupa suma            ║")
        print(R +   "  ║ 13. Filtreaza dupa tip               ║")
        print(R +   "  ║ 14. Filtreaza dupa suma si tip       ║")
        print(W +   "  ║ 15. Undo                             ║")
        print(W +   "  ║  0. Iesire                           ║")
        print(M +   "  ╚══════════════════════════════════════╝")

        opt = input(W + "\n  Optiunea ta: ")
        clear()

        if opt == "1":
            adauga_tranzactie()
        elif opt == "2":
            actualizeaza_tranzactie()
        elif opt == "3":
            afiseaza_tranzactii()
        elif opt == "4":
            sterge_dupa_zi()
        elif opt == "5":
            sterge_dupa_perioada()
        elif opt == "6":
            sterge_dupa_tip()
        elif opt == "7":
            cauta_suma_mai_mare()
        elif opt == "8":
            cauta_inainte_zi_si_suma()
        elif opt == "9":
            cauta_dupa_tip()
        elif opt == "10":
            suma_totala_tip()
        elif opt == "11":
            sold_la_zi()
        elif opt == "12":
            tip_ordonat_suma()
        elif opt == "13":
            filtrare_tip()
        elif opt == "14":
            filtrare_suma_si_tip()
        elif opt == "15":
            undo()
        elif opt == "0":
            print(G + "  La revedere!")
            break
        else:
            print(R + "  ❌ Optiune invalida.")

        pauza()


loading()
login()
meniu()