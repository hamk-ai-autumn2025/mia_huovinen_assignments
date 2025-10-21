import replicate
import argparse

def generate_dictionary(word: str):
    # payload = {
    #     "prompt": word,
    #     "system": (
    #         "You are a dictionary definition generator. "
    #         "Provide a concise and clear definition for the given word in JSON format only. "
    #         "Use this exact structure: "
    #         "{\"word\": \"<word>\", \"definition\": \"<definition>\", "
    #         "\"synonyms\": [\"<synonyms>\"], \"antonyms\": [\"<antonyms>\"], "
    #         "\"examples\": [\"<examples>\"]}. "
    #         "Do NOT include any explanations, preambles, or extra text. "
    #         "Return the JSON in a single code block."
    #     )
    # }

    payload = {
        "prompt": (
            "You are a dictionary definition generator. "
            "Provide a concise and clear definition for the given word in JSON format only. "
            "Use this exact structure: "
            '{'
            '"word": "<word>", "definition": "<definition>", '
            '"synonyms": ['
            '"\n\t<synonym1>", '
            '"\n\t<synonym2>"'
            '], '
            '"antonyms": ['
            '"\n\t<antonym1>",'
            '"\n\t<antonym2>"'
            '], '
            '"examples": ['
            '"\n\t<example1>",'
            '"\n\t<example2>"'
            ']'
            '}'
            "Do NOT include any explanations, preambles, or extra text. "
            "Return the JSON in a single code block. "
            f"Word is '{word}'."
            "Use the language of the word provided."
        )
    }

    for event in replicate.stream(
        "openai/gpt-5",
        input=payload
    ):
        print(event, end="")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a json structured dictionary definition for a given word.")
    parser.add_argument("word", type=str, help="The word to define.")
    args = parser.parse_args()
    generate_dictionary(args.word)
    print("\n")