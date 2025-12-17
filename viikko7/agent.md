## Päätyikö agentti toimivaan ratkaisuun?

Peli toista ihmistä vastaan ei toiminut ollenkaan. Peli tekoälyä vastaan ei käyttänyt mitään logiikkaa vaan vastasi joka kierroksella saman vastauksen. Tämä tapahtui myös parannettua tekoälyä vastaan. Copilot kuitenkin korjasi nämä kun pyysin ja lopputulos on mielestäni toimiva.

## Miten varmistuit, että ratkaisu toimii?

Kokeilin itse pelata kaikkia pelimuotoja.

## Oletko ihan varma, että ratkaisu toimii oikein?

Korjailujen jälkeen olen aika varma.

## Kuinka paljon jouduit antamaan agentille komentoja matkan varrella?

Agentti varmisti aina saako avata sovelluksen tai suorittaa testit. Kysyi myös varmistusta jos jotain piti ladata. Kuten aiemmin sanoin jouduin kysymään agenttia korjaamaan tekemäänsä koodia aika paljon.

## Kuinka hyvät agentit tekemät testit olivat?

Osittain ok, mutta esim ei testaa ollenkaan ihmisten välisiä pelejä (ne ei siis toiminut ollenkaan). Testaa vain että ihmisten välinen peli aukeaa, mutta ei ollenkaan inputteja. Myös testissä:

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

Sanotaan, että testaisi muka pelin loppumista viidellä voitolla, mutta sitä tämä ei ainakaan tee. Kun muutin tarvittavien voittojen määrää kolmeen niin tämä testi meni silti läpi.

## Onko agentin tekemä koodi ymmärrettävää?

Paljon on kommentteja, mitkä helpottavat koodin seuraamista. Pitkiä metodeja, jotka luulisi voivan pilkkoa pienemmiksi.

## Miten agentti on muuttanut edellisessä tehtässä tekemääsi koodia?

Ei mitenkään. Kaikki muutokset ovat tiedostossa app.py sekä kansioissa tests ja templates.

## Mitä uutta opit?

Tekoäly on kätevä työkalu, mutta se on parempi "apukuskin" roolissa. Nyt oli aika paljon virheitä, eikä agentti osannut tehdä kattavia testejä. Lisäksi on helpompi korjata ja ymmärtää koodia, minkä on itse tehnyt.