from flask import Flask, render_template, request, session, redirect, url_for
from tehdasfunktio import luo_peli
from tuomari import Tuomari
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Säilytä peli-instanssit palvelimen muistissa session ID:n perusteella
peli_instanssit = {}

# Web-adapteri pelilogiikalle - ei sisällä pelilogiikkaa itsessään
class WebKiviPaperiSakset:
    VOITTO_RAJA = 3
    
    def __init__(self, pelityyppi):
        self.peli = luo_peli(pelityyppi)
        self.tuomari = Tuomari()
        self.pelityyppi = pelityyppi
        self.odottaa_toista_pelaajaa = False  # Ihminen vs ihminen -tilassa
        self.ensimmaisen_siirto = None
        
    def pelaa_kierros(self, pelaajan_siirto, toisen_pelaajan_siirto=None):
        if not self._onko_ok_siirto(pelaajan_siirto):
            return None
        
        # Ihminen vs ihminen -tila vaatii molemmat siirrot
        if self.pelityyppi == 'a':
            if toisen_pelaajan_siirto is None:
                # Tallennetaan ensimmäisen siirto ja odotetaan toista
                self.odottaa_toista_pelaajaa = True
                self.ensimmaisen_siirto = pelaajan_siirto
                return {
                    'odottaa_toista': True,
                    'pelaajan_siirto': pelaajan_siirto
                }
            else:
                # Molemmat siirrot saatu
                tokan_siirto = toisen_pelaajan_siirto
                self.odottaa_toista_pelaajaa = False
                self.ensimmaisen_siirto = None
        else:
            # Tekoäly-tilat
            tokan_siirto = self.peli._toisen_siirto(pelaajan_siirto)
        
        self.tuomari.kirjaa_siirto(pelaajan_siirto, tokan_siirto)
        
        # Määritä kierroksen voittaja (ennen pelin päätymisen tarkistusta)
        kierroksen_voittaja = self._paata_kierroksen_voittaja(pelaajan_siirto, tokan_siirto)
        
        # Tarkista onko peli voitettu
        peli_voitettu = False
        voittaja = None
        if self.tuomari.ekan_pisteet >= self.VOITTO_RAJA:
            peli_voitettu = True
            voittaja = 'pelaaja1'
        elif self.tuomari.tokan_pisteet >= self.VOITTO_RAJA:
            peli_voitettu = True
            voittaja = 'pelaaja2'
        
        return {
            'pelaajan_siirto': pelaajan_siirto,
            'vastustajan_siirto': tokan_siirto,
            'ekan_pisteet': self.tuomari.ekan_pisteet,
            'tokan_pisteet': self.tuomari.tokan_pisteet,
            'tasapelit': self.tuomari.tasapelit,
            'kierroksen_voittaja': kierroksen_voittaja,
            'peli_voitettu': peli_voitettu,
            'voittaja': voittaja
        }
    
    def _paata_kierroksen_voittaja(self, eka_siirto, toka_siirto):
        """Määrittää kuka voitti tämän kierroksen"""
        if eka_siirto == toka_siirto:
            return 'tasapeli'
        elif eka_siirto == "k" and toka_siirto == "s":
            return 'pelaaja1'
        elif eka_siirto == "s" and toka_siirto == "p":
            return 'pelaaja1'
        elif eka_siirto == "p" and toka_siirto == "k":
            return 'pelaaja1'
        else:
            return 'pelaaja2'
    
    def _onko_ok_siirto(self, siirto):
        return siirto in ['k', 'p', 's']

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/valitse', methods=['POST'])
def valitse_peli():
    pelityyppi = request.form.get('pelityyppi')
    if pelityyppi not in ['a', 'b', 'c']:
        return redirect(url_for('index'))
    
    # Luo uniikki session ID jos ei ole vielä
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)
    
    session['pelityyppi'] = pelityyppi
    session['peli_aktiivinen'] = True
    
    # Tallenna pelimuodon nimi
    pelimuodot = {
        'a': 'Ihminen vs Ihminen',
        'b': 'Ihminen vs Tekoäly',
        'c': 'Ihminen vs Parannettu Tekoäly'
    }
    session['pelimuoto'] = pelimuodot.get(pelityyppi, 'Tuntematon')
    
    # Alusta peli ja tallenna se muistiin
    session_id = session['session_id']
    peli_instanssit[session_id] = WebKiviPaperiSakset(pelityyppi)
    
    return redirect(url_for('pelaa'))

