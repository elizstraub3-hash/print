"""Small helpers shared by the Story/Reels scripts (emoji rendering)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shimmer_style import *
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
EMO = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)


def emoji(ch, size):
    im = Image.new('RGBA', (140, 140), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=EMO, embedded_color=True)
    im = im.crop(im.getbbox())
    return im.resize((int(im.width * size / im.height), size), Image.LANCZOS)
