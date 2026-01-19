import numpy as np
import pandas as pd
import os
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 1. Load the objects (Ensure these files are in your main folder)
scaler = joblib.load('scaler.joblib')
model = joblib.load('logistic_regression_model.joblib')

# 2. Define the exact columns your model expects
FEATURE_COLUMNS = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                   'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

@app.route("/", methods=["GET"])
def home():
    return "Diabetes Prediction API is running successfully."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data
        data = request.get_json(force=True)
        
        # If frontend sends a simple list, convert to dict first
        # Otherwise, assume it's a dict that matches our columns
        input_df = pd.DataFrame([data])

        # Ensure columns exist and are in the correct order
        for col in FEATURE_COLUMNS:
            if col not in input_df.columns:
                input_df[col] = 0 
        
        input_df = input_df[FEATURE_COLUMNS]

        # 3. Use the CORRECT variable names (scaler and model)
        scaled_input = scaler.transform(input_df)
        prediction = model.predict(scaled_input)
        prediction_proba = model.predict_proba(scaled_input)

        response = {
            'prediction': int(prediction[0]),
            'probability_no_diabetes': float(prediction_proba[0][0]),
            'probability_diabetes': float(prediction_proba[0][1])
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
