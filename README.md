<div align="center">
  <!-- <img src="https://storage.googleapis.com/hume-public-logos/hume/hume-banner.png"> -->
  <h1>CHILLBERT : Your emotional sidekick with all the cool vibes!</h1>
</div>

## Overview

<p>
  <strong>We’re on a mission to make mental health check-ins less awkward—our mood-savvy assistant listens to your vibes, cracks a joke, and keeps your therapist in the loop with all the feels!</strong>
</p>

This is a voice-powered agent designed to engage users and mental health patients in casual, mood-lifting check-ins throughout the day. The agent provides friendly interactions, helping users pass time while boosting their mood. After each conversation, a summary is automatically shared with the assigned mental health practitioner via WhatsApp. Additionally, users receive personalized, helpful links based on the topics discussed. Practitioners are equipped with a dashboard, allowing them to explore the conversation further and ask follow-up questions, ensuring more tailored and insightful care.

## Technologies Used

We used model on HumeAI for creating a conversational voice agent. These converations and their emotions are tracked, stored and analysed with a Gemini RAG model in LangChain. A summary of the conversation is sent to the health practitioner via Whatsapp.

## Demo
[![Conversational Voice Agent Demo](https://img.youtube.com/vi/oLZIwUN0kR8/0.jpg)](https://youtu.be/oLZIwUN0kR8?si=5sEKzh9diwHg1u-V)



## Setting up a virtual environment 

Before you install the dependencies, you might want to create a virtual environment to isolate your package installations. To create a virtual environment, run the following commands in your terminal:

```bash
# Create a virtual environment in the directory 'evi-env'
python -m venv venv

# Activate the virtual environment
# On Mac/Linux:
source venv/bin/activate
```

After activating the virtual environment, you can proceed with the installation of dependencies as described below.

## Dependencies

In order to run it, you need to install the `requirements.txt` using `pip`:

### Mac

```bash
pip install -r requirements.txt
```


## Environment variables

Create a `.env` file or set environment variables. You will need a HUME account, a Google AI Studio account and a Twilio account.

Example `.env` file:

```bash
HUME_API_KEY="<HUME API KEY>"
HUME_SECRET_KEY="<HUME SECRET KEY>"
TWILIO_ACCOUNT_SID="<TWILIO ACCOUNT SID>"
TWILIO_AUTH_TOKEN="<TWILIO AUTH TOKEN>"
TWILIO_RECIPIENT="<TWILIO RECIPIENT>"
GOOGLE_API_KEY="<GOOGLE API KEY>"
```

## Usage

```bash
streamlit run chillbert.py
```
