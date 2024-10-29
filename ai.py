"""Handle AI flow using Langflow."""

from typing import Dict
from langflow.load import run_flow_from_json
from dotenv import load_dotenv


load_dotenv()


def ask_ai(preferences: str, allergies: str) -> str:
    """
    Sends user preferences and allergies to an AI flow to generate a response.

    Args:
        preferences (str): The user's meal preferences.
        allergies (str): The user's allergies.

    Returns:
        str: The AI-generated response text.
    """
    tweaks = _prepare_tweaks(preferences, allergies)
    result = _run_ai_flow(tweaks)

    return _extract_result_text(result)


def _prepare_tweaks(preferences: str, allergies: str) -> Dict[str, Dict[str, str]]:
    """
    Prepares tweaks for the AI flow with user input values.

    Args:
        preferences (str): The user's preferences.
        allergies (str): The user's allergies.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary of tweaks for the AI flow.
    """
    return {
        "TextInput-AM18s": {"input_value": preferences},
        "TextInput-Vfnaq": {"input_value": allergies},
    }


def _run_ai_flow(tweaks: Dict[str, Dict[str, str]]) -> list:
    """
    Runs the AI flow with the provided tweaks.

    Args:
        tweaks (Dict[str, Dict[str, str]]): The input tweaks for the AI flow.

    Returns:
        list: The result output from the AI flow.
    """
    return run_flow_from_json(
        flow="langflow_recipe_flow.json",
        input_value="message",
        fallback_to_env_vars=True,
        tweaks=tweaks,
    )


def _extract_result_text(result: list) -> str:
    """
    Extracts the AI-generated response text from the flow result.

    Args:
        result (list): The output result list from the AI flow.

    Returns:
        str: The extracted text response from the AI.
    """
    try:
        return result[0].outputs[0].results["text"].data["text"]
    except (IndexError, KeyError, TypeError) as e:
        raise ValueError("Unexpected format in AI response") from e
