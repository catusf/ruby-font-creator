import json
import os
import subprocess

OUTPUT_DIR = 'output'

# Function to load JSON data
def load_json(json_filepath):
    with open(json_filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


# Function to run pyftsubset command
def run_pyftsubset(base_font_filepath, output_directory):
    # Prepare the pyftsubset command
    _, filepath = os.path.split(base_font_filepath)
    subset_font = filepath.replace(".ttf", "-subset.ttf")
    subset_font_path = os.path.join(output_directory, subset_font)
    command = [
        'pyftsubset', base_font_filepath.replace("/", "\\"), 
        '--unicodes="U+0000-007F"', 
        '--unicodes="U+0080-00FF"', 
        '--unicodes="U+0100-017F"', 
        '--unicodes="U+0180-024F"', 
        '--unicodes="U+0300-036F"', 
        f'--output-file={subset_font_path}', 
    ]
    
    output = subprocess.run(command, check=False)

    return subset_font_path

# Function to run pyftmerge command
def run_pyftmerge(infont_name1, infont_name2, output_font):
    # Prepare the pyftmerge command
    command = [
        'pyftmerge', 
        infont_name1, 
        infont_name2, 
        f'--output-file={output_font}',
    ]
    
    subprocess.run(command, check=True)

BASE_FOLDER = "ruby-font-creator"

# Function to find the ruby-font-creator directory path from baseFontFilepath
def make_relative(base_font_filepath):

    pos = base_font_filepath.find(BASE_FOLDER)

    if pos < 0:
        raise FileNotFoundError(f"ruby-font-creator path not found: {base_font_filepath}")
        # return None
    
    return base_font_filepath[pos + len(BASE_FOLDER) + 1:]

    # # Get the directory of the base font
    # font_dir = os.path.dirname(base_font_filepath)
    
    # # Find the ruby-font-creator directory (assuming it's a sibling directory)
    # ruby_font_creator_dir = os.path.abspath(os.path.join(font_dir, '../../ruby-font-creator/resources/fonts'))
    
    # # Check if the directory exists
    # if not os.path.exists(ruby_font_creator_dir):
    #     raise FileNotFoundError(f"Ruby font creator path not found: {ruby_font_creator_dir}")
    
    # return ruby_font_creator_dir

# Main function to load the json, check for subset and run necessary commands
def process_font(json_filepath, output_directory):
    # Load the JSON file
    json_data = load_json(json_filepath)
    
    # Get the base font filepath and font name from the JSON data
    base_font_filepath = json_data.get('baseFontFilepath')
    font_name = json_data.get('fontName')

    generated_font_path = os.path.join(OUTPUT_DIR, font_name+'.ttf')

    if not base_font_filepath or not font_name:
        print("Base font file path or font name not found in JSON.")
        return

    # Get the ruby-font-creator directory based on baseFontFilepath
    try:
        base_font_rel_path = make_relative(base_font_filepath)
        # print(f"Found ruby-font-creator path: {base_font_rel_path}")
    except FileNotFoundError as e:
        print(e)
        return
    
    # Update the baseFontFilepath if necessary (to point to the correct location)
    # base_font_filepath = os.path.join(ruby_font_creator_path, os.path.basename(base_font_filepath))

    # Check if the subset font already exists
    subset_font_path = run_pyftsubset(base_font_rel_path, output_directory)
    
    # Run pyftmerge
    print("Running pyftmerge...")
    run_pyftmerge(subset_font_path, generated_font_path, generated_font_path.replace(".ttf", "-final.ttf"))

# Example usage
if __name__ == "__main__":
    json_filepath = './src/config/catus.bottom.json'  # Path to your JSON file
    output_directory = 'output'         # Output directory
    process_font(json_filepath, output_directory)

