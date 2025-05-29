import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Auto(ABC):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij

    @abstractmethod
    def __str__(self):
        pass

class Szemelyauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, utasok_szama: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self.utasok_szama = utasok_szama

    def __str__(self):
        return f"Személyautó: {self.rendszam}, {self.tipus}, {self.berleti_dij} Ft/nap, {self.utasok_szama} fő"

class Teherauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, teherbiras: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self.teherbiras = teherbiras

    def __str__(self):
        return f"Teherautó: {self.rendszam}, {self.tipus}, {self.berleti_dij} Ft/nap, {self.teherbiras} kg"    

class Berles:
    def __init__(self, auto: Auto, mettol: str, meddig: str):
        self.auto = auto
        self.mettol = mettol  # pl. "2025-06-01"
        self.meddig = meddig  # pl. "2025-06-05"

    def __str__(self):
        m1 = datetime.strptime(self.mettol, "%Y-%m-%d")
        m2 = datetime.strptime(self.meddig, "%Y-%m-%d")
        napok = (m2 - m1).days + 1
        osszeg = napok * self.auto.berleti_dij
        return f"{self.auto.rendszam} ({self.auto.tipus}) bérlés: {self.mettol} - {self.meddig}, napok: {napok}, ár: {osszeg} Ft"

def datumok_atfednek(m1, m2, e1, e2):
    return not (e1 < m2 or e2 < m1)

class Autokolcsonzo:
    def __init__(self, nev: str):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def hozzaad_auto(self, auto: Auto):
        self.autok.append(auto)

    def berel_auto(self, rendszam: str, mettol: str, meddig: str):
        m1 = datetime.strptime(mettol, "%Y-%m-%d")
        e1 = datetime.strptime(meddig, "%Y-%m-%d")
        if e1 < m1 or m1 < datetime.now():
            print("Hibás időintervallum.")
            return None
        
        for berles in self.berlesek:
            if berles.auto.rendszam == rendszam:
                m2 = datetime.strptime(berles.mettol, "%Y-%m-%d")
                e2 = datetime.strptime(berles.meddig, "%Y-%m-%d")
                if datumok_atfednek(m1, m2, e1, e2):
                    print("Ez az autó már foglalt ebben az időszakban.")
                    return None

        for auto in self.autok:
            if auto.rendszam == rendszam:
                uj_berles = Berles(auto, mettol, meddig)
                self.berlesek.append(uj_berles)
                print(f"Sikeres bérlés: {uj_berles}")
                return uj_berles
        print("Nincs ilyen rendszámú autó.")
        return None

    def lemondas(self, rendszam: str, mettol: str):
        for berles in self.berlesek:
            if berles.auto.rendszam == rendszam and berles.mettol == mettol:
                self.berlesek.remove(berles)
                print(f"Bérlés lemondva: {rendszam} ({mettol} - {berles.meddig})")
                return True
        print("Nincs ilyen bérlés.")
        return False

    def listaz_berlesek(self):
        if not self.berlesek:
            print("Nincs aktuális bérlés.")
        else:
            for berles in self.berlesek:
                print(berles)


    def __init__(self, nev: str):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def hozzaad_auto(self, auto: Auto):
        self.autok.append(auto)

#    def lemondas(self, rendszam: str, datum: str):
#        for berles in self.berlesek:
#            if berles.auto.rendszam == rendszam and berles.datum == datum:
#                self.berlesek.remove(berles)
#                print(f"Bérlés lemondva: {rendszam} ({datum})")
#                return True
#        print("Nincs ilyen bérlés.")
#        return False

    def listaz_berlesek(self):
        if not self.berlesek:
            print("Nincs aktuális bérlés.")
        else:
            for berles in self.berlesek:
                print(berles)

