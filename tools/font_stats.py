from fontTools.ttLib import TTFont
from collections import defaultdict
import unicodedata

# Define Unicode block ranges manually
UNICODE_BLOCKS = {
    "Basic Latin": (0x0000, 0x007F),
    "Latin-1 Supplement": (0x0080, 0x00FF),
    "Latin Extended-A": (0x0100, 0x017F),
    "Latin Extended-B": (0x0180, 0x024F),
    "IPA Extensions": (0x0250, 0x02AF),
    "Spacing Modifier Letters": (0x02B0, 0x02FF),
    "Combining Diacritical Marks": (0x0300, 0x036F),
    "Greek and Coptic": (0x0370, 0x03FF),
    "Cyrillic": (0x0400, 0x04FF),
    "Hebrew": (0x0590, 0x05FF),
    "Arabic": (0x0600, 0x06FF),
    "Devanagari": (0x0900, 0x097F),
    "Bengali": (0x0980, 0x09FF),
    "Gurmukhi": (0x0A00, 0x0A7F),
    "Gujarati": (0x0A80, 0x0AFF),
    "Oriya": (0x0B00, 0x0B7F),
    "Tamil": (0x0B80, 0x0BFF),
    "Telugu": (0x0C00, 0x0C7F),
    "Kannada": (0x0C80, 0x0CFF),
    "Malayalam": (0x0D00, 0x0D7F),
    "Thai": (0x0E00, 0x0E7F),
    "Lao": (0x0E80, 0x0EFF),
    "Georgian": (0x10A0, 0x10FF),
    "Hangul Jamo": (0x1100, 0x11FF),
    "Latin Extended Additional": (0x1E00, 0x1EFF),
    "Greek Extended": (0x1F00, 0x1FFF),
    "General Punctuation": (0x2000, 0x206F),
    "Superscripts and Subscripts": (0x2070, 0x209F),
    "Currency Symbols": (0x20A0, 0x20CF),
    "Combining Diacritical Marks for Symbols": (0x20D0, 0x20FF),
    "Letterlike Symbols": (0x2100, 0x214F),
    "Number Forms": (0x2150, 0x218F),
    "Arrows": (0x2190, 0x21FF),
    "Mathematical Operators": (0x2200, 0x22FF),
    "Miscellaneous Technical": (0x2300, 0x23FF),
    "Control Pictures": (0x2400, 0x243F),
    "Optical Character Recognition": (0x2440, 0x245F),
    "Enclosed Alphanumerics": (0x2460, 0x24FF),
    "Box Drawing": (0x2500, 0x257F),
    "Block Elements": (0x2580, 0x259F),
    "Geometric Shapes": (0x25A0, 0x25FF),
    "Miscellaneous Symbols": (0x2600, 0x26FF),
    "Dingbats": (0x2700, 0x27BF),
    "Braille Patterns": (0x2800, 0x28FF),
    "CJK Radicals Supplement": (0x2E80, 0x2EFF),
    "Kangxi Radicals": (0x2F00, 0x2FDF),
    "Ideographic Description Characters": (0x2FF0, 0x2FFF),
    "CJK Symbols and Punctuation": (0x3000, 0x303F),
    "Hiragana": (0x3040, 0x309F),
    "Katakana": (0x30A0, 0x30FF),
    "Bopomofo": (0x3100, 0x312F),
    "Hangul Compatibility Jamo": (0x3130, 0x318F),
    "Kanbun": (0x3190, 0x319F),
    "Bopomofo Extended": (0x31A0, 0x31BF),
    "CJK Strokes": (0x31C0, 0x31EF),
    "Katakana Phonetic Extensions": (0x31F0, 0x31FF),
    "Enclosed CJK Letters and Months": (0x3200, 0x32FF),
    "CJK Compatibility": (0x3300, 0x33FF),
    "CJK Unified Ideographs Extension A": (0x3400, 0x4DBF),
    "Yijing Hexagram Symbols": (0x4DC0, 0x4DFF),
    "Private Use Area": (0xE000, 0xF8FF),
    "CJK Compatibility Ideographs": (0xF900, 0xFAFF),
    "Alphabetic Presentation Forms": (0xFB00, 0xFB4F),
    "Arabic Presentation Forms-A": (0xFB50, 0xFDFF),
    "Variation Selectors": (0xFE00, 0xFE0F),
    "Vertical Forms": (0xFE10, 0xFE1F),
    "Combining Half Marks": (0xFE20, 0xFE2F),
    "CJK Compatibility Forms": (0xFE30, 0xFE4F),
    "Small Form Variants": (0xFE50, 0xFE6F),
    "Arabic Presentation Forms-B": (0xFE70, 0xFEFF),
    "Halfwidth and Fullwidth Forms": (0xFF00, 0xFFEF),
    "Specials": (0xFFF0, 0xFFFF),
}

def get_unicode_block(codepoint):
    for block_name, (start, end) in UNICODE_BLOCKS.items():
        if start <= codepoint <= end:
            return block_name
    return "Unknown"

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
    # "Basic Latin",
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
        block_name = get_unicode_block(codepoint)
        unicode_blocks[block_name]["count"] += 1
        code2block[codepoint] = block_name
    
    for block_name, (start, end) in UNICODE_BLOCKS.items():
        unicode_blocks[block_name]["total"] = end - start + 1
    
    list_to_add = []

    for codepoint in cmap.keys():
        if code2block[codepoint] in included_blocks:
            list_to_add.append(codepoint)
    
    # Example usage:
    file_path = 'src/noto_codepoints.json'
    file_path_added = 'src/added_codepoints.json'

    save_list_to_json(sorted(list(cmap.keys())), file_path)
    save_list_to_json(sorted(list_to_add), file_path_added)
    
    # Output the results
    filtered_results = [
        f"{block} ({counts['count']} codepoints/{counts['total']} total)"
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


# font_path = "build/Noto-Sans-Mono-Bottom.ttf"  # Replace with the path to your TTF/OTF font file
# summarize_font(font_path)
