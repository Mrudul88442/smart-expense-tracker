import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("FINANCIAL_AI_API_KEY")
# If you want to paste key directly:
# API_KEY = "YOUR_API_KEY"

client = genai.Client(api_key=API_KEY)

def get_ai_response(prompt):
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",   # ✅ Correct model name
            contents=prompt
        )

        # New API always provides .text
        return response.text if hasattr(response, "text") else "No response text."

    except Exception as e:
        return f"AI Error: {str(e)}"
