import os
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

api_key = os.environ["GOOGLE_API_KEY"]
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=api_key)
print(llm.invoke("こんにちは、あなたは何ができますか？").content)
