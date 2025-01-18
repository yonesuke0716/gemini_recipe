import os
import google.generativeai as genai

api_key = os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("こんにちは、あなたは何ができますか？")
print(response.text)
