import matplotlib
from utils import preprocess
matplotlib.use("TkAgg")
# from utils import preprocess, feature_engineer
import pandas as pd
import numpy as np
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import BatchNormalization
from sklearn.metrics import mean_squared_error

try:
    print("Reading in the dataset. This will take some time...")
    df = pd.read_csv('data_predictor.csv', nrows=361)
except:
    print("""
      can not import dataset
      """)
    quit()

df = preprocess(df)
# Scale the features

print(df.loc[df['week'] == 'Friday', ['week']])
print(df.head())
