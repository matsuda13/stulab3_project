import oseti
from oseti.oseti import Analyzer
import numpy as np

import pandas as pd

out_dir = "./out/"
text = pd.read_csv(out_dir+"content.csv")

ana = oseti.Analyzer()

def negaposi(text):
    review = ana.analyze(text)
    re_view= np.average(review)
    return re_view


print(ana.analyze_detail('私はとっても幸せ'))
print(ana.analyze_detail('私はとっても不幸'))

if __name__ == "__main__":
    negaposi()