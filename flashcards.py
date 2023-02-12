from datetime import datetime
from flask import Flask, render_template, abort, request, redirect, url_for
from model import db
from markupsafe import escape



app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("welcome.html",data=db)

@app.route("/card")
def card_view():
    card = db[0]
    print(card)
    return render_template("card.html", data=card)

@app.route("/card/<nomor>")
def card_view_by_nomor(nomor):
    try:
        nomor = int(escape(nomor))
        card = db[nomor]
        print(nomor,card)
        return render_template("card.html", data=card, nomor=nomor, max_nomor=len(db)-1)
    except IndexError:
        abort(404)

@app.route("/add_card", methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        card = {"pertanyaan": request.form['pertanyaan'],
                "jawab": request.form['jawab']}
        db.append(card)
        return redirect(url_for('card_view_by_nomor', nomor=len(db)-1))
    else:
        return render_template("add_card.html")

@app.route("/api/card")
def api_card_view():
    return db

@app.route("/api/card/<nomor>")
def api_card_view_by_nomor(nomor):
    try:
        nomor = int(escape(nomor))
        card = db[nomor]
        print(nomor,card)
        return card
    except IndexError:
        abort(404)



@app.route("/date")
def date():
    return "This page is served at " + str(datetime.now())

counter = 0

@app.route("/count_views")
def count_views():
    global counter
    counter += 1
    return "This page was served " + str(counter) + " times"