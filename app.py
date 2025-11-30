from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Nạp biến môi trường từ file .env
load_dotenv()

# 2. Lấy key an toàn từ file .env
# Lưu ý: Trong file .env bạn phải đặt là GOOGLE_API_KEY=AIza...
my_api_key = os.getenv("GOOGLE_API_KEY")

# 3. Kiểm tra xem đã lấy được key chưa
if not my_api_key:
    print("LỖI: Không tìm thấy API Key! Hãy kiểm tra file .env")
else:
    print("Đã tìm thấy API Key, đang cấu hình...")
    genai.configure(api_key=my_api_key)

# Khởi tạo model (Dùng bản 1.5 flash cho ổn định và rẻ/miễn phí)
model = genai.GenerativeModel("gemini-2.5-flash")

# Lưu ý: Chat history để ở đây là biến toàn cục (Global). 
# Nếu nhiều người dùng cùng lúc, họ sẽ thấy tin nhắn của nhau.
# Nhưng để học tập thì tạm thời chấp nhận được.
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
    