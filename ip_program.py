from random import randint

def main():
    print("Velkommen til IP-adressekonverteringsprogrammet!")
    print("Dette programmet hjelper deg med å øve på subnetting og konvertering av IP-adresser.")

    valg = input("Ønsker du å øve på konvertering av IP-adresser? Skriv 'JA' for å øve. Skriv 'NEI' for å avslutte: ").lower().strip()

    while valg not in ["ja","nei"]:
        valg = input("Venligst skriven enten 'JA' for å øve eller 'NEI' for å avslutte").lower().strip()
                       

    while valg == "ja":

        ip_adresse = lag_ip_adresse()
        subnet_adresse,cidr = lag_subnet_maske()

        nettverks_adresse = regn_nettverks_adresse(ip_adresse,subnet_adresse)
        kringkasting_adresse = regn_kringkasting_adresse(ip_adresse,subnet_adresse)
        antall_verter = regn_antall_verter(cidr)
        cidr_notasjon = adresse_cidr_notasjon(ip_adresse,cidr)

        antall_riktige = 0

        mulige_gjett = [["Hva er nettverksadressen? ", nettverks_adresse],["Hva er kringkastingsadressen? ", kringkasting_adresse], ["Hva er antall brukbare IP-adresser? ", antall_verter ], ["Skriv IP-adressen i CIDR-notasjon: ", cidr_notasjon]]

        for gjett_svar in mulige_gjett:
            svar = input(gjett_svar[0]).strip()
            if svar == gjett_svar[1]:
                antall_riktige +=1
                print("Hurra! Riktig svar.")
            else:
                print("Riktig svar er:", gjett_svar[1])
        
        print("Antall riktige denne runden:", antall_riktige)

        valg = input("Ønsker du å fortsette å øve på konvertering av IP-adresser? Skriv 'JA' for å øve. Skriv 'NEI' for å avslutte ").lower().strip()
        while valg not in ["ja","nei"]:
            valg = input("Venligst skriven enten 'JA' for å øve eller 'NEI' for å avslutte: ").lower().strip()

    print("Takk for at du brukte programmet!")
    ...




def lag_ip_adresse(): # denne returnerer en streng
    oktet_1 = randint(0,255)
    oktet_2 = randint(0,255)
    oktet_3 = randint(0,255)
    oktet_4 = randint(0,255)

    ip_adresse = f"{oktet_1}.{oktet_2}.{oktet_3}.{oktet_4}"

    print("IP-adressen er:", ip_adresse)

    return ip_adresse


    ...

def lag_subnet_maske(): # returnerer streng med subnet og opprinnelige cidr

    cidr_notasjon = randint(1,31) # dette vil føre til ulike klasser av IP-adresser, ikke alle som er like relevante, men siden dette er for læring av hvordan å bruke konvertere så lar jeg det være sånn
    cidr_retur = cidr_notasjon
    liste = [] # bruker liste til å legge til verdiene i de ulike oktettene

    while cidr_notasjon > 0: # mens verdien er over 0 så fortsetter vi å legge til verdier
        if cidr_notasjon - 8 < 0: # hvis dette vlikåret fylles så har vi kommet til slutten av løkken
            padding = 8 - cidr_notasjon # dette er for å sikre at vi får 8 bits i oktetten
            nåværende_binær = "1"*cidr_notasjon + "0"*padding # ved å legge til oktetten sikrer vi at 1`erne får korrekt verdi i forhold til 2 tallsystsmet

            liste.append(str(int(nåværende_binær,2))) # man kan bruke en streng med tall som argument i int funksjonen og angi hva slags tallsystemt mna ønsker å bruke
            break # siden vi har funnet ut at av at dette vilkåret er sant kan vi avslutte --> "if cidr_notasjon - 8 < 0:"
        else:
            liste.append(str(int("1"*8,2)))
            cidr_notasjon -= 8

    while len(liste) != 4: # dette er for "penhet", f eks vil 255.128 bli --> 255.128.0.0
        liste.append("0")
    
    subnet = ".".join(liste)
    print("Subnetmasken er:", subnet)
    return subnet,cidr_retur


