import pronouncing
import re
import json

def clean_line(line):
    return re.sub(r'[^a-zA-Z\s]', '', line).lower().strip()
  
def read_lyrics_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

input_file_path = 'your/input/path/cleaned_lyrics.txt'

lyrics_blob = read_lyrics_from_file(input_file_path)

lines = lyrics_blob.split('\n')

last_words = [clean_line(line).split()[-1] for line in lines if clean_line(line).split()]

rhymes = {}
for word in last_words:
    rhyming_words = set(pronouncing.rhymes(word))
    
    actual_rhymes = rhyming_words.intersection(set(last_words))
    if actual_rhymes:
        rhymes[word] = list(actual_rhymes)

rhymes_json = json.dumps(rhymes, indent=4)

with open('rhyme_analysis.json', 'w') as json_file:
    json_file.write(rhymes_json)

print("Rhyme analysis has been saved to 'rhyme_analysis.json'")
