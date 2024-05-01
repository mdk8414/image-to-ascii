import sys
import os
import time
import argparse
from math import ceil
from PIL import (Image, ImageFont, ImageDraw)

PIL_GRAYSCALE = 'L'
PIL_WIDTH_INDEX = 0
PIL_HEIGHT_INDEX = 1
COMMON_MONO_FONT_FILENAMES = [
    'DejaVuSansMono.ttf',  # Linux
    'Consolas Mono.ttf',   # MacOS, I think
    'Consola.ttf',         # Windows, I think
]

def convertAscii(filename, filetype, reverse=False, b_factor=80, animate=False):
    imgBasePath = 'images'
    artBasePath = 'art'
    txtBasePath = 'text'
    image = Image.open(f'{imgBasePath}/{filename}.{filetype}')
    
    w, h = image.size
    w_scale = w  / (w + h) 
    h_scale = h  / (w + h) 
    # print(w * h)
    size = 500


    image.resize((int(w_scale * size * 1.5), int(h_scale * size))).save(f'{imgBasePath}/{filename}_resized.{filetype}')

    image = Image.open(f'{imgBasePath}/{filename}_resized.{filetype}')
    
    w, h = image.size

    grid = []
    for _ in range(h):
        grid.append([" "] * w)

    # symbols = [' ', '.', ',', ':', ';', 'i', 'r', 's', '%', '$', '&', '2', '3', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', '@', '#']
    symbols = list(' .,:;irsXA253hMHGS#9B&@')
    #symbols = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
    if reverse: symbols = symbols[::-1]

    pixels = image.load()
   # animation_speed = 10    # update every 1/animation_speed seconds
    writeToFile(pixels, w, h, filename, grid, symbols, b_factor)
    # for i in range(100, 1, -1):
    #     writeToFile(pixels, w, h, filename, grid, symbols, i)
    #     time.sleep(1 / animation_speed)
    #     print(i)
    # for i in range(1, 50):
    #     writeToFile(pixels, w, h, filename, grid, symbols, i)
    #     time.sleep(1 / animation_speed)
    #     print(i)

    os.unlink(f'{imgBasePath}/{filename}_resized.{filetype}')

    if animate:
        asciiArt = textfile_to_image(f'art.txt')
        # asciiArt.show()
        asciiArt.save(f'art.png')
    else:
        asciiArt = textfile_to_image(f'{txtBasePath}/{filename}.txt')
        # asciiArt.show()
        asciiArt.save(f'{artBasePath}/{filename}.png')

def writeToFile(pixels, w, h, filename, grid, symbols, b_factor):
    txtBasePath = 'text'
    for y in range(h):
        for x in range(w):
            #print(pixels[x,y])
            try:
                brightness = sum(pixels[x,y])
                #print(brightness)
            except:
                brightness = pixels[x,y]
            if brightness == 0: continue
            i = brightness // b_factor
            index = min(i, len(symbols)-1)
            grid[y][x] = symbols[index]


    if animate: pic = open(f'{txtBasePath}/art.txt', 'w')
    else: pic = open(f'{txtBasePath}/{filename}.txt', 'w')
     
    for row in grid:
        pic.write("".join(row) + "\n")
    pic.close()

# Credit to KobeJohn on stackoverflow: https://stackoverflow.com/questions/29760402/converting-a-txt-file-to-an-image-in-python
def textfile_to_image(textfile_path):
    """Convert text file to a grayscale image.

    arguments:
    textfile_path - the content of this file will be converted to an image
    font_path - path to a font file (for example impact.ttf)
    """
    # parse the file into lines stripped of whitespace on the right side
    with open(textfile_path) as f:
        lines = tuple(line.rstrip() for line in f.readlines())

    # choose a font (you can see more detail in the linked library on github)
    font = None
    large_font = 20  # get better resolution with larger size
    for font_filename in COMMON_MONO_FONT_FILENAMES:
        try:
            font = ImageFont.truetype(font_filename, size=large_font)
            print(f'Using font "{font_filename}".')
            break
        except IOError:
            print(f'Could not load font "{font_filename}".')
    if font is None:
        font = ImageFont.load_default()
        print('Using default font.')

    # make a sufficiently sized background image based on the combination of font and lines
    font_points_to_pixels = lambda pt: round(pt * 96.0 / 72)
    margin_pixels = 20

    # height of the background image
    tallest_line = max(lines, key=lambda line: font.font.getsize(line)[PIL_HEIGHT_INDEX])
    max_line_height = font_points_to_pixels(font.font.getsize(tallest_line)[PIL_HEIGHT_INDEX])
    realistic_line_height = max_line_height * 0.8  # apparently it measures a lot of space above visible content
    image_height = int(ceil(realistic_line_height * len(lines) + 2 * margin_pixels))

    # width of the background image
    widest_line = max(lines, key=lambda s: font.font.getsize(s)[PIL_WIDTH_INDEX])
    max_line_width = font_points_to_pixels(font.font.getsize(widest_line)[PIL_WIDTH_INDEX])
    image_width = int(ceil(max_line_width + (2 * margin_pixels)))

    # draw the background
    background_color = 255  # white
    image = Image.new(PIL_GRAYSCALE, (image_width, image_height), color=background_color)
    draw = ImageDraw.Draw(image)

    # draw each line of text
    font_color = 0  # black
    horizontal_position = margin_pixels
    for i, line in enumerate(lines):
        vertical_position = int(round(margin_pixels + (i * realistic_line_height)))
        draw.text((horizontal_position, vertical_position), line, fill=font_color, font=font)

    return image


if __name__ == "__main__":
        # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Convert.py --filename --filetype reverse b_factor animate')

    # Add arguments
    parser.add_argument('--filename', type=str, help='Filename', required=False)
    parser.add_argument('--filetype', type=str, help='Filetype', required=False)
    parser.add_argument('--reverse', action="store_true", help='Reverse symbols', required=False)
    parser.add_argument('--b_factor', type=int, help='Sensitivity', required=False)
    parser.add_argument('--animate', action="store_true", help='Whether or not to animate image', required=False)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the arguments by name
    filename = args.filename
    filetype = args.filetype
    reverse = args.reverse
    b_factor = args.b_factor
    animate = args.animate


   # animate = False
    animation_speed = 50    # update every 1/animation_speed seconds
    if animate:
        for i in range(100, 1, -2):
            if len(sys.argv) < 4: convertAscii(filename, filetype, b_factor=b_factor, animate=animate)  # convertAscii(filename, filetype)
            else: convertAscii(filename, filetype, reverse, b_factor=b_factor)  # convertAscii(filename, filetype, reverse)
            time.sleep(1 / animation_speed)
            print(i)
        for i in range(1, 50, 2):
            if len(sys.argv) < 4: convertAscii(filename, filetype, b_factor=b_factor, animate=animate)  # convertAscii(filename, filetype)
            else: convertAscii(filename, filetype, reverse, b_factor=b_factor, animate=animate)  # convertAscii(filename, filetype, reverse)
            time.sleep(1 / animation_speed)
            print(i)
    else:
        if len(sys.argv) < 4: convertAscii(filename, filetype, b_factor=b_factor)  # convertAscii(filename, filetype)
        else: convertAscii(filename, filetype, reverse=reverse, b_factor=b_factor)  # convertAscii(filename, filetype, reverse)

