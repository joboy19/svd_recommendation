import numpy as np 
import pandas as pd 
import json
import csv

from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "this_is_a_secret"



def getID(username):
    with open("data/users.csv", "r", encoding='utf-8', newline='\n') as data1:
        for line in data1:
            data = line.rstrip().split(",")
            if data[1] == username:
                return data[0]
    return "False"

@app.route("/get_ratings", methods=["GET"])
def get_ratings():
    out = {}
    with open("data/ratings copy 2.csv", "r", encoding='utf-8', newline='\n') as data1:
        for line in data1:
            data = line.rstrip().split(",")
            if data[0] == session["id"]:
                a = get_book(data[1])
                out[data[1]] = [data[2], a[0], a[1]]
        return json.dumps(out)
    return "False"

def get_book(id_):
    with open("data/books_test.csv", "r", encoding='utf-8', newline='\n') as data1:
        for line in data1:
            data = line.rstrip().replace(", ", " ").replace("\"", "").split(",")
            if data[0] == id_:
                print(data)
                return data[1], data[2]
    return "False" 

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
    count = 0
    print("Signup For: ", username)
    with open("data/users.csv", "r", encoding='utf-8', newline='\n') as data1:
        for line in data1:
            count += 1
            data = line.rstrip().split(",")
            print(data)
            if data[1] == username:
                return "False"
    with open("data/users.csv", "a", encoding='utf-8', newline="\n") as data1:
        writer = csv.writer(data1)
        writer.writerow([count+1,username,password])
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
        print(session["id"], "here")
        return "True"
    return "False"

@app.route("/update_details", methods=["POST"])
def update_details():
    r = csv.reader(open("data/users.csv"))
    data = list(r)
    print(data)
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
    r = csv.reader(open("data/ratings copy 2.csv"))
    data = list(r)
    print(data)
    for x in range(len(data)):
        if data[x][0] == session["id"]:
            if data[x][1] == bookid:
                data.pop(x)
                writer = csv.writer(open('data/ratings copy 2.csv', 'w', newline='\n', encoding='utf-8'))
                writer.writerows(data)
                return "True"

@app.route("/make_rating", methods=["POST"])
def make_rating():
    print(request.form)
    if request.form["rating"] == "-1":
        delete_rating(request.form["bookid"])
        return "True"
    else:
        r = csv.reader(open("data/ratings copy 2.csv"))
        data = list(r)
        for x in range(len(data)):
            if data[x][0] == session["id"]:
                if data[x][1] == request.form["bookid"]:
                    print("here")
                    data[x] = [data[x][0], data[x][1], request.form["rating"]]
                    writer = csv.writer(open('data/ratings copy 2.csv', 'w', newline='\n', encoding='utf-8'))
                    writer.writerows(data)
                    return "True"
        data.append([session["id"], request.form["bookid"], request.form["rating"]])
        writer = csv.writer(open('data/ratings copy 2.csv', 'w', newline='\n', encoding='utf-8'))
        writer.writerows(data)
        return "True"
    
    

if __name__ == '__main__':
    app.run(debug=True)