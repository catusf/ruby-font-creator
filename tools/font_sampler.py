from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
import os

import sys

import os

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the path to the modules directory to the system path
modules_dir = os.path.join(current_dir, '../src')
sys.path.append(modules_dir)

# Import font configurations from the config file
from config import font_configs

# Text to be written on the images
text = (
    "我爱学习汉语\n"  # Simplified Chinese
    "我愛學習漢語\n"  # Traditional Chinese
    "I love to learn Chinese\n"  # English
    "Tôi thích học tiếng Trung\n"  # Vietnamese
    "Me encanta aprender chino\n"  # Spanish
    "J'adore apprendre le chinois"  # French
)

# Output image size and background color
image_size = (1000, 800)
background_color = (255, 255, 255)  # white background
text_color = (0, 0, 0)  # black text

# Function to get the font name from the font file
def get_font_name(font_path):
    font = TTFont(font_path)
    name = ""
    for record in font['name'].names:
        if record.nameID == 4 and record.platformID == 3 and record.platEncID == 1:
            name = record.string.decode('utf-16-be')
            break
        elif record.nameID == 4 and record.platformID == 1 and record.platEncID == 0:
            name = record.string.decode('latin-1')
            break
    return name

# Function to create an image with text
def create_image_with_text(font_path, text, image_size, background_color, text_color):
    font_name = get_font_name(font_path)
    full_text = f"{font_name}\n\n{text}"
    
    image = Image.new('RGB', image_size, background_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, size=40)
    
    # Get the size of the text
    text_bbox = draw.textbbox((0, 0), full_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Centering the text
    position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)
    draw.text(position, full_text, fill=text_color, font=font)
    
    return image

# Ensure the output directory exists
output_dir = './outputs'
os.makedirs(output_dir, exist_ok=True)

# Main function to generate images
def generate_images_from_configs():
    for label, config in font_configs.items():
        font_path = os.path.join(output_dir, config['output_font'])
        image = create_image_with_text(font_path, text, image_size, background_color, text_color)
        image.save(os.path.join(output_dir, f'Sample_{config["font_name"].replace(" ", "-")}.png'))
    print("Images have been created and saved successfully.")

# Call the main function
generate_images_from_configs()
