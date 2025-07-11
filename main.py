import functions_framework
from flask import jsonify, Request
from finance_prebuilt_agent import run_agent

@functions_framework.http
def handler(request: Request):
    request_json = request.get_json(silent=True)
    user_input = request_json.get("user_input", "") if request_json else ""

    if not user_input:
        return jsonify({"error": "Missing user_input"}), 400

    result = run_agent(user_input)
    return jsonify({"response": result})
