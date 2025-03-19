from flask import Flask, request, jsonify
from google.cloud import dialogflow
import os
import json

app = Flask(__name__)

# Đọc biến môi trường từ GOOGLE_APPLICATION_CREDENTIALS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "phat-phap-pho-thong-gnlg"

# Hàm gửi tin nhắn tới Dialogflow
def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(request={"session": session, "query_input": query_input})

    return response.query_result.fulfillment_text

@app.route("/", methods=["GET"])
def home():
    return "Flask-Dialogflow Webhook is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True, force=True)
    session_id = req.get("session", "").split("/")[-1]
    text = req["queryResult"]["queryText"]
    project_id = os.getenv("DIALOGFLOW_PROJECT_ID", "your-dialogflow-project-id")
    
    response_text = detect_intent_texts(project_id, session_id, text, "vi")

    return jsonify({"fulfillmentText": response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
