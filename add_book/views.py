from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from pymongo import MongoClient


def index(request):
    return render(request, "add_book/index.html")

def enter_book(request):
    book_name = ""
    Owner_Name = request.session["Name"]
    if (request.method == "POST"):
        book_name = request.POST["Book_name"]
        Author_Name = request.POST["Author_Name"]
        Genre = request.POST["Genre"]
        Cover = request.FILES['Cover']
        print(Cover)
        print(type(Cover))
        client = MongoClient('localhost', 27017)
        db = client.book_keeping
        collection = db.books
        request.session["Book_name"] = book_name
        id_count = collection.find().count()
        file_name = str(id_count)+"_Book.jpg"
        fs = FileSystemStorage()
        filename = fs.save(file_name, Cover)
        querry = {
        "_id" : id_count+1,
        "Book_Name" : book_name,
        "Author_Name" : Author_Name,
        "Owner_Name" : Owner_Name,
        "Genre" : Genre,
        "Cover" : file_name,
        "Is_Lended" : False
        }
        rec_id1 = collection.insert_one(querry)
        print(rec_id1)
        responce = redirect("added_book")
        return(responce)

def added_book(request):
    book_name = request.session["Book_name"]
    lender_Name = request.session["Name"]
    client = MongoClient('localhost', 27017)
    db = client.book_keeping
    collection = db.books
    row = collection.find_one({"Book_Name" : book_name,"Lender_Name" : lender_Name})
    return redirect('/option')
