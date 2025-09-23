from openai import OpenAI
import warnings
import argparse
warnings.filterwarnings("ignore", category=DeprecationWarning)


def speech_to_text(client, audio):
    audio_file = open(audio, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )

    generated_text = transcription.text
    return generated_text


def text_to_speech(client, text):
    speech_file_path = "speech.mp3"
    prompt = text
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy", 
    input=prompt
    )
    response.stream_to_file(speech_file_path)


def translate(client, text, language):
    prompt = f"Translate following text to {language}:\n{text}"
    response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
    )

    translation = response.choices[0].message.content
    return translation


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command line tool to translate audio speech to another language!")
    parser.add_argument("audio", help="A audio file path")
    args = parser.parse_args()
    audio = args.audio

    print("[exit]/[quit] input will end the program.")
    language = input("To which language do you want to translate the speech?: ")
    if language.lower() in ("exit", "quit"):
        print("Bye byeee!")
        exit(0)

    client = OpenAI()

    generated_text = speech_to_text(client, audio)
    print(f"Generated text:\n{generated_text}\n")

    translated_text = translate(client, generated_text, language)
    print(f"Translation:\n{translated_text}\n")

    text_to_speech(client, translated_text)
    print("New audio file created!")
