from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def sestina(endwords: list[str]) -> list[list[str]]:
    if len(endwords)!=6:
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
        stanza = [endwords[i] for i in rot]
        stanzas.append(stanza)
    return stanzas
def tercet(words: str)->list[list,str]:
     tercet = [
        [words[2], words[5]],
        [words[4], words[3]],
        [words[6 % len(words)], words[1]]  
    ]
     return tercet
def write_prompts(stanzas: list[list[str]], tercet: list[list[str]]) -> list[str]:
    prompts = []
    model="gpt-3.5-turbo"
    
        
    for stanza in stanzas:
        for word in stanza:
            prompt = f"Write one lyric line with the last word being: {word}"
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                #messages includes three lines from Cathy Park Hongs Enginen Empire (2012)
                messages=[messages={"role": "system", "content": "**Act as a poetic assistant that creates lyric lines ending with a given word.**."},

        {"role": "user", "content": "Generate a lyric line ending with the word  'sun'"},

        {"role": "assistant", "content": "Market forces are brighter than the sun"},

        {"role": "user", "content": "Generate a lyric line ending with the word  'supplies'."},
        {"role": "assistant", "content": "Dear natty vessel of chemical dye, dear floating factory for cleaning supplies"},
        {"role": "user", "content": "Generate a lyric line ending with the word 'petrol'" },
        {"role": "assistant", "content": "I will stuff you cheek to jowl and pipetter you with petrol"},
        {"role": "user", "content": prompt}], 
                          
                max_tokens=50,
)
    for line in tercet :
        prompt = f"Write a poetic line where the last words are: {rad[0]} and {rad[1]}"
        prompts.append(prompt)
    prompts.append(response.choices[0].message.content)
    return prompts

def main():
    example_end_words = ["bright", "free", "beyond", "sitcom", "life", "world"]

    stanzas = sestina(example_end_words)
   
    poems = write_prompts(stanzas, tercet)
    for poem in poems:
        print(poem)

if __name__ == "__main__":
    main()