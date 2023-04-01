import requests
import streamlit as st
import openai
from io import BytesIO
from pydub import AudioSegment

# Set up OpenAI API
openai.api_key = st.secrets["openai_api_key"]


def generate_presentation(topic):
    prompt = f"Please explain {topic} in the most easy and attractive way possible."

    # Set up OpenAI API parameters
    model_engine = "text-davinci-002"
    max_tokens = 1048
    temperature = 0.7

    # Generate the presentation content using OpenAI's GPT-3 API
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )

    return response.choices[0].text


def generate_audio(text):
    # Set up text-to-speech API parameters
    api_key = st.secrets["tts_api_key"]
    api_url = "https://api.fpt.ai/hmi/tts/v5"
    voice = "banmai"
    speed = "0"

    # Send a request to the text-to-speech API
    headers = {
        "api-key": api_key,
        "voice": voice,
        "speed": speed
    }
    data = {"text": text}
    response = requests.post(api_url, headers=headers, json=data)

    # Convert the response audio to a playable format
    audio_bytes = BytesIO(response.content)
    audio_segment = AudioSegment.from_file(audio_bytes, format="mp3")
    audio_segment.export("presentation_audio.mp3", format="mp3")

    return audio_bytes


def main():
    st.title("AICademy")

    topic = st.text_input("Enter the topic for your presentation:")
    submit_button = st.button("Generate Presentation")

    if submit_button and topic:
        presentation = generate_presentation(topic)
        audio = generate_audio(presentation)

        # Display the presentation or video and the generated audio
        st.audio(audio)
        st.write(presentation)


if __name__ == "__main__":
    main()
