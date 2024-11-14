from fontTools.ttLib import TTFont

# import unicodedata
import argparse
import os

# Unicode block ranges (start, end, block name)
# Unicode block ranges (start, end, block name)
UNICODE_BLOCKS = [
    (0x0000, "C0 Controls and Basic Latin", 0x007F),
    (0x0080, "C1 Controls and Latin-1 Supplement", 0x00FF),
    (0x0100, "Latin Extended-A", 0x017F),
    (0x0180, "Latin Extended-B", 0x024F),
    (0x0250, "IPA Extensions", 0x02AF),
    (0x02B0, "Spacing Modifier Letters", 0x02FF),
    (0x0300, "Combining Diacritical Marks", 0x036F),
    (0x0370, "Greek and Coptic", 0x03FF),
    (0x0400, "Cyrillic", 0x04FF),
    (0x0500, "Cyrillic Supplement", 0x052F),
    (0x0530, "Armenian", 0x058F),
    (0x0590, "Hebrew", 0x05FF),
    (0x0600, "Arabic", 0x06FF),
    (0x0700, "Syriac", 0x074F),
    (0x0750, "Arabic Supplement", 0x077F),
    (0x0780, "Thaana", 0x07BF),
    (0x07C0, "NKo", 0x07FF),
    (0x0800, "Samaritan", 0x083F),
    (0x0840, "Mandaic", 0x085F),
    (0x0860, "Syriac Supplement", 0x086F),
    (0x0870, "Arabic Extended-B", 0x089F),
    (0x08A0, "Arabic Extended-A", 0x08FF),
    (0x0900, "Devanagari", 0x097F),
    (0x0980, "Bengali", 0x09FF),
    (0x0A00, "Gurmukhi", 0x0A7F),
    (0x0A80, "Gujarati", 0x0AFF),
    (0x0B00, "Oriya", 0x0B7F),
    (0x0B80, "Tamil", 0x0BFF),
    (0x0C00, "Telugu", 0x0C7F),
    (0x0C80, "Kannada", 0x0CFF),
    (0x0D00, "Malayalam", 0x0D7F),
    (0x0D80, "Sinhala", 0x0DFF),
    (0x0E00, "Thai", 0x0E7F),
    (0x0E80, "Lao", 0x0EFF),
    (0x0F00, "Tibetan", 0x0FFF),
    (0x1000, "Myanmar", 0x109F),
    (0x10A0, "Georgian", 0x10FF),
    (0x1100, "Hangul Jamo", 0x11FF),
    (0x1200, "Ethiopic", 0x137F),
    (0x1380, "Ethiopic Supplement", 0x139F),
    (0x13A0, "Cherokee", 0x13FF),
    (0x1400, "Unified Canadian Aboriginal Syllabics", 0x167F),
    (0x1680, "Ogham", 0x169F),
    (0x16A0, "Runic", 0x16FF),
    (0x1700, "Tagalog", 0x171F),
    (0x1720, "Hanunoo", 0x173F),
    (0x1740, "Buhid", 0x175F),
    (0x1760, "Tagbanwa", 0x177F),
    (0x1780, "Khmer", 0x17FF),
    (0x1800, "Mongolian", 0x18AF),
    (0x18B0, "Unified Canadian Aboriginal Syllabics Extended", 0x18FF),
    (0x1900, "Limbu", 0x194F),
    (0x1950, "Tai Le", 0x197F),
    (0x1980, "New Tai Lue", 0x19DF),
    (0x19E0, "Khmer Symbols", 0x19FF),
    (0x1A00, "Buginese", 0x1A1F),
    (0x1A20, "Tai Tham", 0x1AAF),
    (0x1AB0, "Combining Diacritical Marks Extended", 0x1AFF),
    (0x1B00, "Balinese", 0x1B7F),
    (0x1B80, "Sundanese", 0x1BBF),
    (0x1BC0, "Batak", 0x1BFF),
    (0x1C00, "Lepcha", 0x1C4F),
    (0x1C50, "Ol Chiki", 0x1C7F),
    (0x1C80, "Cyrillic Extended-C", 0x1C8F),
    (0x1C90, "Georgian Extended", 0x1CBF),
    (0x1CC0, "Sundanese Supplement", 0x1CCF),
    (0x1CD0, "Vedic Extensions", 0x1CFF),
    (0x1D00, "Phonetic Extensions", 0x1D7F),
    (0x1D80, "Phonetic Extensions Supplement", 0x1DBF),
    (0x1DC0, "Combining Diacritical Marks Supplement", 0x1DFF),
    (0x1E00, "Latin Extended Additional", 0x1EFF),
    (0x1F00, "Greek Extended", 0x1FFF),
    (0x2000, "General Punctuation", 0x206F),
    (0x2070, "Superscripts and Subscripts", 0x209F),
    (0x20A0, "Currency Symbols", 0x20CF),
    (0x20D0, "Combining Diacritical Marks for Symbols", 0x20FF),
    (0x2100, "Letterlike Symbols", 0x214F),
    (0x2150, "Number Forms", 0x218F),
    (0x2190, "Arrows", 0x21FF),
    (0x2200, "Mathematical Operators", 0x22FF),
    (0x2300, "Miscellaneous Technical", 0x23FF),
    (0x2400, "Control Pictures", 0x243F),
    (0x2440, "Optical Character Recognition", 0x245F),
    (0x2460, "Enclosed Alphanumerics", 0x24FF),
    (0x2500, "B0x Drawing", 0x257F),
    (0x2580, "Block Elements", 0x259F),
    (0x25A0, "Geometric Shapes", 0x25FF),
    (0x2600, "Miscellaneous Symbols", 0x26FF),
    (0x2700, "Dingbats", 0x27BF),
    (0x27C0, "Miscellaneous Mathematical Symbols-A", 0x27EF),
    (0x27F0, "Supplemental Arrows-A", 0x27FF),
    (0x2800, "Braille Patterns", 0x28FF),
    (0x2900, "Supplemental Arrows-B", 0x297F),
    (0x2980, "Miscellaneous Mathematical Symbols-B", 0x29FF),
    (0x2A00, "Supplemental Mathematical Operators", 0x2AFF),
    (0x2B00, "Miscellaneous Symbols and Arrows", 0x2BFF),
    (0x2C00, "Glagolitic", 0x2C5F),
    (0x2C60, "Latin Extended-C", 0x2C7F),
    (0x2C80, "Coptic", 0x2CFF),
    (0x2D00, "Georgian Supplement", 0x2D2F),
    (0x2D30, "Tifinagh", 0x2D7F),
    (0x2D80, "Ethiopic Extended", 0x2DDF),
    (0x2DE0, "Cyrillic Extended-A", 0x2DFF),
    (0x2E00, "Supplemental Punctuation", 0x2E7F),
    (0x2E80, "CJK Radicals Supplement", 0x2EFF),
    (0x2F00, "Kangxi Radicals", 0x2FDF),
    (0x2FF0, "Ideographic Description Characters", 0x2FFF),
    (0x3000, "CJK Symbols and Punctuation", 0x303F),
    (0x3040, "Hiragana", 0x309F),
    (0x30A0, "Katakana", 0x30FF),
    (0x3100, "Bopomofo", 0x312F),
    (0x3130, "Hangul Compatibility Jamo", 0x318F),
    (0x3190, "Kanbun", 0x319F),
    (0x31A0, "Bopomofo Extended", 0x31BF),
    (0x31C0, "CJK Strokes", 0x31EF),
    (0x31F0, "Katakana Phonetic Extensions", 0x31FF),
    (0x3200, "Enclosed CJK Letters and Months", 0x32FF),
    (0x3300, "CJK Compatibility", 0x33FF),
    (0x3400, "CJK Unified Ideographs Extension A", 0x4DBF),
    (0x4DC0, "Yijing Hexagram Symbols", 0x4DFF),
    (0x4E00, "CJK Unified Ideographs", 0x9FFF),
    (0xA000, "Yi Syllables", 0xA48F),
    (0xA490, "Yi Radicals", 0xA4CF),
    (0xA4D0, "Lisu", 0xA4FF),
    (0xA500, "Vai", 0xA63F),
    (0xA640, "Cyrillic Extended-B", 0xA69F),
    (0xA6A0, "Bamum", 0xA6FF),
    (0xA700, "Modifier Tone Letters", 0xA71F),
    (0xA720, "Latin Extended-D", 0xA7FF),
    (0xA800, "Syloti Nagri", 0xA82F),
    (0xA830, "Common Indic Number Forms", 0xA83F),
    (0xA840, "Phags-pa", 0xA87F),
    (0xA880, "Saurashtra", 0xA8DF),
    (0xA8E0, "Devanagari Extended", 0xA8FF),
    (0xA900, "Kayah Li", 0xA92F),
    (0xA930, "Rejang", 0xA95F),
    (0xA960, "Hangul Jamo Extended-A", 0xA97F),
    (0xA980, "Javanese", 0xA9DF),
    (0xA9E0, "Myanmar Extended-B", 0xA9FF),
    (0xAA00, "Cham", 0xAA5F),
    (0xAA60, "Myanmar Extended-A", 0xAA7F),
    (0xAA80, "Tai Viet", 0xAADF),
    (0xAAE0, "Meetei Mayek Extensions", 0xAAFF),
    (0xAB00, "Ethiopic Extended-A", 0xAB2F),
    (0xAB30, "Latin Extended-E", 0xAB6F),
    (0xAB70, "Cherokee Supplement", 0xABBF),
    (0xABC0, "Meetei Mayek", 0xABFF),
    (0xAC00, "Hangul Syllables", 0xD7A3),
    (0xD7B0, "Hangul Jamo Extended-B", 0xD7FF),
    (0xD800, "High Surrogates", 0xDB7F),
    (0xDB80, "High Private Use Surrogates", 0xDBFF),
    (0xDC00, "Low Surrogates", 0xDFFF),
    (0xE000, "Private Use Area", 0xF8FF),
    (0xF900, "CJK Compatibility Ideographs", 0xFAFF),
    (0xFB00, "Alphabetic Presentation Forms", 0xFB4F),
    (0xFB50, "Arabic Presentation Forms-A", 0xFDFF),
    (0xFE00, "Variation Selectors", 0xFE0F),
    (0xFE10, "Vertical Forms", 0xFE1F),
    (0xFE20, "Combining Half Marks", 0xFE2F),
    (0xFE30, "CJK Compatibility Forms", 0xFE4F),
    (0xFE50, "Small Form Variants", 0xFE6F),
    (0xFE70, "Arabic Presentation Forms-B", 0xFEFF),
    (0xFF00, "Halfwidth and Fullwidth Forms", 0xFFEF),
    (0xFFF0, "Specials", 0xFFFF),
    (0x10000, "Linear B Syllabary", 0x1007F),
    (0x10080, "Linear B Ideograms", 0x100FF),
    (0x10100, "Aegean Numbers", 0x1013F),
    (0x10140, "Ancient Greek Numbers", 0x1018F),
    (0x10190, "Ancient Symbols", 0x101CF),
    (0x101D0, "Phaistos Disc", 0x101FF),
    (0x10280, "Lycian", 0x1029F),
    (0x102A0, "Carian", 0x102DF),
    (0x102E0, "Coptic Epact Numbers", 0x102FF),
    (0x10300, "Old Italic", 0x1032F),
    (0x10330, "Gothic", 0x1034F),
    (0x10350, "Old Permic", 0x1037F),
    (0x10380, "Ugaritic", 0x1039F),
    (0x103A0, "Old Persian", 0x103DF),
    (0x10400, "Deseret", 0x1044F),
    (0x10450, "Shavian", 0x1047F),
    (0x10480, "Osmanya", 0x104AF),
    (0x104B0, "Osage", 0x104FF),
    (0x10500, "Elbasan", 0x1052F),
    (0x10530, "Caucasian Albanian", 0x1056F),
    (0x10570, "Vithkuqi", 0x105BF),
    (0x105C0, "Todhri", 0x105FF),
    (0x10600, "Linear A", 0x1077F),
    (0x10780, "Latin Extended-F", 0x107BF),
    (0x10800, "Cypriot Syllabary", 0x1083F),
    (0x10840, "Imperial Aramaic", 0x1085F),
    (0x10860, "Palmyrene", 0x1087F),
    (0x10880, "Nabataean", 0x108AF),
    (0x108E0, "Hatran", 0x108FF),
    (0x10900, "Phoenician", 0x1091F),
    (0x10920, "Lydian", 0x1093F),
    (0x10980, "Meroitic Hieroglyphs", 0x1099F),
    (0x109A0, "Meroitic Cursive", 0x109FF),
    (0x10A00, "Kharoshthi", 0x10A5F),
    (0x10A60, "Old South Arabian", 0x10A7F),
    (0x10A80, "Old North Arabian", 0x10A9F),
    (0x10AC0, "Manichaean", 0x10AFF),
    (0x10B00, "Avestan", 0x10B3F),
    (0x10B40, "Inscriptional Parthian", 0x10B5F),
    (0x10B60, "Inscriptional Pahlavi", 0x10B7F),
    (0x10B80, "Psalter Pahlavi", 0x10BAF),
    (0x10C00, "Old Turkic", 0x10C4F),
    (0x10C80, "Old Hungarian", 0x10CFF),
    (0x10D00, "Hanifi Rohingya", 0x10D3F),
    (0x10D40, "Garay", 0x10D8F),
    (0x10E60, "Rumi Numeral Symbols", 0x10E7F),
    (0x10E80, "Yezidi", 0x10EBF),
    (0x10EC0, "Arabic Extended-C", 0x10EFF),
    (0x10F00, "Old Sogdian", 0x10F2F),
    (0x10F30, "Sogdian", 0x10F6F),
    (0x10F70, "Old Uyghur", 0x10FAF),
    (0x10FB0, "Chorasmian", 0x10FDF),
    (0x10FE0, "Elymaic", 0x10FFF),
    (0x11000, "Brahmi", 0x1107F),
    (0x11080, "Kaithi", 0x110CF),
    (0x110D0, "Sora Sompeng", 0x110FF),
    (0x11100, "Chakma", 0x1114F),
    (0x11150, "Mahajani", 0x1117F),
    (0x11180, "Sharada", 0x111DF),
    (0x111E0, "Sinhala Archaic Numbers", 0x111FF),
    (0x11200, "Khojki", 0x1124F),
    (0x11280, "Multani", 0x112AF),
    (0x112B0, "Khudawadi", 0x112FF),
    (0x11300, "Grantha", 0x1137F),
    (0x11380, "Tulu-Tigalari", 0x113FF),
    (0x11400, "Newa", 0x1147F),
    (0x11480, "Tirhuta", 0x114DF),
    (0x11580, "Siddham", 0x115FF),
    (0x11600, "Modi", 0x1165F),
    (0x11660, "Mongolian Supplement", 0x1167F),
    (0x11680, "Takri", 0x116CF),
    (0x116D0, "Myanmar Extended-C", 0x116FF),
    (0x11700, "Ahom", 0x1174F),
    (0x11800, "Dogra", 0x1184F),
    (0x118A0, "Warang Citi", 0x118FF),
    (0x11900, "Dives Akuru", 0x1195F),
    (0x119A0, "Nandinagari", 0x119FF),
    (0x11A00, "Zanabazar Square", 0x11A4F),
    (0x11A50, "Soyombo", 0x11AAF),
    (0x11AB0, "Unified Canadian Aboriginal Syllabics Extended-A", 0x11ABF),
    (0x11AC0, "Pau Cin Hau", 0x11AFF),
    (0x11B00, "Devanagari Extended-A", 0x11B5F),
    (0x11BC0, "Sunuwar", 0x11BFF),
    (0x11C00, "Bhaiksuki", 0x11C6F),
    (0x11C70, "Marchen", 0x11CBF),
    (0x11D00, "Masaram Gondi", 0x11D5F),
    (0x11D60, "Gunjala Gondi", 0x11DAF),
    (0x11EE0, "Makasar", 0x11EFF),
    (0x11F00, "Kawi", 0x11F5F),
    (0x11FB0, "Lisu Supplement", 0x11FBF),
    (0x11FC0, "Tamil Supplement", 0x11FFF),
    (0x12000, "Cuneiform", 0x123FF),
    (0x12400, "Cuneiform Numbers and Punctuation", 0x1247F),
    (0x12480, "Early Dynastic Cuneiform", 0x1254F),
    (0x12F90, "Cypro-Minoan", 0x12FFF),
    (0x13000, "Egyptian Hieroglyphs", 0x1342F),
    (0x13430, "Egyptian Hieroglyph Format Controls", 0x1345F),
    (0x13460, "Egyptian Hieroglyphs Extended-A", 0x143FF),
    (0x14400, "Anatolian Hieroglyphs", 0x1467F),
    (0x16100, "Gurung Khema", 0x1613F),
    (0x16800, "Bamum Supplement", 0x16A3F),
    (0x16A40, "Mro", 0x16A6F),
    (0x16A70, "Tangsa", 0x16ACF),
    (0x16AD0, "Bassa Vah", 0x16AFF),
    (0x16B00, "Pahawh Hmong", 0x16B8F),
    (0x16D40, "Kirat Rai", 0x16D7F),
    (0x16E40, "Medefaidrin", 0x16E9F),
    (0x16F00, "Miao", 0x16F9F),
    (0x16FE0, "Ideographic Symbols and Punctuation", 0x16FFF),
    (0x17000, "Tangut", 0x187F7),
    (0x18800, "Tangut Components", 0x18AFF),
    (0x18B00, "Khitan Small Script", 0x18CFF),
    (0x18D00, "Tangut Supplement", 0x18D08),
    (0x1AFF0, "Kana Extended-B", 0x1AFFF),
    (0x1B000, "Kana Supplement", 0x1B0FF),
    (0x1B100, "Kana Extended-A", 0x1B12F),
    (0x1B130, "Small Kana Extension", 0x1B16F),
    (0x1B170, "Nushu", 0x1B2FF),
    (0x1BC00, "Duployan", 0x1BC9F),
    (0x1BCA0, "Shorthand Format Controls", 0x1BCAF),
    (0x1CC00, "Symbols for Legacy Computing Supplement", 0x1CEBF),
    (0x1CF00, "Znamenny Musical Notation", 0x1CFCF),
    (0x1D000, "Byzantine Musical Symbols", 0x1D0FF),
    (0x1D100, "Musical Symbols", 0x1D1FF),
    (0x1D200, "Ancient Greek Musical Notation", 0x1D24F),
    (0x1D2C0, "Kaktovik Numerals", 0x1D2DF),
    (0x1D2E0, "Mayan Numerals", 0x1D2FF),
    (0x1D300, "Tai Xuan Jing Symbols", 0x1D35F),
    (0x1D360, "Counting Rod Numerals", 0x1D37F),
    (0x1D400, "Mathematical Alphanumeric Symbols", 0x1D7FF),
    (0x1D800, "Sutton SignWriting", 0x1DAAF),
    (0x1DF00, "Latin Extended-G", 0x1DFFF),
    (0x1E000, "Glagolitic Supplement", 0x1E02F),
    (0x1E030, "Cyrillic Extended-D", 0x1E08F),
    (0x1E100, "Nyiakeng Puachue Hmong", 0x1E14F),
    (0x1E290, "Toto", 0x1E2BF),
    (0x1E2C0, "Wancho", 0x1E2FF),
    (0x1E4D0, "Nag Mundari", 0x1E4FF),
    (0x1E5D0, "Ol Onal", 0x1E5FF),
    (0x1E7E0, "Ethiopic Extended-B", 0x1E7FF),
    (0x1E800, "Mende Kikakui", 0x1E8DF),
    (0x1E900, "Adlam", 0x1E95F),
    (0x1EC70, "Indic Siyaq Numbers", 0x1ECBF),
    (0x1ED00, "Ottoman Siyaq Numbers", 0x1ED4F),
    (0x1EE00, "Arabic Mathematical Alphabetic Symbols", 0x1EEFF),
    (0x1F000, "Mahjong Tiles", 0x1F02F),
    (0x1F030, "Domino Tiles", 0x1F09F),
    (0x1F0A0, "Playing Cards", 0x1F0FF),
    (0x1F100, "Enclosed Alphanumeric Supplement", 0x1F1FF),
    (0x1F200, "Enclosed Ideographic Supplement", 0x1F2FF),
    (0x1F300, "Miscellaneous Symbols and Pictographs", 0x1F5FF),
    (0x1F600, "Emoticons", 0x1F64F),
    (0x1F650, "Ornamental Dingbats", 0x1F67F),
    (0x1F680, "Transport and Map Symbols", 0x1F6FF),
    (0x1F700, "Alchemical Symbols", 0x1F77F),
    (0x1F780, "Geometric Shapes Extended", 0x1F7FF),
    (0x1F800, "Supplemental Arrows-C", 0x1F8FF),
    (0x1F900, "Supplemental Symbols and Pictographs", 0x1F9FF),
    (0x1FA00, "Chess Symbols", 0x1FA6F),
    (0x1FA70, "Symbols and Pictographs Extended-A", 0x1FAFF),
    (0x1FB00, "Symbols for Legacy Computing", 0x1FBFF),
    (0x1FF80, "Unassigned", 0x1FFFF),
    (0x20000, "CJK Unified Ideographs Extension B", 0x2A6DF),
    (0x2A700, "CJK Unified Ideographs Extension C", 0x2B739),
    (0x2B740, "CJK Unified Ideographs Extension D", 0x2B81D),
    (0x2B820, "CJK Unified Ideographs Extension E", 0x2CEA1),
    (0x2CEB0, "CJK Unified Ideographs Extension F", 0x2EBE0),
    (0x2EBF0, "CJK Unified Ideographs Extension I", 0x2EE5D),
    (0x2F800, "CJK Compatibility Ideographs Supplement", 0x2FA1F),
    (0x2FF80, "Unassigned", 0x2FFFF),
    (0x30000, "CJK Unified Ideographs Extension G", 0x3134A),
    (0x31350, "CJK Unified Ideographs Extension H", 0x323AF),
    (0x3FF80, "Unassigned", 0x3FFFF),
    (0x4FF80, "Unassigned", 0x4FFFF),
    (0x5FF80, "Unassigned", 0x5FFFF),
    (0x6FF80, "Unassigned", 0x6FFFF),
    (0x7FF80, "Unassigned", 0x7FFFF),
    (0x8FF80, "Unassigned", 0x8FFFF),
    (0x9FF80, "Unassigned", 0x9FFFF),
    (0xAFF80, "Unassigned", 0xAFFFF),
    (0xBFF80, "Unassigned", 0xBFFFF),
    (0xCFF80, "Unassigned", 0xCFFFF),
    (0xDFF80, "Unassigned", 0xDFFFF),
    (0xE0000, "Tags", 0xE007F),
    (0xE0100, "Variation Selectors Supplement", 0xE01EF),
    (0xEFF80, "Unassigned", 0xEFFFF),
    (0xFFF80, "Supplementary Private Use Area-A", 0xFFFFF),
    (0x10FF80, "Supplementary Private Use Area-B", 0x10FFFF),
    # (0x0000, 0x007F, 'Basic Latin'),
    # (0x0080, 0x00FF, 'Latin-1 Supplement'),
    # (0x0100, 0x017F, 'Latin Extended-A'),
    # (0x0180, 0x024F, 'Latin Extended-B'),
    # (0x0250, 0x02AF, 'IPA Extensions'),
    # (0x02B0, 0x02FF, 'Spacing Modifier Letters'),
    # (0x0300, 0x036F, 'Combining Diacritical Marks'),
    # (0x0370, 0x03FF, 'Greek and Coptic'),
    # (0x0400, 0x04FF, 'Cyrillic'),
    # (0x0500, 0x052F, 'Cyrillic Supplement'),
    # (0x0530, 0x058F, 'Armenian'),
    # (0x0590, 0x05FF, 'Hebrew'),
    # (0x0600, 0x06FF, 'Arabic'),
    # (0x0700, 0x074F, 'Syriac'),
    # (0x0750, 0x077F, 'Arabic Supplement'),
    # (0x0780, 0x07BF, 'Thaana'),
    # (0x07C0, 0x07FF, 'NKo'),
    # (0x0800, 0x083F, 'Samaritan'),
    # (0x0840, 0x085F, 'Mandaic'),
    # (0x0860, 0x086F, 'Syriac Supplement'),
    # (0x08A0, 0x08FF, 'Arabic Extended-A'),
    # (0x0900, 0x097F, 'Devanagari'),
    # (0x0980, 0x09FF, 'Bengali'),
    # (0x0A00, 0x0A7F, 'Gurmukhi'),
    # (0x0A80, 0x0AFF, 'Gujarati'),
    # (0x0B00, 0x0B7F, 'Oriya'),
    # (0x0B80, 0x0BFF, 'Tamil'),
    # (0x0C00, 0x0C7F, 'Telugu'),
    # (0x0C80, 0x0CFF, 'Kannada'),
    # (0x0D00, 0x0D7F, 'Malayalam'),
    # (0x0D80, 0x0DFF, 'Sinhala'),
    # (0x0E00, 0x0E7F, 'Thai'),
    # (0x0E80, 0x0EFF, 'Lao'),
    # (0x0F00, 0x0FFF, 'Tibetan'),
    # (0x1000, 0x109F, 'Myanmar'),
    # (0x10A0, 0x10FF, 'Georgian'),
    # (0x1100, 0x11FF, 'Hangul Jamo'),
    # (0x1200, 0x137F, 'Ethiopic'),
    # (0x1380, 0x139F, 'Ethiopic Supplement'),
    # (0x13A0, 0x13FF, 'Cherokee'),
    # (0x1400, 0x167F, 'Unified Canadian Aboriginal Syllabics'),
    # (0x1680, 0x169F, 'Ogham'),
    # (0x16A0, 0x16FF, 'Runic'),
    # (0x1700, 0x171F, 'Tagalog'),
    # (0x1720, 0x173F, 'Hanunoo'),
    # (0x1740, 0x175F, 'Buhid'),
    # (0x1760, 0x177F, 'Tagbanwa'),
    # (0x1780, 0x17FF, 'Khmer'),
    # (0x1800, 0x18AF, 'Mongolian'),
    # (0x18B0, 0x18FF, 'Unified Canadian Aboriginal Syllabics Extended'),
    # (0x1900, 0x194F, 'Limbu'),
    # (0x1950, 0x197F, 'Tai Le'),
    # (0x1980, 0x19DF, 'New Tai Lue'),
    # (0x19E0, 0x19FF, 'Khmer Symbols'),
    # (0x1A00, 0x1A1F, 'Buginese'),
    # (0x1A20, 0x1AAF, 'Tai Tham'),
    # (0x1AB0, 0x1AFF, 'Combining Diacritical Marks Extended'),
    # (0x1B00, 0x1B7F, 'Balinese'),
    # (0x1B80, 0x1BBF, 'Sundanese'),
    # (0x1BC0, 0x1BFF, 'Batak'),
    # (0x1C00, 0x1C4F, 'Lepcha'),
    # (0x1C50, 0x1C7F, 'Ol Chiki'),
    # (0x1C80, 0x1C8F, 'Cyrillic Extended-C'),
    # (0x1C90, 0x1CBF, 'Georgian Extended'),
    # (0x1CC0, 0x1CCF, 'Sundanese Supplement'),
    # (0x1CD0, 0x1CFF, 'Vedic Extensions'),
    # (0x1D00, 0x1D7F, 'Phonetic Extensions'),
    # (0x1D80, 0x1DBF, 'Phonetic Extensions Supplement'),
    # (0x1DC0, 0x1DFF, 'Combining Diacritical Marks Supplement'),
    # (0x1E00, 0x1EFF, 'Latin Extended Additional'),
    # (0x1F00, 0x1FFF, 'Greek Extended'),
    # (0x2000, 0x206F, 'General Punctuation'),
    # (0x2070, 0x209F, 'Superscripts and Subscripts'),
    # (0x20A0, 0x20CF, 'Currency Symbols'),
    # (0x20D0, 0x20FF, 'Combining Diacritical Marks for Symbols'),
    # (0x2100, 0x214F, 'Letterlike Symbols'),
    # (0x2150, 0x218F, 'Number Forms'),
    # (0x2190, 0x21FF, 'Arrows'),
    # (0x2200, 0x22FF, 'Mathematical Operators'),
    # (0x2300, 0x23FF, 'Miscellaneous Technical'),
    # (0x2400, 0x243F, 'Control Pictures'),
    # (0x2440, 0x245F, 'Optical Character Recognition'),
    # (0x2460, 0x24FF, 'Enclosed Alphanumerics'),
    # (0x2500, 0x257F, 'B0x Drawing'),
    # (0x2580, 0x259F, 'Block Elements'),
    # (0x25A0, 0x25FF, 'Geometric Shapes'),
    # (0x2600, 0x26FF, 'Miscellaneous Symbols'),
    # (0x2700, 0x27BF, 'Dingbats'),
    # (0x27C0, 0x27EF, 'Miscellaneous Mathematical Symbols-A'),
    # (0x27F0, 0x27FF, 'Supplemental Arrows-A'),
    # (0x2800, 0x28FF, 'Braille Patterns'),
    # (0x2900, 0x297F, 'Supplemental Arrows-B'),
    # (0x2980, 0x29FF, 'Miscellaneous Mathematical Symbols-B'),
    # (0x2A00, 0x2AFF, 'Supplemental Mathematical Operators'),
    # (0x2B00, 0x2BFF, 'Miscellaneous Symbols and Arrows'),
    # (0x2C00, 0x2C5F, 'Glagolitic'),
    # (0x2C60, 0x2C7F, 'Latin Extended-C'),
    # (0x2C80, 0x2CFF, 'Coptic'),
    # (0x2D00, 0x2D2F, 'Georgian Supplement'),
    # (0x2D30, 0x2D7F, 'Tifinagh'),
    # (0x2D80, 0x2DDF, 'Ethiopic Extended'),
    # (0x2DE0, 0x2DFF, 'Cyrillic Extended-A'),
    # (0x2E00, 0x2E7F, 'Supplemental Punctuation'),
    # (0x2E80, 0x2EFF, 'CJK Radicals Supplement'),
    # (0x2F00, 0x2FDF, 'Kangxi Radicals'),
    # (0x2FF0, 0x2FFF, 'Ideographic Description Characters'),
    # (0x3000, 0x303F, 'CJK Symbols and Punctuation'),
    # (0x3040, 0x309F, 'Hiragana'),
    # (0x30A0, 0x30FF, 'Katakana'),
    # (0x3100, 0x312F, 'Bopomofo'),
    # (0x3130, 0x318F, 'Hangul Compatibility Jamo'),
    # (0x3190, 0x319F, 'Kanbun'),
    # (0x31A0, 0x31BF, 'Bopomofo Extended'),
    # (0x31C0, 0x31EF, 'CJK Strokes'),
    # (0x31F0, 0x31FF, 'Katakana Phonetic Extensions'),
    # (0x3200, 0x32FF, 'Enclosed CJK Letters and Months'),
    # (0x3300, 0x33FF, 'CJK Compatibility'),
    # (0x3400, 0x4DBF, 'CJK Unified Ideographs Extension A'),
    # (0x4DC0, 0x4DFF, 'Yijing Hexagram Symbols'),
    # (0x4E00, 0x9FFF, 'CJK Unified Ideographs'),
    # (0xA000, 0xA48F, 'Yi Syllables'),
    # (0xA490, 0xA4CF, 'Yi Radicals'),
    # (0xA4D0, 0xA4FF, 'Lisu'),
    # # More blocks continue up to Unicode 15.0
]


