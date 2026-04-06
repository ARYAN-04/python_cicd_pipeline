from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route("/add", methods=["POST"])
def add_numbers():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "a" not in data or "b" not in data:
        return jsonify(
            {"error": "Missing required fields: 'a' and 'b' are required"}
        ), 400

    try:
        a = float(data["a"])
        b = float(data["b"])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input: 'a' and 'b' must be numeric"}), 400

    return jsonify({"result": a + b}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
