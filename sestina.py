from openai import OpenAI
import os
from dotenv import load_dotenv
import time


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def sestina(slutord: list[str]) -> list[list[str]]:
    if len(slutord) != 6:
        raise ValueError("Please give six words")
    rotation = [
        [0, 1, 2, 3, 4, 5],
        [5, 0, 4, 1, 3, 2],
        [2, 5, 3, 0, 1, 4],
        [4, 2, 1, 5, 0, 3],
        [3, 4, 0, 2, 5, 1],
        [1, 3, 5, 4, 2, 0]
    ]
    stanzas = []
    for rot in rotation:
        stanza = [slutord[i] for i in rot]
        stanzas.append(stanza)
    return stanzas

def tercet(words: list[str]) -> list[list[str]]:
    return [
        [words[2], words[5]],
        [words[4], words[3]],
        [words[0], words[1]]
    ]

def extract_last_word(line: str) -> str:
    """Extract the last word from a line"""
    words = line.strip().split()
    if words:
        return words[-1].rstrip('.,!?;:')
    return ""

def build_example_messages(example_lines: list[str]) -> list[dict]:

    messages = []
    for line in example_lines:
        last_word = extract_last_word(line)
        if last_word:
            messages.append({
                "role": "user",
                "content": f"Generate a lyric line ending with the word '{last_word}'"
            })
            messages.append({
                "role": "assistant",
                "content": line
            })
    return messages

def write_prompts(stanzas: list[list[str]], tercet_lines: list[list[str]], example_lines: list[str]) -> list[str]:
    poems = []
    model = "gpt-4o-mini"
    
    # Create example from users input
    example_messages = build_example_messages(example_lines)
    
    for stanza in stanzas:
        for word in stanza:
            prompt = f"Write one lyric line with the last word being: {word}"
            print(f"\nSkickar prompt: {prompt}")

            try:
                
                messages = [
                    {"role": "system", "content": "Act as a poetic assistant that creates lyric lines ending with a given word. Respond only with the lyric line, no extra text."}
                ]
                messages.extend(example_messages)
                messages.append({"role": "user", "content": prompt})
                
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=25,
                )
                poem_line = response.choices[0].message.content
                poems.append(poem_line)
               
                time.sleep(1)  # Wait to avoid rate limits

            except Exception as e:
                print(f"Error during call for API : {e}")
                continue

    for line in tercet_lines:
        prompt = f"Write a poetic line where the last words are: {line[0]} and {line[1]}"
        print(f"\nSkickar prompt för tercet: {prompt}")

        try:
            messages = [
                {"role": "system", "content": "Act as a poetic assistant that creates lyric lines ending with two given words. Respond only with the lyric line, no extra text."}
            ]
            messages.extend(example_messages)
            messages.append({"role": "user", "content": prompt})
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=50,
            )
            poem_line = response.choices[0].message.content
            poems.append(poem_line)
            
            time.sleep(1)

        except Exception as e:
            print(f"Error during call for API : {e}")
            continue

    return poems

def main():
    end_words_input = input("Choose six words that will be used in the poem (separated by spaces): ")
    end_words = end_words_input.split()
    
    if len(end_words) != 6:
        print("Error: Please provide exactly six words")
        return
    
    print("\nProvide three lyric lines that will be used as examples:")
    example_lines = []
    for i in range(3):
        line = input(f"Lyric line {i+1}: ")
        if line.strip():
            example_lines.append(line.strip())
    
    if len(example_lines) < 3:
        print("Error: Please provide three lyric lines")
        return
    
    stanzas = sestina(end_words)
    tercet_lines = tercet(end_words)

    print("\nGenererar poem...")
    poems = write_prompts(stanzas, tercet_lines, example_lines)

    print("\n--- Genererade lyrikrader ---")
    for i, poem in enumerate(poems, 1):
        print(f"{i}. {poem}")

if __name__ == "__main__":
    main()
