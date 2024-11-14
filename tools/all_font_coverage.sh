#!/bin/bash

# Define the folder containing the .ttf files
folder="output"

# Check if the folder exists
if [ ! -d "$folder" ]; then
    echo "Folder '$folder' does not exist."
    exit 1
fi

# Loop through each .ttf file in the folder
for file in "$folder"/*.ttf; do
    if [ -f "$file" ]; then
        echo "Checking file: $file"
        python3 tools/font_coverage.py "$file"
    fi
done

echo "All checks completed."
