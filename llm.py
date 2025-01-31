import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API')

llm = ChatGoogleGenerativeAI(model="gemini-pro")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv('LANGSMITH_PROJECT')
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGSMITH_API_KEY')