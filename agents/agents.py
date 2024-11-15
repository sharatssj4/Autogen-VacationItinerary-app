import os
from dotenv import load_dotenv
load_dotenv()
from chainlit_mods.modified_chainlit_agents import ChainlitAssistantAgent, ChainlitUserProxyAgent
import ast

llm_config = ast.literal_eval(os.environ["llm_config"])



user_proxy = ChainlitUserProxyAgent(
        name="User",
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("exit"),
        system_message="""Give the task, and send "
            "instructions to Flights to refine the budget and overall trip." 
            "Make sure flights uses the registered functions to complete the task"
            "use as less tokens as possible
        
        """,
        #Only say APPROVED in most cases, and say exit when nothing to be done further. Do not say others.
        code_execution_config=False,
        #default_auto_reply="Approved", 
        human_input_mode="ALWAYS",
        #llm_config=gpt4_config,
        )
flight_agent = ChainlitAssistantAgent(
            name="Flights",
            human_input_mode="NEVER",
            llm_config=llm_config,
            system_message='''You are gonna help user decide the flights. Ask the user for the flight origin and destination with the start date and return data.
            Number of passengers adults children.
            Seat type can be from economy, premium-economy, business or first class. 
            Origin and destination variable should be the airport ids.
            Dates will be of the format YYYY-MM-DD. if not convert them to YYYY-MM-DD.
            Make sure you have all 6 variables before you proceed further. Children is not needed default to 0.
            Call get_flights_roundtrip and display bullet list of flights in a proper format.
            Make sure the price is there
            You take feedback from the user and make a selection.
            use as less tokens as possible''',
            )
hotel_agent=  ChainlitAssistantAgent(
            name="Hotels",
            human_input_mode="NEVER",
            llm_config=llm_config,
            system_message="""You are gonna help user decide the Hotels in the destination.  
            Find the best accomodation in destination and display the hotel names and prices for the user.
            Show user the list of all Hotels available.
            Show the amount in dollars.
            After you display ask user to make a selection."""
            )
activies_agent = ChainlitAssistantAgent(
            name="Activities",
            human_input_mode="NEVER",
            system_message='''You are gonna help user decide the Activities in the destination.  
            Find the best activities in destination and display the activity names and prices for the user.
            Show user the list of all activities available.
            After you display ask user to make a selection.
            Show the amount in dollars.
            use as less tokens as possible
        ''',
            llm_config=llm_config,
                )
budget_agent = ChainlitAssistantAgent(
            name="Budget",
            system_message="""You are gonna help keep the Budget.  
            After every confirmation you will add the money for flights, hotel and activities to a total sum variable. Change the amount after every decision user makes.
            Show the budget at every step in dollars.
            use as less tokens as possible""",
            human_input_mode="NEVER",
                llm_config=llm_config,

            )