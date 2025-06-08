'''
Script to read words from a CSV file and download their pronunciations from Cambridge Dictionary.
'''
import csv
import os
import argparse
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

def download_cambridge_audio(word, output_folder, accent='uk'):
    """
    Downloads the audio pronunciation of a word from Cambridge Dictionary.

    Args:
        word (str): The word to download.
        output_folder (str): The folder to save the MP3 file.
        accent (str): 'uk' for British English, 'us' for American English.
    """
    headers = {'User-Agent': USER_AGENT}
    # Sanitize word for URL: replace spaces with hyphens, keep alphanumeric and hyphens
    url_word = re.sub(r'[^a-z0-9-]', '', word.lower().replace(' ', '-'))
    if not url_word:
        tqdm.write(f"Skipping word '{word}' as it results in an empty URL component after sanitization.")
        return

    dictionary_url = f"https://dictionary.cambridge.org/dictionary/english/{url_word}"

    try:
        response = requests.get(dictionary_url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the audio source. This selector might need adjustment if the website structure changes.
        # We prioritize UK English audio based on the 'uk' class and data-src-mp3 attribute.
        # Example structure: <source src="/media/english/uk_pron/u/ukc/ukcfd/ukcfd00001.mp3" type="audio/mpeg">
        audio_tag = None
        if accent == 'uk':
            audio_tag = soup.find('source', type='audio/mpeg', src=lambda s: s and f'/uk_pron/' in s)
        elif accent == 'us':
            audio_tag = soup.find('source', type='audio/mpeg', src=lambda s: s and f'/us_pron/' in s)
        
        if not audio_tag or not audio_tag.get('src'):
            tqdm.write(f"Audio not found for '{word}' with '{accent}' accent on Cambridge Dictionary. URL: {dictionary_url}")
            return

        mp3_url = "https://dictionary.cambridge.org" + audio_tag['src']
        audio_response = requests.get(mp3_url, headers=headers, timeout=10)
        audio_response.raise_for_status()

        # Sanitize filename from the original word for saving
        sanitized_filename_word = "".join(c if c.isalnum() or c in (' ', '-') else '' for c in word).strip()
        if not sanitized_filename_word:
            tqdm.write(f"Skipping word '{word}' as it results in an empty filename after sanitization for saving.")
            return
        
        mp3_filename = os.path.join(output_folder, f"{sanitized_filename_word.replace(' ', '_')}_{accent}.mp3")
        
        with open(mp3_filename, 'wb') as f:
            f.write(audio_response.content)
        # tqdm.write(f"Saved MP3 for '{word}' ({accent}) as {mp3_filename}") # Optional success log

    except requests.exceptions.RequestException as e:
        tqdm.write(f"Error downloading audio for '{word}': {e} (URL: {dictionary_url})")
    except Exception as e:
        tqdm.write(f"An unexpected error occurred for '{word}': {e}")

def create_mp3s_from_csv(csv_filepath, output_folder='output_mp3s', accent='uk'):
    """
    Reads words from a CSV file and downloads their pronunciations.

    Args:
        csv_filepath (str): The path to the input CSV file.
        output_folder (str): The folder where MP3 files will be saved.
        accent (str): 'uk' or 'us' for accent selection.
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
                    if word:
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

    print(f"Found {len(words)} words. Starting MP3 generation from Cambridge Dictionary ({accent.upper()} accent)...")

    for word in tqdm(words, desc="Processing words", unit="word"):
        download_cambridge_audio(word, output_folder, accent)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download word pronunciations from Cambridge Dictionary using a CSV file.")
    parser.add_argument("csv_filepath", help="Path to the input CSV file.")
    parser.add_argument("-o", "--output_folder", default="output_mp3s", help="Folder to save the output MP3 files (default: output_mp3s).")
    parser.add_argument("-a", "--accent", default="uk", choices=['uk', 'us'], help="Pronunciation accent: 'uk' for British, 'us' for American (default: uk).")

    args = parser.parse_args()

    create_mp3s_from_csv(args.csv_filepath, args.output_folder, args.accent)
    print("MP3 download process completed.")
