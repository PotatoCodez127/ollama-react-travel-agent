# Autonomous Travel Planner (Agentic Workflow)

## Overview
This project demonstrates the ReAct (Reason + Act) pattern. Instead of a single LLM prompt, this architecture uses an autonomous agent that can decide which tools to use, execute them, read the results, and course-correct if it encounters errors.

## The Problem Solved
Standard LLMs cannot interact with live systems or perform multi-step planning reliably. If a user wants to book a flight and check the weather, a single API call fails. Agents solve this by acting as orchestrators that route tasks to traditional APIs dynamically.

## Tech Stack
* **Python 3.10+**
* **Ollama Cloud:** For the LLM reasoning engine.
* **Custom Python Tools:** Mock APIs for weather and flight booking.

## Setup Instructions
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment.
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file and add your API key:
   `OLLAMA_API_KEY=your_api_key_here`

## Usage
Run the main agent loop:
`python agent.py`