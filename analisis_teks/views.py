from django.shortcuts import render
from analisis_teks import preproses as preproses
import requests
import pymysql
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import model_selection
from sklearn import metrics
from sklearn import naive_bayes

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


def analisis(request):
    x = []
    y = []
    pred = []
    xdata = preproses.random()

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='analisis_sentimen')

    cursor = connection.cursor()
    sql = "SELECT * FROM `preproses`"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        x.append(row[2])
        y.append(row[3])

    x = np.array(x)
    y = np.array(y)

    x_train, x_test, y_train, y_test = model_selection.train_test_split(
        x, y, test_size=0.25, random_state=0)
    # Multinomial Naive Bayes
    vectorizer = CountVectorizer(ngram_range=(1, 2)).fit(x_train)
    x_train_vectorized = vectorizer.transform(x_train)
    x_test_vectorized = vectorizer.transform(x_test)

    Clf = naive_bayes.MultinomialNB()
    Clf.fit(x_train_vectorized, y_train)
    y_pred = Clf.predict(x_test_vectorized)
    acc = metrics.accuracy_score(y_test, y_pred)
    print('accuracy = '+str(acc*100)+'%')
    print(metrics.classification_report(y_test, y_pred))

    # y_pred_nb = preproses.multiNB(x_train, y_train, x_test)
    # acc_nb = accuracy_score(y_test, y_pred_nb)*100
    # report_nb = classification_report(y_test, y_pred_nb)

    df = pd.DataFrame()
    df['xdata'] = xdata
    df['x_test'] = x_test
    df['y_test'] = y_test
    df['y_pred'] = y_pred

    dict = {'xdata': xdata, 'x_test': df['x_test'],
            ' y_test': df['y_test'], 'y_pred': df['y_pred']}
    df = pd.DataFrame(dict)
    engine = create_engine('mysql+pymysql://root:@localhost/analisis_sentimen')
    df.to_sql('analisis', con=engine, if_exists='replace', index=False)

    # df['x_train'] = x_train
    # df['y_train'] = y_train
    # dict2 = {'x_train': df['x_train'], ' y_train': df['y_train']}
    # df2 = pd.DataFrame(dict2)
    # engine = create_engine('mysql+pymysql://root:@localhost/analisis_sentimen')
    # df2.to_sql('analisis_train', con=engine,
    #            if_exists='replace', index=False)

    # df3 = pd.DataFrame()
    # dict3 = {'acc': acc}
    # df3 = pd.DataFrame([dict3])
    # engine = create_engine('mysql+pymysql://root:@localhost/analisis_sentimen')
    # df3.to_sql('akurasi', con=engine, if_exists='replace', index=False)

    result = preproses.klasifikasi()
    # for a in result:
    #     pred.append(a[3])
    #     sentimentStats = preproses.computeSentimentStats(pred)
    #     percent_net = sentimentStats[0]
    #     percent_pos = sentimentStats[1]
    #     percent_neg = sentimentStats[2]

    return render(request, "analisis.html", {'result': result})
