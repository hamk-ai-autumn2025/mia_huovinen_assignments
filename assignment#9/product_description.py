import replicate
import argparse
import base64

def create_product_description(image):
    input = {
        "image_input": [image],
        "prompt": "Create a detailed product description for the item shown in the image. Make it engaging and informative and marketable. Keep it under 200 words. Must include heading, bullet points, and a short summary at the end.",
    }

    for event in replicate.stream(
        "openai/gpt-4.1-mini",
        input=input
    ):
        print(event, end="")

    print("\n")

def main():
    # Argumentit: accept one or more image filepaths
    parser = argparse.ArgumentParser(description="Command line tool that creates product descriptions from images")
    parser.add_argument("images", nargs="+", help="One or more image filepaths")
    args = parser.parse_args()

    image_paths = args.images

    # Process each image: read, encode and call the description generator
    for image_path in image_paths:
        try:
            with open(image_path, "rb") as image_file:
                create_product_description(image_file)
        except FileNotFoundError:
            print(f"File not found: {image_path}")
            continue

    # Done processing images; skip the single-image block below
    return


if __name__ == "__main__":
    main()