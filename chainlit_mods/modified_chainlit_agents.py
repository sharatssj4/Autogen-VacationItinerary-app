from autogen import Agent, AssistantAgent, UserProxyAgent, config_list_from_json
import chainlit as cl
from typing import Dict, Optional, Union

async def ask_helper(func, **kwargs):
    res = await func(**kwargs).send()
    while not res:
        res = await func(**kwargs).send()
    return res

class ChainlitAssistantAgent(AssistantAgent):
    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ) -> bool:
        if type(message) is dict:
            if message["content"]!=None and message["role"]!="tool":
                cl.run_sync(
                            cl.Message(
                                content=f'{self.name}:\n\n{message}',
                                author=self.name,
                            ).send()
                        )
        else:
         cl.run_sync(
                            cl.Message(
                                content=f'{self.name}:\n\n{message}',
                                author=self.name,
                            ).send()
                        )
        super(ChainlitAssistantAgent, self).send(
                message=message,
                recipient=recipient,
                request_reply=request_reply,
                silent=silent,
        )

class ChainlitUserProxyAgent(UserProxyAgent):
    def get_human_input(self, prompt: str) -> str:
        reply = cl.run_sync(ask_helper(cl.AskUserMessage, content=prompt, timeout=60))
        return reply["output"].strip()
        


    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        if type(message) is dict:
            cl.run_sync(
            cl.Message(
                content=f"{self.name}:\n\nYou selected option(s) {message['content']}",
                author="UserProxyAgent",
            ).send()
            )
        else:
             cl.run_sync(
            cl.Message(
                content=f'{self.name}:\n\n{message}',
                author="UserProxyAgent",
            ).send()
            )   
        super(ChainlitUserProxyAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )
