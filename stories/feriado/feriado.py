"""Story: aviso de feriado (sexta 20/11) sobre o fundo do solitário editado no ChatGPT.
Canvas kept at the photo's native 941x1672 (9:16) so the photo is never upscaled."""
import sys
from PIL import Image, ImageDraw
sys.path.insert(0, '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad')
from shimmer_style import *
from story_nativo_lib import emoji

D = '/home/user/print/stories/feriado/'
INK = (58, 45, 34); BR = (132, 101, 46); SOFT = (100, 92, 84)


def make(bg_name, out):
    im = Image.open(D + bg_name).convert('RGBA'); W, H = im.size
    k = W / 1080                                   # sizes designed for 1080 wide
    def C(lay, y): paste(im, lay, W / 2, y, anchor='center'); return y + ink_size(lay)[1]
    y = C(solid_text('AVISO', caps_font(int(30 * k), 600), BR, int(12 * k)), 270)
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).line([(W / 2 - 50 * k, y + 22 * k), (W / 2 + 50 * k, y + 22 * k)], fill=255, width=3); im.alpha_composite(gold_fill(m))
    y = C(gold_text('Amanhã é feriado', script_font(int(122 * k))), y + 44 * k)
    y = C(solid_text('NESTA SEXTA (20/11) NÃO TEREMOS ATENDIMENTO', caps_font(int(27 * k), 600), INK, int(3 * k)), y + 26 * k)
    y = C(solid_text('Retornamos na segunda-feira ✦'.replace(' ✦', ''), sans(int(40 * k), 600), INK), y + 34 * k)
    t = solid_text('Mas qualquer dúvida, respondemos no direct', sans(int(34 * k), 500), SOFT)
    tw = ink_size(t)[0]; e = emoji('💬', int(40 * k))
    paste(im, t, W / 2 - (e.width + 10) / 2, y + 22 * k, anchor='center')
    im.alpha_composite(e, (int(W / 2 + tw / 2 - (e.width + 10) / 2 + 10), int(y + 20 * k)))
    im.convert('RGB').save(D + out, quality=95, subsampling=0)


make('fundo-solitario.png', 'story-feriado-solitario.jpg')
make('fundo-tres-aneis.png', 'story-feriado-tres-aneis.jpg')
print('ok')
