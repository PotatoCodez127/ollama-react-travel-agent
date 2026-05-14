import os
import json
from dotenv import load_dotenv
from ollama import Client

load_dotenv()

client = Client(
    host='https://ollama.com',
    headers={'Authorization': f"Bearer {os.getenv('OLLAMA_API_KEY')}"}
)

# ==========================================
# 1. THE TOOLS (Mock APIs)
# ==========================================
def get_weather(destination: str) -> str:
    """Mock API to get the weather for a destination."""
    print(f"   [TOOL EXECUTION] Fetching weather for {destination}...")
    weather_db = {
        "tokyo": "Rainy, 15°C",
        "paris": "Sunny, 22°C",
        "london": "Cloudy, 12°C"
    }
    return weather_db.get(destination.lower(), "Weather data not available.")

def check_flight_price(destination: str) -> str:
    """Mock API to check flight prices."""
    print(f"   [TOOL EXECUTION] Checking flights to {destination}...")
    flight_db = {
        "tokyo": "$1200",
        "paris": "$850",
        "london": "$600"
    }
    return flight_db.get(destination.lower(), "Flight data not available.")

# We must define the tools in a schema so the LLM knows what it can do
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {"type": "string", "description": "The city name, e.g., Tokyo"}
                },
                "required": ["destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_flight_price",
            "description": "Get the cheapest flight price to a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {"type": "string", "description": "The city name, e.g., Tokyo"}
                },
                "required": ["destination"]
            }
        }
    }
]

# ==========================================
# 2. THE AGENT ORCHESTRATOR (ReAct Loop)
# ==========================================
def run_agent(user_prompt: str):
    print(f"\n🎯 USER GOAL: {user_prompt}\n")
    print("-" * 50)
    
    # We store the conversation history to maintain state
    messages = [
        {"role": "system", "content": "You are an autonomous travel agent. Use the provided tools to answer the user's request. You must gather all necessary data before giving a final answer."},
        {"role": "user", "content": user_prompt}
    ]
    
    # The Autonomous Loop (Max 5 iterations to prevent infinite loops)
    for step in range(5):
        print(f"🧠 AGENT THINKING (Step {step + 1})...")
        
        # 1. Ask the LLM what to do next
        response = client.chat(
            model="qwen3:480b-cloud", # Assuming you are using this cloud model
            messages=messages,
            tools=tools_schema
        )
        
        message = response['message']
        messages.append(message) # Save the AI's thought/action to history
        
        # 2. Check if the AI decided to use a Tool
        if not message.get('tool_calls'):
            # If no tools were called, the AI believes it has the final answer!
            print("\n✅ FINAL OUTPUT:")
            print(message['content'])
            break
            
        # 3. Execute the tools the AI requested
        for tool_call in message['tool_calls']:
            function_name = tool_call['function']['name']
            arguments = tool_call['function']['arguments']
            
            # Map the LLM's requested function name to our actual Python functions
            if function_name == "get_weather":
                result = get_weather(arguments['destination'])
            elif function_name == "check_flight_price":
                result = check_flight_price(arguments['destination'])
            else:
                result = "Error: Unknown function."
                
            # 4. Feed the tool's result BACK to the LLM as a "tool" role message
            messages.append({
                "role": "tool",
                "content": result,
                "name": function_name
            })
            
    print("-" * 50)

if __name__ == "__main__":
    # A complex prompt that requires multiple tool executions
    prompt = "I want to go to Tokyo. Can you tell me what the weather is like there right now and how much a flight would cost?"
    run_agent(prompt)