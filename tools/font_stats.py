

from fontTools.ttLib import TTFont
from collections import defaultdict
import unicodedata
import unicodedataplus as ud

def codepoint_to_int(codepoint):
    """
    Convert a Unicode code point (e.g., "U+3428") to its corresponding character.

    :param codepoint: A string representing the Unicode code point (e.g., "U+3428").
    :return: The corresponding character.
    """
    # Convert the codepoint to an integer
    unicode_int = int(codepoint[2:], 16)
    
    return unicode_int
import json

def save_list_to_json(int_list, file_path):
    """
    Save a list of integers to a JSON file.

    :param int_list: List of integers to be saved.
    :param file_path: The file path where the JSON file will be saved.
    """
    with open(file_path, 'w') as json_file:
        json.dump(int_list, json_file, indent=4)


included_blocks = set([
    "Basic Latin",
    "Latin-1 Supplement",
    "Latin Extended-A",
    "Latin Extended-B",
    # "Combining Diacritical Marks",
    # "Latin Extended Additional",
    # "General Punctuation",
    # "Superscripts and Subscripts",
    # "Currency Symbols",
    # "Combining Diacritical Marks for Symbols"
    ]
 )

import unicodedata

def get_unicode_blocks():
    block_items = {}
    for i in range(0x110000):  # Unicode range up to 0x10FFFF
        block_name = ud.block(chr(i))
        block_items.setdefault(block_name, [])
        block_items[block_name].append(chr(i))

    return block_items

block_items = get_unicode_blocks()

def summarize_font(font_path):
    print(f'Summary for {font_path}')
    font = TTFont(font_path)
    cmap = font['cmap'].getcmap(3, 1).cmap  # Platform 3 (Windows), Encoding 1 (Unicode)
    code2block = {}
    
    if 'CFF ' in font:
        num_glyphs = len(font['CFF '].cff.topDictIndex[0].CharStrings.charStrings)
    else:
        num_glyphs = len(font['glyf'].glyphs)
    
    num_codepoints = len(cmap)
    
    unicode_blocks = defaultdict(lambda: {"count": 0, "total": 0})

    font.close()

    for codepoint in cmap.keys():
        block_name = ud.block(chr(codepoint))
        unicode_blocks[block_name]["count"] += 1
        code2block[codepoint] = block_name
    
    # for block_name, (start, end) in UNICODE_BLOCKS.items():
    #     unicode_blocks[block_name]["total"] = end - start + 1
    
    list_to_add = []

    ignore_list = {codepoint_to_int("U+002F")}
    for codepoint in cmap.keys():
        if codepoint in ignore_list:
            continue

        if True or code2block[codepoint] in included_blocks:
            list_to_add.append(codepoint)
    
    # Example usage:
    file_path = 'src/noto_codepoints.json'
    file_path_added = 'src/added_codepoints.json'

    save_list_to_json(sorted(list(cmap.keys())), file_path)
    save_list_to_json(sorted(list_to_add), file_path_added)
    
    # Output the results
    filtered_results = [
        f"{block} ({counts['count']} codepoints/{len(block_items[block])} total)"
        for block, counts in unicode_blocks.items()
        if counts["count"] > 0
    ]

    for result in filtered_results:
        print(result)

    print(f"\nNumber of Glyphs: {num_glyphs}")
    print(f"Number of Codepoints: {num_codepoints}")
    print(f"Total in those blocks: {sum([v['count'] for v in unicode_blocks.values()])}")

# Example usage:
font_path = "resources/fonts/NotoSansSC-Regular.ttf"  # Replace with the path to your TTF/OTF font file
summarize_font(font_path)



# for block in block_items:
#     print(f"{block}: {len(block_items[block])} code points")
