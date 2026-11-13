import json, subprocess, sys, time
B = 'https://graph.facebook.com/v21.0'; IG = '17841460199986069'
SHA = sys.argv[1]
RAW = f'https://raw.githubusercontent.com/elizstraub3-hash/print/{SHA}/black-friday-kit/'
TAGS = '#blackfriday #shimmerjoias #joiascuritiba #aliancasdeouro #aliancadecasamento #ouro18k'

CAP_PRECO = f"""BLACK FRIDAY SHIMMER 🖤

Par de alianças tradicionais em ouro 18k + solitário de brinde.
R$ 3.199 em até 10x de R$ 319,90 sem juros
ou R$ 2.879,10 à vista (10% OFF)

⏳ Válido até 18 de dezembro
📍 Centro de Curitiba, com hora marcada
Garanta o seu pelo WhatsApp, link na bio.

{TAGS}"""

CAP_MEIO = f"""Três peças, uma história inteira pela frente. 💍

Ouro 18k · garantia vitalícia
Black Friday Shimmer até 18/12. Detalhes no post ao lado 👈

{TAGS}"""

CAP_CARROSSEL = f"""BLACK FRIDAY SHIMMER 🖤
Comprou o par de alianças, ganhou o solitário.

Par de alianças tradicionais abauladas em ouro 18k (3 mm) + solitário em ouro 18k com moissanite de 3 mm, e a cor da pedra você escolhe.
R$ 3.199 em até 10x sem juros, ou 10% OFF à vista.
Garantia vitalícia.

⏳ Válido até 18 de dezembro
📍 Centro de Curitiba, com hora marcada
Garanta o seu pelo WhatsApp, link na bio.

{TAGS}"""


def post(path, data):
    r = subprocess.run(['curl', '-sS', '-X', 'POST', f'{B}/{path}'] + sum([['--data-urlencode', f'{k}={v}'] for k, v in data.items()], []), capture_output=True, text=True)
    j = json.loads(r.stdout); print(path, j, flush=True); return j


def get(path):
    return json.loads(subprocess.run(['curl', '-sS', f'{B}/{path}'], capture_output=True, text=True).stdout)


def ready(cid):
    for _ in range(30):
        st = get(f'{cid}?fields=status_code').get('status_code')
        if st == 'FINISHED': return
        time.sleep(2)
    raise SystemExit(f'container {cid} not ready: {st}')


def publish(cid):
    ready(cid)
    mid = post(f'{IG}/media_publish', {'creation_id': cid})['id']
    print('permalink', get(f'{mid}?fields=permalink')['permalink'], flush=True)


# order matters: newest lands on the left of the grid row
publish(post(f'{IG}/media', {'image_url': RAW + '03-black-friday.jpg', 'caption': CAP_PRECO})['id'])        # right
time.sleep(5)
publish(post(f'{IG}/media', {'image_url': RAW + '00-meio-sem-texto.jpg', 'caption': CAP_MEIO})['id'])       # middle
time.sleep(5)
kids = [post(f'{IG}/media', {'image_url': RAW + f, 'is_carousel_item': 'true'})['id']
        for f in ['01-black-friday.jpg', '02-black-friday.jpg', '03-black-friday.jpg']]
for k in kids: ready(k)
publish(post(f'{IG}/media', {'media_type': 'CAROUSEL', 'children': ','.join(kids), 'caption': CAP_CARROSSEL})['id'])  # left
