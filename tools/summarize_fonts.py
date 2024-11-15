import os
import json
from fontTools.ttLib import TTFont

# Path to your local 'src/config' folder
config_folder_path = 'src/config'
font_summary_file = 'font_summary.json'
markdown_file = 'font_summary.md'
prefix = "ruby-font-creator/"

def fix_file_path(path):
    return path[pos + len(prefix):] if (pos := path.find(prefix)) >= 0 else path
    
# Function to extract relevant data from JSON files in the 'src/config' folder
def extract_font_config_from_folder(config_folder_path):
    # Initialize an empty list to store summaries
    summary_list = []

    # List all files in the 'src/config' folder
    json_files = [f for f in os.listdir(config_folder_path) if f.endswith('.json')]

    for json_file in json_files:
        summary = {
            "config": json_file,
            "baseFontFilepath": None,
            "rubyFontFilepath": None,
            "fontName": None,
            "baseFontName": None,
            "rubyFontName": None
        }

        file_path = os.path.join(config_folder_path, json_file)
        
        # Open and read each JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            # Parse JSON content
            try:
                config_data = json.loads(content)
            except json.JSONDecodeError:
                print(f"Error parsing JSON in {json_file}")
                continue

            # Extract relevant data based on expected keys
            if 'baseFontFilepath' in config_data:
                summary["baseFontFilepath"] = fix_file_path(config_data['baseFontFilepath'])
            if 'rubyFontFilepath' in config_data:
                summary["rubyFontFilepath"] = fix_file_path(config_data['rubyFontFilepath'])
            if 'fontName' in config_data:
                summary["fontName"] = config_data['fontName'].replace("-", " ")

            # Extract font names from font files
            extract_font_names(summary)

            # Append the summary to the list
            summary_list.append(summary)

    # Save summary list to font_summary.json file
    save_summary_to_json(summary_list)

    return summary_list

# Function to extract the font name from a font file (e.g., .ttf or .otf)
def extract_font_names(summary):
    # Extract font names from base and ruby font files
    base_font_filepath = summary.get("baseFontFilepath")
    ruby_font_filepath = summary.get("rubyFontFilepath")

    # Extract font name from base font file if available
    if base_font_filepath and os.path.isfile(base_font_filepath):
        base_font_name = get_font_name_from_file(base_font_filepath)
        summary["baseFontName"] = base_font_name

    # Extract font name from ruby font file if available
    if ruby_font_filepath and os.path.isfile(ruby_font_filepath):
        ruby_font_name = get_font_name_from_file(ruby_font_filepath)
        summary["rubyFontName"] = ruby_font_name

# Function to extract font name from font file using fontTools
def get_font_name_from_file(font_file):
    try:
        font = TTFont(font_file)
        name_table = font['name']
        return name_table.getBestFullName()
    
    except Exception as e:
        print(f"Error reading font file {font_file}: {e}")
    return None

# Function to save summary to a JSON file
def save_summary_to_json(summary_list):
    with open(font_summary_file, 'w', encoding='utf-8') as json_file:
        json.dump(summary_list, json_file, ensure_ascii=False, indent=4)
        print(f"Summary saved to {font_summary_file}")

# Function to convert font summary JSON into Markdown format
def convert_summary_to_markdown(summary_list):
    markdown_content = "# Font Summary\n\n"

    # Markdown table headers (changed order here)
    markdown_content += "| Config File | Base Font Name | Ruby Font Name | Base Font Filepath | Ruby Font Filepath |\n"
    markdown_content += "|-------------|----------------|----------------|--------------------|--------------------|\n"

    # Add rows for each summary entry
    for summary in summary_list:
        markdown_content += f"| {summary['config']} | {summary.get('baseFontName', 'N/A')} | {summary.get('rubyFontName', 'N/A')} | {summary.get('baseFontFilepath', 'N/A')} | {summary.get('rubyFontFilepath', 'N/A')} |\n"

    return markdown_content

# Function to save the markdown content to a .md file
def save_markdown_file(markdown_content):
    with open(markdown_file, 'w', encoding='utf-8') as md_file:
        md_file.write(markdown_content)
        print(f"Markdown file saved to {markdown_file}")

# Example usage:
summary_list = extract_font_config_from_folder(config_folder_path)

# Convert the summary list to markdown format
markdown_content = convert_summary_to_markdown(summary_list)

# Save the markdown content to a .md file
save_markdown_file(markdown_content)
