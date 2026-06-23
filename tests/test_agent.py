from unittest.mock import patch

from agent import check_flight_price, get_weather, run_agent


def test_mock_tools():
    """Ensure local mock data structures resolve correctly for valid inputs."""
    assert "Rainy" in get_weather("tokyo")
    assert "$1200" in check_flight_price("tokyo")
    assert "Weather data not available." == get_weather("unknown_city")


@patch("agent.client.chat")
def test_run_agent_native_tool_call(mock_chat):
    """Verify processing logic when the model utilizes standard API tool calls."""
    # Step Turn 1: Simulate the model returning a standard structured tool call parameter array
    mock_response_1 = {
        "message": {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "function": {
                        "name": "get_weather",
                        "arguments": {"destination": "tokyo"},
                    }
                }
            ],
        }
    }
    # Step Turn 2: Simulate the final model answer turn summarizing the returned context data
    mock_response_2 = {
        "message": {
            "role": "assistant",
            "content": "The weather in Tokyo is rainy and around 15 degrees Celsius.",
        }
    }
    mock_chat.side_effect = [mock_response_1, mock_response_2]

    # Execute orchestrator loop
    run_agent("Check weather in Tokyo")
    assert mock_chat.call_count == 2


@patch("agent.client.chat")
def test_run_agent_fallback_xml_parser(mock_chat):
    """Verify processing logic when the model slips parameters into raw XML blocks."""
    # Step Turn 1: Simulate a non-compliant text block leaking raw XML tags into content
    rogue_content = (
        "<tools>\n"
        '{"name": "check_flight_price", "arguments": {"destination": "paris"}}\n'
        "</tools>"
    )
    mock_response_1 = {
        "message": {"role": "assistant", "content": rogue_content, "tool_calls": None}
    }
    # Step Turn 2: Simulate final loop convergence following successful data processing
    mock_response_2 = {
        "message": {
            "role": "assistant",
            "content": "Flights to Paris are currently pricing at $850.",
        }
    }
    mock_chat.side_effect = [mock_response_1, mock_response_2]

    # Execute orchestrator loop
    run_agent("Check flights to Paris")
    assert mock_chat.call_count == 2
