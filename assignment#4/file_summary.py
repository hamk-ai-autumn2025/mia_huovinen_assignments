from openai import OpenAI
import argparse
from markitdown import MarkItDown

def convert_to_md(source):
    md = MarkItDown()
    result = md.convert(source)
    return result.text_content

# OpenAI asetukset
client = OpenAI()
system_prompt = "Create a summary of one or more user input files or URL pages." \
" Use the same language as in the markdown source unless the user prompt asks otherwise. " \
"Summary must be in Markdown format and with headline."

# Argumentit
parser = argparse.ArgumentParser(description="Command line tool to summarize file content. (txt, hmtl, .docx, PDF, csv)")
parser.add_argument("source", nargs="+", help="One or more Filepath or URL")
parser.add_argument("-p", "--prompt", help="User prompt")
parser.add_argument("-o", "--output", help="Output textfile (.txt)")
args = parser.parse_args()

# Lähde tiedostojen/URL käsittely
sources = []
for s in args.source:
    try:
        sources.append(convert_to_md(s))
    except Exception as e:
        print(f"Error: Invalid source file/URL input {s}: {e}")

if not sources:
    print(f"No file/URL input")
    exit(1)

combined_sources = "\n\n".join(sources)

# User promptin tallennus muuttujaan
user_prompt = args.prompt or ""

# OpenAI API kutsu
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{user_prompt}\n{combined_sources}"}
    ],
    temperature=0.5,
    max_completion_tokens=1000,
    stream=False,  # default, wait until everything is ready
)

summary = completion.choices[0].message.content
print(summary)

if args.output:
    filename = args.output
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(summary)
    except Exception as e:
        print(f"Erro: writing {filename} failed: {e}")

