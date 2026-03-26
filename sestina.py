from openai import OpenAI
import os
from dotenv import load_dotenv
import time

# Ladda miljövariabler
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

def write_prompts(stanzas: list[list[str]], tercet_lines: list[list[str]]) -> list[str]:
    poems = []
    model = "gpt-4o-mini"

    for stanza in stanzas:
        for word in stanza:
            prompt = f"Write one lyric line with the last word being: {word}"
            print(f"\nSkickar prompt: {prompt}")

            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "Act as a poetic assistant that creates lyric lines ending with a given word. Respond only with the lyric line, no extra text."},
                        {"role": "user", "content": "Generate a lyric line ending with the word 'sun'"},
                        {"role": "assistant", "content": "Market forces are brighter than the sun"},
                        {"role": "user", "content": "Generate a lyric line ending with the word 'supplies'"},
                        {"role": "assistant", "content": "Dear natty vessel of chemical dye, dear floating factory for cleaning supplies"},
                        {"role": "user", "content": "Generate a lyric line ending with the word 'petrol'"},
                        {"role": "assistant", "content": "I will stuff you cheek to jowl and pipetter you with petrol"},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=50,
                )
                poem_line = response.choices[0].message.content
                poems.append(poem_line)
               
                time.sleep(1)  # Wait to awoyed rate limits

            except Exception as e:
                print(f"Error during call for API : {e}")
                continue

    for line in tercet_lines:
        prompt = f"Write a poetic line where the last words are: {line[0]} and {line[1]}"
        print(f"\nSkickar prompt för tercet: {prompt}")

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Act as a poetic assistant that creates lyric lines ending with two given words. Respond only with the lyric line, no extra text."},
                    {"role": "user", "content": prompt},
                ],
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
    example_end_words = ["bright", "free", "beyond", "sitcom", "life", "world"]
    stanzas = sestina(example_end_words)
    tercet_lines = tercet(example_end_words)

    print("Genererar poem...")
    poems = write_prompts(stanzas, tercet_lines)


    for i, poem in enumerate(poems, 1):
        print(f"{i}. {poem}")

if __name__ == "__main__":
    main()
