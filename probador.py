from dotenv import load_dotenv
import os

load_dotenv("gemini.env")
print(os.getenv("GEMINI_API_KEY"))