def get_upeem(font_path):
    # Load the font file
    font = TTFont(font_path)

    # Check if the 'head' table exists (it should exist for most fonts)
    if 'head' not in font:
        raise ValueError("No 'head' table found in font.")

    # Get the head table, which contains the UPEM value
    head_table = font['head']
    
    # The UPEM value is stored in the 'unitsPerEm' attribute of the 'head' table
    upeem = head_table.unitsPerEm

    return upeem
    
def get_unicode_ranges_with_names(font_path):
    # Load the font file
    font = TTFont(font_path)

    name_table = font["name"]
    font_name = None
    for record in name_table.names:
        if record.nameID == 4:  # Name ID 4 is the font's full name
            font_name = record.toStr()
            break

    # Get the cmap table
    cmap_table = font["cmap"]

    # Find the platform and encoding type for the cmap table
    cmap = cmap_table.getBestCmap()

    # Extract Unicode code points
    code_points = sorted(cmap.keys())

    count_codepoints = len(code_points)

    # Group code points into blocks and their ranges
    block_ranges = []

    for start, block_name, end in UNICODE_BLOCKS:
        block_covered = [
            code_point for code_point in code_points if start <= code_point <= end
        ]

        if block_covered:
            block_ranges.append(
                (
                    block_name,
                    start,
                    end,
                    len(block_covered),
                    len(block_covered) / (end - start + 1) * 100,
                )
            )

    # Calculate the number of covered code points
    covered_code_points = sum(block[3] for block in block_ranges)

    # Define the total possible Unicode code points
    total_code_points = 0x10FFFF + 1  # Unicode range is from 0 to 0x10FFFF

    # Calculate the coverage percentage

    print("Covered Unicode blocks:")

    for block_name, start, end, covered, percentage in block_ranges:
        print(
            f"  U+{start:04X}-U+{end:04X} {block_name}\tCovered: {covered} ({percentage:.2f}%)"
        )

    # print(f"Number of U blocks: {len(UNICODE_BLOCKS)}")

    print(f"Summary for {font_name} located at {font_path}")
    # Print the results
    print(f"Total Unicode code points: {total_code_points}")
    print(
        f"Covered code points: {covered_code_points} ({(covered_code_points / total_code_points) * 100:.4f}%)"
    )
    print(f"Missing: {count_codepoints-covered_code_points}")
    upeem = get_upeem(font_path)
    print(f'Font UPEEM: {upeem}')


# font_path = "resources/Hanzi-Pinyin-Font.top (1).ttf"  # Path to your font file
# font_path = "resources/fonts/Mengshen-Handwritten.ttf"  # Path to your font file
font_path = "resources/fonts/Noto-Sans-Mono-Top.ttf"

font_path = "resources/fonts/NotoSansSC-Regular.ttf"
font_path = "resources/fonts/LXGWWenKaiMono-Regular.ttf"
font_path = "resources/fonts/SourceHanSansCN-Regular.ttf"
font_path = "resources/fonts/WqyMono.ttf"
font_path = "output/Pinyin-Test-Bottom-Small.ttf"


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Check font codepouint coverage.")
    parser.add_argument(
        "file_path",
        nargs="?",  # file_path is optional
        default="resources/fonts/LXGWWenKaiMono-Regular.ttf",  # Default value if no argument is provided,
        help="The path to the file to check",
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    if os.path.isfile(args.file_path):
        # Check if the file exists
        get_unicode_ranges_with_names(args.file_path)
    else:
        print(f"The file '{args.file_path}' does not exist.")
        return


if __name__ == "__main__":
    main()
