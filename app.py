import chainlit as cl
import autogen
from agents.agents import user_proxy, flight_agent, activies_agent,hotel_agent,budget_agent
from dotenv import load_dotenv
import os
from agents.agent_tools import register_agent_tools
import ast
load_dotenv()

llm_config = ast.literal_eval(os.environ["llm_config"])


register_agent_tools()

TASK = "Plan a trip for the user from JFK to BLR on 17 nov 2024 and back on 30 nov 2024 with 2 adults and economy seats"

@cl.on_chat_start
async def on_chat_start():

    groupchat = autogen.GroupChat(agents=[user_proxy, flight_agent,activies_agent,hotel_agent,budget_agent], messages=[], max_round=10)
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    await cl.Message(content=f"Starting agents on task: {TASK}...").send()
    await cl.make_async(user_proxy.initiate_chat)(
        manager,
        message=TASK,
    )