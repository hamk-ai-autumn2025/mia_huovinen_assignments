import sounddevice as sd
import wave
from openai import OpenAI
import random

# Luo client OpenAI:lle
client = OpenAI() 

# Tallennuksen asetukset
samplerate = 16000
channels = 1
duration = 3  # sekunteina

def record_chunk():
    print("Nauhoitetaan...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
    sd.wait()
    return audio

def save_wav(filename, audio):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio.tobytes())

def transcribe(audio_file):
    with open(audio_file, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            prompt="Transcribe only single board coordinates in the form A5, C2, B3. Do not change the format. Audio input can be in english or finnish. But you should expect always format where is one letter and one number."
        )
    return transcript.text


def print_grid():
    print("  " + " ".join(letters))
    for i, row in enumerate(grid, start=1):
        print(i, " ".join(row))


if __name__ == "__main__":
    # Koordinaatit
    letters = ['a', 'b', 'c', 'd', 'e']
    numbers = ["1","2", "3", "4", "5"]

    # Luo tyhjä ruudukko (~ = vesi)
    grid = [["~" for _ in range(5)] for _ in range(5)]

    # Sijoita yksi laiva satunnaisesti
    ship = ["b2", "c3", "d4"]

    # käytetyt koordinaatit
    used_cordinates = []

    count = 12

    print(f"Tämä on laivanipotus peli, joka toimii äänikomennoilla. Pelialueella on yksi laiva, joka on 3 ruutua pitkä.\
          \nSano sen ruudun koordinaatit mihin haluat ampua (esim B3). Äänen nauhoitusaika on {duration} sekunttia.\
          \nSymbolit: VESI [~] | OHI [O] | OSUMA [X] \n")
    print_grid()
    while True:
        start = input(f"\nPaina [ENTER] ja anna äänikomento! ({count} pommia jäljellä): ")
        if start.lower() == "exit":
            exit(0)
        audio = record_chunk()
        filename = "temp_audio.wav"
        save_wav(filename, audio)
        cordinates = transcribe(filename).lower()
        print("ANNETUT KOORDINAATIT:", cordinates)

            # Tarkista syötteen pituus ja muoto
        if len(cordinates) < 2 or cordinates[0] not in letters or cordinates[1] not in numbers:
            print("Virheellinen syöte. Kokeile uudestaan.")
            continue

        if cordinates in used_cordinates:
            print("Olet jo ampunut tähän kohteeseen, valitse uudet koordinaatit!")
            continue
        
        x, y = cordinates[0], cordinates[1]

        # Tarkista osuma
        if cordinates in ship:
            print("💥 Osuma!")
            # Merkitään osuma gridille
            grid[numbers.index(y)][letters.index(x)] = "X"
            print_grid()
            # Poistetaan koordinaatit laivan tiedoista
            ship.remove(cordinates)

            if len(ship) < 1:
                print("VOITIT PELIN! Sait laivan upotettua.\n")
                break
        else:
            print("🌊 Ohitus!")
            # Merkitään ohitus gridille
            grid[numbers.index(y)][letters.index(x)] = "O"
            print_grid()

        # Lisätään käytettyihin koordinaatteihin
        used_cordinates.append(cordinates)
        count -= 1
        if count < 1:
            print("PELI PÄÄTTYI! Käytit kaikki pommit.")