@app.route('/pelaa')
def pelaa():
    if not session.get('peli_aktiivinen'):
        return redirect(url_for('index'))
    
    session_id = session.get('session_id')
    if session_id not in peli_instanssit:
        return redirect(url_for('index'))
    
    web_peli = peli_instanssit[session_id]
    
    return render_template('pelaa.html',
                         pelimuoto=session.get('pelimuoto'),
                         pelityyppi=web_peli.pelityyppi,
                         ekan_pisteet=web_peli.tuomari.ekan_pisteet,
                         tokan_pisteet=web_peli.tuomari.tokan_pisteet,
                         tasapelit=web_peli.tuomari.tasapelit)

@app.route('/siirto', methods=['POST'])
def tee_siirto():
    if not session.get('peli_aktiivinen'):
        return redirect(url_for('index'))
    
    session_id = session.get('session_id')
    if session_id not in peli_instanssit:
        return redirect(url_for('index'))
    
    siirto = request.form.get('siirto')
    toisen_siirto = request.form.get('toisen_siirto')
    web_peli = peli_instanssit[session_id]
    
    # Ihminen vs ihminen -tila
    if web_peli.pelityyppi == 'a':
        tulos = web_peli.pelaa_kierros(siirto, toisen_siirto)
        
        # Jos odottaa toisen pelaajan siirtoa
        if tulos and tulos.get('odottaa_toista'):
            return render_template('pelaa.html',
                                 pelimuoto=session.get('pelimuoto'),
                                 ekan_pisteet=web_peli.tuomari.ekan_pisteet,
                                 tokan_pisteet=web_peli.tuomari.tokan_pisteet,
                                 tasapelit=web_peli.tuomari.tasapelit,
                                 odottaa_toista_pelaajaa=True,
                                 ensimmaisen_siirto=tulos['pelaajan_siirto'])
    else:
        # Tekoäly-pelit
        tulos = web_peli.pelaa_kierros(siirto)
    
    if tulos is None:
        return render_template('pelaa.html',
                             pelimuoto=session.get('pelimuoto'),
                             pelityyppi=web_peli.pelityyppi,
                             ekan_pisteet=web_peli.tuomari.ekan_pisteet,
                             tokan_pisteet=web_peli.tuomari.tokan_pisteet,
                             tasapelit=web_peli.tuomari.tasapelit,
                             virhe="Virheellinen siirto! Valitse k, p tai s")
    
    siirto_nimet = {'k': 'Kivi', 'p': 'Paperi', 's': 'Sakset'}
    
    if web_peli.pelityyppi == 'a':
        viesti = f"Pelaaja 1 valitsi: {siirto_nimet[tulos['pelaajan_siirto']]}, Pelaaja 2 valitsi: {siirto_nimet[tulos['vastustajan_siirto']]}"
    else:
        viesti = f"Sinä valitsit: {siirto_nimet[tulos['pelaajan_siirto']]}, Vastustaja valitsi: {siirto_nimet[tulos['vastustajan_siirto']]}"
    
    # Jos peli on voitettu, näytä voittaja
    if tulos['peli_voitettu']:
        if tulos['voittaja'] == 'pelaaja1':
            viesti = f"🎉 PELAAJA 1 VOITTI PELIN! {viesti}"
        else:
            viesti = f"🎉 PELAAJA 2 VOITTI PELIN! {viesti}"
    
    return render_template('pelaa.html',
                         pelimuoto=session.get('pelimuoto'),
                         pelityyppi=web_peli.pelityyppi,
                         ekan_pisteet=tulos['ekan_pisteet'],
                         tokan_pisteet=tulos['tokan_pisteet'],
                         tasapelit=tulos['tasapelit'],
                         viesti=viesti,
                         kierroksen_voittaja=tulos['kierroksen_voittaja'],
                         pelaajan_siirto=tulos['pelaajan_siirto'],
                         vastustajan_siirto=tulos['vastustajan_siirto'],
                         peli_voitettu=tulos['peli_voitettu'],
                         voittaja=tulos['voittaja'])

@app.route('/lopeta')
def lopeta():
    session_id = session.get('session_id')
    if session_id and session_id in peli_instanssit:
        del peli_instanssit[session_id]
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
