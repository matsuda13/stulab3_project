import itertools
import os
from random import sample
import pandas as pd
import snscrape.modules.twitter as sntwitter #pip install snscrape 
import oseti
import numpy as np
from oseti.oseti import Analyzer

import pandas as pd

ana = Analyzer()

#ツイート検索するキーワード
def Twitterscraping():
    """
    Get 1000 tweets from twitter then transform tweets to csv file.
    Filename is "sample.csv".
    """
    out_dir = "./out"
    search = "コロナ"
    #Twitterでスクレイピングを行い特定キーワードの情報を取得
    scraped_tweets = sntwitter.TwitterSearchScraper(search).get_items()
    # #最初の10ツイートだけを取得し格
    sliced_scraped_tweets = itertools.islice(scraped_tweets, 1000)
    #データフレームに変換する
    df = pd.DataFrame(sliced_scraped_tweets)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    df.to_csv("./out/sample.csv")


def extract_content():
    """
    Sntwitter item has url, date, id, and many other data.
    Extract only contents.
    """
    out_dir = "./out/"
    df = pd.read_csv(out_dir+"sample.csv")
    con = df["content"]
    con.to_csv(out_dir+"content.csv", index=False)
    
def judge(text):
    """_summary_

    Args:
        text (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        review=ana.analyze(text)
        re_view= np.average(review)
        return re_view
    except:
    #review = ana.analyze(text)
        return 1

def negaposi():
    """_summary_
    """
    out_dir = "./out/"
    df = pd.read_csv(out_dir+"content.csv")
    for t in df["content"]:
        if t==0:
            print("空白")
    df['negaposi'] = df['content'].map(judge)
    df = df[df["negaposi"]<0]
    df.to_csv(out_dir+"nega.csv",index=False)