from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.agent.workflow import FunctionAgent
import os
import asyncio
from Gsheets import* 

from dotenv import load_dotenv

load_dotenv()

llm=GoogleGenAI(
    model="gemini-2.0-flash",
    api_key=os.environ['GEMINI_API_KEY']
)

agent= FunctionAgent(
    tools=[get_alldetails],
    llm=llm,
    system_prompt="Your an expert data analyst, and given with spreadsheet data to carefully analyse"
)
async def main():
    response = await agent.run(user_msg="Look at my spreadsheet and tell the details")
    return response

# Call main function in an asynchronous context
if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)   


