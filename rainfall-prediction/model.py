import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle

raw_df = pd.read_csv('C:/college/Python/machine-learning/rainfall-prediction/weatherAUS.csv')
raw_df.dropna(subset=['RainTomorrow'], inplace=True)


"""Creating training, validation and test data sets
Year < 2015 is for training data set
Year > 2015 is for test data set"""
year = pd.to_datetime(raw_df.Date).dt.year
train_df = raw_df[year <= 2015]
test_df = raw_df[year > 2015]

#Identifying input and target columns
input_cols = list(train_df.columns)[1:-1]
target_col = 'RainTomorrow'

train_inputs = train_df[input_cols].copy()
train_targets = train_df[target_col].copy()
test_inputs = test_df[input_cols].copy()
test_targets = test_df[target_col].copy()

#Identifying input and target columns
numeric_cols = train_inputs.select_dtypes(include=np.number).columns.tolist()
categorical_cols = train_inputs.select_dtypes('object').columns.tolist()

#imputing missing values
imputer = SimpleImputer(strategy = 'mean').fit(raw_df[numeric_cols])
train_inputs[numeric_cols] = imputer.transform(train_inputs[numeric_cols])
test_inputs[numeric_cols] = imputer.transform(test_inputs[numeric_cols])

#Scaling values from 0 to 1
scaler = MinMaxScaler().fit(raw_df[numeric_cols])
train_inputs[numeric_cols] = scaler.transform(train_inputs[numeric_cols])
test_inputs[numeric_cols] = scaler.transform(test_inputs[numeric_cols])

#encoding categorical data
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore').fit(raw_df[categorical_cols])
encoded_cols = list(encoder.get_feature_names_out(categorical_cols))
train_inputs[encoded_cols] = encoder.transform(train_inputs[categorical_cols])
test_inputs[encoded_cols] = encoder.transform(test_inputs[categorical_cols])

#Drop the textual categorical columns so that we are left with only numeric values
X_train = train_inputs[numeric_cols + encoded_cols]
X_test = test_inputs[numeric_cols + encoded_cols]

model = RandomForestClassifier( 
                                n_jobs=-1,
                                random_state=42,
                                n_estimators=20,
                                max_features=7,
                                max_depth=30,
                                class_weight={
                                  'No':1,
                                  'Yes':1.5
                                }
                              )

model.fit(X_train, train_targets)

def predict_input(model, single_input):
  inputs_df = pd.DataFrame([single_input])
  inputs_df[numeric_cols] = imputer.transform(inputs_df[numeric_cols])
  inputs_df[numeric_cols] = scaler.transform(inputs_df[numeric_cols])
  inputs_df[encoded_cols] = encoder.transform(inputs_df[categorical_cols])
  X_input = inputs_df[numeric_cols + encoded_cols]
  pred = model.predict(X_input)[0]
  prob = model.predict_proba(X_input)[0][list(model.classes_).index(pred)]
  return pred, prob

pickle.dump(imputer, open("C:/college/Python/machine-learning/rainfall-prediction/imputer.pkl","wb"))
pickle.dump(scaler, open("C:/college/Python/machine-learning/rainfall-prediction/scaler.pkl","wb"))
pickle.dump(encoder, open("C:/college/Python/machine-learning/rainfall-prediction/encoder.pkl","wb"))
pickle.dump(model, open("C:/college/Python/machine-learning/rainfall-prediction/model.pkl","wb"))


