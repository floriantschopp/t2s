# CSV to MP3 Conversion Scripts

This project provides two Python scripts to convert words from a CSV file into MP3 audio pronunciations:

1.  **`t2s.py`**: Uses Google Text-to-Speech (gTTS) to generate audio.
    *   Relies on Google Translate's TTS engine.
    *   Currently hardcoded for British English accent (`tld='co.uk'`).
2.  **`cdd.py`**: Downloads audio pronunciations from the Cambridge Dictionary website.
    *   Scrapes the dictionary website for official pronunciation files.
    *   Allows selection between UK and US accents.

**Note on Voice Gender (for `t2s.py` with gTTS):** `gTTS` does not provide a direct option to select a specific voice gender. The voice used is the default provided by Google Translate for the selected language and accent. For British English (`tld='co.uk'`), this often results in a voice perceived as female, but this is not guaranteed.

**Note on Web Scraping (for `cdd.py`):** The `cdd.py` script scrapes the Cambridge Dictionary website. Please be mindful of their terms of service and use the script responsibly to avoid overloading their servers.

## Setup and Usage

### 1. Create and Activate a Virtual Environment

It is recommended to use a virtual environment to manage project dependencies.

```bash
# Create a virtual environment (e.g., named .venv)
python3 -m venv .t2s_venv

# Activate the virtual environment
# On macOS and Linux:
source .t2s_venv/bin/activate
# On Windows (Git Bash or similar):
# source .t2s_venv/Scripts/activate
# On Windows (Command Prompt):
# .t2s_venv\Scripts\activate.bat
```

### 2. Install Dependencies

Once the virtual environment is activated, install the required packages from `requirements.txt`. This file includes dependencies for both scripts.

```bash
pip install -r requirements.txt
```

### 3. Prepare Your CSV File

Ensure you have a CSV file with the words you want to convert. By default, the script looks for `example.csv` in the same directory. Each cell in the CSV will be treated as a word.

For example, `example.csv`:
```csv
Hello,World
Python,Is,Fun
```

### 4. Run the Scripts

You can choose which script to run based on your preferred audio source.

#### A. Using `t2s.py` (Google Text-to-Speech)

This script uses gTTS and is hardcoded for a British English accent.

```bash
# Example:
python t2s.py example.csv

# To specify an output folder:
python t2s.py path/to/your/input.csv --output_folder path/to/your/gtts_output
```

#### B. Using `cdd.py` (Cambridge Dictionary)

This script downloads audio from the Cambridge Dictionary website.

```bash
# Example (defaulting to UK accent):
python cdd.py example.csv

# To specify US accent:
python cdd.py example.csv -a us

# To specify an output folder:
python cdd.py path/to/your/input.csv --output_folder path/to/your/cambridge_output -a uk
```

The scripts will create the specified output folder (if it doesn't exist) and save the generated MP3 files there.

### 5. Deactivate the Virtual Environment (Optional)

When you are finished, you can deactivate the virtual environment:

```bash
deactivate
```
