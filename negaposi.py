import oseti
import numpy as np
from oseti.oseti import Analyzer

import pandas as pd

ana = Analyzer()

def judge(text):
    
    try:
        review=ana.analyze(text)
        re_view= np.average(review)
        return re_view

    except:
    #review = ana.analyze(text)
        return 1


#print(ana.analyze_detail('私はとっても幸せ'))
#print(ana.analyze_detail('私はとっても不幸'))

def negaposi():
    out_dir = "./out/"
    df = pd.read_csv(out_dir+"content.csv")
    for t in df["content"]:
        if t==0:
            print("空白")
    df['negaposi'] = df['content'].map(judge)
    df = df[df["negaposi"]<0]
    df.to_csv(out_dir+"nega.csv",index=False)


if __name__ == "__main__":
    negaposi()