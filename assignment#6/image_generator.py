from openai import OpenAI
import base64
import requests

ASPECT_RATIOS = {
    "1:1": "1024x1024",
    "7:4": "1024x1792",
    "4:7": "1792x1024",
}

client = OpenAI()

def generate_images(prompt, negative_prompt, size, filename):

    full_prompt=f"{prompt}\nAvoid: {negative_prompt}"
    response = client.images.generate(
        model="dall-e-3",
        prompt=full_prompt,
        size=size
    )

    image_url = response.data[0].url
    print(f"Image URL: {image_url}")

    # Lataa ja tallenna kuva
    image_data = requests.get(image_url).content
    with open(filename, "wb") as f:
        f.write(image_data)
    print(f"Image saved to {filename}")


def main():
    aspect_ratio = input("Aspect ratio (1:1, 7:4, 4:7): ").strip()
    size = ASPECT_RATIOS.get(aspect_ratio)
    if not size:
        print("Invalid aspect ratio")
        exit(1)
    
    prompt = input("Prompt: ")
    negative_prompt = input("Negative prompt: ")
    try:
        num_images = int(input("Number of images: ").strip())
    except ValueError:
        print("Invalid number of images")
        exit(1)

    print(f"Start generating {num_images} pictures...")
    for i in range(num_images):
        filename = f"image{i}.jpg"
        generate_images(prompt, negative_prompt, size, filename)

if __name__ == "__main__":
    main()