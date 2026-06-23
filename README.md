# ollama-react-travel-agent

[![CI Pipeline](https://github.com/potatocodez127/ollama-react-travel-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/potatocodez127/ollama-react-travel-agent/actions/workflows/ci.yml)

## Executive Summary
`ollama-react-travel-agent` is an institutional-grade autonomous agent orchestrator built around the ReAct (Reason + Act) loop execution pattern. The engine coordinates multi-step planning, dynamic tool-routing workflows, and runtime error mitigation to turn unstructured objectives into sequential API evaluations. It features a robust, regex-backed parsing recovery engine designed to trap and normalize rogue or malformed LLM tool call states.

## Architectural Ingenuity
* **Autonomous ReAct Orchestration**: Drives a stateful observation-and-action loop constrained by maximum iteration barriers to completely eliminate infinite processing loops during complex runtime sequences.
* **Universal Parser Fallback Subsystem**: Implements a fail-safe defensive tracking script that intercepts outputs when an LLM slips native protocol wrappers, automatically extracting and restructuring raw JSON/XML blocks into compliant execution structures.
* **Dependency-Free Test Architecture**: Utilizes localized mocking structures to intercept the cloud inference layer, providing comprehensive test coverage across our multi-step routing pipelines inside automated CI runners.
* **Parity-Locked Container Blueprint**: Packaged within a minimal, layer-cached `python:3.11-slim` Docker footprint with forced `TZ=UTC` clock synchronization to eliminate temporal session drift across distributed execution environments.

## System Topology & Control Loop
1. **Tool Definition Registry**: Exposes strict schema-validated utility definitions outlining parameters and data boundaries to instruct the underlying reasoning engine.
2. **Context Tracker**: Main state arrays aggregate operational histories, tool feedback blocks, and agent observations to give the system full memory continuity over its execution timeline.
3. **Defensive Normalization Layer**: Evaluates incoming text fields, traps structural discrepancies (such as leaked tags), normalizes function payloads, and routes the data to internal execution modules.
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