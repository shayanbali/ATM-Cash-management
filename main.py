# author : Shayan Bali

import matplotlib
from utils import preprocess

matplotlib.use("TkAgg")
# from utils import preprocess, feature_engineer
import pandas as pd
import numpy as np
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import BatchNormalization
from sklearn.metrics import mean_squared_error

# Getting Data set
try:
    a = input("please enter file : ")
    print("Reading in the dataset. This will take some time...")
    df = pd.read_csv(a, nrows=720)
    print("Forecast day info \n")
    year = input("year : ")
    month = input("month : ")
    day = input("day : ")
    week = input("week (start with capital letter) : ")
    typee = input("type of day (0-> Normal day 1-> Holiday 2-> Friday) : ")
    dict = {'amount': df['amount'].mean(), 'year': int(year), 'month': int(month), 'day': int(day), 'week': week, 'holiday': int(typee), 'avg': 0, 'season': 0, 'before': 0, 'beginning': 0}

    df = df.append(dict, ignore_index=True)

except:
    print("""
      can not import dataset
      """)
    quit()

# Preprocess data
avg = df['amount'].mean()
df_copy = df.copy()
df = preprocess(df)

print(df.loc[df['week'] == 'Friday', ['week']])
print(df.head())

# Scales the features
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

# Builds neural network in Keras
model = Sequential()
model.add(Dense(1000, activation='relu'
                , input_dim=X_train.shape[1]))
model.add(BatchNormalization())
model.add(Dense(800, activation='relu'))
model.add(Dense(400, activation='relu'))
model.add(Dense(1))

# Compile model
model.compile(loss='mse', optimizer='adam', metrics=['mse'])

model.fit(X_train, y_train, epochs=5050)

# getting layer's weights
# for layer in model.layers:
#     weights = layer.get_weights() # list of numpy arrays

# shows part of our dataset after scaling and preprocessing
print(df.head())
print(X_train.shape[1])

# Results
train_pred = model.predict(X_train)
print("------------------------------")
train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
test_pred = model.predict(X_test)
test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
print("Train RMSE: {:0.2f}".format(train_rmse))
print("Test RMSE: {:0.2f}".format(test_rmse))
print('------------------------')


# predict a random day in our data set
def predict_random(df_prescaled, X_test, model):
    sample = X_test.sample(n=1, random_state=np.random.randint(low=0, high=50))
    idx = sample.index[0]

    actual_fare = df_prescaled.loc[idx, 'amount']
    day_names = ['Sunday', 'monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    day_of_week = df_copy.loc[idx, 'week']
    year = df_prescaled.loc[idx, 'year']
    month = df_prescaled.loc[idx, 'month']
    day = df_prescaled.loc[idx, 'day']
    predicted_fare = model.predict(sample)[0][0]
    rmse = np.sqrt(np.square(predicted_fare - actual_fare))

    print("withdraw Details: {}, {}-{}-{}".format(day_of_week, year, month, day))
    print("Actual fare: ${:0.2f}".format(actual_fare))
    print("Predicted fare: ${:0.2f}".format(predicted_fare))
    print("RMSE: ${:0.2f}".format(rmse))
    print("Train average: ", df_prescaled['amount'].mean())
    print("\n")

# prediction function
def prediction(df_prescaled, x, model):
    sample = x.tail(1)
    idx = sample.index[0]

    actual_fare = df_prescaled.loc[idx, 'amount']
    day_names = ['Sunday', 'monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    day_of_week = df_copy.loc[idx, 'week']
    year = df_prescaled.loc[idx, 'year']
    month = df_prescaled.loc[idx, 'month']
    day = df_prescaled.loc[idx, 'day']
    predicted_fare = model.predict(sample)[0][0]
    rmse = np.sqrt(np.square(predicted_fare - actual_fare))

    print("withdraw Details: {}, {}-{}-{}".format(day_of_week, year, month, day))
    #print("Actual fare: ${:0.2f}".format(actual_fare))
    print("Predicted fare: ${:0.2f}".format(predicted_fare))
    #print("RMSE: ${:0.2f}".format(rmse))
    print("Train average: ", df_prescaled['amount'].mean())


predict_random(df_prescaled, X_test, model)
prediction(df_prescaled, X, model)
