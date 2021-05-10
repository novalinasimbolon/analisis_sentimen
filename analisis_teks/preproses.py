import nltk
import string
import re
import requests
import numpy
import pymysql
import pandas as pd
import numpy as np
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from sklearn import model_selection


def bacafile(tweet):
    # tweet = tweet.str.replace('b+', '')
    remove_url = tweet.str.replace('http\S+|www.\S+', '')
    remove_urldua = remove_url.str.replace('https\S+|www.\S+', '')
    remove_rt = remove_urldua.str.replace('RT+', '')
    remove_mention = remove_rt.str.replace('@[A-Za-z0-9|A_Za_z0_9]+', '')
    remove_hashtag = remove_mention.str.replace('#[A-Za-z0-9|A_Za_z0_9]+', '')
    remove_number = remove_hashtag.str.replace('\d+', '')
    remove_punctuation = remove_number.str.replace(
        '[{}]'.format(string.punctuation), '')
    lower_case = remove_punctuation.str.lower()
    lower_case = lower_case.str.replace('\ufeff', '')
    lower_case = lower_case.str.replace('\n', ' ')
    lower_case = lower_case.str.replace('\r', ' ')
    lower_case = lower_case.str.replace('\n\n', ' ')
    lower_case = lower_case.str.replace('\r\r', ' ')
    return lower_case


def stem(tweets):
    factorys = StopWordRemoverFactory()
    stopword = factorys.create_stop_word_remover()

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    result = []
    for sentence in tweets:
        #         result.append(stemmer.stem(stopword.remove(sentence)))
        stop = stopword.remove(sentence)
        result.append(stemmer.stem(stop))
    return result


def random():
    x = []
    y = []
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
    for row in result:
        x.append(row[2])
        y.append(row[3])

    x = np.array(x)
    y = np.array(y)

    x_train, x_test, y_train, y_test = model_selection.train_test_split(
        x, y, test_size=0.25, random_state=0)

    return x_test


def klasifikasi():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='analisis_sentimen')

    # create cursor
    cursor = connection.cursor()

    # Execute query
    sql = "SELECT * FROM `analisis`"
    cursor.execute(sql)

    # Fetch all the records
    result = cursor.fetchall()

    return result