class KolcsonzoGUI:
    def __init__(self, root, kolcsonzo):
        self.root = root
        self.kolcsonzo = kolcsonzo
        self.root.title("Autókölcsönző Rendszer")

        # Gombok
        tk.Button(root, text="Autó bérlése", command=self.auto_berlese, width=30).pack(pady=3)
        tk.Button(root, text="Bérlés lemondása", command=self.berles_lemondasa, width=30).pack(pady=3)
        tk.Button(root, text="Bérlések listázása", command=self.berlesek_listazasa, width=30).pack(pady=3)
        tk.Button(root, text="Autók listázása", command=self.autok_listazasa, width=30).pack(pady=3)
        tk.Button(root, text="Új autó hozzáadása", command=self.uj_auto_hozzaadasa, width=30).pack(pady=3)

        self.kimenet = ScrolledText(root, width=60, height=20)
        self.kimenet.pack(pady=10)

    
    def auto_berlese(self):
        rendszam = simpledialog.askstring("Bérlés", "Add meg az autó rendszámát:")
        mettol = simpledialog.askstring("Bérlés", "Add meg a bérlés kezdetét (ÉÉÉÉ-HH-NN):")
        meddig = simpledialog.askstring("Bérlés", "Add meg a bérlés végét (ÉÉÉÉ-HH-NN):")
        if rendszam and mettol and meddig:
            eredmeny = self.kolcsonzo.berel_auto(rendszam, mettol, meddig)
            if eredmeny:
                messagebox.showinfo("Sikeres bérlés", str(eredmeny))
            else:
                messagebox.showwarning("Hiba", "Bérlés sikertelen. Ellenőrizd az adatokat.")

    
    def berles_lemondasa(self):
        rendszam = simpledialog.askstring("Lemondás", "Add meg a rendszámot:")
        mettol = simpledialog.askstring("Lemondás", "Add meg a bérlés kezdetét (ÉÉÉÉ-HH-NN):")
 #       meddig = simpledialog.askstring("Lemondás", "Add meg a bérlés végét (ÉÉÉÉ-HH-NN):")
        if rendszam and mettol:
            siker = self.kolcsonzo.lemondas(rendszam, mettol)
            if siker:
                messagebox.showinfo("Siker", "Bérlés lemondva.")
            else:
                messagebox.showwarning("Hiba", "Nem található ilyen bérlés.")

    
    def berlesek_listazasa(self):
        self.kimenet.delete(1.0, tk.END)
        if not self.kolcsonzo.berlesek:
            self.kimenet.insert(tk.END, "Nincs aktuális bérlés.")
        else:
            self.kimenet.insert(tk.END, "Foglalt időszakok:\n\n")
            for berles in self.kolcsonzo.berlesek:
                self.kimenet.insert(tk.END, f"{berles.auto.rendszam}: {berles.mettol} - {berles.meddig}\n")
            self.kimenet.insert(tk.END, "\n--- Egyszerű naptárnézet ---\n\n")
            foglalasok = {}
            for berles in self.kolcsonzo.berlesek:
                d1 = datetime.strptime(berles.mettol, "%Y-%m-%d")
                d2 = datetime.strptime(berles.meddig, "%Y-%m-%d")
                while d1 <= d2:
                    foglalasok[d1.strftime("%Y-%m-%d")] = foglalasok.get(d1.strftime("%Y-%m-%d"), []) + [berles.auto.rendszam]
                    d1 += timedelta(days=1)
            napok = sorted(foglalasok.keys())
            for nap in napok:
                autok = ", ".join(foglalasok[nap])
                self.kimenet.insert(tk.END, f"{nap}: {autok}\n")

    def autok_listazasa(self):
        self.kimenet.delete(1.0, tk.END)
        if not self.kolcsonzo.autok:
            self.kimenet.insert(tk.END, "Nincs elérhető autó.\n")
        else:
            for auto in self.kolcsonzo.autok:
                self.kimenet.insert(tk.END, str(auto) + "\n")

    def uj_auto_hozzaadasa(self):
        tipus_valasz = simpledialog.askstring("Autó típusa", "Személyautó vagy Teherautó? (s/t)")
        if tipus_valasz not in ("s", "t"):
            messagebox.showwarning("Hiba", "Csak 's' vagy 't' válasz lehetséges.")
            return

        rendszam = simpledialog.askstring("Rendszám", "Add meg a rendszámot:")
        tipus = simpledialog.askstring("Típus", "Add meg az autó típusát (pl. Toyota):")
        dij = simpledialog.askinteger("Díj", "Add meg a bérleti díjat (Ft/nap):")

        if tipus_valasz == "s":
            utasok = simpledialog.askinteger("Utasok száma", "Add meg az utasok számát:")
            uj_auto = Szemelyauto(rendszam, tipus, dij, utasok)
        else:
            teherbiras = simpledialog.askinteger("Teherbírás", "Add meg a teherbírást (kg):")
            uj_auto = Teherauto(rendszam, tipus, dij, teherbiras)

        self.kolcsonzo.hozzaad_auto(uj_auto)
        messagebox.showinfo("Siker", "Autó hozzáadva.")

def inditas():
    kolcsonzo = Autokolcsonzo("BestAutoRent")

    kolcsonzo.hozzaad_auto(Szemelyauto("ABC-123", "Toyota Corolla", 10000, 5))
    kolcsonzo.hozzaad_auto(Teherauto("DEF-456", "Ford Transit", 15000, 1200))
    kolcsonzo.hozzaad_auto(Szemelyauto("GHI-789", "Suzuki Swift", 8000, 4))

    kolcsonzo.berel_auto("ABC-123", "2025-07-20","2025-07-20")
    kolcsonzo.berel_auto("DEF-456", "2025-07-21","2025-07-26")
    kolcsonzo.berel_auto("GHI-789", "2025-07-22","2025-07-22")
    kolcsonzo.berel_auto("ABC-123", "2025-07-23","2025-07-28")

    return kolcsonzo

# Főprogram
if __name__ == "__main__":
    root = tk.Tk()
    app = KolcsonzoGUI(root, inditas())
    root.mainloop()
