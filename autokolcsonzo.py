from abc import ABC, abstractmethod
from datetime import datetime

class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self._rendszam = rendszam
        self._tipus = tipus
        self._berleti_dij = berleti_dij

    @property
    def rendszam(self):
        return self._rendszam

    @property
    def tipus(self):
        return self._tipus

    @property
    def berleti_dij(self):
        return self._berleti_dij

class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, utasok_szama):
        super().__init__(rendszam, tipus, berleti_dij)
        self._utasok_szama = utasok_szama

class Teherauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, teherbiras_kg):
        super().__init__(rendszam, tipus, berleti_dij)
        self._teherbiras_kg = teherbiras_kg

class Berles:
    def __init__(self, auto, datum):
        self._auto = auto
        self._datum = datum

    @property
    def auto(self):
        return self._auto

    @property
    def datum(self):
        return self._datum

class Autokolcsonzo:
    def __init__(self, nev):
        self._nev = nev
        self._autok = []
        self._berlesek = []

    def auto_hozzaadas(self, auto):
        self._autok.append(auto)

    def berles(self, rendszam, datum_str):
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
            if datum < datetime.today().date():
                return "Hiba: A bérlés dátuma nem lehet a múltban!"
        except ValueError:
            return "Hiba: Érvénytelen dátum formátum! Használja a YYYY-MM-DD formátumot."

        keresett_auto = next((auto for auto in self._autok if auto.rendszam == rendszam), None)
        if not keresett_auto:
            return "Hiba: Nem létezik ilyen rendszámú autó a rendszerben."

        for b in self._berlesek:
            if b.auto.rendszam == rendszam and b.datum == datum:
                return "Hiba: Ez az autó ezen a napon már ki van bérelve."

        uj_berles = Berles(keresett_auto, datum)
        self._berlesek.append(uj_berles)
        return f"Sikeres bérlés! A fizetendő összeg: {keresett_auto.berleti_dij} Ft."

    def lemondas(self, rendszam, datum_str):
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
        except ValueError:
            return "Hiba: Érvénytelen dátum formátum!"

        for b in self._berlesek:
            if b.auto.rendszam == rendszam and b.datum == datum:
                self._berlesek.remove(b)
                return f"A {rendszam} rendszámú autó {datum_str} dátumra szóló bérlése sikeresen lemondva."
        
        return "Hiba: Nem található ilyen bérlés a rendszerben."

    def listazas(self):
        if not self._berlesek:
            return "Jelenleg nincsenek aktív bérlések."
        
        eredmeny = [f"--- {self._nev} Aktív Bérlései ---"]
        for b in self._berlesek:
            eredmeny.append(f"Dátum: {b.datum} | Autó: {b.auto.tipus} ({b.auto.rendszam}) | Ár: {b.auto.berleti_dij} Ft")
        return "\n".join(eredmeny)


def main():
    kolcsonzo = Autokolcsonzo("YouheY-Brumm Kölcsönző Kft.")
    
    kolcsonzo.auto_hozzaadas(Szemelyauto("AAA-111", "Suzuki Swift", 10000, 5))
    kolcsonzo.auto_hozzaadas(Szemelyauto("BBB-222", "Toyota Corolla", 15000, 5))
    kolcsonzo.auto_hozzaadas(Teherauto("CCC-333", "Ford Transit", 25000, 1500))


    kolcsonzo.berles("AAA-111", "2026-06-10")
    kolcsonzo.berles("AAA-111", "2026-06-11")
    kolcsonzo.berles("BBB-222", "2026-06-15")
    kolcsonzo.berles("CCC-333", "2026-06-20")

    while True:
        print("\n" + "="*30)
        print("    AUTÓKÖLCSÖNZŐ RENDSZER")
        print("="*30)
        print("1. Bérlések listázása")
        print("2. Autó bérlése")
        print("3. Bérlés lemondása")
        print("4. Kilépés")
        
        valasztas = input("\nVálasszon egy menüpontot (1-4): ")

        if valasztas == '1':
            print("\n" + kolcsonzo.listazas())
            
        elif valasztas == '2':
            print("\n--- Autó Bérlése ---")
            print("Elérhető autók: AAA-111 (Suzuki), BBB-222 (Toyota), CCC-333 (Ford)")
            rsz = input("Adja meg a rendszámot: ").upper()
            datum = input("Adja meg a dátumot (ÉÉÉÉ-HH-NN): ")
            eredmeny = kolcsonzo.berles(rsz, datum)
            print(eredmeny)
            
        elif valasztas == '3':
            print("\n--- Bérlés Lemondása ---")
            rsz = input("Adja meg a lemondani kívánt autó rendszámát: ").upper()
            datum = input("Adja meg a bérlés dátumát (ÉÉÉÉ-HH-NN): ")
            eredmeny = kolcsonzo.lemondas(rsz, datum)
            print(eredmeny)
            
        elif valasztas == '4':
            print("\nKilépés... Köszönjük, hogy minket választott!")
            break
            
        else:
            print("\nHiba: Érvénytelen választás. Kérem, 1 és 4 közötti számot adjon meg.")

if __name__ == "__main__":
    main()