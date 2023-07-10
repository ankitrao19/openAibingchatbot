# openAibingchatbot

# BingOpenAI Bot

This is a Python-based bot that integrates Bing Search API and OpenAI GPT-3 to provide responses based on user queries. The bot is built using the FastAPI framework and utilizes the `requests` library for making API calls.

## Features

- Queries the Bing Search API to retrieve search results based on user input.
- Formats the retrieved data and uses it as a prompt for the OpenAI GPT-3 model.
- Sends the prompt to the OpenAI GPT-3 model and receives a generated response.
- Provides the generated response as the final output.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/ankitrao19/openAibingchatbot.git
cd openAibingchatbot
pip install -r requirements.txt
