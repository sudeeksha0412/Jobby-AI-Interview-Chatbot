# 🤖 Jobby – AI Technical Interview Helper

An AI-powered Technical Interview Helper that assists users in preparing for technical interviews through voice interaction, PDF and image analysis, and intelligent question answering.

Built using **Flask** and **OpenRouter**.

---

## ✨ Features

- 💬 Technical interview question answering
- 🎤 Voice input (Speech-to-Text)
- 🔊 Voice output (Text-to-Speech)
- 📄 PDF upload and analysis
- 🖼️ Image upload with OCR (Tesseract OCR)
- 📚 PDF summarization
- 📝 Automatic interview question detection
- 💻 Programming solutions with explanations
- ⚡ Interactive chatbot interface

---

## 🛠️ Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- OpenRouter API
- PyPDF
- Pillow
- Tesseract OCR
- Speech Recognition API
- Speech Synthesis API

---

## 📂 Project Structure

```
Jobby-AI-Interview-Chatbot/
│
├── app.py
├── openrouter_setup.py
├── requirements.txt
├── static/
├── templates/
├── README.md
└── .gitignore
```

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/sudeeksha0412/Jobby-AI-Interview-Chatbot.git
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

```
OPENROUTER_API_KEY=your_api_key
```

### 4. Install Tesseract OCR

Download and install Tesseract OCR and update the executable path in `app.py`.

Example:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\YourName\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
```

### 5. Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 🎯 Project Capabilities

- Answer technical interview questions
- Summarize interview PDFs
- Answer questions from uploaded PDFs
- Extract interview questions from images
- Explain programming questions with code
- Support voice-based interaction
- Interactive chatbot UI

---
---

## 📸 Screenshots

### 💬 Chatbot Interface

Interactive chatbot interface for asking interview-related questions.

![Chatbot Interface](ScreenShots/chatbot.png)

---

### 💻 Technical Interview Question

Example of answering a technical interview question with explanation.

![Technical Interview](ScreenShots/Techinical.png)

---

### 📄 PDF Upload & Analysis

Upload an interview PDF and ask questions or summarize its contents.

![PDF Upload](ScreenShots/PdfInput.png)

---

### 🖼️ Image OCR Analysis

Upload an image containing interview questions. The chatbot extracts the text using OCR and processes it.

![Image OCR](ScreenShots/ImageInput.png)

---

### 📝 Multiple Question Answering

Answer multiple interview questions can be answered at a time.

![Multiple Questions](ScreenShots/MultipleQuestion Ans.png)
![Voice Interaction](ScreenShots/Screenshot 2026-07-13 184839.png)

---

### 🧠 Interview Suggestions

Provides interview preparation guidance and suggestions.

![Interview Suggestions](ScreenShots/InterviewSuggestion.png)

---

### 📊 Aptitude Question Solving

Supports aptitude and reasoning questions with step-by-step explanations.

![Aptitude](ScreenShots/Aptitude.png)

---

### 🎤 Voice-Based Interaction

Supports voice input and voice output for hands-free interview preparation.We can click on mic to give the voice input which converted into text and if we want bot to give voice output

![Voice Interaction](ScreenShots/Screenshot 2026-07-13 184839.png)

## 👩‍💻 Author

**Sudeeksha **

B.E. Information Science & Engineering

Canara Engineering College

GitHub: https://github.com/sudeeksha0412
