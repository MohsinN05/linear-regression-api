
import random
from flask import Flask, request, jsonify

REGISTRATION_NUMBER = "FA23-BDS-021"

# Deterministically generate the coefficients.
random.seed(REGISTRATION_NUMBER)

a1 = random.uniform(-5, 5)
a2 = random.uniform(-5, 5)
a3 = random.uniform(-5, 5)
b = random.uniform(-10, 10)

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200


@app.route("/predict", methods=["GET"])
def predict():
    try:
        x1 = float(request.args["x1"])
        x2 = float(request.args["x2"])
        x3 = float(request.args["x3"])
    except KeyError as exc:
        return jsonify({
            "error": f"Missing required parameter: {exc.args[0]}"
        }), 400
    except ValueError:
        return jsonify({
            "error": "x1, x2, and x3 must be numeric"
        }), 400

    prediction = a1 * x1 + a2 * x2 + a3 * x3 + b

    return jsonify({
        "registration number": REGISTRATION_NUMBER,
        "prediction": round(prediction, 2)
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
