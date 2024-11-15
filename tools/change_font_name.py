import sys
from fontTools.ttLib import TTFont

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


if __name__ == "__main__":
    # Check if enough arguments were provided
    if len(sys.argv) != 3:
        print("Usage: python change_font_name.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

        cleanup_font_name(input_file, output_file)
