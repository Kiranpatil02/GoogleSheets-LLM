from llama_index.llms.google_genai import GoogleGenAI
import os
import asyncio

from dotenv import load_dotenv

load_dotenv()

llm=GoogleGenAI(
    model="gemini-2.0-flash",
    api_key=os.environ['GEMINI_API_KEY']
)
def main():
    while True:
        text_input=input("User:")
        if text_input=="exit":
            break
        response_stream =  llm.stream_complete(text_input)
        for chunk in response_stream:
            print(chunk.delta, end="")

main()
