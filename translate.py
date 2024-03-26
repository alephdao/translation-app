import argparse
from openai import OpenAI
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def translate_text(text, source_lang, target_lang):
    """
    Translate text from source language to target language using OpenAI's GPT.
    """
    # Define the prompt for translation based on source and target languages
    prompt = f"You are a highly intelligent translator that translates {source_lang} text to {target_lang}."
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": text,
            }
        ],
    )

    # Accessing the translated text correctly
    translated_text = response.choices[0].message.content.strip()
    return translated_text

def split_text(text, max_chunk_size=4096, output_dir="output"):
    """
    Split text into chunks without exceeding the specified maximum chunk size
    and save each chunk as a separate Markdown file in the specified output directory,
    preserving original line breaks and paragraph structure.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    chunks = []  # List to hold the chunks of text
    current_chunk = ""  # String to build the current chunk
    file_counter = 1  # Counter to name the files uniquely

    paragraphs = text.split('\n\n')  # Split the text into paragraphs
    for paragraph in paragraphs:
        # Check if the current paragraph can fit into the current chunk
        if len(current_chunk) + len(paragraph) + 2 <= max_chunk_size:  # +2 for double newline characters
            current_chunk += ('\n\n' + paragraph if current_chunk else paragraph)
        else:
            # If the paragraph itself exceeds max_chunk_size, split it further into sentences
            if len(paragraph) > max_chunk_size:
                sentences = re.split(r'(?<=[.!?]) +', paragraph)
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:  # +1 for space or newline
                        current_chunk += (' ' + sentence if current_chunk else sentence)
                    else:
                        # Save the current chunk and start a new one
                        chunks.append(current_chunk)
                        current_chunk = sentence
                        file_counter += 1
            else:
                # If the current chunk is not empty, save it before adding a large paragraph
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = paragraph
                    file_counter += 1
                else:
                    # If the chunk is empty and paragraph is large but within the limit, start a new chunk
                    current_chunk = paragraph

    # Handle the last chunk if it's not empty
    if current_chunk.strip():
        chunks.append(current_chunk)

    return chunks

def main(input_filename, source_lang, target_lang):
    """
    Main function to read the input file, split the text, translate it, and save the translated text.
    """
    with open(input_filename, "r", encoding="utf-8") as file:
        input_text = file.read()

    chunks = split_text(input_text)

    base_filename = os.path.basename(os.path.splitext(input_filename)[0])

    combined_translated_text = ""

    for i, chunk in enumerate(chunks):
        translated_text = translate_text(chunk, source_lang, target_lang)
        output_filename = f"output/{base_filename}_chunk_{i+1}.md"
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write(translated_text)
        print(f"Translated chunk {i+1} saved to {output_filename}")

        combined_translated_text += translated_text + "\n\n"

    combined_output_filename = f"output/{base_filename}_translated.md"
    with open(combined_output_filename, "w", encoding="utf-8") as file:
        file.write(combined_translated_text.strip())
    print(f"Combined translated text saved to {combined_output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate text from one language to another.")
    parser.add_argument("input_filename", help="The location of the input file")
    parser.add_argument("source_lang", help="The source language of the text")
    parser.add_argument("target_lang", help="The target language for the translation")

    args = parser.parse_args()

    main(args.input_filename, args.source_lang, args.target_lang)
