from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
import sys
import os

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the path to the modules directory to the system path
modules_dir = os.path.join(current_dir, "../src")
sys.path.append(modules_dir)

# Text to be written on the images
text = (
    "我爱学习汉语\n"  # Simplified Chinese
    "我愛學習漢語\n"  # Traditional Chinese
    # "I love to learn Chinese\n"  # English
    # "Tôi thích học tiếng Trung\n"  # Vietnamese
    # "Me encanta aprender chino\n"  # Spanish
    # "J'adore apprendre le chinois"  # French
)

# Output image size and background color
image_size = (800, 600)
background_color = (255, 255, 255)  # white background
text_color = (0, 0, 0)  # black text

# Path to Segoe UI font (from the output folder)
segoeui_font_path = "resources/fonts/segoeui.ttf"  # Segoe UI font in the output folder


# Function to get the font name from the font file
def get_font_name(font_path):
    font = TTFont(font_path)
    name = ""
    for record in font["name"].names:
        if record.nameID == 4 and record.platformID == 3 and record.platEncID == 1:
            name = record.string.decode("utf-16-be")
            break
        elif record.nameID == 4 and record.platformID == 1 and record.platEncID == 0:
            name = record.string.decode("latin-1")
            break
    return name


# Function to create an image with text
def create_image_with_text(
    font_path, text, image_size, background_color, text_color, segoeui_font_path
):
    font_name = get_font_name(font_path)
    full_text = f"{font_name}\n\n{text}"

    image = Image.new("RGB", image_size, background_color)
    draw = ImageDraw.Draw(image)

    # Use Segoe UI font to display the font name
    try:
        segoeui_font = ImageFont.truetype(
            segoeui_font_path, size=30
        )  # Use Segoe UI for the font name
    except IOError:
        segoeui_font = (
            ImageFont.load_default()
        )  # Fallback to default if Segoe UI is not found

    # First, write the font name using Segoe UI
    font_name_bbox = draw.textbbox(
        (0, 0), font_name, font=segoeui_font
    )  # Use textbbox instead of textsize
    font_name_width, font_name_height = (
        font_name_bbox[2] - font_name_bbox[0],
        font_name_bbox[3] - font_name_bbox[1],
    )
    font_name_position = (
        (image_size[0] - font_name_width) // 2,
        10,
    )  # Position the font name at the top center
    draw.text(font_name_position, font_name, fill=text_color, font=segoeui_font)

    # Use the font from the TTF file for the remaining text
    font_size = 80
    font = ImageFont.truetype(font_path, size=font_size)

    # Check if the text fits in the image, and scale down if necessary
    while True:
        # Get the size of the text
        text_bbox = draw.textbbox(
            (0, 0), full_text, font=font
        )  # Use textbbox instead of textsize
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Check if the text fits within the image dimensions
        if text_width <= image_size[0] and text_height <= image_size[1]:
            break

        # Reduce the font size if the text doesn't fit
        font_size -= 2
        font = ImageFont.truetype(font_path, size=font_size)

    # Position the remaining text below the font name
    text_position = ((image_size[0] - text_width) // 2, font_name_height + 20)
    draw.text(text_position, full_text, fill=text_color, font=font)

    return image


# Ensure the output directory exists
output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)


# Function to generate images from all .ttf fonts in the output directory except segoeui.ttf
def generate_images_from_ttf():
    # Get all .ttf files in the output directory, excluding segoeui.ttf
    ttf_files = [
        f for f in os.listdir(output_dir) if f.endswith(".ttf") and f != "segoeui.ttf"
    ]

    if not ttf_files:
        print(
            "No TTF font files found in the output directory (excluding segoeui.ttf)."
        )
        return

    for ttf_file in ttf_files:
        font_path = os.path.join(output_dir, ttf_file)
        image = create_image_with_text(
            font_path, text, image_size, background_color, text_color, segoeui_font_path
        )
        image.save(os.path.join(output_dir, f'{ttf_file.replace(".ttf", "")}.png'))

    print(
        f"Images have been created and saved successfully for {len(ttf_files)} font(s)."
    )


# Call the function to generate images from all TTF files in the output folder, excluding segoeui.ttf
generate_images_from_ttf()
