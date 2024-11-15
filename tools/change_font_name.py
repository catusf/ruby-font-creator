import sys
from fontTools.ttLib import TTFont

def change_font_name(input_file, output_file):
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

if __name__ == "__main__":
    # Check if enough arguments were provided
    if len(sys.argv) != 3:
        print("Usage: python change_font_name.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

        change_font_name(input_file, output_file)
