"""Main webapp logic."""

import json
from typing import List, Dict, Any
import streamlit as st
from profiles import get_profile
from ai import ask_ai
from db import write_record_to_local_drive

st.title("Meal Planner")


def display_input_form() -> None:
    """Displays a form for the user to input their preferences and allergies."""
    with st.form("enduser_input_data"):
        profile = st.session_state.get("profile", {})

        st.subheader("Preferences and allergies")
        preferences = st.text_input("Preferences", value=profile.get("preferences", ""))
        allergies = st.text_input("Allergies", value=profile.get("allergies", ""))

        submit = st.form_submit_button("Save")
        if submit:
            handle_form_submission(preferences, allergies)


def handle_form_submission(preferences: str, allergies: str) -> None:
    """
    Handles the submission of the preferences and allergies form.

    Args:
        preferences (str): The user's meal preferences.
        allergies (str): The user's allergies.

    Saves the data to session state if both fields are filled out.
    """
    if preferences:
        st.session_state.profile = write_record_to_local_drive(preferences, allergies)
        with st.spinner("Saving..."):
            st.success("Information saved.")
    else:
        st.warning("Please provide preferences.")


def display_ai_suggestion() -> None:
    """Displays a button to generate and display an AI-generated meal suggestion based on user profile."""
    st.subheader("Ask recipe from AI")
    profile = st.session_state.get("profile", {})

    if st.button("Ask AI"):
        with st.spinner("Generating recipe..."):
            result = ask_ai(
                profile.get("preferences", ""), profile.get("allergies", "")
            )
            if result:
                display_ai_result(json.loads(result))


def display_ai_result(result_json: Dict[str, Any]) -> None:
    """
    Formats and displays the AI's meal suggestion result.

    Args:
        result_json (Dict[str, Any]): The JSON response from the AI containing the meal name,
                                      recipe steps, and ingredients.
    """
    st.header("Answer by AI")
    st.subheader("Suggested Meal", divider=True)
    st.text(result_json.get("meal_name", "No meal name provided"))

    st.subheader("Recipe", divider=True)
    for step in result_json.get("meal_recipe", []):
        st.caption(f"** {step}")

    st.subheader("Ingredients", divider=True)
    display_ingredients(result_json.get("ingredients", []))


def display_ingredients(ingredients: List[Dict[str, Any]]) -> None:
    """
    Displays a list of ingredients in a structured format with columns for name, quantity, and unit.

    Args:
        ingredients (List[Dict[str, Any]]): A list of ingredient dictionaries, each containing
                                            'name', 'quantity', and 'unit' keys.
    """
    col1, col2, col3 = st.columns([2, 1, 1])
    col1.write("Ingredient")
    col2.write("Quantity")
    col3.write("Unit")
    for ingredient in ingredients:
        col1, col2, col3 = st.columns([2, 1, 1])
        col1.write(ingredient.get("name", ""))
        col2.write(ingredient.get("quantity", ""))
        col3.write(ingredient.get("unit", ""))


def initialize_profile() -> None:
    """Initializes the user profile in session state if not already present."""
    if "profile" not in st.session_state:
        st.session_state.profile = get_profile()
        st.session_state.profile_id = 1


def main() -> None:
    """Main function to control the app's flow."""
    initialize_profile()
    display_input_form()
    display_ai_suggestion()


if __name__ == "__main__":
    main()
