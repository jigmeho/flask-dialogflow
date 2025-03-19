from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Flask server is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    
    # Lấy intent từ Dialogflow
    intent = req.get("queryResult", {}).get("intent", {}).get("displayName")

    # Xử lý intent
    if intent == "Chào hỏi":
        response_text = "Xin chào! Tôi có thể giúp gì cho bạn?"
    elif intent == "Hỏi giờ":
        response_text = "Bây giờ là 12:00 PM."
    else:
        response_text = "Tôi chưa hiểu yêu cầu của bạn."

    # Trả kết quả về Dialogflow
    return jsonify({
        "fulfillmentText": response_text
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=5000)
