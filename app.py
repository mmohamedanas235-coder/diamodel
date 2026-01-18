import numpy as np
import pandas as pd
import os
import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the StandardScaler object
scaler = joblib.load('scaler.joblib')

# Load the Logistic Regression model
model = joblib.load('logistic_regression_model.joblib')


print("StandardScaler and Logistic Regression model loaded successfully.")
# Define a route for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get data from the POST request
    data = request.get_json(force=True)

    # Assuming the input data matches the format X_new
    # Convert the input data to a DataFrame, ensure column order, scale, and predict
    # For this example, we'll assume `data` is a dictionary where keys are feature names
    # and values are the input values for a single sample.
    # In a real application, you'd likely expect a list of dictionaries for batch prediction
    # or handle single samples carefully.

    # Create a DataFrame from the input data. We need to match the columns from X_new.
    # X_new columns are obtained from df_processed earlier.
    # For simplicity, we create a DataFrame from the incoming JSON data.
    input_df = pd.DataFrame([data])

    # Ensure the columns are in the same order as X_new during training (if X_new was a DataFrame originally)
    # If X_new was converted to numpy array directly, this step is crucial for consistency.
    # It's safest to rely on the columns of df_processed for ordering and existence.
    expected_columns = df_processed.drop('Outcome', axis=1).columns
    missing_cols = set(expected_columns) - set(input_df.columns)
    for c in missing_cols:
        input_df[c] = 0 # Or a default/mean value
    input_df = input_df[expected_columns]

    # Scale the input data
    scaled_input = scaler_new.transform(input_df)

    # Make prediction
    prediction = bayes_search_new.best_estimator_.predict(scaled_input)
    prediction_proba = bayes_search_new.best_estimator_.predict_proba(scaled_input)

    # Return the prediction as a JSON response
    response = {
        'prediction': int(prediction[0]),
        'probability_no_diabetes': prediction_proba[0][0],
        'probability_diabetes': prediction_proba[0][1]
    }

    print(f"Prediction request received: {data}")
    print(f"Predicted outcome: {response['prediction']}")
    print(f"Probabilities: {response['probability_no_diabetes']:.2f} (No), {response['probability_diabetes']:.2f} (Yes)")
    return jsonify(response)

print("Prediction route '/predict' defined successfully.")
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
