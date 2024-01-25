import sqlite3
from flask import Flask, render_template, request, redirect,url_for

app = Flask(__name__)

data = []

def veriAl():
    global data
    with sqlite3.connect('veri.db') as con:
        cur = con.cursor()
        cur.execute("select * from tblVeri")
        data = cur.fetchall()
        for i in data:
            print(i)


def veriEkle(title, author, year):
    with sqlite3.connect('veri.db') as con:
        cur = con.cursor()
        cur.execute("insert into tblVeri(verititle, veriauthor, veriyear) values(?,?,?)",(title, author, year))
        con.commit()
        print("veriler eklendi")


def veriSil(id):
    with sqlite3.connect('veri.db') as con:
        cur = con.cursor()
        cur.execute("delete from tblVeri where id = ?",(id))
        print("veriler silindi")


def veriGuncelle(id, title, author, year):
    with sqlite3.connect('veri.db') as con:
        cur = con.cursor()
        cur.execute("update tblVeri set verititle = ?, veriauthor = ?, veriyear = ? where id =?" ,(title, author, year, id))
        con.commit()
        print("veriler güncellendi")




@app.route("/index")
def index():

    return render_template("index.html")


@app.route("/veri")
def veri():

    veriAl()

    return render_template("veri.html", alinan = data)


@app.route("/contact")
def contact():

    return render_template("contact.html")


@app.route("/hastaekle", methods=['GET', 'POST'])
def hastaekle():

    if request.method == "POST":
        hastaTitle = request.form['hastaTitle']
        hastaAuthor = request.form['hastaAuthor']
        hastaYear = request.form['hastaYear']
        veriEkle(hastaTitle, hastaAuthor, hastaYear)
        print("veriler kaydedildi: ",hastaTitle,hastaAuthor,hastaYear)

    return render_template("hastaekle.html")



@app.route("/hastasil/<string:id>")
def hastasil(id):

    print("hasta silecenek id:",id)
    veriSil(id)

    return redirect(url_for("veri"))



@app.route("/hastaguncelle/<string:id>", methods=['GET', 'POST'])
def hastaguncelle(id):

    if request.method == "GET":
        print("guncellenecek id:",id)
        guncellenecekVeri = []
        for d in data:
            if(str(d[0])) == id:
                guncellenecekVeri = list(d)

        return render_template("hastaguncelle.html", alinan = guncellenecekVeri)
    
    else:
        hastaID = request.form['hastaID']
        hastaTitle = request.form['hastaTitle']
        hastaAuthor = request.form['hastaAuthor']
        hastaYear = request.form['hastaYear']
        veriGuncelle(hastaID, hastaTitle, hastaAuthor, hastaYear)

        return redirect(url_for("veri"))



@app.route("/hastadetay/<string:id>")
def hastadetay(id):

    detayVeri = []
    for d in data:
        if(str(d[0])) == id:
            detayVeri = list(d)

    return render_template("hastadetay.html", alinan = detayVeri)


# @app.route("/doktorgiris", methods=['GET', 'POST'])
# def doktorgiris():

#     if request.method == "POST":
#         doktorTitle = request.form['doktorTitle']
#         doktorAuthor = request.form['doktorAuthor']
#         doktorYear = request.form['doktorYear']
#         veriEkle(doktorTitle, doktorAuthor, doktorYear)
#         print("veriler kaydedildi: ",doktorTitle,doktorAuthor,doktorYear)
#     return render_template("doktorgiris.html")

# @app.route("/doktorsil/<string:id>")
# def doktorsil(id):

#     print("silinecek doktor id:",id)
#     veriSil(id)

#     return redirect(url_for("veri"))



if __name__ == "__main__":
    # app.run(debug = True)
    app.run(host='0.0.0.0', port=8080)

