import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
from abc import ABC, abstractmethod

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
    def __init__(self, auto: Auto, datum: str):
        self.auto = auto
        self.datum = datum  # egyszerűség kedvéért string (pl. "2025-05-20")

    def __str__(self):
        return f"{self.auto.rendszam} ({self.auto.tipus}) bérlés dátuma: {self.datum}, ár: {self.auto.berleti_dij} Ft"
    
class Autokolcsonzo:
    def __init__(self, nev: str):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def hozzaad_auto(self, auto: Auto):
        self.autok.append(auto)

    def berel_auto(self, rendszam: str, datum: str):
        for berles in self.berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                print("Ez az autó már ki van bérelve ezen a napon.")
                return None
        for auto in self.autok:
            if auto.rendszam == rendszam:
                uj_berles = Berles(auto, datum)
                self.berlesek.append(uj_berles)
                print(f"Sikeres bérlés: {uj_berles}")
                return uj_berles
        print("Nincs ilyen rendszámú autó.")
        return None

    def lemondas(self, rendszam: str, datum: str):
        for berles in self.berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                self.berlesek.remove(berles)
                print(f"Bérlés lemondva: {rendszam} ({datum})")
                return True
        print("Nincs ilyen bérlés.")
        return False

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
        datum = simpledialog.askstring("Bérlés", "Add meg a bérlés dátumát (ÉÉÉÉ-HH-NN):")
        if rendszam and datum:
            eredmeny = self.kolcsonzo.berel_auto(rendszam, datum)
            if eredmeny:
                messagebox.showinfo("Sikeres bérlés", str(eredmeny))
            else:
                messagebox.showwarning("Hiba", "Bérlés sikertelen. Lehet, hogy már foglalt az autó.")

    def berles_lemondasa(self):
        rendszam = simpledialog.askstring("Lemondás", "Add meg a rendszámot:")
        datum = simpledialog.askstring("Lemondás", "Add meg a bérlés dátumát (ÉÉÉÉ-HH-NN):")
        if rendszam and datum:
            siker = self.kolcsonzo.lemondas(rendszam, datum)
            if siker:
                messagebox.showinfo("Siker", "Bérlés lemondva.")
            else:
                messagebox.showwarning("Hiba", "Nem található ilyen bérlés.")

    def berlesek_listazasa(self):
        self.kimenet.delete(1.0, tk.END)
        if not self.kolcsonzo.berlesek:
            self.kimenet.insert(tk.END, "Nincs aktuális bérlés.\n")
        else:
            for berles in self.kolcsonzo.berlesek:
                self.kimenet.insert(tk.END, str(berles) + "\n")

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

# Indítófüggvény, az előző inditas() függvényre építve
def inditas():
    kolcsonzo = Autokolcsonzo("BestAutoRent")

    kolcsonzo.hozzaad_auto(Szemelyauto("ABC-123", "Toyota Corolla", 10000, 5))
    kolcsonzo.hozzaad_auto(Teherauto("DEF-456", "Ford Transit", 15000, 1200))
    kolcsonzo.hozzaad_auto(Szemelyauto("GHI-789", "Suzuki Swift", 8000, 4))

    kolcsonzo.berel_auto("ABC-123", "2025-05-20")
    kolcsonzo.berel_auto("DEF-456", "2025-05-21")
    kolcsonzo.berel_auto("GHI-789", "2025-05-22")
    kolcsonzo.berel_auto("ABC-123", "2025-05-23")

    return kolcsonzo

# Főprogram
if __name__ == "__main__":
    root = tk.Tk()
    app = KolcsonzoGUI(root, inditas())
    root.mainloop()
