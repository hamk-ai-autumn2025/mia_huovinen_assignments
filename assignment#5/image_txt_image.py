from openai import OpenAI
import argparse
import base64
import requests
import os


def image_to_text(base64_image):
    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    system_prompt = "You are a highly accurate visual description assistant." \
    "Your task is to carefully analyze any image provided and generate a clear, detailed, and structured textual description." \
    "Description must be less than 50 words."


    system_prompt = (
        "You are a highly accurate visual description assistant. "
        "Describe any provided image in clear, structured text, less than 50 words."
    )

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    description = (response.json().get("choices")[0].get("message").get("content"))
    print(description)


def text_to_image(description):
    # TEKSISTÄ KUVAKSI
    client = OpenAI()
    response = client.images.generate(
        model="dall-e-3",
        prompt=description,
        size="1792x1024",
        n=1
    )

    if response.data and len(response.data) > 0:
        image_url = response.data[0].url
        print("Image URL:", image_url)

        try:
            r = requests.get(image_url)
            r.raise_for_status()
            image_data = r.content
        except Exception as e:
            print("Error fetching image:", e)
            image_data = None

        if image_data:
            file_name = f"AI_image.jpg"
            try:
                with open(file_name, "wb") as f:
                    f.write(image_data)
                print(f"Image saved to {file_name}")
            except Exception as e:
                print("Error saving file:", e)
    else:
        print("No image was generated.")


def main():
    # Argumentit
    parser = argparse.ArgumentParser(description="Command line tool that create image-to-text and texr-to-image")
    parser.add_argument("image", help="Image filepath")
    args = parser.parse_args()

    if args.image:
        image_path = args.image
    else:
        print("Please, add an image filepath")
        exit(1)

    with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    
    new_prompt = image_to_text(base64_image)
    text_to_image(new_prompt)