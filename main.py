from bitcoinrpc.authproxy import AuthServiceProxy
import datetime


# Funkcija ispisa podataka bloka
def InformacijeOBlokuIspis(blok):
    vrijeme = datetime.datetime.fromtimestamp(blok['time'])
    print("---Informacije bloka---")
    print("Hash bloka:", blok['hash'])
    print("Visina bloka:", blok['height'])
    print("Težina bloka: ", blok['weight'])
    print("Broj potvrda bloka:", blok['confirmations'])
    print("Veličina bloka:", blok['size'], "bajtova")
    print("Verzija bloka:", blok['version'])
    print("Vrijeme bloka:", f"{vrijeme:%Y-%m-%d %H:%M:%S}")
    print("Poteškoće bloka:", blok['difficulty'])
    print("Korijen Merkle bloka:", blok['merkleroot'])
    print("Broj transakcija bloka:", blok['nTx'])
    print("ID transakcija:", blok['tx'])
    print("------\n")


# Funkcija ispisa podataka transakcije
def InformacijeOTransakcijiIspis(client, transakcija):
    vrijeme = datetime.datetime.fromtimestamp(transakcija['time'])
    ulazneTransakcije = transakcija['vin']
    izlazneTransakcije = transakcija['vout']
    ukupnaVrijednostOut = 0
    ukupnaVrijednostIn = 0
    provjera = 1
    print("---Informacije o transakciji---")
    print("Hash transakcije:", transakcija['hash'])
    print("Verzija:", transakcija['version'])
    print("Veličina:", transakcija['size'])
    print("Vrijeme:", vrijeme)
    print("Potvrđena:", transakcija['confirmations'])
    print()
    print("Ulazne transakcije:")
    for inTx in ulazneTransakcije:
        if 'txid' in inTx:
            print("ID transakcije:", inTx['txid'])
            outputIndex = inTx['vout']
            print("Index output:", inTx['vout'])
            tx = client.getrawtransaction(inTx['txid'], True)
            izlTx = tx['vout']
            for izl in izlTx:
                if izl['n'] == outputIndex:
                    ukupnaVrijednostIn = izl['value']
            print("Vrijednost ulaza:", ukupnaVrijednostIn)
        else:
            print("Coinbase transakcija")
            provjera = 0
        print()
    if not izlazneTransakcije:
        print("Nema izlaznih transakcija")
    else:
        print("Izlazne transakcije:")
        for outTx in izlazneTransakcije:
            script = outTx['scriptPubKey']
            ukupnaVrijednostOut += outTx['value']
            print("Vrijednost:", outTx['value'], "BTC")
            if 'addresses' in script:
                print("Adrese:", script['addresses'])
            print()
        print("Vrijednost izlaza:", ukupnaVrijednostOut)
        if provjera:
            print("Naknada transakcije: ", (ukupnaVrijednostIn - ukupnaVrijednostOut))
    print("------\n")


# Spajanje na server
print("---Spajanje na server---")
username = input("Unesite korisničko ime: ")
password = input("Unesite password: ")
hostname = input("Unesite hostname: ")
port = input("Unesite port: ")

url = "http://" + username + ":" + password + "@" + hostname + ":" + port
client = AuthServiceProxy(url)

