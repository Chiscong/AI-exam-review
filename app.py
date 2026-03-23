import json
import os
import re

import docx
import google.generativeai as genai
import pdfplumber
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return os.path.splitext(filename.lower())[1] in ALLOWED_EXTENSIONS


def extract_text_from_docx(path):
    doc = docx.Document(path)
    lines = [paragraph.text.strip() for paragraph in doc.paragraphs if paragraph.text.strip()]
    return "\n".join(lines)


def extract_text_from_pdf(path):
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            if text.strip():
                pages.append(text.strip())
    return "\n".join(pages)


def normalize_ai_payload(payload):
    if not isinstance(payload, list):
        raise ValueError("AI response is not a JSON array")

    normalized = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ValueError(f"Question {index + 1} is not an object")

        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer_index = item.get("answer_index")
        image_url = str(item.get("image_url", "")).strip()

        if not question:
            raise ValueError(f"Question {index + 1} is missing question text")
        if not isinstance(options, list) or len(options) < 2:
            raise ValueError(f"Question {index + 1} has invalid options")

        cleaned_options = [str(option).strip() for option in options if str(option).strip()]
        if len(cleaned_options) < 2:
            raise ValueError(f"Question {index + 1} has empty options")

        if not isinstance(answer_index, int) or answer_index < 0 or answer_index >= len(cleaned_options):
            raise ValueError(f"Question {index + 1} has invalid answer_index")

        normalized.append(
            {
                "question": question,
                "options": cleaned_options,
                "answer_index": answer_index,
                "image_url": image_url or None,
            }
        )

    if not normalized:
        raise ValueError("AI did not return any valid questions")

    return normalized


def parse_ai_json(raw_text):
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\[[\s\S]*\]", cleaned)
        if not match:
            raise ValueError("AI response does not contain a valid JSON array")
        return json.loads(match.group(0))


def get_quiz_from_ai(text):
    # Prompt được tối ưu cho định dạng có dấu *
    prompt = f"""
    Bạn là một chuyên gia trích xuất dữ liệu. Hãy phân tích văn bản trắc nghiệm sau:
    1. Tìm các câu hỏi và 4 lựa chọn tương ứng.
    2. NHẬN DIỆN ĐÁP ÁN ĐÚNG: Đáp án đúng là lựa chọn có dấu sao (*) ở đầu.
    3. Yêu cầu trả về định dạng JSON array chuẩn:
       - "question": Nội dung câu hỏi.
       - "options": Mảng 4 lựa chọn (LƯU Ý: Phải XÓA dấu * và các ký tự A., B., C., D. ở đầu mỗi lựa chọn).
       - "answer_index": Số nguyên (0, 1, 2 hoặc 3) là vị trí của lựa chọn có dấu * lúc đầu.
    
    Văn bản cần xử lý:
    {text}
    """
    
    response = model.generate_content(prompt)
    # Loại bỏ các ký tự thừa để lấy JSON sạch
    clean_json = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(clean_json)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "No file uploaded"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only .pdf and .docx files are supported"}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    try:
        ext = os.path.splitext(filename.lower())[1]
        if ext == ".docx":
            text = extract_text_from_docx(path)
        else:
            text = extract_text_from_pdf(path)

        questions = get_quiz_from_ai(text)
        return jsonify(questions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
