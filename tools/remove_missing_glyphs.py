from fontTools.ttLib import TTFont

def remove_missing_glyph_references(font_path, missing_glyphs):
    # Load the font
    font = TTFont(font_path)
    
    # Check if the font has a GDEF table
    if 'GDEF' not in font:
        print("GDEF table not found in the font.")
        return
    
    gdef_table = font['GDEF'].table

    # Helper function to remove references from a list
    def filter_missing_glyphs(glyph_list):
        return [glyph for glyph in glyph_list if glyph not in missing_glyphs]

    # Remove references from GlyphClassDef
    if gdef_table.GlyphClassDef:
        gdef_table.GlyphClassDef.classDefs = {glyph: class_def for glyph, class_def in gdef_table.GlyphClassDef.classDefs.items() if glyph not in missing_glyphs}

    # Remove references from AttachList
    if gdef_table.AttachList:
        gdef_table.AttachList.Coverage.glyphs = filter_missing_glyphs(gdef_table.AttachList.Coverage.glyphs)

    # Remove references from LigCaretList
    if gdef_table.LigCaretList:
        gdef_table.LigCaretList.Coverage.glyphs = filter_missing_glyphs(gdef_table.LigCaretList.Coverage.glyphs)

    # Remove references from MarkAttachClassDef
    if gdef_table.MarkAttachClassDef:
        gdef_table.MarkAttachClassDef.classDefs = {glyph: class_def for glyph, class_def in gdef_table.MarkAttachClassDef.classDefs.items() if glyph not in missing_glyphs}

    # Save the updated font
    fixed_font_path = font_path.replace('.ttf', '_fixed.ttf')
    font.save(fixed_font_path)
    print(f"References to missing glyphs have been removed. Saved as {fixed_font_path}.")

# Define the font file path and missing glyphs
font_path = '/workspaces/Mengshen-pinyin-font/res/fonts/han-serif/WenQuanYiMicroHeiMono-Reduced.ttf'
missing_glyphs = ['uniFA0C', 'uniFA0D',]  # Remove the '/' as glyph names do not include it

# Remove missing glyph references
remove_missing_glyph_references(font_path, missing_glyphs)


