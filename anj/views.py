from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def home(request):
    return render(request, 'home.html', {'name':'Anjaneyulu'})

def add(request):
    a = int(request.POST["R&D Spend"])
    b = int(request.POST["Administration"])
    c = int(request.POST["Marketing Spend"])
    d = int(request.POST["Profit"])
    conn = sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS startup (randd INTEGER, administration INTEGER, marketing INTEGER, profit INTEGER)")
    cur.execute("INSERT INTO startup VALUES (?, ?, ?, ?)", (a, b, c, d))
    conn.commit()
    cur.execute("SELECT * FROM startup")
    rows = cur.fetchall()
    for i, j in enumerate(rows):
        print(i, "Startup Data : {}".format(j))
    conn.close()    
    res = rows
    return render(request, "result.html", {'result':res})

def predict(request):
    a = int(request.POST["R&D Spend"])
    b = int(request.POST["Administration"])
    c = int(request.POST["Marketing Spend"])
    data = pd.read_csv('startup.csv')
    x = data.iloc[:, 0:3].values
    y = data.iloc[:,-1].values
    trainx, testx, trainy, testy = train_test_split(x, y, test_size=0.25, random_state=0)
    lr = LinearRegression()
    lr.fit(trainx, trainy)
    pred = lr.predict(testx)
    y0 = lr.intercept_ + lr.coef_[0] * a + lr.coef_[1] * b + lr.coef_[2] * c
    y1 = (np.array(y0))
    p1 = (lr.score(trainx, trainy)*100)
    p2 = (lr.score(testx, testy)*100)
    p4 = [p1, p2, y1]
    output = [x for x in p4]
    return render(request, "result.html", {'result0':output})
    
def view(request):
    conn = sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM startup")
    rows = cur.fetchall()
    for i, j in enumerate(rows):
        print(i, "Store Data : {}".format(j))
    conn.close()
    rows = j
    return render(request, "result.html", {'result1':rows})
