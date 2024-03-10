import re

def clean_normalize_lyrics(lyrics_blob):
    lyrics_blob = re.sub(r'\[.*?\]', '', lyrics_blob)
    lyrics_blob = re.sub(r'\(.*?\)', '', lyrics_blob)
    
    lyrics_blob = lyrics_blob.lower()

    lyrics_blob = re.sub(r'[^a-zA-Z0-9\s\']', '', lyrics_blob)
    
    return lyrics_blob

def read_lyrics_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_cleaned_lyrics_to_file(cleaned_lyrics, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_lyrics)
    print(f"Cleaned lyrics have been saved to '{output_file_path}'")

input_file_path = 'your/input/path/lyrics.txt'

lyrics_blob = read_lyrics_from_file(input_file_path)

cleaned_lyrics = clean_normalize_lyrics(lyrics_blob)

output_file_path = 'your/output/path/cleaned_lyrics.txt'

write_cleaned_lyrics_to_file(cleaned_lyrics, output_file_path)
