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

def Twitterscraping(out_dir):
    """
    ユーザー、ユーザープロファイル、ハッシュタグ、検索、ツイート（単一またはスレッド）、リスト投稿、トレンドから「コロナ」を含むテキストを25,000件取得する。その後、csvファイルに出力する。
    ファイル名は ”scraping_results.csv” である。
    """
    
    search = "コロナ" # ツイート検索するキーワード
    # Twitterでスクレイピングを行い特定キーワードの情報を取得
    scraped_tweets = sntwitter.TwitterSearchScraper(search).get_items()
    # 最初の25000ツイートだけを取得し格納する
    sliced_scraped_tweets = itertools.islice(scraped_tweets, 10)
    # データフレームに変換する
    df = pd.DataFrame(sliced_scraped_tweets)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    df.to_csv("./out/scraping_results.csv")


def extract_content():
    """
    "scraping_results.csv" には、URL、日付、IDなど、様々なデータが含まれている。その内、contentのみを抽出する。
    ファイル名は "contents.csv" である。
    """
    out_dir = "./out/"
    df = pd.read_csv(out_dir+"scraping_results.csv")
    con = df["content"]
    con.to_csv(out_dir+"contents.csv", index=False)
    
def judge(text):
    """
    テキストをネガポジ判定する。
    Args:
        text (str): 内容（ツイート、ハッシュタグ、リプライを含む。)
    Returns:
        int: score(1に近いほどポジティブ、-1に近いほどネガティブと判定される。)
    """
    try:
        review = ana.analyze(text)
        re_view = np.average(review)
        return re_view
    except:
        return 1

def negaposi():
    """
    判定関数の結果が0未満であったテキストを出力する。
    ファイル名は "negative.csv" である。
    """
    out_dir = "./out/"
    df = pd.read_csv(out_dir+"contents.csv")
    for t in df["content"]:
        if t==0:
            print("空白")
    df['negaposi'] = df['content'].map(judge)
    df = df[df["negaposi"]<0]
    df.to_csv(out_dir+"negative.csv",index=False)



def parse(tweet_temp):
    """引数で与えられたテキストを形態素解析する。

    Args:
        tweet_temp (_type_): negative.csvのcontentカラムに保存されている値の１つ(1ツイート文)。

    Returns:
        list: 形態素解析した結果をリストに保存する。
    """
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
    """negative.csvのcontentカラムに保存されている値の１つ(1ツイート文)をparse関数で形態素解析する。その後、カラムを形態素の種類ごとに設定したデータフレームを作成し、parse関数の結果を該当するカラムに保存する。作成したデータフレームを戻り値として返す。

    Args:
        tweet_temp (numpy.ndarray): negative.csvのcontentカラムに保存されている値の１つ(1ツイート文)

    Returns:
        pandas.core.frame.DataFrame: カラムを形態素の種類ごとに設定したデータフレーム。該当するカラムにparse関数の結果を保存している。
    """
    return pd.DataFrame(parse(tweet_temp),
                        columns=["単語","品詞","品詞細分類1",
                                 "品詞細分類2","品詞細分類3",
                                 "活用型","活用形","原形","読み","発音"])
    
def make_lda_docs(texts):
    """
    Save words in Bag-of-Words format.
    Args:
    texts(String): negative.csvのcontentカラムに保存されている値

    Returns:
    String: 一般名詞と固有名詞のみ
    """
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
    """
    コーパス作成の後, クラスター数4個のLDAモデルで学習.
    学習したldaのベクトルをarrに格納.
    pyldavizによる結果をpyldavis_output.htmlで保存.
    """

    nega = pd.read_csv("./out/negative.csv")
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
    arr = gensim.matutils.corpus2dense(
        corpus_lda,
        num_terms=n_cluster
    ).T
    vis = pyLDAvis.gensim_models.prepare(lda, corpus, dictionary, sort_topics=False)
    pyLDAvis.save_html(vis, "./out/pyldavis_output.html")
    