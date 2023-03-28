import requests
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, flash, jsonify

app = Flask(__name__)
app.secret_key = "imm_sukruburakcetin"

url = "http://www.koeri.boun.edu.tr/scripts/lst4.asp"

sonuc = requests.get(url)
sonuc2 = BeautifulSoup(sonuc.content, "lxml")
liste = []
sonuc2 = sonuc2.text
sonuc2 = sonuc2.strip()
sonuc2 = sonuc2.split("\r")

enlem = []
boylam = []
yer = []
tarih = []
saat = []
derinlik = []
buyukluk = []

for i in range(14, len(sonuc2) - 20):
    i = sonuc2[i].split()
    if len(i) >= 9:
        enlem.append(i[2])
        boylam.append(i[3])
        tarih.append(i[0])
        saat.append(i[1])
        derinlik.append(i[4])
        buyukluk.append(str(i[6]))
        yer.append(str(i[8]) + " " + str(i[9]))

df = pd.DataFrame({"Enlem": enlem, "Boylam": boylam, "Yer": yer,
                   "Tarih": tarih, "Saat": saat,
                   "Derinlik(km)": derinlik, "Buyukluk": buyukluk})

df['Buyukluk'] = [x.replace('.', '') for x in df['Buyukluk']]

df["Enlem"] = df["Enlem"].astype("float64")
df["Boylam"] = df["Boylam"].astype("float64")
df["Derinlik(km)"] = df["Derinlik(km)"].astype("float64")
df["Buyukluk"] = df["Buyukluk"].astype("float64")

df_p = df.T.to_dict('dict')


@app.route("/hello")
def index():
    flash("what's your name?")
    return render_template("index.html")


@app.route("/greet", methods=['POST', 'GET'])
def greeter():
    flash("Hi " + str(request.form['name_input']) + ", great to see you!")
    return render_template("index.html")


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/earthquakes/all', methods=['GET'])
def api_all():
    return jsonify(df_p)


app.config['JSON_AS_ASCII'] = False
app.run(debug=False)