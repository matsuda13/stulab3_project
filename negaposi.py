import oseti
import numpy as np
from oseti.oseti import Analyzer

import pandas as pd

out_dir = "./out/"
df = pd.read_csv(out_dir+"content.csv")

ana = oseti.Analyzer()

def judgement(text):
    review = ana.analyze(text)
    re_view= np.average(review)
    return re_view


#print(ana.analyze_detail('私はとっても幸せ'))
#print(ana.analyze_detail('私はとっても不幸'))

if __name__ == "__main__":
    df['negaposi'] = df['content'].map(judgement)
    print(df.head())
    df.to_csv(out_dir+"judge.csv")