flag = 1
while flag:
    # Ispis izbornika
    print("---Block Explorer---")
    print("---IZBORNIK---")
    print("Za pretragu po visini bloka - 1\nZa pretragu po transakciji IDa - 2\nZa pregled statistike bloka - 3\n"
          "Za dohvaćanje najboljeg bloka - 4\nZa informacije o blockchainu - 5\nZa pregled mempoola - 6\n"
          "Za informacije o mreži čvora - 7\nZa ispis poteškoće - 8\nPrekid - 0")
    odabir = int(input("Unos: "))
    if odabir == 1:

       # Unos visine bloka i dohvaćanje bloka getblockhash() funkcijom
        visinaBloka = int(input("Unesite visinu bloka koji želite pregledati: "))
        try:
            hashBloka = client.getblockhash(visinaBloka)

            blok = client.getblock(hashBloka)
            listaTransakcija = blok['tx']
            InformacijeOBlokuIspis(blok)
            for tx in listaTransakcija:
                rwTx = client.getrawtransaction(tx, True)
                InformacijeOTransakcijiIspis(client, rwTx)

        except:
            print("Pogrešan unos visine bloka")

    elif odabir == 2:
        # Unos IDa transakcije te dohvaćanje transakcije getrawtransactions funkcijom
        txId = input("Unesite txID transakcije koju želite dohvatiti: ")
        try:
            rawTransakcija = client.getrawtransaction(txId, True)
            InformacijeOTransakcijiIspis(client, rawTransakcija)

        except:
            print("Pogrešan unos IDa transakcije")

    elif odabir == 3:
        # Dohvaćanje statistike bloka getblockstat funkcijom te ispis dohvaćenih podataka
        print("---Pregled statistike bloka")
        visinaBloka = int(input("Unesite visinu bloka koji želite pregledati: "))
        try:
            statistikaBloka = client.getblockstats(visinaBloka)
            ukupno = statistikaBloka['totalfee'] + statistikaBloka['subsidy']
            omjerNagrade = statistikaBloka['subsidy'] / ukupno
            omjerNaknade = statistikaBloka['totalfee'] / ukupno
            print("Prosječna naknada bloka:", statistikaBloka['avgfee'], "satoshija")
            print("Prosječna stopa naknade", statistikaBloka['avgfeerate'], "satoshija po virtualnom bajtu")
            print("Maksimalna naknada bloka:", statistikaBloka['maxfee'], "satoshija")
            print("Stopa maksimalne naknade bloka:", statistikaBloka['maxfeerate'], "satoshija po virtualnom bajtu")
            print("Minimalna naknada bloka:", statistikaBloka['minfee'], "satoshija")
            print("Stopa minimalne naknade bloka:", statistikaBloka['minfeerate'], "satoshija po virtualnom bajtu")
            print("Novo generirani novac, nagrada za rudarenje bloka:", statistikaBloka['subsidy'], "satoshija")
            print("Ukupna naknada bloka:", statistikaBloka['totalfee'], "satoshija")
            print("Ukupan zbroj nagrade i naknade: ", ukupno, "satoshija")
            print("Omjer nagrade bloka i naknade iznosi: ", "{:.3f}".format(omjerNagrade), ":",
                  "{:.3f}.".format(omjerNaknade))
            print("Broj transakcija, uključujući coinbase transakciju:", statistikaBloka['txs'])
        except:
            print("Pogrešan unos visine")
        print("------\n")

    elif odabir == 4:
        # Dohvaćanje hasha najboljeg bloka funkcijom getbestblockhash() te ispis podataka
        print("---Dohvaćanje najboljeg bloka---")
        hashNajboljegBloka = client.getbestblockhash()
        try:
            najboljiBlok = client.getblock(hashNajboljegBloka)
            InformacijeOBlokuIspis(najboljiBlok)
        except:
            print("Greška pri dohvaćanju najboljeg bloka")

    elif odabir == 5:
        # Dohvaćanje podataka o blockchainu getblockchaininfo() funkcijom te ispis podataka
        blockchainInfo = client.getblockchaininfo()
        print("---Informacije o blockchainu---")
        print("Ime mreže:", blockchainInfo['chain'])
        print("Broj blokova:", blockchainInfo['blocks'])
        print("Broj headera koji su validirani:", blockchainInfo['headers'])
        print("Hash najboljeg bloka:", blockchainInfo['bestblockhash'])
        print("Poteškoća blockchaina:", blockchainInfo['difficulty'])
        print("Veličina na disku:", blockchainInfo['size_on_disk'])
        print("Procjena verifikacije:", blockchainInfo['verificationprogress'])
        print("------\n")

    elif odabir == 6:
        # Dohvaćanje podataka o mempool getmempoolinfo() funkcijom te ispis podataka
        mempool = client.getmempoolinfo()
        print("Pregled mempoola")
        print("Trenutni broj transakcija:", mempool['size'])
        print("Ukupno zauzeta memorija mempoola:", mempool['usage'])
        print("Maksimalno korištenje memorije za mempool", mempool['maxmempool'])
        print("Minimalna stopa naknade u BTC/kB kako bi se prihvatila transakcija:", mempool['mempoolminfee'])
        print("Minimalna relay naknada za transakcije:", mempool['minrelaytxfee'])
        print("------\n")

    elif odabir == 7:
        # Dohvaćanje informacija o mreži getnetworkinfo() funkcijom te ispis informacija mreže
        networkInfo = client.getnetworkinfo()
        print("---Pregled informacija o mreži---")
        print("Verzija mreže:", networkInfo['version'])
        print("Podverzija mreže:", networkInfo['subversion'])
        print("Verzija protokola:", networkInfo['protocolversion'])
        print("Ukupan broj konekcija:", networkInfo['connections'])
        print("------\n")

    elif odabir == 8:
        # Dohvaćanje poteškoće getdifficulty() funkcijom
        poteskoca = client.getdifficulty()
        print("---Dohvaćanje poteškoće---")
        print("Poteškoća:", poteskoca)
        print("------\n")

    elif odabir == 0:
        print("---Prekid---")
        flag = 0

    else:
        print("Pogrešan unos")
