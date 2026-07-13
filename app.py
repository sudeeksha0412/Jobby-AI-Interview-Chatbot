"""
==================================================================
🧠 Smart AI Chatbot using Flask & Google Gemini
==================================================================
"""

import logging
import pytesseract
from flask import Flask, render_template, request, jsonify
from openrouter_setup import get_openrouter_response
from pypdf import PdfReader
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Sudeeksha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:

        user_message = request.form.get("message", "").strip()

        pdf = request.files.get("pdf")
        image = request.files.get("image")
        pdf_text = ""

        # ---------------- Extract PDF ----------------
        if pdf:
            reader = PdfReader(pdf)

            for page in reader.pages:
                text = page.extract_text()

                if text:
                    pdf_text += text + "\n"
        image_text = ""

        if image:
            img = Image.open(image)
            image_text = pytesseract.image_to_string(img)
            print(image_text)

        logging.info(f"User Message : {user_message}")
        logging.info(f"PDF Uploaded : {bool(pdf)}")

        # ---------------- Prompt ----------------
        if pdf_text:

            final_prompt = f"""
                You are Jobby.

                The user uploaded the following PDF.

                =====================
                PDF CONTENT
                =====================
                {pdf_text}

                =====================
                USER REQUEST
                =====================
                {user_message}

                            IMPORTANT RULES

1. ALWAYS use the uploaded PDF first.

2. If the user says:
- this pdf
- this document
- question 1
- question 2
- question 3
- answer the third question
- summarize this pdf
- explain question 2

then answer ONLY from the uploaded PDF.

3. If the PDF contains interview questions,
answer them.

4. If it contains coding questions,
include code.

5. Only use this reply when the user requests a specific question, section, or information that does not exist in the uploaded PDF.

Do NOT use this reply for requests like:
- Summarize this PDF
- Explain this PDF
- Answer all questions

6. Ignore your default interview restriction whenever a PDF is uploaded.
"""
        elif image_text:

                        final_prompt = f"""
                    You are Jobby.

                    The user uploaded an image.

                    IMAGE TEXT:

                    {image_text}

                    Rules:

                    1. Extract all readable text.

                    2. Decide whether the image contains interview-related content.

                    Examples:
                    - Java questions
                    - DBMS
                    - Aptitude
                    - Resume
                    - HR questions
                    - Programming code
                    - Networking
                    - Operating System
                    - DSA

                    3. If it is interview related:

                    Summarize it.

                    If it contains interview questions,
                    answer every question.

                    If it contains code,
                    explain the code.

                    4. If it is NOT interview related, reply:

                    "This image does not appear to contain interview-related content."

                    Do not guess unreadable text.
                    """
        else:
            final_prompt = user_message
        print("\n========== FINAL PROMPT ==========\n")
        print(final_prompt)
        print("\n==================================\n")
        # ---------------- Call AI ----------------
        response = get_openrouter_response(final_prompt)

        return jsonify({
            "response": response
        })

    except Exception as e:

        logging.exception(e)

        return jsonify({
            "response": "An error occurred while processing your request."
        })


if __name__ == "__main__":
    app.run(debug=True)