from django.shortcuts import render, redirect
from pymongo import MongoClient

from .modules.password import hash_password

def index(request):
    return render(request,"register/register_page.html")

def register_feed(request):
    Esignum = ""
    Password = ""
    Name = ""
    if (request.method == "POST"):
        Esignum = request.POST["Esignum"]
        Password = request.POST["Password"]
        Name = request.POST["Name"]
        Password_encoded = hash_password(Password)
        client = MongoClient('localhost', 27017)
        db = client.book_keeping
        collection = db.login
        querry = {
        "Name" : Name,
        "Esignum" : Esignum,
        "Password" : Password_encoded
        }
        rec_id1 = collection.insert_one(querry)
        print(rec_id1)
        responce = redirect("/login")
        return(responce)
