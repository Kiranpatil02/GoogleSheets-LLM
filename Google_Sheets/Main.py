from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.agent.workflow import FunctionAgent
import os
import asyncio
from llama_index.core.workflow import Context
from Gsheets import* 

from dotenv import load_dotenv

load_dotenv()

llm=GoogleGenAI(
    model="gemini-2.0-flash-lite",
    api_key=os.environ['GEMINI_API_KEY']
)


agent= FunctionAgent(
    tools=[get_alldetails,create_Sheet,delete_Sheet,updateTitle,Get_allSheets,UpdateValue,get_entirecol,SelectSheet],
    llm=llm,
    system_prompt="Your an expert data analyst, and given with spreadsheet access, carefully select based on the user requrest and answer queries"
)
ctx=Context(agent)

async def main():
    while True:
        query=input("USER:")
        if query=="exit":
            break
        response = await agent.run(user_msg=str(query),ctx=ctx)
        print(f"Agent:{response}")
    

# Call main function in an asynchronous context
if __name__ == "__main__":
    result = asyncio.run(main())
    # print(result)   


