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
    df = pd.read_csv('data_predictor.csv', nrows=1000000)
except:
    print("""
      can not import dataset
      """)
    quit()

# Preprocess data
df = preprocess(df)

print(df.loc[df['week'] == 'Friday', ['week']])
print(df.head())
# Scale the features
df_prescaled = df.copy()
df_scaled = df.drop(['amount'], axis=1)
df_scaled = scale(df_scaled)
cols = df.columns.tolist()
cols.remove('amount')
df_scaled = pd.DataFrame(df_scaled, columns=cols, index=df.index)
df_scaled = pd.concat([df_scaled, df['amount']], axis=1)
df = df_scaled.copy()

# Split the dataframe into a training and testing set
X = df.loc[:, df.columns != 'amount']
y = df.amount
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Build neural network in Keras
model = Sequential()
model.add(Dense(128, activation='relu', input_dim=X_train.shape[1]))
model.add(BatchNormalization())
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(4, activation='relu'))
model.add(Dense(1))

# Compile model
model.compile(loss='mse', optimizer='adam', metrics=['mse'])

model.fit(X_train, y_train, epochs=1)
print(df.head())
print(X_train.shape[1])
# Results
train_pred = model.predict(X_train) * 100000000
print(train_pred)
print("------------------------------")
train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
test_pred = model.predict(X_test)
test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
print("Train RMSE: {:0.2f}".format(train_rmse))
print("Test RMSE: {:0.2f}".format(test_rmse))
print('------------------------')



