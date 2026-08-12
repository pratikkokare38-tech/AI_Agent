from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain.agents import create_agent
# for google serper 
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool

from fastapi import FastAPI
from langserve import add_routes

search =GoogleSerperAPIWrapper()
llm = ChatGroq(model='openai/gpt-oss-20b')

# proper langchain tool
search_tool=Tool( name="google_serper",
       description="Search Google for current and up-to-date information.", 
     func=search.run )

# tools for llms that can convert my llm to agent because of tools and system_prompt
'''
tools=[search.run]
'''
tools=[search_tool]

# system_prompt
prompt="you are a assistant  and can search on google for user queries"

agent= create_agent(
    model=llm,
    tools=tools,
    system_prompt=prompt
)

app =FastAPI(
    title="My AI agent"
)

add_routes(
    app,
    agent,
    path="/agent"
    )

"""
query="who win the ipl 2026?"
'''
# this for invoking only a model/llm
response =llm.invoke(query)
'''
response=agent.invoke({"messages":[{"role":"user","content":query}]})

print(response["messages"][-1].content)"""


