# CSV to MP3 Conversion Script

This script reads words from a CSV file and generates an MP3 audio file for each word using Google Text-to-Speech (gTTS).
By default, the script is configured to use a British English accent.

**Note on Voice Gender:** `gTTS` does not provide a direct option to select a specific voice gender (e.g., male/female). The voice used is the default provided by Google Translate for the selected language and accent. For British English (`tld='co.uk'`), this often results in a voice that is perceived as female, but this is not a guaranteed or configurable setting within `gTTS`.

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

Once the virtual environment is activated, install the required packages from `requirements.txt`:

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

### 4. Run the Script

Execute the Python script. You need to provide the path to your CSV file. You can optionally specify an output folder.
The script is hardcoded to use a British English accent.

```bash
# Example:
python t2s.py example.csv

# To specify an output folder:
python t2s.py path/to/your/input.csv --output_folder path/to/your/output_directory
```

The script will create the specified output folder (if it doesn't exist) and save the generated MP3 files there. Each MP3 file will be named after the word it contains (sanitized for file system compatibility).

### 5. Deactivate the Virtual Environment (Optional)

When you are finished, you can deactivate the virtual environment:

```bash
deactivate
```
