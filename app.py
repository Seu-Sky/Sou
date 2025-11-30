from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# cấu hình Gemini
API_KEY = "AIzaSyClxR_UHkxh5Yl_Kiw8cvYm5XAWoofd7d0"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")
chat = model.start_chat()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")   # load giao diện

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    try:
        answer = chat.send_message(question)
        return jsonify({"answer": answer.text})
    except Exception as e:
        return jsonify({"answer": f"Đã xảy ra lỗi: {e}"})


if __name__ == "__main__":
    app.run(debug=True)
