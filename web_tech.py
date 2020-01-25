import numpy as np 
import pandas as pd 
import json
import csv

from recommendations import make_prediction
from flask import Flask, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "this_is_a_secret"


##getID for a single user
def getID(username):
    with open("data/users.csv", "r", encoding='utf-8', newline='\n') as data1:
        for line in data1:
            data = line.rstrip().split(",")
            if data[1] == username:
                return data[0]
    return "False"

#get individual ratings for each user
@app.route("/get_ratings", methods=["GET"])
def get_ratings():
    out = {}
    with open("data/ratings.csv", "r", encoding='utf-8', newline='\n') as data1:
        for line in data1:
            data = line.rstrip().split(",")
            if data[0] == session["id"]:
                a = get_book(data[1])
                out[data[1]] = [data[2], a[0], a[1]]
        return json.dumps(out)
    return "False"

#get book details from an id
def get_book(id_):
    with open("data/books.csv", "r", encoding='utf-8', newline='\n') as data1:
        for line in data1:
            data = line.rstrip().replace(", ", " ").replace("\"", "").split(",")
            if data[0] == id_:
                return data[1], data[2]
    return "False" 

#default page render 
@app.route('/')
def hello_world():
    return render_template("index.html")

def checkuser(username, password):
    with open("data/users.csv", "r", encoding='utf-8', newline='\n') as data1:
        for line in data1:
            data = line.rstrip().split(",")
            if data[1] == username:
                if data[2] == password:
                    return True
    return False

def signup(username, password):
    print("Signup For: ", username)
    with open("data/users.csv", "r", encoding='utf-8', newline='\n') as data1:
        for line in data1:
            data = line.rstrip().split(",")
            last_id = data[0]
            if data[1] == username:
                return "False"
    with open("data/users.csv", "a", encoding='utf-8', newline="\n") as data1:
        writer = csv.writer(data1)
        writer.writerow([int(last_id)+100000,username,password])
        data1.close()
    return True
        

@app.route('/login', methods=["GET"])
def login():
    if request.args["signup"] == "1":
        signup_ = signup(request.args["username"], request.args["password"])
        if signup_ == False:
            return "False"
    val = checkuser(request.args["username"], request.args["password"])
    if val:
        session["id"] = getID(request.args["username"])
        print(session["id"], request.args["username"])
        return "True"
    return "False"

@app.route("/update_details", methods=["POST"])
def update_details():
    r = csv.reader(open("data/users.csv"))
    data = list(r)
    for x in range(len(data)):
        if data[x][0] == session["id"]:
            print("here")
            print(request.form)
            data[x] = [data[x][0], request.form["username"], data[x][2]]
            writer = csv.writer(open('data/users.csv', 'w', newline='\n', encoding='utf-8'))
            writer.writerows(data)
            return "True"
    return "False"

def delete_rating(bookid):
    r = csv.reader(open("data/ratings.csv"))
    data = list(r)
    for x in range(len(data)):
        if data[x][0] == session["id"]:
            if data[x][1] == bookid:
                data.pop(x)
                writer = csv.writer(open('data/ratings.csv', 'w', newline='\n', encoding='utf-8'))
                writer.writerows(data)
                return "True"

@app.route("/make_rating", methods=["POST"])
def make_rating():
    if request.form["rating"] == "-1":
        delete_rating(request.form["bookid"])
        return "True"
    else:
        r = csv.reader(open("data/ratings.csv"))
        data = list(r)
        for x in range(len(data)):
            if data[x][0] == session["id"]:
                if data[x][1] == request.form["bookid"]:
                    print("here")
                    data[x] = [data[x][0], data[x][1], request.form["rating"]]
                    writer = csv.writer(open('data/ratings.csv', 'w', newline='\n', encoding='utf-8'))
                    writer.writerows(data)
                    return "True"
        data.append([session["id"], request.form["bookid"], request.form["rating"]])
        writer = csv.writer(open('data/ratings.csv', 'w', newline='\n', encoding='utf-8'))
        writer.writerows(data)
        return "True"

@app.route("/add_book", methods=["POST"])
def add_book():
    r = csv.reader(open('data/books.csv', encoding="utf-8"))
    data = list(r)
    book_id = len(data)
    print(book_id)
    data.append([book_id, request.form["bookname"], request.form["genre"]])
    writer = csv.writer(open('data/books.csv', 'w', newline='\n', encoding='utf-8'))
    writer.writerows(data)
    return str(book_id)

@app.route("/get_recoms", methods=["GET"])
def get_recoms():
    out = {}
    bookIDs = make_prediction(str(session["id"]))
    for x in bookIDs:
        a = get_book(str(x))
        out[x] = [a[0], a[1]]
    print(out)
    return json.dumps(out)

@app.route("/search_books", methods=["GET"])
def search_books():
    book = request.args["bookname"]
    with open("data/books.csv", "r", encoding='utf-8', newline='\n') as data1:
        for line in data1:
            data = line.rstrip().split(",")
            if data[1] == book:
                return str(data[0])
    return "False"


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return "True"
    

if __name__ == '__main__':
    app.run(debug=True)