def regn_nettverks_adresse(ip_adresse,subnet_adresse): # vurderte å bruke zip funksjonen men er ikke så kjent med det
    okteter_ip = ip_adresse.split(".") # splitte ip adressen inn i okteter
    okteter_ip = [f'{int(tall):08b}' for tall in okteter_ip] # gjør om verdiene som er i 10-tallsystemet om til 2-tallssystemet

    okteter_sub = subnet_adresse.split(".") # samme som over
    okteter_sub = [f'{int(tall):08b}' for tall in okteter_sub]

    nettverks_adresse = [] # tom liste som blir nettverksadressen
    bryt_løkke = False # hvis den nøstetde listen blir brytet på innsiden er vi ferdig med hele løkken

    for indeks_element in range(len(okteter_sub)): # begge oktetene har samme mengde elementer (4) og like mange karakaterer i strengene (8)
        if bryt_løkke: # hvis denne blir sann i den nøstede løkken er vi ferdig
            break
        oktet = "" # streng som skal legges til nettverks_adressen
        for indeks_kar in range(len(okteter_sub[indeks_element])): # vi går i gjennom hver streng, og for hver streng går i gjennom hver karakter
            if okteter_sub[indeks_element][indeks_kar] == "1": # hvis subnettemasken sin karakter er 1, må vi legge til ip_adresseb sin verdi på denne plassen
                oktet += okteter_ip[indeks_element][indeks_kar] # legger ip_adressen sin karakter i oktetet for nettverket
            else:
                bryt_løkke = True
                break

        nettverks_adresse.append(oktet)
    
    while len(nettverks_adresse) != 4: # hvis vi ikke har nok elementer kan vi bare fylle på, dette vil da være 0'ere
        nettverks_adresse.append("0")
    
    for indeks in range(len(nettverks_adresse)):
        if len(nettverks_adresse[indeks]) != 8: # hvis ikke vært element har 8 karakterer for å ikke verdiene riktig vekting
            padding = 8 - len(nettverks_adresse[indeks]) # finner ut av hvor mange ekstra 0 som treng
            nettverks_adresse[indeks] += "0" * padding # legger til 0 ene
        nettverks_adresse[indeks] = str(int(nettverks_adresse[indeks],2)) # endrer elementet fra  binær form til tallform
    
    return ".".join(nettverks_adresse)
        



            

    ...

def regn_kringkasting_adresse(ip_adresse,subnet_adresse): # dette er em replica av samme funksjonen med små endringer
    okteter_ip = ip_adresse.split(".")
    okteter_ip = [f'{int(tall):08b}' for tall in okteter_ip]

    okteter_sub = subnet_adresse.split(".")
    okteter_sub = [f'{int(tall):08b}' for tall in okteter_sub]

    nettverks_adresse = []
    bryt_løkke = False

    for indeks_element in range(len(okteter_sub)):
        if bryt_løkke:
            break
        oktet = ""
        for indeks_kar in range(len(okteter_sub[indeks_element])):
            if okteter_sub[indeks_element][indeks_kar] == "1":
                oktet += okteter_ip[indeks_element][indeks_kar]
            else:
                bryt_løkke = True
                break

        nettverks_adresse.append(oktet)
    
    while len(nettverks_adresse) != 4:
        nettverks_adresse.append("1") # hvis ikke har nok elementer legger vi til 1 ere
    
    for indeks in range(len(nettverks_adresse)):
        if len(nettverks_adresse[indeks]) != 8:
            padding = 8 - len(nettverks_adresse[indeks])
            nettverks_adresse[indeks] += "1" * padding # siden vi ønsker kringkasting adressen må vi få den høyeste verdien muli, som gjøres med enere
        nettverks_adresse[indeks] = str(int(nettverks_adresse[indeks],2))
    
    return ".".join(nettverks_adresse)
    ...


def regn_antall_verter(cidr): # man kan enkelt finnne ut av hvor mange verter på denne måten, 2 opphøyd i 32-cidr - 2 (trekke fra kringkasting og nettverk)
    return str((2**(32-cidr) - 2)) # returnerer antall brukbare verter


def adresse_cidr_notasjon(ip_adresse,cidr):
    return ip_adresse + "/" + str(cidr)


if __name__ == "__main__":
    main()