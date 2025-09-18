from openai import OpenAI

client = OpenAI()

system_prompt = """
You are a creative social media writer. 
When given a topic, write engaging post about it. 
Keep the post clear, fun, and easy to read. 
Use different ways to say the same thing so each post feels unique. 
Add hashtags when it makes sense. 
Always focus on the topic and write in the same language as the user.
"""

model = "gpt-4o"
temperature = 0.8
top_p = 0.9
presence_penalty = 1.2
frequency_penalty = 0.5
n = 3


history = [{"role": "system", "content": system_prompt}]

print(f"Chat with {model}. Enter 'exit' or 'quit' to stop.\n")
print(f"Hello! Let’s make some engaging social media posts. Give me a topic and I’ll create 3 fun versions for you.")
while True:
    prompt = input("> ").strip()
    if prompt.lower() in ["exit", "quit"] or not prompt:
        break

    history.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model=model,
        messages=history,
        temperature=temperature,
        top_p=top_p,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        n=3
    )

    print("\nCreative writer answers:\n")

    for i, choice in enumerate(completion.choices, start=1):
        print(f"Versio {i}:\n{choice.message.content}\n")

   
