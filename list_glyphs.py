from fontTools.ttLib import TTFont

def list_glyphs(font_path):
    # Open the font file
    font = TTFont(font_path)
    
    # Get the 'glyf' table, which contains the glyphs
    glyf_table = font['glyf']
    
    # List all glyph names
    glyph_names = glyf_table.keys()
    
    # Print the glyph names
    for glyph_name in glyph_names:
        print(glyph_name)

if __name__ == "__main__":
    font_path = "resources/fonts/Mengshen-Handwritten.ttf"  # Replace with your font file path
    list_glyphs(font_path)
