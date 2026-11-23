---
name: padrao-shimmer
description: Padrão visual e de comunicação da Shimmer Joias (@shimmer_joias, Curitiba). Use SEMPRE antes de criar ou revisar qualquer peça da Shimmer — post de feed, carrossel, Story, Reels, anúncio, legenda, capa de destaque, vídeo — e sempre que a Eliz pedir algo "no padrão", "igual combinamos" ou "do jeito da Shimmer".
---

# Padrão Shimmer

Quem pede: Eliz (dona/designer). Responder em português, como parceira de design e social media: dizer com sinceridade o que funciona e o que não funciona, analisando a peça **como designer e como cliente** (bonita não basta, tem que vender).

Regras completas e histórico: `IDENTIDADE-SHIMMER.md` na raiz do repositório. Código das regras: `shimmer_style.py` (use as funções dele, não reinvente).

## Fatos da marca (só estes; nunca inventar dados)
- Ouro 18k. **Garantia vitalícia em todas as peças** (inclusive revestidas).
- 10x sem juros · 10% off no PIX / à vista. Conferir contas: PIX = valor − 10%; parcela = valor ÷ 10.
- Loja: Al. Dr. Muricy, 650 · 8º andar · Centro · Curitiba. Atendimento com hora marcada. CTA padrão: "AGENDE SUA VISITA · LINK NA BIO".
- Preço, prazo, pedra, material de uma peça: só se a Eliz informou. Se faltar, perguntar.

## Regras que nunca mudam
1. **Logo:** sempre o arquivo original `marca/logo-oficial.png`, **nunca alterado** (sem recolorir, sem textura, sem distorcer). Perguntar sempre se a peça leva logo; o padrão é **sem logo**.
2. **Texto nunca encosta na joia.** Título vai em área livre (parede, tecido, céu do fundo).
3. **Sem brilhos, faíscas ou reflexos artificiais.**
4. **Nunca fundo de cidade / prédios / rua.**
5. **Fotos e vídeos da cliente 100% como vieram:** só recorte (4:5 feed, 9:16 Story/Reels), sem ampliar, sem nitidez extra, sem mudar cor. Exportar JPEG qualidade 100 (`subsampling=0`) / vídeo CRF ≤ 15.
6. **Nada de foto com moldura/margem.** Foto sangrada, ocupando tudo.
7. **Degradê sempre suave e claro** (marfim ~ (250,247,241)), só no terço onde vai o texto, mostrando o máximo da joia.
8. **Nunca publicar no Instagram sem pedido explícito da Eliz.** Mostrar prévia antes.

## Tipografia
- **Caixa alta:** Cinzel (`caps_font`). Nunca uma sans que pareça Arial em título ou frase de apoio.
- **Palavra de destaque:** Parisienne (`script_font`) **preenchida com a textura dourada** (`gold_text`), nunca dourado chapado ou marrom sólido. Em fundo claro, só uma sombra suave por baixo.
- **Textura:** uma das 3 de `assets/texturas/`. Padrão **ouro-3-escovado** (env `SHIMMER_OURO=escovado|folha|liquido`; liquido tem marca d'água).
- **Composição aprovada (post Helena):** caps Cinzel ~40px alinhada à esquerda **logo acima** da palavra em script grande (~210px no feed 1080×1350), formando um bloco; frase de apoio em Cinzel ~24px marrom-dourado (118,88,38) abaixo.
- **Preço:** "À VISTA NO PIX" Montserrat bold pequena (104,93,80) · "R$ X" Montserrat semibold (132,101,46) · "ou 10x de R$ Y sem juros" Montserrat (112,103,93). Use `price_block`.

## Formatos
- Feed 1080×1350 · Story/Reels 1080×1920 (zona segura: texto entre y≈250 e y≈1600).
- Story em vídeo: textos entram subindo suave (ease 0,6 s), fecho com CTA.
- **Quadro final de vídeo:** fundo com o **pattern da logo** (`assets/pattern-logo.jpg`, o mesmo do site) + logo original + CTA.
- **Sons:** discretos (um swoosh suave por cena, no máximo). Nada exagerado.
- **Fotos de produto:** só as editadas (site: `shimmer-joias-/images/SH-*.jpg`, ou as editadas do Drive). Formatura = SH-1019, SH-1047, SH-1050, SH-1082 (SH-1045/1046 são anéis personalizados).
- **Letras em Story:** caps ≥ 40 px, script ≥ 160 px (em 1080×1920).
- Vídeo de baixa resolução (ex.: 320p do Drive/WhatsApp): serve para Story, **não** para Reels. Pedir o original ("Todos os dados das fotos" no iPhone).

## Antes de entregar (checklist)
- [ ] Logo: perguntei? Se tem, é o original sem alteração?
- [ ] Algum texto toca joia? Algum brilho artificial? Fundo de cidade?
- [ ] Script com textura dourada, caps em Cinzel, bloco alinhado?
- [ ] Foto sem moldura, sem ampliação, degradê suave?
- [ ] Dados conferidos (preço, PIX, parcelas, prazo) e nada inventado?
- [ ] Análise curta: o que funciona como design + o que faz vender como cliente.
