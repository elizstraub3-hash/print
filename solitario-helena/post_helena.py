import json, subprocess, time, urllib.parse
B = 'https://graph.facebook.com/v21.0'; IG = '17841460199986069'
SHA = '49a27b81c21f9e5733ad65aaf149af063399493a'
RAW = f'https://raw.githubusercontent.com/elizstraub3-hash/print/{SHA}/solitario-helena/'
CAP = """O primeiro brilho do resto da vida de vocês.

Anel Solitário Helena. Do grego, "a que brilha".
Ouro 18k, 4,35 g e pedra central de 7,5 mm, feito para um pedido que ninguém esquece. Com garantia vitalícia.

R$ 4.050 à vista no PIX
ou 10x de R$ 450,00 sem juros

Atendimento com hora marcada em Curitiba
Al. Dr. Muricy, 650 · 8º andar · Centro

Chame no WhatsApp (link na bio) e peça pelo nome: HELENA 💍

#anelsolitario #aneldenoivado #pedidodecasamento #ouro18k #noivas #curitiba #joiasemcuritiba #shimmerjoias"""
def post(path, data):
    r = subprocess.run(['curl', '-sS', '-X', 'POST', f'{B}/{path}'] + sum([['--data-urlencode', f'{k}={v}'] for k, v in data.items()], []), capture_output=True, text=True)
    j = json.loads(r.stdout); print(path, j); return j
def get(path):
    return json.loads(subprocess.run(['curl', '-sS', f'{B}/{path}'], capture_output=True, text=True).stdout)
kids = []
for f in ['01-helena-produto.jpg', '02-helena-significado.jpg', '03-helena-garantia.jpg']:
    kids.append(post(f'{IG}/media', {'image_url': RAW + f, 'is_carousel_item': 'true'})['id'])
for k in kids:
    for _ in range(20):
        st = get(f'{k}?fields=status_code').get('status_code')
        if st == 'FINISHED': break
        time.sleep(2)
    print(k, st)
car = post(f'{IG}/media', {'media_type': 'CAROUSEL', 'children': ','.join(kids), 'caption': CAP})['id']
for _ in range(30):
    st = get(f'{car}?fields=status_code').get('status_code')
    if st == 'FINISHED': break
    time.sleep(2)
print('carousel', st)
pub = post(f'{IG}/media_publish', {'creation_id': car})
mid = pub.get('id')
if mid: print('permalink', get(f'{mid}?fields=permalink,timestamp'))
