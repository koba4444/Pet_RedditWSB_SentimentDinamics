import numpy as np
from catboost import CatBoostClassifier, Pool
import pandas as pd
import os
from catboost import CatBoostClassifier
MEME = ['UPST','PTON','AMC','COIN','SNAP','NIO','PLTR','DKNG',
        'HOOD','TLRY','RKLB','BB','MRNA','ZIM','GME','BBIG','KOSS','EXPR','','','','',]
df = pd.read_csv(os.path.join("../data/r_wallstreetbets_new_2022.csv"))

columns=['created_utc', 'title','selftext']
df = df.fillna('')
df = df[columns].astype(str)

df['text'] = df['title'] + df['selftext']
df = df.drop_duplicates()
df=df[['created_utc', 'text']]


model = CatBoostClassifier()      # parameters not required.
model.load_model('cb_model_0.7933.cbm')
df['OriginalTweet'] = df['text']

test_pool = Pool(
    data=df[['OriginalTweet']],
    #label=df['Sentiment_predict'],
    text_features=['OriginalTweet']
)

y_proba_cb = model.predict_proba(test_pool)
y_pred = np.argmax(y_proba_cb, axis=1)
df['predict'] = model.predict(test_pool)

df = df.drop(df[df['created_utc'] == 'created_utc'].index)
df = df.drop(df[df['created_utc'] == 'title'].index)
df = df.drop(df[df['created_utc'] == 'author'].index)
df['date'] = pd.to_datetime(df['created_utc'], format='%Y-%m-%dT%H:%M:%SZ').dt.date
df['predict'] = df['predict'].replace(['Negative', 'Neutral', 'Positive'],[-1., 0., 1.])
df.reset_index(drop=True)

output = pd.concat([df.groupby('date').mean('predict').reset_index(drop=False),
                   df.groupby('date').count().reset_index(drop=False)['text']], axis=1)
output.to_csv('../streamlit/output.csv')