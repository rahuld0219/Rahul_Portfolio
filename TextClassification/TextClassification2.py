import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# parses  data into dataframe
data = pd.read_csv('spam_assassin.csv')

stops = set(stopwords.words('english'))
total = []
for dat in data['text']:
    dataToks = word_tokenize(dat)
    for elem in dataToks:
        if elem not in stops:
            total.append(elem)
    total = list(set(total))

set(total)
print(len(total))