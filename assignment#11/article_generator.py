import replicate
import argparse
from markdown_pdf import MarkdownPdf, Section
import os

def create_pdf(markdown_content: str, output_filename: str = "article.pdf"):
    pdf = MarkdownPdf(toc_level=1)
    pdf.add_section(Section(markdown_content, paper_size="A4"), user_css="table, td, th {border: 1px solid black;}")
    pdf.meta["title"] = "Finland"
    pdf.meta["author"] = "Google Gemini"
    pdf.save(output_filename)
    
    print(f"PDF saved as {output_filename}")

def generate_article(topic: str):
    prompt = f"""
    You are a scientific article generator. 

    Task:
    Generate a full scientific article on the topic: "{topic}". 

    Requirements:
    1. Use a standard scientific article structure:
    - Abstract
    - Introduction
    - Methods
    - Results
    - Discussion
    - Conclusions
    - References
    2. Divide the article into chapters and subchapters with appropriate headings.
    3. Include tables if relevant.
    4. Provide in-text citations using APA style.
    5. Generate a reference list in APA style at the end.
    6. Format the output in Markdown, using headings (#, ##, ###), tables, and lists.
    7. Ensure all references are real and verifiable..
    8. Write clearly, concisely, and in formal scientific style.
    9. Use the language of the topic provided.

    Output must be in Markdown format. No reambles, explanations, or extra text outside the article content.

    Topic: "{topic}"
    """
    payload = {
        "prompt": prompt
    }

    output = replicate.run(
        "openai/gpt-5",
        input=payload
    )
    
    md_text = "".join(output)
    #print(md_text)
    create_pdf(md_text, output_filename="article.pdf")

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a article on a given topic.")
    parser.add_argument("topic", type=str, help="The topic of the article.")
    args = parser.parse_args()
    generate_article(args.topic)
    print("\n")