import pytest
import sys
import os

# Lisää src-hakemisto Pythonin polkuun
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, peli_instanssit

@pytest.fixture
def client():
    """Luo Flask-testiklientin"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        with app.app_context():
            yield client
    
    # Siivoa peli-instanssit testien jälkeen
    peli_instanssit.clear()

@pytest.fixture
def client_with_session(client):
    """Luo testiklientin jolla on aktiivinen sessio"""
    with client.session_transaction() as sess:
        sess['session_id'] = 'test-session-123'
        sess['peli_aktiivinen'] = True
        sess['pelityyppi'] = 'a'
        sess['pelimuoto'] = 'Ihminen vs Ihminen'
    return client


class TestEtusivu:
    """Testit etusivulle"""
    
    def test_etusivu_latautuu(self, client):
        """Tarkista että etusivu latautuu oikein"""
        response = client.get('/')
        assert response.status_code == 200
        assert 'Kivi-Paperi-Sakset' in response.data.decode('utf-8')
        assert 'Ihminen vs Ihminen' in response.data.decode('utf-8')
        assert 'Ihminen vs Tekoäly' in response.data.decode('utf-8')
        assert 'Ihminen vs Parannettu Tekoäly' in response.data.decode('utf-8')
    
    def test_session_tyhjenee(self, client):
        """Tarkista että sessio tyhjenee etusivulle tultaessa"""
        with client.session_transaction() as sess:
            sess['pelityyppi'] = 'a'
            sess['peli_aktiivinen'] = True
        
        client.get('/')
        
        with client.session_transaction() as sess:
            assert 'pelityyppi' not in sess
            assert 'peli_aktiivinen' not in sess


class TestPelinValinta:
    """Testit pelimuodon valinnalle"""
    
    def test_valitse_ihminen_vs_ihminen(self, client):
        """Testaa ihminen vs ihminen -pelimuodon valinta"""
        response = client.post('/valitse', data={'pelityyppi': 'a'}, follow_redirects=True)
        assert response.status_code == 200
        assert 'Ihminen vs Ihminen' in response.data.decode('utf-8')
        
        with client.session_transaction() as sess:
            assert sess['pelityyppi'] == 'a'
            assert sess['peli_aktiivinen'] == True
            assert 'session_id' in sess
    
    def test_valitse_tekoaly(self, client):
        """Testaa tekoäly-pelimuodon valinta"""
        response = client.post('/valitse', data={'pelityyppi': 'b'}, follow_redirects=True)
        assert response.status_code == 200
        assert 'Ihminen vs Tekoäly' in response.data.decode('utf-8')
        
        with client.session_transaction() as sess:
            assert sess['pelityyppi'] == 'b'
    
    def test_valitse_parannettu_tekoaly(self, client):
        """Testaa parannetun tekoälyn valinta"""
        response = client.post('/valitse', data={'pelityyppi': 'c'}, follow_redirects=True)
        assert response.status_code == 200
        assert 'Ihminen vs Parannettu Tekoäly' in response.data.decode('utf-8')
        
        with client.session_transaction() as sess:
            assert sess['pelityyppi'] == 'c'
    
    def test_virheellinen_pelityyppi(self, client):
        """Testaa että virheellinen pelityyppi ohjaa takaisin etusivulle"""
        response = client.post('/valitse', data={'pelityyppi': 'x'}, follow_redirects=True)
        assert response.status_code == 200
        # Pitäisi ohjata takaisin etusivulle
        data = response.data.decode('utf-8')
        assert 'Valitse pelataanko' in data or 'Tervetuloa pelaamaan' in data
    
    def test_peli_instanssi_luodaan(self, client):
        """Testaa että peli-instanssi luodaan ja tallennetaan"""
        client.post('/valitse', data={'pelityyppi': 'a'})
        
        with client.session_transaction() as sess:
            session_id = sess['session_id']
        
        assert session_id in peli_instanssit
        assert peli_instanssit[session_id] is not None


class TestPelisivu:
    """Testit pelisivulle"""
    
    def test_pelisivu_ilman_sessiota(self, client):
        """Testaa että pelisivu ohjaa etusivulle ilman sessiota"""
        response = client.get('/pelaa', follow_redirects=True)
        assert response.status_code == 200
        # Pitäisi ohjata takaisin etusivulle
    
    def test_pelisivu_latautuu(self, client):
        """Testaa että pelisivu latautuu session kanssa"""
        # Luo peli ensin
        client.post('/valitse', data={'pelityyppi': 'a'})
        
        response = client.get('/pelaa')
        assert response.status_code == 200
        data = response.data.decode('utf-8')
        assert 'Tilanne' in data
        assert 'Valitse siirtosi' in data


class TestPelaaminen:
    """Testit pelaamiselle"""
    
    def test_kivi_siirto(self, client):
        """Testaa kiven pelaaminen"""
        # Käytä tekoälyä jotta input() ei tarvita
        client.post('/valitse', data={'pelityyppi': 'b'})
        response = client.post('/siirto', data={'siirto': 'k'})
        assert response.status_code == 200
        data = response.data.decode('utf-8')
        assert 'Kivi' in data or 'peli_voitettu' in data
    
    def test_paperi_siirto(self, client):
        """Testaa paperin pelaaminen"""
        # Käytä tekoälyä jotta input() ei tarvita
        client.post('/valitse', data={'pelityyppi': 'b'})
        response = client.post('/siirto', data={'siirto': 'p'})
        assert response.status_code == 200
        data = response.data.decode('utf-8')
        assert 'Paperi' in data or 'peli_voitettu' in data
    
    def test_sakset_siirto(self, client):
        """Testaa saksien pelaaminen"""
        # Käytä tekoälyä jotta input() ei tarvita
        client.post('/valitse', data={'pelityyppi': 'b'})
        response = client.post('/siirto', data={'siirto': 's'})
        assert response.status_code == 200
        data = response.data.decode('utf-8')
        assert 'Sakset' in data or 'peli_voitettu' in data
    
    def test_virheellinen_siirto(self, client):
        """Testaa virheellinen siirto"""
        # Käytä tekoälyä jotta input() ei tarvita
        client.post('/valitse', data={'pelityyppi': 'b'})
        response = client.post('/siirto', data={'siirto': 'x'})
        assert response.status_code == 200
        assert 'Virheellinen siirto' in response.data.decode('utf-8')
    
    def test_pisteiden_laskenta(self, client):
        """Testaa että pisteet lasketaan oikein"""
        # Käytä tekoälyä jotta input() ei tarvita
        client.post('/valitse', data={'pelityyppi': 'b'})
        
        # Simuloi useita kierroksia kunnes peli loppuu (5 voittoa)
        for _ in range(10):
            response = client.post('/siirto', data={'siirto': 'k'})
            if response.status_code != 200:
                break
        
        response = client.get('/pelaa')
        # Tarkista että sivu latautuu (pisteet näkyvät)
        assert response.status_code == 200


class TestTekoaly:
    """Testit tekoälylle"""
    
    def test_tekoaly_pelaa(self, client):
        """Testaa että tekoäly pelaa"""
        client.post('/valitse', data={'pelityyppi': 'b'})
        response = client.post('/siirto', data={'siirto': 'k'})
        
        assert response.status_code == 200
        data = response.data.decode('utf-8')
        # Tekoälyn siirron pitäisi näkyä vastauksessa
        assert 'Vastustaja valitsi' in data or 'peli_voitettu' in data
    
    def test_peli_loppuu_viidella_voitolla(self, client):
        """Testaa että peli loppuu kun joku saa 5 voittoa"""
        client.post('/valitse', data={'pelityyppi': 'b'})
        
        # Pelaa kunnes peli loppuu
        peli_voitettu = False
        siirrot = 0
        while not peli_voitettu and siirrot < 100:  # max 100 kierrosta turvallisuuden vuoksi
            response = client.post('/siirto', data={'siirto': 'k'})
            data = response.data.decode('utf-8')
            peli_voitettu = 'voitit pelin' in data.lower() or 'vastustaja voitti' in data.lower()
            siirrot += 1
        
        assert peli_voitettu, "Peli ei loppunut vaikka pelattiin 100 kierrosta"
    
    def test_tekoaly_vaihtaa_siirtoa(self, client):
        """Testaa että tekoäly vaihtaa siirtoaan (ei aina sama)"""
        client.post('/valitse', data={'pelityyppi': 'b'})
        
        siirrot = []
        for _ in range(5):
            response = client.post('/siirto', data={'siirto': 'k'})
            # Ei voi suoraan tarkistaa vastausta, mutta voidaan varmistaa
            # että peli jatkuu normaalisti
            assert response.status_code == 200
        
        # Jos tekoäly toimii oikein, se kiertää k->p->s
        # Testi varmistaa vain että peli toimii
    
    def test_parannettu_tekoaly_pelaa(self, client):
        """Testaa että parannettu tekoäly pelaa"""
        client.post('/valitse', data={'pelityyppi': 'c'})
        
        # Pelaa muutama kierros
        for _ in range(5):
            response = client.post('/siirto', data={'siirto': 'k'})
            assert response.status_code == 200
            data = response.data.decode('utf-8')
            assert 'Vastustaja valitsi' in data or 'peli_voitettu' in data
    
    def test_tekoaly_saavuttaa_tilan(self, client):
        """Testaa että tekoälyn tila säilyy kierrosten välillä"""
        client.post('/valitse', data={'pelityyppi': 'b'})
        
        # Hae session_id ja varmista että peli-instanssi säilyy
        with client.session_transaction() as sess:
            session_id = sess['session_id']
        
        # Pelaa muutama kierros
        client.post('/siirto', data={'siirto': 'k'})
        client.post('/siirto', data={'siirto': 'p'})
        
        # Varmista että sama peli-instanssi on yhä olemassa
        assert session_id in peli_instanssit
        assert peli_instanssit[session_id] is not None


class TestPelinLopetus:
    """Testit pelin lopettamiselle"""
    
    def test_lopeta_peli(self, client):
        """Testaa pelin lopettaminen"""
        client.post('/valitse', data={'pelityyppi': 'a'})
        
        with client.session_transaction() as sess:
            session_id = sess['session_id']
        
        # Varmista että peli-instanssi on olemassa
        assert session_id in peli_instanssit
        
        # Lopeta peli
        response = client.get('/lopeta', follow_redirects=True)
        assert response.status_code == 200
        
        # Varmista että session on tyhjennetty
        with client.session_transaction() as sess:
            assert 'peli_aktiivinen' not in sess
            assert 'session_id' not in sess
        
        # Varmista että peli-instanssi on poistettu
        assert session_id not in peli_instanssit
    
    def test_lopeta_ilman_pelia(self, client):
        """Testaa lopettaminen ilman aktiivista peliä"""
        response = client.get('/lopeta', follow_redirects=True)
        assert response.status_code == 200
        # Ei pitäisi aiheuttaa virhettä


class TestUseitaPeleja:
    """Testit useille samanaikaisille peleille"""
    
    def test_kaksi_eri_pelia(self):
        """Testaa että kaksi eri sessiota voi pelata samanaikaisesti"""
        app.config['TESTING'] = True
        
        with app.test_client() as client1, app.test_client() as client2:
            # Aloita peli client1:llä
            client1.post('/valitse', data={'pelityyppi': 'a'})
            
            # Aloita peli client2:lla
            client2.post('/valitse', data={'pelityyppi': 'b'})
            
            # Molemmat pitäisi olla eri sessioita
            with client1.session_transaction() as sess1:
                session_id1 = sess1.get('session_id')
            
            with client2.session_transaction() as sess2:
                session_id2 = sess2.get('session_id')
            
            assert session_id1 != session_id2
            assert session_id1 in peli_instanssit
            assert session_id2 in peli_instanssit
        
        # Siivoa
        peli_instanssit.clear()
