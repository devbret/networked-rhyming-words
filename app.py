import re
import pronouncing
import json

# Function to clean and normalize lyrics
def clean_normalize_lyrics(lyrics_blob):
    lyrics_blob = re.sub(r'\[.*?\]', '', lyrics_blob)
    lyrics_blob = re.sub(r'\(.*?\)', '', lyrics_blob)
    lyrics_blob = lyrics_blob.lower()
    lyrics_blob = re.sub(r'[^a-zA-Z0-9\s\']', '', lyrics_blob)
    return lyrics_blob

# Function to read lyrics from a file
def read_lyrics_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to clean a line of text
def clean_line(line):
    return re.sub(r'[^a-zA-Z\s]', '', line).lower().strip()

# Main function to process the lyrics and generate the network data
def main():
    # File paths
    input_file_path = '/home/bret/code/personal/networked-rhyming-words/eap.txt'
    network_data_path = 'network_data.json'
    
    # Step 1: Read and clean lyrics
    lyrics_blob = read_lyrics_from_file(input_file_path)
    cleaned_lyrics = clean_normalize_lyrics(lyrics_blob)

    # Step 2: Analyze rhymes and generate network data
    lines = cleaned_lyrics.split('\n')
    last_words = [clean_line(line).split()[-1] for line in lines if clean_line(line).split()]

    rhymes = {}
    for word in last_words:
        rhyming_words = set(pronouncing.rhymes(word))
        actual_rhymes = rhyming_words.intersection(set(last_words))
        if actual_rhymes:
            rhymes[word] = list(actual_rhymes)

    nodes = []
    links = []
    seen_words = set()

    for word, rhymes in rhymes.items():
        if word not in seen_words:
            nodes.append({"id": word, "group": 1})
            seen_words.add(word)
        
        for rhyme in rhymes:
            if rhyme not in seen_words:
                nodes.append({"id": rhyme, "group": 2})
                seen_words.add(rhyme)
            
            links.append({"source": word, "target": rhyme, "value": 1})

    graph_data = {"nodes": nodes, "links": links}
    with open(network_data_path, 'w') as outfile:
        json.dump(graph_data, outfile, indent=4)
    print("Network data has been saved to 'network_data.json'")

# Run the main function
if __name__ == '__main__':
    main()
