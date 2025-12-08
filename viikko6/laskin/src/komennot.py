class Summa:
    def __init__(self, logiikka, lue_syote):
        self._logiikka = logiikka
        self._lue_syote = lue_syote
        self._edellinen = 0

    def suorita(self):
        self._edellinen = self._logiikka.arvo()
        print(self._edellinen)
        self._logiikka.plus(self._lue_syote())

    def kumoa(self):
        self._logiikka.aseta_arvo(self._edellinen)

class Erotus:
    def __init__(self, logiikka, lue_syote):
        self._logiikka = logiikka
        self._lue_syote = lue_syote
        self._edellinen = 0

    def suorita(self):
        self._edellinen = self._logiikka.arvo()
        print(self._edellinen)
        self._logiikka.miinus(self._lue_syote())

    def kumoa(self):
        self._logiikka.aseta_arvo(self._edellinen)

class Nollaus:
    def __init__(self, logiikka, lue_syote):
        self._logiikka = logiikka
        self._edellinen = 0

    def suorita(self):
        self._edellinen = self._logiikka.arvo()
        print(self._edellinen)
        self._logiikka.nollaa()

    def kumoa(self):
        self._logiikka.aseta_arvo(self._edellinen)

class Kumoa:
    def __init__(self, logiikka, lue_syote):
        self._edellinen_komento = None

    def aseta_komento(self, komento):
        self._edellinen_komento = komento

    def suorita(self):
        if self._edellinen_komento:
            self._edellinen_komento.kumoa()