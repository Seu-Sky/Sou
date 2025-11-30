from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Nạp biến môi trường
load_dotenv()

my_api_key = os.getenv("GOOGLE_API_KEY")

if not my_api_key:
    print("LỖI: Không tìm thấy API Key! Hãy kiểm tra file .env")
else:
    print("Đã tìm thấy API Key, đang cấu hình...")
    genai.configure(api_key=my_api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

chat = model.start_chat(history=[])

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "")
        
        if not question:
            return jsonify({"answer": "Bạn chưa nhập câu hỏi!"})

        # Gửi tin nhắn cho Gemini
        response = chat.send_message(question)
        
        # Trả về text câu trả lời
        return jsonify({"answer": response.text})

    except Exception as e:
        print(f"Lỗi: {e}") # In lỗi ra terminal để dễ debug
        return jsonify({"answer": "Xin lỗi, hệ thống đang bận hoặc key bị lỗi."})

if __name__ == "__main__":
    app.run(debug=True)
    