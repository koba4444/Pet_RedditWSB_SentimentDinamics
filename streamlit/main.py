# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import os
import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(layout="centered", page_icon="wsb_icon.ico", page_title="Wallstreetbet subreddit sentiment dynamics")


MEME = ['UPST','PTON','AMC','COIN','SNAP','NIO','PLTR','DKNG',
        'HOOD','TLRY','RKLB','BB','MRNA','ZIM','GME','BBIG','KOSS','EXPR','','','','',]
header = st.container()
dataset = st.container()

with header:
    st.title('Wallstreetbet subreddit sentiment dynamics')
    st.markdown("""
                Know what is sentiment on ***r/wallstreetbet*** - subreddit with 13 mln readers
            """)

with dataset:
    all_symbols = MEME
    symbols = st.multiselect("Choose stocks to visualize", all_symbols, all_symbols[:3])
    data = pd.read_csv('./output.csv')
    #st.write(data.columns)
    data = data.rename(columns={data.columns[0]: 'ind',
                        data.columns[1]: 'Date',
                        data.columns[2]: 'Sentiment',
                        data.columns[3]: 'Post count',
                        })
    #st.write(data[['Date', 'Sentiment']].head(10))
    st.area_chart(data['Sentiment'])
    st.bar_chart(data['Post count'])



if __name__ == '__main__':
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
#
