from typing_extensions import Annotated
from fast_flights import FlightData, Passengers, create_filter, get_flights, Airport
import autogen 
from agents.agents import flight_agent

def get_flights_roundtrip(origin: Annotated[str, "From flight airport id"],
                          destination: Annotated[str, "to flight airport id"],
                          fromdate: Annotated[str, "The initial trip date YYYY-MM-DD"],
                          todate: Annotated[str, "The return date YYYY-MM-DD"],
                          adults: Annotated[int, "Number of passengers"],
                          children: Annotated[int, "Number of children passenges defaults to 0 if not entered"],
                          seat: Annotated[str, "The seat type to be selected economy, premium-economy, business or first class"])-> Annotated[dict, "A list of flight details"]:
    filter = create_filter(
    flight_data=[
        FlightData(
            date=fromdate, 
            from_airport=origin, 
            to_airport=destination
        ), FlightData(
            date=todate,  
            from_airport=destination, 
            to_airport=origin
        ),
    
   
    ],
    trip="round-trip",  
    seat="economy",

    passengers=Passengers(
        adults=adults,
        children=children,
        infants_in_seat=0,
        infants_on_lap=0
    ),
    
)


    result = get_flights(filter,currency="usd")
    results=[]
    for flight in result.flights:
        if(flight.is_best):
            app_data = {
            "name": flight.name,
            "departure":flight.departure,
            "arrival":flight.arrival,
                "arrival_time_ahead":flight.arrival_time_ahead,
                "stops":flight.stops,
                "delay":flight.delay,
                "price":flight.price,
                    }
 
            results.append(app_data)
    return results 

def register_agent_tools():
    for caller in [flight_agent]:
            autogen.agentchat.register_function(
            get_flights_roundtrip,
            caller=flight_agent,
            executor=flight_agent,
            name="get_flights_roundtrip",
            description="Get details of the flights",
            )