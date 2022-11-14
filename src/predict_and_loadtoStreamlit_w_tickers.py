import datetime

import numpy as np
from catboost import CatBoostClassifier, Pool
import pandas as pd
import os
START_DATE = '2022-10-28'
MEME = ['UPST','PTON','AMC','COIN','SNAP','NIO','PLTR','DKNG',
        'HOOD','TLRY','RKLB','BB','MRNA','ZIM','GME','BBIG',
        'KOSS','EXPR','SPY','BBBY','CLOV','ORA','WDR', 'TDC', 'SNBR', 'THS', 'BLKB', 'UIS', 'PCRX', 'INFN', 'FGEN',
        'ALTR', 'TDS', 'NOK', 'JBT', 'FUBO', 'BLNK', 'MEGL', 'DDS', 'MULN','--ALL TICKERS']

df = pd.read_csv(os.path.join("../data/comment_wallstreetbets_new_2022.csv"), sep='\t')
df = df.drop_duplicates(subset=['selftext'])
df.to_csv(os.path.join("../data/comment_wallstreetbets_new_2022.csv"),sep='\t', index=False)

columns=['created_utc', 'title', 'selftext']
df = df.fillna('')
df = df[columns].astype(str)

df['text'] = df['title'] + df['selftext']

df = df[['created_utc', 'text']]


model = CatBoostClassifier()      # parameters not required.
model.load_model('../src/cb_model_0.7933.cbm')
df['OriginalTweet'] = df['text']

test_pool = Pool(
    data=df[['OriginalTweet']],
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

dates = pd.DataFrame(pd.date_range(START_DATE, datetime.datetime.today().date()).date, columns=['date'])


# Cathegorize by
output = pd.DataFrame()
for ticker in MEME:
    output_ticker = pd.DataFrame(columns=['date','predict','text','ticker'])
    if ticker != '--ALL TICKERS':
        df_topredict = pd.DataFrame(columns=['date','predict','text','ticker'])
        for _, r in df.iterrows():
            if (((" " + ticker.lower() + " ") in r['OriginalTweet']) or
                ((" " + ticker.lower() + " ") in r['OriginalTweet']) or
                ((" " + ticker.lower() + ".") in r['OriginalTweet']) or
                ((" " + ticker.lower() + ",") in r['OriginalTweet'])or
                ((" " + ticker.lower() + "!") in r['OriginalTweet'])or
                ((" " + ticker.lower() + "?") in r['OriginalTweet']) or
                ((" " + ticker.lower() + ":") in r['OriginalTweet'])):
                df_topredict = pd.concat([df_topredict, r.to_frame().T])

    else:
        df_topredict = df



    if df_topredict.shape[0] > 0:
        row = pd.DataFrame()
        gbydate = df_topredict.groupby(by='date', as_index=False)
        #output1 = df_topredict.agg()
        row = pd.concat([gbydate[['predict']].mean()[['date','predict']], gbydate[['text']].count()[['text']]], axis=1)

        output_ticker = pd.concat([output_ticker, row])
    output_ticker = pd.merge(dates, output_ticker, on='date', how='left')
    output_ticker.fillna(value=0, inplace=True)
    output_ticker['ticker'] = ticker
    output = pd.concat([output, output_ticker])
output.drop_duplicates()


output.to_csv('../streamlit/output_w_tickers.csv', sep='\t', index=False, header=True)


print('success')