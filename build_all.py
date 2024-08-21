import os
import subprocess
import itertools

font_name_map = {
'resources/fonts/NotoSansSC-Regular.ttf': 'Noto-Sans', 
'resources/fonts/NotoSerifSC-Regular.ttf': 'Noto-Serif',
'resources/fonts/XiaolaiMonoSC-Regular.ttf': 'Xiaolai-Mono',
'resources/fonts/LXGWWenKaiMono-Regular.ttf': 'WenKai-Serif'
}

def get_font_name(data, base_font, config):
    # Determine parts of the font name based on parameters
    data_part = "Small" if "small" in data else ""
    config_part = config.replace("src/config/", "").replace(".js", "").capitalize()
    font_part = font_name_map[base_font]

    # Construct the font name
    font_name = f"Leo-Pinyin-{data_part}-{config_part}-{font_part}"
    return font_name.replace("--", "")

def run_commands(data, base_font, config):
    # Generate the font name
    font_name = get_font_name(data, base_font, config)

    # Define the commands
    commands = [
        "rm -f build/svg/*",
        f"time node --max_old_space_size=8192 --optimize_for_size --stack_size=4096 --require babel-core/register ./index.js --config={config} --data={data} --font-name={font_name} --base-font={base_font} --ruby-font=resources/fonts/LXGWWenKaiMono-Regular.ttf",
        f"python3 tools/font_stats.py build/{font_name}.ttf --detailed"
    ]

    # Run the commands
    for command in commands:
        print(f"Running: {command}")
        subprocess.run(command, shell=True, check=True)

def main():
    # data_options = ['src/data-small-org.json', 'src/data.json']
    data_options = ['src/data-small-org.json']

    base_font_options = [
        # 'resources/fonts/NotoSansSC-Regular.ttf', 
        # 'resources/fonts/NotoSerifSC-Regular.ttf',
        'resources/fonts/XiaolaiMonoSC-Regular.ttf',
        'resources/fonts/LXGWWenKaiMono-Regular.ttf'
                         ]
    config_options = ['src/config/top.js', 'src/config/bottom.js', 'src/config/left.js']

    # Generate all combinations of the parameters
    combinations = itertools.product(data_options, base_font_options, config_options)

    # Loop through each combination and run the commands
    for data, base_font, config in combinations:
        print(f"Processing combination: data={data}, base_font={base_font}, config={config}")
        run_commands(data, base_font, config)

if __name__ == "__main__":
    main()
