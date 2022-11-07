# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np

import pandas as pd
import pydeck as pdk
import streamlit as st



chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)

df = pd.DataFrame(
    np.random.randn(100, 2) / [0.5, 0.5] + [55.5, 37.33],
    columns=['lat', 'lon'])
st.map(df)

#======================================
