import oseti
import numpy as np
from oseti.oseti import Analyzer

import pandas as pd


def judgement(text):
    ana = oseti.Analyzer()
    review = ana.analyze(text)
    re_view= np.average(review)
    return re_view


#print(ana.analyze_detail('私はとっても幸せ'))
#print(ana.analyze_detail('私はとっても不幸'))

if __name__ == "__main__":
    out_dir = "./out/"
    df = pd.read_csv(out_dir+"content.csv")
    df['negaposi'] = df['content'].map(judgement)
    df = df[df["negaposi"]<0]
    df.to_csv(out_dir+"nega.csv",index=False)