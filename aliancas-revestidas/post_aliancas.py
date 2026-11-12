import json, subprocess, time, urllib.parse
B = 'https://graph.facebook.com/v21.0'; IG = '17841460199986069'
SHA = 'c5163f6be113e7da5deb4170773ed45d6a75df7d'
RAW = f'https://raw.githubusercontent.com/elizstraub3-hash/print/{SHA}/aliancas-revestidas/'
CAP = """Do pedido ao altar 💍✨

Par de alianças revestidas, com 4 mm de largura, feitas sob medida para o casal e com garantia vitalícia.

💳 R$ 2.250 à vista no PIX
ou 10x de R$ 250,00 sem juros

📍 Atendimento com hora marcada em Curitiba
Al. Dr. Muricy, 650 · 8º andar · Centro

📲 Chame no WhatsApp (link na bio) e agende sua visita para escolher o par de vocês.

Marque aqui quem vai subir ao altar com você 👇

#aliancas #aliancasdecasamento #aliancasdenoivado #noivos #noivas #casamento #curitiba #joiasemcuritiba #shimmerjoias"""
def post(path, data):
    r = subprocess.run(['curl', '-sS', '-X', 'POST', f'{B}/{path}'] + sum([['--data-urlencode', f'{k}={v}'] for k, v in data.items()], []), capture_output=True, text=True)
    j = json.loads(r.stdout); print(path, j); return j
def get(path):
    return json.loads(subprocess.run(['curl', '-sS', f'{B}/{path}'], capture_output=True, text=True).stdout)
kids = []
for f in ['01-par-de-aliancas.jpg', '02-conjunto.jpg', '03-detalhes.jpg']:
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
