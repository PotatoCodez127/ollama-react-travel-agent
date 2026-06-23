import json
import os
import re
from dotenv import load_dotenv
from ollama import Client

load_dotenv()

client = Client(
    host="https://ollama.com",
    headers={"Authorization": f"Bearer {os.getenv('OLLAMA_API_KEY')}"},
)


# ==========================================
# 1. THE TOOLS (Mock APIs)
# ==========================================
def get_weather(destination: str) -> str:
    """Mock API to get the weather for a destination."""
    print(f"   [TOOL EXECUTION] Fetching weather for {destination}...")
    weather_db = {"tokyo": "Rainy, 15°C", "paris": "Sunny, 22°C", "london": "Cloudy, 12°C"}
    return weather_db.get(destination.lower(), "Weather data not available.")


def check_flight_price(destination: str) -> str:
    """Mock API to check flight prices."""
    print(f"   [TOOL EXECUTION] Checking flights to {destination}...")
    flight_db = {"tokyo": "$1200", "paris": "$850", "london": "$600"}
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
                    "destination": {
                        "type": "string",
                        "description": "The city name, e.g., Tokyo",
                    }
                },
                "required": ["destination"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_flight_price",
            "description": "Get the cheapest flight price to a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string",
                        "description": "The city name, e.g., Tokyo",
                    }
                },
                "required": ["destination"],
            },
        },
    },
]


# ==========================================
# 2. THE AGENT ORCHESTRATOR (ReAct Loop)
# ==========================================
def run_agent(user_prompt: str):
    print(f"\n🎯 USER GOAL: {user_prompt}\n")
    print("-" * 50)

    # We store the conversation history to maintain state
    messages = [
        {
            "role": "system",
            "content": (
                "You are an autonomous travel agent. Use the provided tools to "
                "answer the user's request. You must gather all necessary data "
                "before giving a final answer."
            ),
        },
        {"role": "user", "content": user_prompt},
    ]

    # The Autonomous Loop (Max 5 iterations to prevent infinite loops)
    for step in range(5):
        print(f"🧠 AGENT THINKING (Step {step + 1})...")

        # 1. Ask the LLM what to do next
        response = client.chat(
            model="gemma4:31b-cloud",
            messages=messages,
            tools=tools_schema,
        )

        message = response["message"]
        messages.append(message)

        # --- THE UNIVERSAL PARSER ENHANCEMENT ---
        tool_calls_to_execute = []

        # Case A: The model played nice and used the native API structure
        if message.get("tool_calls"):
            tool_calls_to_execute = message["tool_calls"]

        # Case B: The model went rogue and leaked XML or JSON directly into the text
        elif message.get("content"):
            raw_text = message["content"]

            # Catch <tools> JSON </tools> format
            if "<tools>" in raw_text or "<tool_call>" in raw_text:
                print("   [DEBUG] Intercepted raw XML tool call!")

                # Top-level brace-tracking stack algorithm to handle nested structures
                matches = []
                brace_stack = []
                start_index = -1

                for idx, char in enumerate(raw_text):
                    if char == "{":
                        if not brace_stack:
                            start_index = idx
                        brace_stack.append(char)
                    elif char == "}":
                        if brace_stack:
                            brace_stack.pop()
                            if not brace_stack:
                                matches.append(raw_text[start_index : idx + 1])

                for match in matches:
                    try:
                        parsed_tool = json.loads(match)
                        if "name" in parsed_tool and "arguments" in parsed_tool:
                            # Format it to match the standard API structure
                            tool_calls_to_execute.append(
                                {
                                    "function": {
                                        "name": parsed_tool["name"],
                                        "arguments": parsed_tool["arguments"],
                                    }
                                }
                            )
                    except json.JSONDecodeError:
                        continue
        # ----------------------------------------

        # 2. Check if the AI decided to use a Tool
        if not tool_calls_to_execute:
            print("\n✅ FINAL OUTPUT:")
            print(message["content"])
            with open("Outputs.txt", "a", encoding="utf-8") as file:
                file.write(message["content"] + "\n")
            break

        # 3. Execute the tools (using our new normalized list)
        for tool_call in tool_calls_to_execute:
            function_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]

            # (The rest of your execution logic remains exactly the same...)
            if function_name == "get_weather":
                result = get_weather(arguments["destination"])
            elif function_name == "check_flight_price":
                result = check_flight_price(arguments["destination"])
            else:
                result = "Error: Unknown function."

            messages.append({"role": "tool", "content": result, "name": function_name})

    print("-" * 50)


if __name__ == "__main__":
    # A complex prompt that requires multiple tool executions
    prompt = (
        "I want to go to Tokyo. Can you tell me what the weather is like "
        "there right now and how much a flight would cost?"
    )
    run_agent(prompt)