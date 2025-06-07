'''
Script to read words from a CSV file and generate MP3 files using Google Text-to-Speech.
'''
import csv
from gtts import gTTS
import os
import argparse
from tqdm import tqdm # Import tqdm for the progress bar

def create_mp3s_from_csv(csv_filepath, output_folder='output_mp3s', tld='co.uk'):
    """
    Reads words from a CSV file and generates an MP3 file for each word.

    Args:
        csv_filepath (str): The path to the input CSV file.
        output_folder (str): The folder where MP3 files will be saved.
        tld (str): The top-level domain for the Google Translate host to be used
                   for accent selection (e.g., 'com' for US English, 'co.uk' for UK English).
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    words = []
    try:
        with open(csv_filepath, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                for item in row:
                    word = item.strip()
                    if word: # Ensure the word is not empty after stripping whitespace
                        words.append(word)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_filepath}")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    if not words:
        print("No words found in the CSV file.")
        return

    print(f"Found {len(words)} words. Starting MP3 generation...")

    # Wrap the words list with tqdm for a progress bar
    for word in tqdm(words, desc="Processing words", unit="word"):
        try:
            # The progress bar will display the current word due to tqdm's default behavior
            # No need for: print(f"Processing word {i+1}/{len(words)}: {word}")
            tts = gTTS(text=word, lang='en', tld=tld)
            sanitized_word = "".join(c if c.isalnum() or c in (' ', '-') else '' for c in word).strip()
            if not sanitized_word:
                # tqdm.write can be used to print messages without disturbing the progress bar
                tqdm.write(f"Skipping word '{word}' as it results in an empty filename after sanitization.")
                continue
            mp3_filename = os.path.join(output_folder, f"{sanitized_word.replace(' ', '_')}.mp3")
            tts.save(mp3_filename)
            # tqdm.write(f"Saved MP3 for '{word}' as {mp3_filename}") # Optional: if you want to log successful saves
        except Exception as e:
            tqdm.write(f"Error generating MP3 for '{word}': {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert words from a CSV file to MP3 audio files using gTTS.")
    parser.add_argument("csv_filepath", help="Path to the input CSV file.")
    parser.add_argument("-o", "--output_folder", default="output_mp3s", help="Folder to save the output MP3 files (default: output_mp3s).")

    args = parser.parse_args()

    # Hardcode tld for British English
    british_english_tld = 'co.uk'

    create_mp3s_from_csv(args.csv_filepath, args.output_folder, tld=british_english_tld)
    print("MP3 generation process completed.")
