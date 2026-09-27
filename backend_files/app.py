
from flask import Flask, request, jsonify
import pandas as pd
import joblib

# Initialize Flask application
superkart_api = Flask(__name__)

# Load the trained ML model
model = joblib.load("superkart_model.joblib")


# Health check endpoint
@superkart_api.route("/", methods=["GET"])
def home():

    return jsonify(
        {
            "message":
            "SuperKart Sales Prediction API is running"
        }
    )


# Single prediction endpoint
@superkart_api.route(
    "/v1/predict",
    methods=["POST"]
)
def predict():

    try:

        # Receive JSON request
        input_data = request.get_json()

        # Convert JSON into dataframe
        input_df = pd.DataFrame(
            [input_data]
        )

        # Make prediction
        prediction = model.predict(
            input_df
        )[0]

        # Return prediction
        return jsonify(
            {
                "predicted_sales":
                float(prediction)
            }
        )

    except Exception as e:

        return jsonify(
            {
                "error": str(e)
            }
        ), 400


# Batch prediction endpoint
@superkart_api.route(
    "/v1/predictbatch",
    methods=["POST"]
)
def predict_batch():

    try:

        # Check whether CSV file exists
        if "file" not in request.files:

            return jsonify(
                {
                    "error":
                    "CSV file not provided"
                }
            ), 400

        # Read uploaded file
        file = request.files["file"]

        input_df = pd.read_csv(file)

        # Generate predictions
        predictions = model.predict(
            input_df
        )

        # Convert predictions to JSON
        result = {
            str(index): float(prediction)
            for index, prediction
            in enumerate(predictions)
        }

        return jsonify(result)

    except Exception as e:

        return jsonify(
            {
                "error": str(e)
            }
        ), 400


# Start Flask API
if __name__ == "__main__":

    superkart_api.run(
        host="0.0.0.0",
        port=7860
    )
