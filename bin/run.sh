#!/bin/bash

# Directory containing the configuration files
CONFIG_DIR="src/config"

# Iterate over each .js file in the directory
for config_file in "$CONFIG_DIR"/*.js; do
    # Check if the file name contains "common"
    if [[ $config_file == *"common"* ]]; then
        echo "Skipping $config_file (contains 'common')"
        continue
    fi

    echo "Processing $config_file (data.json)"
    
    # Run the node command with the specified options and configuration file
    time node --max_old_space_size=8192 \
              --optimize_for_size \
              --stack_size=4096 \
              --require babel-core/register \
              ./index.js --config="$config_file" --data=src/data.json
              
    echo "Finished processing $config_file (data.json)"
    echo ""
done
