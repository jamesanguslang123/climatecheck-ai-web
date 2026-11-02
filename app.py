
import json
import os
import streamlit as st
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# Page settings
st.set_page_config(
    page_title="ClimateCheck AI",
    page_icon="🌤️",
    layout="wide"
)

# Ollama settings
OLLAMA_URL = os.environ.get(
    "OLLAMA_HOST", "http://localhost:11434"
).rstrip("/")

OLLAMA_MODEL = os.environ.get(
    "OLLAMA_MODEL", "gpt-oss:20b-cloud"
)

# Custom website styling
st.markdown("""
<style>

.stApp {
    background-color: #0B1628;
    color: #FFFFFF;
}

[data-testid="stHeader"] {
    background-color: #0B1628;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #FFFFFF;
}

p, label {
    color: #C5D4E8;
}

.metric-card {
    background-color: #172C48;
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #263F60;
    min-height: 125px;
}

.metric-label {
    color: #9CB5D1;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    color: #FFFFFF;
    font-size: 27px;
    font-weight: bold;
    margin-top: 10px;
}

div.stButton > button {
    background-color: #168BDF;
    color: white;
    border: none;
    border-radius: 9px;
    height: 48px;
    font-weight: bold;
    width: 100%;
}

div.stButton > button:hover {
    background-color: #0874BE;
    color: white;
}

.analysis-card {
    background-color: #172C48;
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #263F60;
}

</style>
""", unsafe_allow_html=True)


# Website heading
st.markdown("# 🌤️ ClimateCheck AI")
st.markdown(
    "Understand your local climate with artificial intelligence."
)

st.write("")

# Dashboard heading
st.subheader("Climate Overview")

# Input section
st.markdown("### Enter your climate information")

col1, col2 = st.columns(2)

with col1:
    userCountry = st.selectbox(
        "Select your country",
        [
            "United States", "Canada", "Mexico",
            "United Kingdom", "France", "Germany",
            "Japan", "Australia", "Brazil", "India"
        ]
    )

with col2:
    userMonth = st.selectbox(
        "Select the month",
        [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]
    )

userTemperature = st.number_input(
    "Current temperature (°C)",
    min_value=-90.0,
    max_value=60.0,
    value=18.0,
    step=0.5
)

# Dashboard information cards
st.write("")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Selected country</div>
        <div class="metric-value">{userCountry}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Current temperature</div>
        <div class="metric-value">{userTemperature}°C</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.markdown("### AI Climate Analysis")

# Analyse button
if st.button("Analyse temperature"):

    if not userCountry.strip():
        st.warning("Please select a country.")

    else:

        prompt = f"""
        Analyse the temperature entered by the user.

        Country: {userCountry}
        Temperature: {userTemperature} degrees Celsius
        Month: {userMonth}

        Explain whether the temperature is cold, mild, warm, or hot.
        Discuss whether it is typical or unusual for that country
        at this time of year.

        Be clear if you are uncertain.
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

        with st.spinner("ClimateCheck AI is analysing..."):

            try:
                with urlopen(request, timeout=120) as response:
                    response_text = response.read().decode("utf-8")

                result = json.loads(response_text)

                if "response" in result:
                    st.markdown("""
                    <div class="analysis-card">
                        <h3>🌍 ClimateCheck AI Report</h3>
                    </div>
                    """, unsafe_allow_html=True)

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
