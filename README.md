# ClimateCheck AI Web

An AI-powered climate analysis web application built using Python, Streamlit and Ollama.

## Features
- User inputs their country.
- User enters the current temperature in Celsius.
- User selects the month.
- Ollama AI analyses the temperature.
- Results are displayed directly on an interactive website.

## Technologies
- Python
- Streamlit
- Ollama
- JSON and HTTP requests

## How it works
The application collects information from the user and sends it to an Ollama model through its API. The model generates an explanation of the temperature and whether it may be typical for that country and time of year.

## Current limitations
The application does not yet use verified live weather or historical climate datasets. Its analysis is based on the AI model's existing knowledge.

## Future improvements
- Integrate live weather data.
- Compare temperatures against historical climate averages.
- Improve the website's design.
- Add visual temperature comparisons.
