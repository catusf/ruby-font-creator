#!/usr/bin/env python3

import subprocess
import itertools
import json
import os
from fontTools.ttLib import TTFont

OUTPUT_DIR = 'output'

def get_name_encoding(name):
    """
    Parameters:
        names (NameRecord): Name record from the naming record
    Returns:
        The cmap codepoint encoding.
        If GDI does not support the name, return None.
    """
    # From: https://github.com/MicrosoftDocs/typography-issues/issues/956#issuecomment-1205678068
    if name.platformID == 3:
        if name.platEncID == 3:
            return "cp936"
        elif name.platEncID == 4:
            if name.nameID == 2:
                return "utf_16_be"
            else:
                return "cp950"
        elif name.platEncID == 5:
            if name.nameID == 2:
                return "utf_16_be"
            else:
                return "cp949"
        else:
            return "utf_16_be"
    elif name.platformID == 1 and name.platEncID == 0:
        return "iso-8859-1"

    return None

def get_decoded_name(name) -> str:
    """
    Parameters:
        names (NameRecord): Name record from the naming record
    Returns:
        The decoded name
    """

    encoding = get_name_encoding(name)

    if name.platformID == 3 and encoding != "utf_16_be":
        # Compatibility for really old font
        name_to_decode = name.string.replace(b"\x00", b"")
    else:
        name_to_decode = name.string

    return name_to_decode.decode(encoding)

def cleanup_font_name(input_file, output_file):
    """ Remove the - character in font name
    """

    # Load the font file
    font = TTFont(input_file)

    fontFamilyName = font['name'].getDebugName(1)
    newfontFamilyName = fontFamilyName.replace("-", " ")

    # Access the 'name' table
    name_table = font['name']

    # Iterate through the name table to find the font name entry (name_id = 4)
    for record in name_table.names:
        encoding = get_name_encoding(record)

        decoded_name = record.string.decode(encoding)
        # print(f"{decoded_name=}")

        if fontFamilyName == decoded_name:  # Font Name
            record.string = newfontFamilyName.encode(encoding)

    font.save(output_file)
    print(f"Font has been updated and saved as '{newfontFamilyName}' in '{output_file}'.")

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

        with open(json_config, "r", encoding="utf-8") as f:
            parameters = json.load(f)
    
            fontname = parameters['fontName']
            fontpath = os.path.join(OUTPUT_DIR, fontname+".ttf")
            new_fontpath = os.path.join(OUTPUT_DIR, fontname+"-new.ttf")
        
            cleanup_font_name(fontpath, new_fontpath)

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build fonts for all available config")
    parser.add_argument('--save_config', action='store_true', help="Save the configuration then quit (optional)")
    parser.add_argument('--small_data', action='store_true', help="Use small data (optional)")

    args = parser.parse_args()

    main(save_config=args.save_config, small_data=args.small_data)