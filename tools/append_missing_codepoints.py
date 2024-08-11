import json


def codepoint_to_int(codepoint):
    """
    Convert a Unicode code point (e.g., "U+3428") to its corresponding character.

    :param codepoint: A string representing the Unicode code point (e.g., "U+3428").
    :return: The corresponding character.
    """
    # Convert the codepoint to an integer
    unicode_int = int(codepoint[2:], 16)
    
    return unicode_int

def codepoint_to_char(codepoint):
    """
    Convert a Unicode code point (e.g., "U+3428") to its corresponding character.

    :param codepoint: A string representing the Unicode code point (e.g., "U+3428").
    :return: The corresponding character.
    """
    # Convert the codepoint to an integer
    unicode_int = int(codepoint[2:], 16)
    
    # Convert the integer to the corresponding character
    character = chr(unicode_int)
    
    return character
def load_glyph_data_json_to_dict(file_path):
    """
    Load a list of integers from a JSON file and convert it to a set.

    :param file_path: The file path of the JSON file to be loaded.
    :return: A set of integers.
    """
    with open(file_path, 'r') as json_file:
        list_glyph = json.load(json_file)

        dict_glyph = {codepoint_to_char(item['codepoint']): {item['glyph'], item['ruby']} for item in list_glyph}

    return list_glyph, dict_glyph

def load_noto_json_to_set(file_path):
    """
    Load a list of integers from a JSON file and convert it to a set.

    :param file_path: The file path of the JSON file to be loaded.
    :return: A set of integers.
    """
    with open(file_path, 'r') as json_file:
        int_list = json.load(json_file)
        int_set = set([chr(item) for item in int_list])
    return int_set

# Example usage:
file_path = '/workspaces/ruby-font-creator/src/added_codepoints.json'
noto_set = load_noto_json_to_set(file_path)
print(len(noto_set))

data_file_path = '/workspaces/ruby-font-creator/src/data-full.json'
list_glyph, dict_glyph = load_glyph_data_json_to_dict(data_file_path)
set_glyph = set(dict_glyph.keys())
print(len(dict_glyph))

not_in_data = noto_set - set_glyph
print(len(not_in_data))

def char_to_codepoint(char):
    """
    Convert a character to its corresponding Unicode code point in the format "U+XXXX".

    :param char: A single character string.
    :return: The corresponding Unicode code point as a string in the format "U+XXXX".
    """
    # Get the Unicode code point of the character
    unicode_int = ord(char)
    
    # Convert to the "U+XXXX" format
    codepoint = f"U+{unicode_int:04X}"
    
    return codepoint


for item in not_in_data:
    list_glyph.append(  
        {
        "codepoint": char_to_codepoint(item),
        "ruby": "",
        "glyph": item
        }
  )

new_data_file= '/workspaces/ruby-font-creator/src/data-new.json'

with open(new_data_file, 'w', encoding='utf-8') as json_file:
    json.dump(list_glyph, json_file, indent=4, ensure_ascii=False)

print(len(list_glyph))