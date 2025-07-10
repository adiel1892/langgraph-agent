from flask import Flask, request, jsonify
from finance_prebuilt_agent import run_agent

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handler():
    user_input = request.json.get("user_input", "")
    if not user_input:
        return jsonify({"error": "Missing user_input"}), 400
    result = run_agent(user_input)
    return jsonify({"response": result})
