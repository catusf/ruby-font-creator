import argparse
from fontTools.ttLib import TTFont
from fontTools.merge import Merger

def merge_fonts(output, input1, input2):
    # Merge the fonts using file paths (not TTFont objects)
    merger = Merger()
    new_font = merger.merge([input1, input2])

    # Save the merged font to the specified output path
    new_font.save(output)

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Merge two font files into one.")
    
    # Add arguments for input and output files
    parser.add_argument('input1', metavar='input1', type=str, 
                        help="Path to the first font file (input1).")
    parser.add_argument('input2', metavar='input2', type=str, 
                        help="Path to the second font file (input2).")
    parser.add_argument('output', metavar='output', type=str, 
                        help="Path to save the merged font file (output).")

    # Parse the arguments
    args = parser.parse_args()

    # Call the merge_fonts function with the parsed arguments
    merge_fonts(args.output, args.input1, args.input2)

if __name__ == "__main__":
    main()
