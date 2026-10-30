
import json
import os
import streamlit as st
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# Ollama settings
OLLAMA_URL = os.environ.get(
    "OLLAMA_HOST", "http://localhost:11434"
).rstrip("/")

OLLAMA_MODEL = os.environ.get(
    "OLLAMA_MODEL", "gpt-oss:20b-cloud"
)

# Website layout
st.title("ClimateCheck AI")

st.write("Welcome to ClimateCheck AI!")

st.subheader("Analyse your local temperature")

st.write(
    "Find out how your current temperature compares "
    "with typical conditions."
)

# User inputs
userCountry = st.text_input("What country are you from?")

userTemperature = st.number_input(
    "What is the current temperature in Celsius?",
    min_value=-90.0,
    max_value=60.0
)

userMonth = st.selectbox(
    "What month is it?",
    [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]
)

# Analyse button
if st.button("Analyse temperature"):

    if not userCountry.strip():
        st.warning("Please enter a country.")

    else:

        prompt = f"""
        Analyse the temperature entered by the user.

        Country: {userCountry}
        Temperature: {userTemperature} degrees Celsius
        Month: {userMonth}

        Explain whether the temperature is cold, mild, warm, or hot.
        Discuss whether it is typical or unusual for that country
        at this time of year. Be clear if you are uncertain.
        Do not invent climate statistics.
        """

        data = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }

        request = Request(
            f"{OLLAMA_URL}/api/generate",
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with st.spinner("ClimateCheck AI is analysing the temperature..."):

            try:
                with urlopen(request, timeout=120) as response:
                    response_text = response.read().decode("utf-8")

                result = json.loads(response_text)

                if "response" in result:
                    st.subheader("ClimateCheck AI Analysis")
                    st.write(result["response"])

                else:
                    st.error("The AI response did not contain an answer.")

            except HTTPError as error:
                st.error(f"HTTP error: {error.code} - {error.reason}")

            except URLError as error:
                st.error(f"Could not connect to Ollama: {error.reason}")

            except json.JSONDecodeError:
                st.error("Could not understand Ollama's response.")

            except TimeoutError:
                st.error("Ollama took too long to respond. Please try again.")
