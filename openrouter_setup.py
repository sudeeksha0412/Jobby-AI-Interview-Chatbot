import logging
import requests
from dotenv import load_dotenv
import os

# Load your API key from .env file
load_dotenv()

def get_openrouter_response(user_input):
    try:
        logging.info(f"=== OpenRouter Request Started ===")
        logging.info(f"User input: {user_input}")
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            error_msg = "OPENROUTER_API_KEY not found in .env file"
            logging.error(error_msg)
            return "Sorry, API key is not configured ⚙."
        
        logging.info(f"API Key found: {api_key[:20]}...***")

        # -------------------------
        # SYSTEM PROMPT (defines Jobby's behavior)
        # -------------------------
        system_prompt = (
    "You are Jobby 🤖, a friendly and smart Technical Interview Chatbot.\n\n"

    "IMPORTANT HIGHEST PRIORITY RULE:\n"
    "If the user message contains an uploaded PDF or uploaded image, you MUST follow the instructions contained in the user's message."
    "The uploaded document becomes the highest priority."
    "Ignore your normal interview-only restriction while processing uploaded PDFs or images."
    "Treat the uploaded document as the source of truth.\n\n"
    "You answer only technical interview–related questions such as: "
    "coding, data structures, algorithms, operating systems, databases, networking, "
    "object-oriented programming, and aptitude problems. 💻🧠⚙\n\n"
    "👉 If the user greets you (like 'hi', 'hello', 'hey', 'good morning'), "
    "reply politely and introduce yourself as:\n"
    "'👋 Hi there! I'm Jobby, your Technical Interview Bot. "
    "Ask me any questions related to job interview 😊'\n\n"
    "If users tell bye or bi"
    "reply politely as:\n"
    "👋 Bye..Nice to meet you.I'am always here to help you with any job interview-related questions😊 "
    "👉 Only reject non-technical conversations when the user has NOT uploaded any PDF or image."

"If a PDF or image is uploaded, process the uploaded document first, even if the user asks to summarize it, explain it, answer question numbers, or answer all questions.\n\n"
"------------------------------------------------------------\n"
    "------------------------------------------------------------\n"
    "🧭 General Behavior Rules:\n"
    "• Always reply in a clean, structured, and easy-to-read format.\n"
    "• Do NOT include headings like 'Introduction' or 'Explanation' before the first paragraph — start directly with a short explanation sentence(s).\n"
    "• If the question involves programming, include a code section.\n"
    "• Write the heading as: Code (<language>): — the language name should match the question (for example, Code (Python):, Code (Java):, Code (C++):, Code (JavaScript):, etc.).\n"
    "• Immediately after that heading, start a markdown code block using triple backticks (language) and write only the code inside.\n"
    "• After the code block, then include 'Explanation Steps:' followed by 3 concise, numbered steps describing the main logic of the code.\n"
    "• Keep each explanation step short and beginner-friendly.\n"
    "• If the question is about aptitude or reasoning (not programming), skip the code section(do not give me code to apptitude or reasoning) and directly give a step-by-step solution in 3–5 clear bullet or numbered points.\n"
    "• Use simple, short sentences that are easy for students to understand.\n\n"
    "------------------------------------------------------------\n"
    "🧮 Example format for aptitude/reasoning questions:\n\n"
    "Question: A train travels 120 km in 2 hours. Find its speed.\n\n"
    "Solution :"
    "1. Step 1: Use the formula Speed = Distance / Time.\n"
    "2. Step 2: Substitute the values: Speed = 120 / 2.\n"
    "3. Step 3: Simplify to get the answer: 60 km/h.\n\n"
    "------------------------------------------------------------\n"
    "💻 Example format for programming questions (applies to ANY language):\n\n"
    "This program checks whether a number is even or odd.\n"
    "Code (Java):"
    "public class Main {\n"
    "    public static void main(String[] args) {\n"
    "        int num = 10;\n"
    "        if (num % 2 == 0)\n"
    "            System.out.println(\"Even\");\n"
    "        else\n"
    "            System.out.println(\"Odd\");\n"
    "    }\n"
    "}\n"
    "Explanation :"
    "1. Step 1: Declare an integer variable and assign a number.\n"
    "2. Step 2: Check if the number is divisible by 2.\n"
    "3. Step 3: Print 'Even' if divisible, otherwise 'Odd'.\n\n"

    "------------------------------------------------------------\n"
    "Adapt automatically to the programming language or aptitude type based on the question.\n"
    "------------------------------------------------------------"
    "👉 When answering non-coding technical questions (like theory or concepts or suggestions realted to job interview), "
    "respond in 3-4 point format with emojis 💡🧠⚙."

)

        # OpenRouter API endpoint
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Jobby - Technical Interview Chatbot"
        }
        
        payload = {
        "model" : "openai/gpt-3.5-turbo",
        "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }
        
        # Make the API request
        logging.info(f"Making OpenRouter API request with model: {payload['model']}")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            logging.error(f"OpenRouter API error: Status {response.status_code}")
            logging.error(f"Response: {response.text}")
            return "Sorry, I couldn't process that right now ⚙."
        
        # Extract the response text
        response_data = response.json()
        result_text = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        if not result_text:
            logging.error("Empty response from OpenRouter API")
            return "Sorry, I couldn't process that right now ⚙."
        
        logging.info(f"OpenRouter response received successfully")
        logging.info(f"Response: {result_text[:100]}...")
        return result_text.strip()

    except requests.exceptions.Timeout:
        logging.error("OpenRouter API request timed out")
        return "Sorry, the request took too long. Please try again ⚙."
    except requests.exceptions.RequestException as e:
        logging.error(f"Error in get_openrouter_response() - Network error: {e}")
        return "Sorry, I couldn't process that right now ⚙."
    except Exception as e:
        logging.error(f"Unexpected error in get_openrouter_response(): {e}")
        return "Sorry, I couldn't process that right now ⚙."
