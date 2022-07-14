import itertools
import os
from random import sample
import pandas as pd
import snscrape.modules.twitter as sntwitter #pip install snscrape 
import oseti
import numpy as np
from oseti.oseti import Analyzer
import MeCab
import gensim
import ipadic
import pyLDAvis
import pyLDAvis.gensim_models

ana = Analyzer()
n_cluster = 4

def Twitterscraping():
    """
    Retrieve 25,000 texts containing "Corona" from users, user profiles, hashtags, searches, tweets (single or threaded), list posts, and trends. Then output to csv file.
    Filename is "scraping_results.csv".
    """
    out_dir = "./out"
    search = "コロナ" # ツイート検索するキーワード
    # Twitterでスクレイピングを行い特定キーワードの情報を取得
    scraped_tweets = sntwitter.TwitterSearchScraper(search).get_items()
    # 最初の25000ツイートだけを取得し格納する
    sliced_scraped_tweets = itertools.islice(scraped_tweets, 25000)
    # データフレームに変換する
    df = pd.DataFrame(sliced_scraped_tweets)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    df.to_csv("./out/sample.csv")


def extract_content():
    """
    "scraping_results.csv" have various data such as URL, date, ID, etc.
    Extract only contents.
    """
    out_dir = "./out/"
    df = pd.read_csv(out_dir+"sample.csv")
    con = df["content"]
    con.to_csv(out_dir+"content.csv", index=False)
    
def judge(text):
    """
    Judges text as negative-positive.
    Args:
        text (String): contents(include tweets, hashtags and replies.)

    Returns:
        int: score(Closer to -1 is considered positive and closer to -1 is considered negative.)
    """
    try:
        review = ana.analyze(text)
        re_view = np.average(review)
        return re_view
    except:
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



def parse(tweet_temp):
    t = MeCab.Tagger(ipadic.MECAB_ARGS)
    temp1 = t.parse(tweet_temp)
    temp2 = temp1.split("\n")
    t_list = []
    for keitaiso in temp2:
        if keitaiso not in ["EOS", ""]:
            word, hinshi = keitaiso.split("\t")
            t_temp = [word] + hinshi.split(",")
            if len(t_temp) != 10:
                t_temp += ["*"]*(10-len(t_temp))
            t_list.append(t_temp)
    return t_list

def parse_to_df(tweet_temp):
    return pd.DataFrame(parse(tweet_temp),
                        columns=["単語","品詞","品詞細分類1",
                                 "品詞細分類2","品詞細分類3",
                                 "活用型","活用形","原形","読み","発音"])
    
def make_lda_docs(texts):
    docs = []
    for text in texts:
        df = parse_to_df(text)
        extract_df = df[(df["品詞"]+"/"+df["品詞細分類1"]).isin(["名詞/一般","名詞/固有名詞"])]
        extract_df = extract_df[extract_df["原形"]!="*"]
        doc = []
        for genkei in extract_df["原形"]:
            doc.append(genkei)
        docs.append(doc)
    return docs

def do_lda():
    nega = pd.read_csv("./out/nega.csv")
    texts = nega["content"].values
    docs = make_lda_docs(texts)
    dictionary = gensim.corpora.Dictionary(docs)
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    n_cluster = 4
    lda = gensim.models.LdaModel(
                corpus=corpus,
                id2word=dictionary,
                num_topics=n_cluster,
                minimum_probability=0.001,
                passes=20,
                update_every=0,
                chunksize=10000,
                random_state=1
    )
    corpus_lda = lda[corpus]
    vis = pyLDAvis.gensim_models.prepare(lda, corpus, dictionary, sort_topics=False)
    pyLDAvis.save_html(vis, "./out/pyldavis_output.html")
    