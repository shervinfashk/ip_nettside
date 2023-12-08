from flask import Flask, render_template, request,session
from flask_session import Session
from ip_program import lag_ip_adresse, lag_subnet_maske, regn_nettverks_adresse, regn_kringkasting_adresse, regn_antall_verter, adresse_cidr_notasjon

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route("/")

def index():
    return render_template("index.html")

@app.route("/spill")

def spill():

    if "RIKTIGE_SVAR" not in session:
        session["RIKTIGE_SVAR"] = {}
    if "IP_SUBNET_CIDR" not in session:
        session["IP_SUBNET_CIDR"] = {}

    RIKTIGE_SVAR = session["RIKTIGE_SVAR"]

    IP_SUBNET_CIDR = session["IP_SUBNET_CIDR"]



    ip_adresse = lag_ip_adresse()
    IP_SUBNET_CIDR["ip_adresse"] = ip_adresse

    subnet_adresse, cidr = lag_subnet_maske()
    IP_SUBNET_CIDR["subnet_adresse"] = subnet_adresse
    IP_SUBNET_CIDR[cidr] = cidr

    nettverks_adresse = regn_nettverks_adresse(ip_adresse,subnet_adresse)
    RIKTIGE_SVAR["nettverks_adresse"] = nettverks_adresse

    kringkasting_adresse = regn_kringkasting_adresse(ip_adresse,subnet_adresse)
    RIKTIGE_SVAR["kringkasting_adresse"] = kringkasting_adresse

    antall_verter = regn_antall_verter(cidr)
    RIKTIGE_SVAR["antall_verter"] = antall_verter

    cidr_notasjon = adresse_cidr_notasjon(ip_adresse,cidr)
    RIKTIGE_SVAR["cidr_notasjon"] = cidr_notasjon

    return render_template("spill.html",ip_adresse=ip_adresse,subnet_adresse=subnet_adresse)

@app.route("/sjekk")

def sjekk():    

    RIKTIGE_SVAR = session["RIKTIGE_SVAR"]

    IP_SUBNET_CIDR = session["IP_SUBNET_CIDR"]

    bruker_svar = {
    "nettverks_adresse":request.args.get("nettverksadresse"),
    "kringkasting_adresse":request.args.get("kringkastingsadresse"),
    "antall_verter":request.args.get("antallverter"),
    "cidr_notasjon":request.args.get("cidr")
    }
  

    for nøkkel in bruker_svar:
        if bruker_svar[nøkkel] == RIKTIGE_SVAR[nøkkel]:
            bruker_svar[nøkkel] = "Hurra riktig svar!"
        else:
            bruker_svar[nøkkel] = f"Feil. Riktig svar er {RIKTIGE_SVAR[nøkkel]}"


    return render_template("sjekk.html",nettverksadresse=bruker_svar["nettverks_adresse"],kringkastingsadresse=bruker_svar["kringkasting_adresse"],antallverter=bruker_svar["antall_verter"],cidr=bruker_svar["cidr_notasjon"], ip_adresse=IP_SUBNET_CIDR["ip_adresse"],subnet_adresse=IP_SUBNET_CIDR["subnet_adresse"])
    ...

@app.route("/faq")

def faq():
    return render_template("faq.html")
