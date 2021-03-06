from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
import pandas as pd

from pymongo import MongoClient

def index(request):
    Borrower_Name = request.session["Name"]
    client = MongoClient('localhost', 27017)
    db = client.book_keeping
    collection_books = db.books
    collection_borrow = db.borrower
    dic_list = []
    book_querry = {}
    if (request.method == "POST"):
        print(len(request.POST["Book_Name_search"]))
        print(len(request.POST["Author_Name_search"]))
        if (len(request.POST["Book_Name_search"]) != 0):
            book_querry["Book_Name"] = request.POST["Book_Name_search"]
        if (len(request.POST["Author_Name_search"]) != 0):
            book_querry["Author_Name"] = request.POST["Author_Name_search"]
        if (len(request.POST["Genre_search"]) != 0):
            book_querry["Genre"] = request.POST["Genre_search"]
    books_querry = collection_books.find(book_querry)
    for x in books_querry:
        if (x["Is_Lended"] == True):
            lended_books = collection_borrow.find({"Book_Name":x["Book_Name"]}).sort([("End_date", -1)]).limit(1)
            print(lended_books.count())
            for y in lended_books:
                x["Start_date"] = y["Start_date"]
                x["End_date"] = y["End_date"]
                text = "Borrow "+ x["Book_Name"]
                x["button"] = text
                print(x)
                dic_list.append(x)
        else:
            x["Start_date"] = ""
            x["End_date"] = ""
            text = "Borrow "+ x["Book_Name"]
            x["button"] = text
            dic_list.append(x)
    return render(request,"borrow_book/index.html",{"parent_dict" : dic_list, "Name":Borrower_Name, "MEDIA_URL":'/media/'})

def success(request):
    if (request.method == "POST"):
        client = MongoClient('localhost', 27017)
        try:
            collection_borrow = client.book_keeping.borrower
            collection_books = client.book_keeping.books
            try:
                Book_id = request.POST["Book_id"]
                Book_Name = request.POST["Book_Name"]
                Owner_Name = request.POST["Owner_Name"]
                Borrower_Name = request.session["Name"]
                Borrower_Signum = request.session["Esignum"]
                Start_date = request.POST["Start_date"]
                end_date = (pd.to_datetime(Start_date) + pd.DateOffset(days=14)).strftime('%Y-%m-%d')
                End_date = str(end_date)
                querry = {
                "Book_id" : Book_id,
                "Book_Name" : Book_Name,
                "Owner_Name" : Owner_Name,
                "Borrower_Name" : Borrower_Name,
                "Borrower_Signum" : Borrower_Signum,
                "Start_date" : Start_date,
                "End_date" : End_date
                }
                print(type(querry))
                try:
                    rec_id1 = collection_borrow.insert_one(querry)
                    try:
                        myquery = { "_id": int(request.POST["Book_id"]) }
                        newvalues = { "$set": { "Is_Lended": True } }
                        rec_id1 = collection_books.update_one(myquery, newvalues)
                        print(rec_id1)
                        try:
                            response = redirect("/option")
                            return (response)
                        except:
                            print("after update")
                    except:
                        print("after insert")
                except Exception as e:
                    print(e)
                    print(querry)
                    print("after querry form")

            except Exception as e:
                print(e)
                print(type(request.POST["Start_date"]))
                print(request.POST)
                print("after collection")
        except:
            print("inside client")
    else:
        print("none")
