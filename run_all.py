#!/usr/bin/env python3

import os
import subprocess
import itertools


def run_commands(data, config):
    # Generate the font name

    # Define the commands
    commands = [
        "rm -f build/svg/*",
        f"time node --max_old_space_size=8192 --optimize_for_size --stack_size=4096 --require babel-core/register ./index.js --config={config} --data={data}",
        # f"python3 tools/font_stats.py build/{font_name}.ttf --detailed"
    ]

    # Run the commands
    for command in commands:
        print(f"Running: {command}")
        subprocess.run(command, shell=True, check=True, executable="/bin/bash")


def main():
    data_options = ["src/data-small-org.json", "src/data.json"]
    # data_options = ["src/data-small-org.json"]

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
        run_commands(data, config)


if __name__ == "__main__":
    main()
