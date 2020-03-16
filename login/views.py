from django.shortcuts import render, redirect
from pymongo import MongoClient

from .modules.password import verify_password

def index(request):
    return render(request, "login/login.html")

def check_pass(request):
    Esignum = ""
    Password = ""
    if (request.method == "POST"):
        Esignum = request.POST["Esignum"]
        Password = request.POST["Password"]
        client = MongoClient('localhost', 27017)
        db = client.book_keeping
        collection = db.login
        row = collection.find_one({"Esignum" : Esignum})
        if (row != None):
            given_password = request.POST["Password"]
            if (verify_password(row["Password"], Password)):
                request.session["Name"] = row["Name"]
                request.session["Esignum"] = Esignum
                responce = redirect("/option")
                return (responce)
            else:
                responce = redirect("/login")
                return(responce)
        else:
            responce = redirect("/login")
            return(responce)
