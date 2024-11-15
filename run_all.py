#!/usr/bin/env python3

import subprocess
import itertools
import json
import os
from fontTools.ttLib import TTFont

OUTPUT_DIR = 'output'

def cleanup_font_name(input_file, output_file):
    try:
        # Load the input font
        font = TTFont(input_file)

        # Access the 'name' table which contains metadata like font name
        name_table = font['name']

        # Iterate through all name entries and modify the family name (nameID == 1)
        for record in name_table.names:
            if record.nameID == 1:  # Font Family name
                original_name = record.string.decode('utf-16-be')  # Decode to string
                modified_name = original_name.replace("-", " ")  # Replace dashes with spaces
                
                print(f"Old: {original_name} New {modified_name}")
                record.string = modified_name.encode('utf-16-be')  # Encode back to utf-16

        # Save the modified font to the output file
        font.save(output_file)
        print(f"Font name changed successfully! Saved to {output_file}")
    
    except Exception as e:
        print(f"Error: {e}")

def run_build_commands(data, config, save_config):
    # Generate the font name

    node_cmd = f"time node --max_old_space_size=8192 --optimize_for_size --stack_size=4096 --require babel-core/register ./index.js --config={config} --data={data}"

    if save_config:
        node_cmd += " --save_config"

    # Define the commands
    commands = [
        "rm -f build/svg/*",
        node_cmd,
    ]

    # Run the commands
    for command in commands:
        print(f"Running: {command}")
        subprocess.run(command, shell=True, check=True, executable="/bin/bash")


def main(save_config=False, small_data=False):

    if small_data:  
        data_options = ["src/data-small-org.json"]
    else:
        data_options = ["src/data.json"]

    config_options = [
        "src/config/default.js",
        "src/config/catus.bottom.js",
        "src/config/catus.left.js",
        "src/config/catus.top.js",
        "src/config/leo.bottom.js",
        "src/config/leo.left.js",
        "src/config/leo.top.js",
        "src/config/onca.bottom.js",
        "src/config/onca.left.js",
        "src/config/onca.top.js",
        "src/config/tigris.bottom.js",
        "src/config/tigris.left.js",
        "src/config/tigris.top.js",
    ]

    # Generate all combinations of the parameters
    combinations = itertools.product(data_options, config_options)

    # Loop through each combination and run the commands
    for data, config in combinations:
        print(f"Processing combination: data={data}, config={config}")
        run_build_commands(data, config, save_config)

        json_config = config.replace(".js", ".json")
        parameters = json.load(json_config)
        fontname = parameters['fontName']
        fontpath = os.path.join(OUTPUT_DIR, fontname+".ttf")
        cleanup_font_name(fontpath, fontpath)

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build fonts for all available config")
    parser.add_argument('--save_config', action='store_true', help="Save the configuration then quit (optional)")
    parser.add_argument('--small_data', action='store_true', help="Use small data (optional)")

    args = parser.parse_args()

    main(save_config=args.save_config, small_data=args.small_data)