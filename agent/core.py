"""
Ladakh Travel & Tourism AI Agent
Core agent logic using LangChain.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

from agent.tools import get_tools

load_dotenv()


SYSTEM_TEMPLATE = """You are a friendly and knowledgeable Ladakh Travel Assistant. 
You help tourists plan safe and enjoyable trips to Ladakh, India.

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

IMPORTANT GUIDELINES:
- Always prioritize SAFETY, especially regarding altitude sickness (AMS)
- Be honest when you don't know something — suggest checking official sources
- Include cultural sensitivity tips when relevant
- For permits, always recommend checking the latest official requirements
- Mention weather unpredictability when discussing travel plans
- Keep responses concise but helpful
- Use a warm, welcoming tone

Question: {input}
{agent_scratchpad}"""


def create_agent():
    """Create and return the Ladakh travel agent."""
    
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.3,
        api_key=os.getenv("GROQ_API_KEY"),
    )
    
    tools = get_tools()
    
    prompt = PromptTemplate.from_template(SYSTEM_TEMPLATE)
    
    agent = create_react_agent(llm, tools, prompt)
    
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
    )
    
    return executor


def ask_agent(question: str) -> str:
    """Ask the agent a question and return the response."""
    executor = create_agent()
    result = executor.invoke({"input": question})
    return result["output"]
