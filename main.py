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
    url = "https://text-to-speech-neural-google.p.rapidapi.com/generateAudioFiles"
    audio_format = "ogg"
    voice_name = "Wavenet-B"
    engine = "google"
    language_code = "en-IN"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "8146e2a7a9mshe43236ad48a66a4p11efb1jsn84fd4294f4f1",
        "X-RapidAPI-Host": "text-to-speech-neural-google.p.rapidapi.com"
    }
    data = {
        "audioFormat": audio_format,
        "paragraphChunks": [text],
        "voiceParams": {
            "name": voice_name,
            "engine": engine,
            "languageCode": language_code
        }
    }
    response = requests.post(url, json=data, headers=headers)

    # Convert the response audio to a playable format
    audio_bytes = BytesIO(response.content)
    audio_segment = AudioSegment.from_file(audio_bytes, format=audio_format)
    audio_segment.export("presentation_audio." + audio_format, format=audio_format)

    return audio_bytes



def main():
    st.title("AICademy")

    topic = st.text_input("Enter the topic for your presentation:")
    submit_button = st.button("Generate Presentation")

    if submit_button and topic:
        presentation = generate_presentation(topic)
        audio = generate_audio(presentation)

        # Display the presentation or video and the generated audio
        st.audio(audio.read(), format='audio/mp3')
        st.write(presentation)


if __name__ == "__main__":
    st.set_page_config(page_title="AICademy", page_icon=":books:")
    main()
