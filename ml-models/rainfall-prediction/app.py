from flask import Flask, render_template, request
import pickle
import pandas as pd

# Load the saved model, scaler, imputer, and encoder
model = pickle.load(open('C:/college/Python/machine-learning/rainfall-prediction/model.pkl', 'rb'))
imputer = pickle.load(open('C:/college/Python/machine-learning/rainfall-prediction/imputer.pkl', 'rb'))
scaler = pickle.load(open('C:/college/Python/machine-learning/rainfall-prediction/scaler.pkl', 'rb'))
encoder = pickle.load(open('C:/college/Python/machine-learning/rainfall-prediction/encoder.pkl', 'rb'))

# Define input columns based on the HTML form
numeric_cols = ['MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine', 'WindGustSpeed',
                'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm', 'Pressure9am', 
                'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Temp9am', 'Temp3pm']

categorical_cols = ['Location', 'WindGustDir', 'WindDir9am', 'WindDir3pm', 'RainToday']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Gather input data from form
    input_data = {
        'Date': request.form['Date'],
        'Location': request.form['Location'],
        'MinTemp': float(request.form['MinTemp']),
        'MaxTemp': float(request.form['MaxTemp']),
        'Rainfall': float(request.form['Rainfall']),
        'Evaporation': float(request.form['Evaporation']),
        'Sunshine': float(request.form['Sunshine']) if request.form['Sunshine'] else 0.0,
        'WindGustDir': request.form['WindGustDir'],
        'WindGustSpeed': float(request.form['WindGustSpeed']),
        'WindDir9am': request.form['WindDir9am'],
        'WindDir3pm': request.form['WindDir3pm'],
        'WindSpeed9am': float(request.form['WindSpeed9am']),
        'WindSpeed3pm': float(request.form['WindSpeed3pm']),
        'Humidity9am': float(request.form['Humidity9am']),
        'Humidity3pm': float(request.form['Humidity3pm']),
        'Pressure9am': float(request.form['Pressure9am']),
        'Pressure3pm': float(request.form['Pressure3pm']),
        'Cloud9am': float(request.form['Cloud9am']),
        'Cloud3pm': float(request.form['Cloud3pm']),
        'Temp9am': float(request.form['Temp9am']),
        'Temp3pm': float(request.form['Temp3pm']),
        'RainToday': request.form['RainToday']
    }

    # Convert input data to DataFrame
    inputs_df = pd.DataFrame([input_data])

    # Process numeric and categorical columns
    inputs_df[numeric_cols] = imputer.transform(inputs_df[numeric_cols])
    inputs_df[numeric_cols] = scaler.transform(inputs_df[numeric_cols])
    inputs_df[encoder.get_feature_names_out(categorical_cols)] = encoder.transform(inputs_df[categorical_cols])

    # Prepare inputs for prediction
    X_input = inputs_df[numeric_cols + list(encoder.get_feature_names_out(categorical_cols))]

    # Make prediction
    pred = model.predict(X_input)[0]
    prob = model.predict_proba(X_input)[0][list(model.classes_).index(pred)]

    prediction_text = f'Rain Tomorrow: {pred}, Probability: {prob:.2f}'

    # Render the result
    return render_template('index.html', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True)
