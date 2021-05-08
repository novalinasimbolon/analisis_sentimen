from django.shortcuts import render
from analisis_teks import preproses as preproses
import requests
import pymysql
from sqlalchemy import create_engine
import pandas as pd

# Create your views here.


def home(request):
    return render(request, "home.html")


def data(request):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='analisis_sentimen')

    # create cursor
    cursor = connection.cursor()

    # Execute query
    sql = "SELECT * FROM `crawling`"
    cursor.execute(sql)

    # Fetch all the records
    result = cursor.fetchall()
    return render(request, "data.html", {'result': result})


def proses(request):
    engine = create_engine('mysql+pymysql://root:@localhost/analisis_sentimen')
    df = pd.read_sql("select * from crawling", engine)
    tweet = df["tweet"]
    lower = preproses.bacafile(tweet)
    # stemm = preproses.stem(lower)
    # tweet_id = df["id"]
    tweet_date = df["tanggal"]
    tweet_sentimen = df["sentimen_manual"]

    dict = {'date': tweet_date, 'tweet': tweet,
            'lower': lower, 'tweet_sentimen': tweet_sentimen}
    df = pd.DataFrame(dict)

    df.to_sql('preproses', con=engine, if_exists='replace', index=False)

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='analisis_sentimen')

    # create cursor
    cursor = connection.cursor()

    # Execute query
    sql = "SELECT * FROM `preproses`"
    cursor.execute(sql)

    # Fetch all the records
    result = cursor.fetchall()
    return render(request, "preproses.html", {'result': result})
