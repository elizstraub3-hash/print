/* Play TV — player de IPTV (PWA).
   Não fornece conteúdo: reproduz playlists M3U, logins Xtream e links do próprio usuário. */
(() => {
  'use strict';
  const VERSION = '2.0.0';

  // ================= Utilidades =================
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
  const enc = encodeURIComponent;
  const uid = () => Math.random().toString(36).slice(2, 10);
  const arr = (x) => (Array.isArray(x) ? x : x && typeof x === 'object' ? Object.values(x) : []);
  function hash(s) { let h = 5381; for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0; return (h >>> 0).toString(36); }
  function initials(name) {
    return (String(name).replace(/[^\p{L}\p{N} ]/gu, ' ').split(' ').filter(Boolean).slice(0, 2).map((w) => w[0]).join('') || 'TV').toUpperCase();
  }
  const fmtTime = (s) => { s = Math.floor(s); const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = s % 60; return (h ? h + ':' + String(m).padStart(2, '0') : m) + ':' + String(x).padStart(2, '0'); };
  const isAdult = (s) => /(adult|xxx|\+18|18\+|adulto|porn|er[oó]tic)/i.test(s || '');
  const COLORS = ['#ffb020', '#ff5d7a', '#5ad1ff', '#7cf29c', '#c79bff', '#ff8a3d'];

  const I = {
    menu: '<path d="M4 7h16M4 12h16M4 17h16"/>',
    home: '<path d="M4 10.5 12 4l8 6.5V20a1 1 0 0 1-1 1h-4.5v-6h-5v6H5a1 1 0 0 1-1-1z"/>',
    live: '<circle cx="12" cy="12" r="1.8"/><path d="M8.6 8.6a4.8 4.8 0 0 0 0 6.8M15.4 8.6a4.8 4.8 0 0 1 0 6.8M5.8 5.8a8.8 8.8 0 0 0 0 12.4M18.2 5.8a8.8 8.8 0 0 1 0 12.4"/>',
    film: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7.5 4v16M16.5 4v16M3 9h4.5M3 15h4.5M16.5 9H21M16.5 15H21"/>',
    tv: '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 3l4 4 4-4"/>',
    list: '<path d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
    gear: '<circle cx="12" cy="12" r="3.2"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/>',
    play: '<path d="M7 4.5v15l12.5-7.5z"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    check: '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    star: '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
    back: '<path d="M15 5l-7 7 7 7"/>',
    up: '<path d="m6 15 6-6 6 6"/>',
    down: '<path d="m6 9 6 6 6-6"/>',
    next: '<path d="M5 5v14l10-7zM19 5v14"/>',
    grid: '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
    full: '<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/>',
  };
  const ico = (n, fill) => `<svg class="ico" viewBox="0 0 24 24" fill="${fill ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${I[n]}</svg>`;
  const img = (src, name, cls = '') => src
    ? `<img loading="lazy" decoding="async" class="${cls}" src="${esc(src)}" alt="" data-fb="${esc(initials(name))}">`
    : `<div class="ph">${esc(initials(name))}</div>`;
  // Troca imagens quebradas por um placeholder com as iniciais
  document.addEventListener('error', (e) => {
    const t = e.target;
    if (t.tagName === 'IMG' && t.dataset.fb !== undefined) {
      const d = document.createElement('div'); d.className = 'ph'; d.textContent = t.dataset.fb; t.replaceWith(d);
    }
  }, true);

  // ================= Armazenamento (IndexedDB) =================
  const DB = (() => {
    let dbp; const mem = {};
    const open = () => dbp || (dbp = new Promise((res) => {
      try { const r = indexedDB.open('playtv', 1); r.onupgradeneeded = () => r.result.createObjectStore('kv'); r.onsuccess = () => res(r.result); r.onerror = () => res(null); }
      catch { res(null); }
    }));
    return {
      async get(k) {
        const db = await open(); if (!db) return mem[k];
        return new Promise((res) => { const q = db.transaction('kv').objectStore('kv').get(k); q.onsuccess = () => res(q.result); q.onerror = () => res(mem[k]); });
      },
      async set(k, v) {
        mem[k] = v; const db = await open(); if (!db) return;
        return new Promise((res) => { const t = db.transaction('kv', 'readwrite'); t.objectStore('kv').put(v, k); t.oncomplete = t.onerror = () => res(); });
      },
    };
  })();

  // ================= Estado =================
  const S = {
    playlists: [],
    profiles: [],
    profileId: null,
    settings: { hideAdult: false, pin: '', deviceId: '' },
    P: { favs: [], later: [], progress: {} },   // dados do perfil ativo
    items: { live: [], movie: [], series: [] },
    cats: { live: [], movie: [], series: [] },
    byKey: new Map(),
    byCat: new Map(),
    homeTab: 'all',
    ctx: {},           // listas de contexto para tocar (ex.: canais de uma fileira)
    infoCache: new Map(),
  };
  const profile = () => S.profiles.find((p) => p.id === S.profileId) || S.profiles[0];
  const saveP = () => DB.set('p:' + S.profileId, S.P);
  const saveSettings = () => DB.set('settings', S.settings);
  const savePlaylists = () => DB.set('playlists', S.playlists);
  const saveProfiles = () => DB.set('profiles', { list: S.profiles, active: S.profileId });

  // ================= Playlists: M3U =================
  function attr(line, name) { const m = line.match(new RegExp(name + '="([^"]*)"', 'i')); return m ? m[1].trim() : ''; }
  function kindOf(url, group) {
    const u = url.toLowerCase(), g = (group || '').toLowerCase();
    if (/\/series\//.test(u) || /s[eé]rie/.test(g)) return 'series';
    if (/\/movie\//.test(u) || /\.(mp4|mkv|avi|mov)(\?|$)/.test(u) || /(filme|movie|vod|cinema)/.test(g)) return 'movie';
    return 'live';
  }
  function parseM3U(text) {
    const out = []; let cur = null;
    for (const raw of text.replace(/\r/g, '').split('\n')) {
      const line = raw.trim(); if (!line) continue;
      if (line.startsWith('#EXTINF')) {
        const c = line.lastIndexOf(',');
        cur = { name: (c >= 0 ? line.slice(c + 1).trim() : '') || attr(line, 'tvg-name') || 'Sem nome', logo: attr(line, 'tvg-logo'), group: attr(line, 'group-title') || 'Outros' };
      } else if (line.startsWith('#EXTGRP:') && cur) cur.group = line.slice(8).trim() || cur.group;
      else if (!line.startsWith('#')) { const e = cur || { name: line.split('/').pop() || 'Canal', logo: '', group: 'Outros' }; e.url = line; out.push(e); cur = null; }
    }
    return out;
  }
  function m3uToData(text) {
    const data = { live: [], movie: [], series: [], cats: { live: {}, movie: {}, series: {} } };
    const smap = new Map();
    for (const e of parseM3U(text)) {
      const kind = kindOf(e.url, e.group);
      data.cats[kind][e.group] = e.group;
      if (kind === 'series') {
        const m = e.name.match(/^(.*?)[\s._-]*S(\d{1,2})\s*E(\d{1,3})/i);
        const sname = (m ? m[1] : e.name).trim() || e.name;
        const k = e.group + '|' + sname;
        let s = smap.get(k);
        if (!s) { s = { id: hash(k), name: sname, logo: e.logo, cat: e.group, eps: [] }; smap.set(k, s); data.series.push(s); }
        s.eps.push({ id: hash(e.url), season: m ? +m[2] : 1, num: m ? +m[3] : s.eps.length + 1, title: e.name, url: e.url, logo: e.logo });
      } else {
        data[kind].push({ id: hash(e.url), name: e.name, logo: e.logo, cat: e.group, url: e.url, year: (e.name.match(/\((\d{4})\)/) || [])[1] || '' });
      }
    }
    return data;
  }

  // ================= Playlists: Xtream Codes =================
  const xbase = (pl) => `${pl.server}/player_api.php?username=${enc(pl.user)}&password=${enc(pl.pass)}`;
  async function xget(pl, action, extra = '') {
    const r = await fetch(xbase(pl) + (action ? '&action=' + action : '') + extra, { cache: 'no-store' });
    if (!r.ok) throw new Error('O servidor respondeu ' + r.status);
    return r.json();
  }
  async function xtreamToData(pl) {
    const auth = await xget(pl, '');
    if (!auth || !auth.user_info || String(auth.user_info.auth) === '0') throw new Error('Usuário ou senha inválidos.');
    if (auth.user_info.exp_date) pl.exp = +auth.user_info.exp_date * 1000;
    const [lc, ls, vc, vs, sc, ss] = await Promise.all(['get_live_categories', 'get_live_streams', 'get_vod_categories', 'get_vod_streams', 'get_series_categories', 'get_series'].map((a) => xget(pl, a).catch(() => [])));
    const cats = (a) => Object.fromEntries(arr(a).map((c) => [String(c.category_id), c.category_name]));
    const u = enc(pl.user), p = enc(pl.pass), srv = pl.server;
    const year = (s) => (String(s || '').match(/(19|20)\d{2}/) || [''])[0];
    return {
      cats: { live: cats(lc), movie: cats(vc), series: cats(sc) },
      live: arr(ls).map((s) => ({ id: String(s.stream_id), name: s.name, logo: s.stream_icon || '', cat: String(s.category_id), url: `${srv}/live/${u}/${p}/${s.stream_id}.m3u8`, num: s.num })),
      movie: arr(vs).map((s) => ({ id: String(s.stream_id), name: s.name, logo: s.stream_icon || '', cat: String(s.category_id), url: `${srv}/movie/${u}/${p}/${s.stream_id}.${s.container_extension || 'mp4'}`, rating: s.rating ? (+s.rating).toFixed(1) : '', added: +s.added || 0, year: s.year || year(s.name), xt: 1 })),
      series: arr(ss).map((s) => ({ id: String(s.series_id), name: s.name, logo: s.cover || '', cat: String(s.category_id), rating: s.rating ? (+s.rating).toFixed(1) : '', plot: s.plot || '', genre: s.genre || '', year: year(s.releaseDate || s.release_date), backdrop: arr(s.backdrop_path)[0] || '', added: +s.last_modified || 0, xt: 1 })),
    };
  }
  // Busca detalhes (sinopse, trailer, episódios) sob demanda
  async function getInfo(item) {
    if (S.infoCache.has(item.key)) return S.infoCache.get(item.key);
    let info = {};
    const pl = S.playlists.find((x) => x.id === item.src);
    if (item.kind === 'series' && !item.xt) {
      info.eps = (item.eps || []).slice();
    } else if (pl && pl.type === 'xtream') {
      const u = enc(pl.user), p = enc(pl.pass);
      try {
        if (item.kind === 'movie') {
          const r = await xget(pl, 'get_vod_info', '&vod_id=' + item.id);
          const i = r.info || {};
          info = { plot: i.plot || i.description, genre: i.genre, duration: i.duration, trailer: i.youtube_trailer, backdrop: arr(i.backdrop_path)[0], cast: i.cast, director: i.director, rating: i.rating ? (+i.rating).toFixed(1) : '', year: (i.releasedate || '').slice(0, 4) };
        } else if (item.kind === 'series') {
          const r = await xget(pl, 'get_series_info', '&series_id=' + item.id);
          const i = r.info || {};
          info = { plot: i.plot, genre: i.genre, trailer: i.youtube_trailer, backdrop: arr(i.backdrop_path)[0], cast: i.cast, director: i.director, eps: [] };
          for (const [season, eps] of Object.entries(r.episodes || {})) {
            for (const e of arr(eps)) {
              info.eps.push({ id: String(e.id), season: +season || +e.season || 1, num: +e.episode_num || 0, title: e.title || `Episódio ${e.episode_num}`, url: `${pl.server}/series/${u}/${p}/${e.id}.${e.container_extension || 'mp4'}`, logo: (e.info && e.info.movie_image) || '', plot: e.info && e.info.plot, duration: e.info && e.info.duration });
            }
          }
        }
      } catch { /* sem detalhes extras */ }
    }
    if (info.eps) info.eps.sort((a, b) => a.season - b.season || a.num - b.num);
    S.infoCache.set(item.key, info);
    return info;
  }

  function friendlyError(e, url) {
    if (location.protocol === 'https:' && /^http:/i.test(url || '')) return 'Esse servidor usa http:// e o app está em https://. O navegador bloqueia essa combinação. Use um link https:// ou a versão instalada do app.';
    if (e instanceof TypeError) return 'Não foi possível conectar. O servidor pode estar fora do ar ou bloquear acesso pelo navegador (CORS). Para listas M3U, tente a opção "Arquivo".';
    return e.message || 'Erro ao carregar.';
  }

  async function loadPlaylist(pl, file) {
    if (pl.type === 'xtream') pl.data = await xtreamToData(pl);
    else if (pl.type === 'm3u') pl.data = m3uToData(file ? await file.text() : await (async () => {
      const r = await fetch(pl.url, { cache: 'no-store' }); if (!r.ok) throw new Error('O servidor respondeu ' + r.status); return r.text();
    })());
    pl.updated = Date.now();
  }

  // ================= Índice =================
  function rebuild() {
    const hide = S.settings.hideAdult;
    S.byKey.clear(); S.byCat.clear();
    for (const k of ['live', 'movie', 'series']) { S.items[k] = []; S.cats[k] = []; }
    for (const pl of S.playlists) {
      if (!pl.data) continue;
      for (const kind of ['live', 'movie', 'series']) {
        const names = pl.data.cats[kind] || {};
        const seen = new Map();
        for (const it of pl.data[kind] || []) {
          const catName = names[it.cat] || it.cat || 'Outros';
          if (hide && (isAdult(catName) || isAdult(it.name))) continue;
          it.kind = kind; it.src = pl.id; it.key = `${kind}:${pl.id}:${it.id}`; it.catKey = pl.id + '|' + it.cat; it.catName = catName;
          if (S.byKey.has(it.key)) continue;
          S.byKey.set(it.key, it);
          S.items[kind].push(it);
          if (!S.byCat.has(it.catKey)) { S.byCat.set(it.catKey, []); seen.set(it.catKey, catName); }
          S.byCat.get(it.catKey).push(it);
        }
        // mantém a ordem das categorias como vem do provedor
        for (const [cid, cname] of Object.entries(names)) {
          const key = pl.id + '|' + cid;
          if (S.byCat.has(key)) S.cats[kind].push({ key, name: cname, kind, count: S.byCat.get(key).length });
          seen.delete(key);
        }
        for (const [key, cname] of seen) S.cats[kind].push({ key, name: cname, kind, count: S.byCat.get(key).length });
      }
    }
  }

  // ================= Componentes =================
  function regCtx(list) { const id = uid(); S.ctx[id] = list; return id; }
  const detailHref = (it) => `#/detail/${enc(it.key)}`;
  function cardPoster(it) {
    return `<a class="card poster" href="${detailHref(it)}">
      <div class="img">${img(it.logo, it.name)}${it.rating && +it.rating > 0 ? `<span class="badge">${ico('star', 1)}${esc(it.rating)}</span>` : ''}</div>
      <div class="t">${esc(it.name)}</div></a>`;
  }
  function cardChan(it, ctx, i) {
    return `<button class="card chan" data-play="${ctx}" data-i="${i}">
      <div class="img">${img(it.logo, it.name)}<span class="badge live">AO VIVO</span></div>
      <div class="t">${S.P.favs.includes(it.key) ? '★ ' : ''}${esc(it.name)}</div></button>`;
  }
  function cardContinue(entry) {
    const it = S.byKey.get(entry.key); if (!it) return '';
    const pct = Math.min(100, Math.round((entry.t / entry.d) * 100));
    const sub = entry.ep ? `T${entry.ep.season} E${entry.ep.num}` : fmtTime(entry.d - entry.t) + ' restantes';
    return `<button class="card wide" data-resume="${esc(entry.key)}">
      <div class="img">${img(entry.ep?.logo || it.backdrop || it.logo, it.name)}<div class="prog"><i style="width:${pct}%"></i></div></div>
      <div class="t">${esc(it.name)} <span style="color:var(--muted);font-weight:500">· ${esc(sub)}</span></div></button>`;
  }
  function row(title, items, type, more) {
    if (!items.length) return '';
    let cards;
    if (type === 'chan') { const ctx = regCtx(items); cards = items.slice(0, 24).map((it, i) => cardChan(it, ctx, i)).join(''); }
    else if (type === 'continue') cards = items.map(cardContinue).join('');
    else cards = items.slice(0, 24).map(cardPoster).join('');
    return `<section class="row"><div class="row-head"><h3>${esc(title)}</h3>${more ? `<a href="${more}">Ver tudo</a>` : ''}</div><div class="rail">${cards}</div></section>`;
  }
  function header(title, { home, back } = {}) {
    return `<header class="header">
      ${back ? `<button class="icon-btn" data-back aria-label="Voltar">${ico('back')}</button>` : ''}
      ${home ? '<img class="mark" src="icon.svg" alt="">' : ''}
      <h1>${esc(title)}</h1>
      <a class="icon-btn" href="#/search" aria-label="Pesquisar">${ico('search')}</a>
    </header>`;
  }
  function emptyState() {
    return `<div class="empty"><div class="big">${ico('tv')}</div><h2>Vamos começar?</h2>
      <p>Adicione sua playlist: login Xtream (servidor, usuário e senha), link M3U ou arquivo. Seus canais, filmes e séries aparecem aqui.</p>
      <a class="btn primary" href="#/playlists">${ico('plus')} Adicionar playlist</a></div>`;
  }

  // ================= Telas =================
  let heroTimer = null;

  function viewHome() {
    const t = S.homeTab;
    const chips = [['all', 'Tudo'], ['series', 'Séries'], ['movie', 'Filmes'], ['cats', 'Categorias']]
      .map(([k, l]) => `<button class="chip${t === k ? ' active' : ''}" data-home="${k}">${l}</button>`).join('');
    let body = '';
    if (!S.playlists.length) body = emptyState();
    else if (t === 'cats') body = catsSections();
    else {
      const recent = (k) => S.items[k].slice().sort((a, b) => (b.added || 0) - (a.added || 0));
      const pool = t === 'all' ? [...recent('movie').slice(0, 12), ...recent('series').slice(0, 6)] : recent(t).slice(0, 18);
      const featured = pool.filter((x) => x.logo).sort(() => Math.random() - 0.5).slice(0, 5);
      body += hero(featured);
      if (t === 'all') {
        body += row('Continuar assistindo', continueList(), 'continue');
        body += row('Canais favoritos', S.P.favs.map((k) => S.byKey.get(k)).filter((x) => x && x.kind === 'live'), 'chan', '#/live/__fav');
        for (const c of S.cats.live.slice(0, 3)) body += row(c.name, S.byCat.get(c.key), 'chan', `#/live/${enc(c.key)}`);
        body += row('Filmes adicionados recentemente', recent('movie'), 'poster', '#/movies');
        body += row('Séries em destaque', recent('series'), 'poster', '#/series');
        for (const c of S.cats.movie.slice(0, 4)) body += row(c.name, S.byCat.get(c.key), 'poster', `#/cat/${enc(c.key)}`);
        for (const c of S.cats.series.slice(0, 3)) body += row(c.name, S.byCat.get(c.key), 'poster', `#/cat/${enc(c.key)}`);
      } else {
        body += row(t === 'movie' ? 'Adicionados recentemente' : 'Atualizadas recentemente', recent(t), 'poster', t === 'movie' ? '#/movies' : '#/series');
        for (const c of S.cats[t].slice(0, 14)) body += row(c.name, S.byCat.get(c.key), 'poster', `#/cat/${enc(c.key)}`);
      }
      if (!S.items.live.length && !S.items.movie.length && !S.items.series.length) body = '<div class="empty"><p>Nenhum conteúdo encontrado nas suas playlists.</p></div>';
    }
    return header('Início', { home: 1 }) + `<div class="chips">${chips}</div>` + body;
  }

  function continueList() {
    return Object.entries(S.P.progress).map(([key, v]) => ({ key, ...v })).filter((e) => S.byKey.has(e.key)).sort((a, b) => b.ts - a.ts).slice(0, 20);
  }

  function hero(items) {
    if (!items.length) return '';
    const slides = items.map((it, i) => `
      <article class="slide${i === 0 ? ' on' : ''}" data-key="${esc(it.key)}">
        <img class="bg" src="${esc(it.backdrop || it.logo)}" alt="" data-fb="">
        <div class="shade"></div>
        <div class="info">
          <h2>${esc(it.name.replace(/\s*\(\d{4}\)\s*$/, ''))}</h2>
          <div class="meta">${metaLine(it)}</div>
          <div class="btns">
            <button class="btn primary" data-watch="${esc(it.key)}">${ico('play', 1)} Assistir agora</button>
            <a class="btn ghost" href="${detailHref(it)}">${ico('film')} Detalhes</a>
          </div>
          <p class="plot">${esc(it.plot || it.catName || '')}</p>
        </div>
      </article>`).join('');
    const dots = items.length > 1 ? `<div class="dots">${items.map((_, i) => `<button data-dot="${i}" class="${i === 0 ? 'on' : ''}" aria-label="Destaque ${i + 1}"></button>`).join('')}</div>` : '';
    return `<div class="hero" id="hero">${slides}${dots}</div>`;
  }
  function metaLine(it, info = {}) {
    const rating = info.rating || it.rating;
    const parts = [];
    if (rating && +rating > 0) parts.push(`<span class="rate">${ico('star')} ${esc(rating)}</span>`);
    if (info.year || it.year) parts.push(`<span>${esc(info.year || it.year)}</span>`);
    if (info.duration) parts.push(`<span>${esc(String(info.duration).replace(/^00:/, '').replace(/^(\d+):(\d+):\d+$/, (_, h, m) => `${+h}h ${m}min`))}</span>`);
    if (info.genre || it.genre) parts.push(`<span>${esc(info.genre || it.genre)}</span>`);
    if (it.kind === 'series' && info.eps) parts.push(`<span>${new Set(info.eps.map((e) => e.season)).size} temporada(s)</span>`);
    return parts.join('');
  }
  function startHero() {
    clearInterval(heroTimer);
    const h = $('#hero'); if (!h) return;
    const slides = $$('.slide', h), dots = $$('.dots button', h);
    let i = 0;
    const show = (n) => {
      i = (n + slides.length) % slides.length;
      slides.forEach((s, k) => s.classList.toggle('on', k === i));
      dots.forEach((d, k) => d.classList.toggle('on', k === i));
      enrichSlide(slides[i]);
    };
    h.addEventListener('click', (e) => { const d = e.target.closest('[data-dot]'); if (d) { show(+d.dataset.dot); restart(); } });
    const restart = () => { clearInterval(heroTimer); if (slides.length > 1) heroTimer = setInterval(() => show(i + 1), 8000); };
    enrichSlide(slides[0]); restart();
  }
  async function enrichSlide(el) {
    if (!el || el.dataset.done) return; el.dataset.done = 1;
    const it = S.byKey.get(el.dataset.key); if (!it || !it.xt) return;
    const info = await getInfo(it);
    if (info.plot) $('.plot', el).textContent = info.plot;
    $('.meta', el).innerHTML = metaLine(it, info);
    if (info.backdrop && window.innerWidth >= 820) $('.bg', el).src = info.backdrop;
  }

  function catsSections() {
    const sec = (title, icon, kind) => S.cats[kind].length ? `<h2 class="section-title">${ico(icon)} ${title}</h2><div class="cat-grid">${S.cats[kind].map((c) =>
      `<a class="cat-tile" href="${kind === 'live' ? `#/live/${enc(c.key)}` : `#/cat/${enc(c.key)}`}"><b>${esc(c.name)}</b><small>${c.count} ${kind === 'live' ? 'canais' : 'títulos'}</small></a>`).join('')}</div>` : '';
    return sec('TV ao vivo', 'live', 'live') + sec('Filmes', 'film', 'movie') + sec('Séries', 'tv', 'series');
  }

  // ----- Ao vivo -----
  function viewLive(catKey = '__all') {
    if (!S.playlists.length) return header('TV ao vivo') + emptyState();
    const favs = S.P.favs.map((k) => S.byKey.get(k)).filter((x) => x && x.kind === 'live');
    const opts = [['__all', 'Todos', S.items.live.length], ['__fav', '★ Favoritos', favs.length], ...S.cats.live.map((c) => [c.key, c.name, c.count])];
    const list = catKey === '__all' ? S.items.live : catKey === '__fav' ? favs : S.byCat.get(catKey) || [];
    const chips = opts.map(([k, l, n]) => `<button class="chip${k === catKey ? ' active' : ''}" data-livecat="${esc(k)}">${esc(l)}</button>`).join('');
    const side = opts.map(([k, l, n]) => `<button class="${k === catKey ? 'on' : ''}" data-livecat="${esc(k)}"><span>${esc(l)}</span><small>${n}</small></button>`).join('');
    return header('TV ao vivo') +
      `<div class="search-box">${ico('search')}<input id="liveFilter" type="search" placeholder="Filtrar canais…" autocomplete="off"></div>
       <div class="live-layout"><div class="live-cats">${side}</div><div><div class="chips">${chips}</div><div class="chan-list" id="chanList"></div><div class="more-sentinel" id="sentinel"></div></div></div>`
;
  }
  function mountLive(catKey) {
    const favs = S.P.favs.map((k) => S.byKey.get(k)).filter((x) => x && x.kind === 'live');
    const base = catKey === '__all' ? S.items.live : catKey === '__fav' ? favs : S.byCat.get(catKey) || [];
    const listEl = $('#chanList'); if (!listEl) return;
    let list = base, shown = 0, ctx = regCtx(list);
    const draw = (reset) => {
      if (reset) { listEl.innerHTML = ''; shown = 0; }
      const next = list.slice(shown, shown + 80);
      listEl.insertAdjacentHTML('beforeend', next.map((it, j) => {
        const i = shown + j;
        return `<button class="chan-item" data-play="${ctx}" data-i="${i}"><span class="num">${i + 1}</span><span class="logo">${img(it.logo, it.name)}</span><span class="nm">${esc(it.name)}</span>${S.P.favs.includes(it.key) ? '<span class="star">★</span>' : ''}</button>`;
      }).join(''));
      shown += next.length;
      if (!list.length) listEl.innerHTML = `<div class="empty"><p>${catKey === '__fav' ? 'Nenhum favorito ainda. Abra um canal e toque na estrela.' : 'Nenhum canal encontrado.'}</p></div>`;
    };
    draw(true);
    infinite(() => { if (shown < list.length) draw(); });
    let tm;
    $('#liveFilter').addEventListener('input', (e) => {
      clearTimeout(tm);
      tm = setTimeout(() => { const q = e.target.value.trim().toLowerCase(); list = q ? base.filter((c) => c.name.toLowerCase().includes(q)) : base; ctx = regCtx(list); draw(true); }, 160);
    });
  }

  let io = null;
  function infinite(fn) {
    if (io) io.disconnect();
    const s = $('#sentinel'); if (!s) return;
    io = new IntersectionObserver((en) => { if (en[0].isIntersecting) fn(); }, { rootMargin: '600px' });
    io.observe(s);
  }

  // ----- Filmes / Séries (catálogo) -----
  function viewCatalog(kind, catKey = '__all') {
    const title = kind === 'movie' ? 'Filmes' : 'Séries';
    if (!S.playlists.length) return header(title) + emptyState();
    const chips = [['__all', 'Todos'], ...S.cats[kind].map((c) => [c.key, c.name])]
      .map(([k, l]) => `<button class="chip${k === catKey ? ' active' : ''}" data-catalog="${esc(k)}">${esc(l)}</button>`).join('');
    return header(title) + `<div class="chips">${chips}</div><div class="grid" id="gridList"></div><div class="more-sentinel" id="sentinel"></div>`;
  }
  function mountGrid(list) {
    const el = $('#gridList'); if (!el) return;
    let shown = 0;
    const draw = () => { const next = list.slice(shown, shown + 60); el.insertAdjacentHTML('beforeend', next.map(cardPoster).join('')); shown += next.length; };
    draw();
    if (!list.length) el.outerHTML = '<div class="empty"><p>Nada por aqui ainda.</p></div>';
    infinite(() => { if (shown < list.length) draw(); });
  }

  function viewCat(catKey) {
    const list = S.byCat.get(catKey) || [];
    const c = [...S.cats.movie, ...S.cats.series].find((x) => x.key === catKey);
    return header(c ? c.name : 'Categoria', { back: 1 }) + '<div class="grid" id="gridList"></div><div class="more-sentinel" id="sentinel"></div>';
  }

  // ----- Pesquisa -----
  function viewSearch() {
    return header('Pesquisar', { back: 1 }) + `<div class="search-box">${ico('search')}<input id="q" type="search" placeholder="Canal, filme ou série…" autocomplete="off"></div><div id="results"></div>`;
  }
  function mountSearch() {
    const q = $('#q'), out = $('#results');
    q.focus();
    let tm;
    const run = () => {
      const s = q.value.trim().toLowerCase();
      if (s.length < 2) { out.innerHTML = '<div class="empty"><p>Digite pelo menos 2 letras.</p></div>'; return; }
      const f = (k) => S.items[k].filter((x) => x.name.toLowerCase().includes(s)).slice(0, 40);
      const html = row('Canais', f('live'), 'chan') + row('Filmes', f('movie'), 'poster') + row('Séries', f('series'), 'poster');
      out.innerHTML = html || '<div class="empty"><p>Nada encontrado.</p></div>';
    };
    q.addEventListener('input', () => { clearTimeout(tm); tm = setTimeout(run, 200); });
    run();
  }

  // ----- Assistir depois -----
  function viewLater() {
    const list = S.P.later.map((k) => S.byKey.get(k)).filter(Boolean);
    return header('Assistir depois') + (list.length ? `<div class="grid">${list.map(cardPoster).join('')}</div>`
      : `<div class="empty"><div class="big">${ico('clock')}</div><h2>Sua lista está vazia</h2><p>Abra um filme ou série e toque em "Assistir depois" para guardar aqui.</p></div>`);
  }

  // ----- Detalhe -----
  function viewDetail(key) {
    const it = S.byKey.get(key);
    if (!it) return header('Não encontrado', { back: 1 }) + '<div class="empty"><p>Este título não está mais na sua playlist.</p></div>';
    const inLater = S.P.later.includes(key);
    const prog = S.P.progress[key];
    return `<div class="detail-hero">
        <img class="bg" id="dBg" src="${esc(it.backdrop || it.logo)}" alt="" data-fb="">
        <div class="shade"></div>
        ${header('', { back: 1 })}
        <div class="detail-body">
          <div class="poster-lg">${img(it.logo, it.name)}</div>
          <div><h1>${esc(it.name)}</h1><div class="meta" id="dMeta">${metaLine(it)}</div></div>
        </div>
      </div>
      <div class="detail-actions">
        <button class="btn primary" id="dPlay">${ico('play', 1)} ${prog ? 'Continuar' : 'Assistir agora'}</button>
        <a class="btn hidden" id="dTrailer" target="_blank" rel="noopener">${ico('film')} Trailer</a>
        <button class="btn" id="dLater">${ico(inLater ? 'check' : 'plus')} ${inLater ? 'Na sua lista' : 'Assistir depois'}</button>
      </div>
      <p class="detail-plot" id="dPlot">${esc(it.plot || '')}</p>
      <div class="detail-extra" id="dExtra"></div>
      <div id="dEps">${it.kind === 'series' ? '<div class="loading"><div class="spinner"></div></div>' : ''}</div>`;
  }
  async function mountDetail(key) {
    const it = S.byKey.get(key); if (!it) return;
    $('#dLater').addEventListener('click', async () => {
      const i = S.P.later.indexOf(key);
      i >= 0 ? S.P.later.splice(i, 1) : S.P.later.unshift(key);
      await saveP();
      const on = S.P.later.includes(key);
      $('#dLater').innerHTML = `${ico(on ? 'check' : 'plus')} ${on ? 'Na sua lista' : 'Assistir depois'}`;
    });
    const info = await getInfo(it);
    if (location.hash !== `#/detail/${enc(key)}`) return; // usuário já saiu da tela
    $('#dMeta').innerHTML = metaLine(it, info);
    if (info.plot) $('#dPlot').textContent = info.plot;
    if (info.backdrop) $('#dBg').src = info.backdrop;
    const extra = [];
    if (info.cast) extra.push(`<b>Elenco:</b> ${esc(info.cast)}`);
    if (info.director) extra.push(`<b>Direção:</b> ${esc(info.director)}`);
    $('#dExtra').innerHTML = extra.join('<br>');
    if (info.trailer) { const t = $('#dTrailer'); t.href = /^https?:/.test(info.trailer) ? info.trailer : 'https://www.youtube.com/watch?v=' + enc(info.trailer); t.classList.remove('hidden'); }

    if (it.kind === 'movie') {
      $('#dPlay').addEventListener('click', () => playMovie(it));
      return;
    }
    // Séries: temporadas e episódios
    const eps = info.eps || [];
    const box = $('#dEps');
    if (!eps.length) { box.innerHTML = '<div class="empty"><p>Nenhum episódio disponível.</p></div>'; $('#dPlay').disabled = true; return; }
    const seasons = [...new Set(eps.map((e) => e.season))];
    const prog = S.P.progress[key];
    let season = prog?.ep ? prog.ep.season : seasons[0];
    const draw = () => {
      const list = eps.filter((e) => e.season === season);
      box.innerHTML = `<h2 class="section-title">Episódios</h2>
        ${seasons.length > 1 ? `<div class="chips">${seasons.map((s) => `<button class="chip${s === season ? ' active' : ''}" data-season="${s}">Temporada ${s}</button>`).join('')}</div>` : ''}
        <div class="ep-list">${list.map((e) => {
          const p = prog && prog.ep && prog.ep.url === e.url ? Math.round((prog.t / prog.d) * 100) : 0;
          return `<button class="ep" data-ep="${eps.indexOf(e)}"><div class="thumb">${img(e.logo || it.logo, 'E' + e.num)}${p ? `<div class="prog"><i style="width:${p}%"></i></div>` : ''}</div>
          <div class="tx"><b>E${e.num} · ${esc(e.title)}</b><small>${esc(e.plot || (e.duration ? e.duration : ''))}</small></div></button>`;
        }).join('')}</div>`;
    };
    draw();
    box.addEventListener('click', (e) => {
      const s = e.target.closest('[data-season]'); if (s) { season = +s.dataset.season; draw(); return; }
      const b = e.target.closest('[data-ep]'); if (b) playEpisode(it, eps, +b.dataset.ep);
    });
    $('#dPlay').addEventListener('click', () => {
      const idx = prog?.ep ? Math.max(0, eps.findIndex((e) => e.url === prog.ep.url)) : 0;
      playEpisode(it, eps, idx);
    });
  }

  // ----- Playlists -----
  let addMode = 'xtream';
  function viewPlaylists() {
    const items = S.playlists.map((pl) => `
      <div class="pl-item">
        <div class="tx"><b>${esc(pl.name)}</b>
          <small>${pl.type === 'xtream' ? 'Xtream' : pl.type === 'm3u' ? 'M3U' : 'Link'} · ${pl.data ? `${(pl.data.live || []).length} canais · ${(pl.data.movie || []).length} filmes · ${(pl.data.series || []).length} séries` : 'não carregada'}</small>
          ${pl.exp ? `<small>Vence em ${new Date(pl.exp).toLocaleDateString('pt-BR')}</small>` : ''}
        </div>
        ${pl.type !== 'single' && !pl.fileOnly ? `<button class="btn sm" data-refresh="${pl.id}">Atualizar</button>` : ''}
        <button class="btn sm" data-remove="${pl.id}">Remover</button>
      </div>`).join('');
    const modes = [['xtream', 'Login Xtream'], ['m3u', 'Link M3U'], ['file', 'Arquivo'], ['single', 'Um canal']];
    return header('Playlists', { back: 1 }) + `
      ${S.playlists.length ? `<div class="panel"><h3>Suas playlists</h3>${items}</div>` : ''}
      <form class="panel" id="addForm" autocomplete="off">
        <h3>Adicionar playlist</h3>
        <div class="seg">${modes.map(([k, l]) => `<button type="button" data-mode="${k}" class="${k === addMode ? 'on' : ''}">${l}</button>`).join('')}</div>
        <div id="addFields">${addFields()}</div>
        <p class="msg" id="addMsg"></p>
        <button class="btn primary" id="addBtn">${ico('plus')} Adicionar</button>
        <p class="note">Suas playlists ficam salvas apenas neste aparelho. O Play TV não fornece canais nem conteúdo: use somente listas que você tem direito de assistir.</p>
      </form>`;
  }
  function addFields() {
    const f = (name, label, ph = '', type = 'text') => `<label>${label}<input name="${name}" type="${type}" placeholder="${ph}"></label>`;
    if (addMode === 'xtream') return f('name', 'Nome', 'Ex.: Meu provedor') + f('server', 'Servidor (URL)', 'https://servidor.com:8080', 'url') + f('user', 'Usuário') + f('pass', 'Senha', '', 'password');
    if (addMode === 'm3u') return f('name', 'Nome', 'Ex.: Minha lista') + f('url', 'Link da playlist (.m3u)', 'https://…', 'url');
    if (addMode === 'file') return f('name', 'Nome', 'Ex.: Lista do computador') + `<label>Arquivo .m3u<input name="file" type="file" accept=".m3u,.m3u8,audio/x-mpegurl,application/x-mpegurl,text/plain"></label>`;
    return f('name', 'Nome do canal', 'Ex.: Canal da cidade') + f('url', 'Link do vídeo (.m3u8, .mp4, .ts)', 'https://…', 'url') + f('logo', 'Logo (opcional)', 'https://…/logo.png', 'url');
  }
  function mountPlaylists() {
    const form = $('#addForm');
    form.addEventListener('click', (e) => {
      const m = e.target.closest('[data-mode]'); if (!m) return;
      addMode = m.dataset.mode;
      $$('[data-mode]', form).forEach((b) => b.classList.toggle('on', b === m));
      $('#addFields').innerHTML = addFields(); $('#addMsg').textContent = '';
    });
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const v = (n) => (form.elements[n] ? form.elements[n].value.trim() : '');
      const msg = $('#addMsg'), btn = $('#addBtn');
      msg.className = 'msg'; msg.textContent = 'Carregando sua playlist…'; btn.disabled = true;
      const pl = { id: uid(), name: v('name') };
      try {
        if (addMode === 'xtream') {
          let server = v('server').replace(/\/+$/, '');
          if (!server || !v('user') || !form.elements.pass.value) throw new Error('Preencha servidor, usuário e senha.');
          if (!/^https?:\/\//i.test(server)) server = 'http://' + server;
          Object.assign(pl, { type: 'xtream', server, user: v('user'), pass: form.elements.pass.value, name: pl.name || 'Xtream' });
          try { await loadPlaylist(pl); } catch (err) { throw new Error(friendlyError(err, server)); }
        } else if (addMode === 'm3u') {
          if (!v('url')) throw new Error('Cole o link da playlist.');
          Object.assign(pl, { type: 'm3u', url: v('url'), name: pl.name || 'Playlist' });
          try { await loadPlaylist(pl); } catch (err) { throw new Error(friendlyError(err, pl.url)); }
        } else if (addMode === 'file') {
          const file = form.elements.file.files[0]; if (!file) throw new Error('Escolha um arquivo .m3u.');
          Object.assign(pl, { type: 'm3u', fileOnly: true, name: pl.name || file.name.replace(/\.[^.]+$/, '') });
          await loadPlaylist(pl, file);
        } else {
          if (!v('url')) throw new Error('Cole o link do vídeo.');
          const name = pl.name || 'Canal', url = v('url'), kind = kindOf(url, '');
          Object.assign(pl, { type: 'single', name, updated: Date.now(), data: { live: [], movie: [], series: [], cats: { live: { m: 'Meus canais' }, movie: { m: 'Meus vídeos' }, series: {} } } });
          pl.data[kind === 'series' ? 'movie' : kind].push({ id: hash(url), name, url, logo: v('logo'), cat: 'm' });
        }
        const d = pl.data, total = d.live.length + d.movie.length + d.series.length;
        if (!total) throw new Error('Nenhum conteúdo encontrado. Confira se a playlist é válida.');
        S.playlists.push(pl);
        await savePlaylists(); rebuild();
        S.infoCache.clear();
        render();
        const m2 = $('#addMsg'); m2.className = 'msg ok'; m2.textContent = `✓ "${pl.name}" adicionada: ${d.live.length} canais, ${d.movie.length} filmes, ${d.series.length} séries.`;
      } catch (err) {
        msg.textContent = err.message; btn.disabled = false;
      }
    });
    $$('[data-remove]').forEach((b) => b.addEventListener('click', async () => {
      if (!confirm('Remover esta playlist?')) return;
      S.playlists = S.playlists.filter((p) => p.id !== b.dataset.remove);
      await savePlaylists(); rebuild(); render();
    }));
    $$('[data-refresh]').forEach((b) => b.addEventListener('click', async () => {
      const pl = S.playlists.find((p) => p.id === b.dataset.refresh);
      b.textContent = 'Atualizando…'; b.disabled = true;
      try { await loadPlaylist(pl); await savePlaylists(); rebuild(); S.infoCache.clear(); }
      catch (err) { alert(friendlyError(err, pl.server || pl.url)); }
      render();
    }));
  }

  // ----- Configurações -----
  function viewSettings() {
    const p = profile();
    return header('Configurações', { back: 1 }) + `
      <div class="panel"><h3>Perfil</h3>
        <p>Você está usando o perfil <b style="color:var(--text)">${esc(p.name)}</b>. Cada perfil tem seus favoritos, sua lista "Assistir depois" e o histórico.</p>
        <div><button class="btn" data-open-profiles>Trocar ou criar perfil</button></div>
      </div>
      <div class="panel"><h3>Controle parental</h3>
        <label class="switch">Ocultar conteúdo adulto<input type="checkbox" id="setAdult" ${S.settings.hideAdult ? 'checked' : ''}></label>
        <p>Esconde categorias e títulos com termos como "adulto", "+18" e "XXX". Para desativar, é preciso o PIN.</p>
      </div>
      <div class="panel"><h3>Playlists</h3><p>${S.playlists.length} playlist(s) adicionada(s).</p><div><a class="btn" href="#/playlists">Gerenciar playlists</a></div></div>
      <div class="panel"><h3>Sobre</h3><p>Play TV ${VERSION} · ID do aparelho ${esc(S.settings.deviceId)}</p>
        <p>O Play TV é um reprodutor. Não oferece, vende nem hospeda canais ou filmes.</p>
        <div><button class="btn" id="setClear">Apagar todos os dados deste aparelho</button></div>
      </div>`;
  }
  function mountSettings() {
    $('#setAdult').addEventListener('change', async (e) => {
      if (e.target.checked) {
        const pin = prompt('Crie um PIN de 4 dígitos para o controle parental:');
        if (!pin || !/^\d{4}$/.test(pin)) { e.target.checked = false; if (pin !== null) alert('O PIN precisa ter 4 números.'); return; }
        S.settings.pin = pin; S.settings.hideAdult = true;
      } else {
        const pin = prompt('Digite o PIN para desativar:');
        if (pin !== S.settings.pin) { e.target.checked = true; if (pin !== null) alert('PIN incorreto.'); return; }
        S.settings.hideAdult = false;
      }
      await saveSettings(); rebuild();
    });
    $('#setClear').addEventListener('click', async () => {
      if (!confirm('Isso apaga playlists, perfis, favoritos e histórico deste aparelho. Continuar?')) return;
      indexedDB.deleteDatabase('playtv');
      location.hash = ''; location.reload();
    });
  }

  // ================= Roteador =================
  const NAV = [
    ['search', 'Pesquisar', 'search', '#/search'],
    ['home', 'Início', 'home', '#/home'],
    ['live', 'TV ao vivo', 'live', '#/live'],
    ['movies', 'Filmes', 'film', '#/movies'],
    ['series', 'Séries', 'tv', '#/series'],
    ['playlists', 'Playlist', 'list', '#/playlists'],
    ['later', 'Assistir depois', 'clock', '#/later'],
  ];
  function render() {
    const [name = 'home', ...args] = location.hash.replace(/^#\/?/, '').split('/').map((x) => { try { return decodeURIComponent(x); } catch { return x; } });
    const view = $('#view');
    S.ctx = {};
    clearInterval(heroTimer);
    if (io) { io.disconnect(); io = null; }
    let html, mount;
    switch (name) {
      case 'live': html = viewLive(args[0] || '__all'); mount = () => mountLive(args[0] || '__all'); break;
      case 'movies': case 'series': {
        const kind = name === 'movies' ? 'movie' : 'series', ck = args[0] || '__all';
        html = viewCatalog(kind, ck); mount = () => mountGrid(ck === '__all' ? S.items[kind] : S.byCat.get(ck) || []); break;
      }
      case 'cat': html = viewCat(args[0]); mount = () => mountGrid(S.byCat.get(args[0]) || []); break;
      case 'search': html = viewSearch(); mount = mountSearch; break;
      case 'later': html = viewLater(); break;
      case 'detail': html = viewDetail(args.join('/')); mount = () => mountDetail(args.join('/')); break;
      case 'playlists': html = viewPlaylists(); mount = mountPlaylists; break;
      case 'settings': html = viewSettings(); mount = mountSettings; break;
      default: html = viewHome(); mount = startHero;
    }
    view.innerHTML = html;
    if (mount) mount();
    // Destaque no menu e barra
    const active = name === 'cat' || name === 'detail' ? '' : name || 'home';
    $$('#drawerNav a').forEach((a) => a.classList.toggle('active', a.dataset.nav === active));
    $$('#bottomNav [data-nav]').forEach((a) => a.classList.toggle('on', a.dataset.nav === (active || 'home')));
  }
  let lastHash = '';
  window.addEventListener('hashchange', () => {
    closeDrawer();
    const sameView = lastHash.split('/')[1] === location.hash.split('/')[1] && /^#\/(live|movies|series)/.test(location.hash);
    lastHash = location.hash;
    render();
    if (!sameView) window.scrollTo(0, 0);
  });

  // Cliques globais
  document.addEventListener('click', (e) => {
    const t = e.target;
    const play = t.closest('[data-play]');
    if (play) { const list = S.ctx[play.dataset.play]; if (list) playLive(list, +play.dataset.i); return; }
    const watch = t.closest('[data-watch]');
    if (watch) { const it = S.byKey.get(watch.dataset.watch); if (it) it.kind === 'movie' ? playMovie(it) : (location.hash = detailHref(it)); return; }
    const resume = t.closest('[data-resume]');
    if (resume) { resumeEntry(resume.dataset.resume); return; }
    const home = t.closest('[data-home]');
    if (home) { S.homeTab = home.dataset.home; render(); return; }
    const lc = t.closest('[data-livecat]');
    if (lc) { history.replaceState(null, '', '#/live/' + enc(lc.dataset.livecat)); render(); return; }
    const cg = t.closest('[data-catalog]');
    if (cg) { const base = location.hash.startsWith('#/movies') ? '#/movies' : '#/series'; history.replaceState(null, '', base + '/' + enc(cg.dataset.catalog)); render(); return; }
    if (t.closest('[data-back]')) { goBack(); return; }
    if (t.closest('[data-open-profiles]')) { openProfiles(); return; }
    if (t.closest('[data-menu]')) { openDrawer(); return; }
  });
  function goBack() { if (history.length > 1 && lastHash) history.back(); else location.hash = '#/home'; }

  // ================= Menu lateral, barra e perfis =================
  function buildChrome() {
    $('#drawerNav').innerHTML = NAV.map(([k, l, i, h]) => `<a href="${h}" data-nav="${k}">${ico(i)}<span>${l}</span></a>`).join('')
      + '<div class="lbl">CONTA</div>' + `<a href="#/settings" data-nav="settings">${ico('gear')}<span>Configurações</span></a>`;
    $('#bottomNav').innerHTML = `<button data-menu aria-label="Menu">${ico('menu')}</button><span class="sep"></span>
      <a href="#/home" data-nav="home">${ico('home')}<span>Início</span></a>
      <a href="#/live" data-nav="live">${ico('live')}<span>Ao vivo</span></a>
      <a href="#/search" data-nav="search">${ico('search')}<span>Buscar</span></a>`;
    $('#deviceId').textContent = S.settings.deviceId;
    $('#appVer').textContent = 'Versão ' + VERSION;
    paintProfile();
  }
  function paintProfile() {
    const p = profile();
    const av = $('#drawerAvatar'); av.textContent = initials(p.name)[0]; av.style.background = p.color;
    $('#drawerName').textContent = p.name;
  }
  const openDrawer = () => { $('#drawer').classList.add('on'); $('#scrim').classList.add('on'); const a = $('#drawerNav a.active') || $('#drawerNav a'); a && a.focus(); };
  const closeDrawer = () => { $('#drawer').classList.remove('on'); $('#scrim').classList.remove('on'); };
  $('#scrim').addEventListener('click', closeDrawer);
  $('#drawerProfile').addEventListener('click', () => { closeDrawer(); openProfiles(); });

  const dlgP = $('#dlgProfiles');
  function openProfiles() {
    $('#profileList').innerHTML = S.profiles.map((p) => `
      <button class="profile${p.id === S.profileId ? ' on' : ''}" data-pick="${p.id}">
        <span class="avatar" style="background:${p.color}">${esc(initials(p.name)[0])}</span><span>${esc(p.name)}</span>
        ${S.profiles.length > 1 ? `<span class="del" data-del="${p.id}" title="Excluir">✕</span>` : ''}
      </button>`).join('');
    dlgP.showModal();
  }
  dlgP.addEventListener('click', async (e) => {
    if (e.target.closest('[data-close]')) { dlgP.close(); return; }
    const del = e.target.closest('[data-del]');
    if (del) {
      e.stopPropagation();
      if (!confirm('Excluir este perfil e seus dados?')) return;
      S.profiles = S.profiles.filter((p) => p.id !== del.dataset.del);
      if (S.profileId === del.dataset.del) await switchProfile(S.profiles[0].id);
      await saveProfiles(); openProfiles(); return;
    }
    const pick = e.target.closest('[data-pick]');
    if (pick) { await switchProfile(pick.dataset.pick); dlgP.close(); render(); }
  });
  $('#profileForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = e.target.pname.value.trim(); if (!name) return;
    S.profiles.push({ id: uid(), name, color: COLORS[S.profiles.length % COLORS.length] });
    e.target.reset(); await saveProfiles(); openProfiles();
  });
  async function switchProfile(id) {
    S.profileId = id;
    S.P = Object.assign({ favs: [], later: [], progress: {} }, await DB.get('p:' + id));
    await saveProfiles(); paintProfile();
  }

  // ================= Player =================
  const player = $('#player'), video = $('#video');
  let hls = null, mts = null, cur = null, idleT = null, saveT = 0;

  function stopEngines() {
    if (hls) { hls.destroy(); hls = null; }
    if (mts) { try { mts.destroy(); } catch { } mts = null; }
    video.removeAttribute('src'); video.load();
  }
  function pMsg(html) { const m = $('#pMsg'); m.innerHTML = html; m.classList.toggle('hidden', !html); }
  function toast(t) { const el = $('#pToast'); el.textContent = t; el.classList.remove('hidden'); clearTimeout(el._t); el._t = setTimeout(() => el.classList.add('hidden'), 2800); }
  function playError() {
    const url = cur?.url || '';
    const httpBlock = location.protocol === 'https:' && /^http:/i.test(url);
    pMsg(`<b>Não foi possível reproduzir.</b><span style="color:var(--muted)">${httpBlock
      ? 'Este conteúdo usa http:// e o navegador bloqueia em sites seguros. Ele funciona na versão instalada do app.'
      : 'O conteúdo pode estar fora do ar, em um formato que o navegador não abre, ou o servidor bloqueia navegadores.'}</span>
      <button class="btn sm" id="pRetry">Tentar de novo</button>`);
    $('#pRetry').onclick = () => start(cur);
  }

  function openPlayer() {
    if (player.classList.contains('hidden')) { player.classList.remove('hidden'); history.pushState({ player: 1 }, '', location.hash); }
    poke();
  }
  function closePlayer(fromPop) {
    if (player.classList.contains('hidden')) return;
    saveProgress(true);
    stopEngines();
    player.classList.add('hidden');
    if (document.fullscreenElement) document.exitFullscreen().catch(() => { });
    cur = null;
    if (!fromPop && history.state && history.state.player) history.back();
    else render();
  }
  window.addEventListener('popstate', () => { if (!player.classList.contains('hidden')) closePlayer(true); });

  function start(c) {
    cur = c;
    stopEngines(); pMsg('');
    $('#pName').textContent = c.title;
    $('#pSub').textContent = c.sub || '';
    const logo = $('#pLogo'); if (c.logo && c.kind === 'live') { logo.src = c.logo; logo.classList.remove('hidden'); } else logo.classList.add('hidden');
    paintActions();
    const url = c.url;
    const isHls = /\.m3u8(\?|$)/i.test(url) || /type=m3u8|output=m3u8|\/hls\//i.test(url);
    const isTs = /\.ts(\?|$)/i.test(url) || (c.kind === 'live' && !isHls && !/\.(mp4|mkv|webm|mov)(\?|$)/i.test(url));
    const go = () => video.play().catch(() => { });
    if (isHls && window.Hls && Hls.isSupported()) {
      hls = new Hls({ enableWorker: true, lowLatencyMode: c.kind === 'live' });
      hls.on(Hls.Events.ERROR, (_, d) => { if (d.fatal) playError(); });
      hls.loadSource(url); hls.attachMedia(video); hls.on(Hls.Events.MANIFEST_PARSED, go);
    } else if (isHls && video.canPlayType('application/vnd.apple.mpegurl')) { video.src = url; go(); }
    else if (isTs && window.mpegts && mpegts.getFeatureList().mseLivePlayback) {
      mts = mpegts.createPlayer({ type: 'mpegts', isLive: c.kind === 'live', url });
      mts.on(mpegts.Events.ERROR, playError); mts.attachMediaElement(video); mts.load(); go();
    } else { video.src = url; go(); }
    if (c.resumeAt) {
      const seek = () => { if (video.duration && c.resumeAt < video.duration - 10) { video.currentTime = c.resumeAt; toast('Continuando de ' + fmtTime(c.resumeAt)); } };
      video.addEventListener('loadedmetadata', seek, { once: true });
    }
    openPlayer();
  }
  video.addEventListener('error', () => { if (!hls && !mts && cur) playError(); });
  video.addEventListener('playing', () => pMsg(''));
  video.addEventListener('timeupdate', () => saveProgress(false));
  video.addEventListener('ended', () => { saveProgress(true); if (cur && cur.kind === 'episode' && cur.eps[cur.epIndex + 1]) nextEpisode(); });

  function paintActions() {
    const a = $('#pActions'); const c = cur;
    let h = '';
    if (c.kind === 'live') {
      const fav = S.P.favs.includes(c.item.key);
      h += `<button class="icon-btn" id="pFav" aria-label="Favoritar" style="color:${fav ? '#ffc531' : 'inherit'}">${ico('star', fav)}</button>`;
      h += `<button class="icon-btn" id="pPrev" aria-label="Canal anterior">${ico('up')}</button><button class="icon-btn" id="pNext" aria-label="Próximo canal">${ico('down')}</button>`;
    }
    if (c.kind === 'episode' && c.eps[c.epIndex + 1]) h += `<button class="btn sm ghost" id="pNextEp">${ico('next')} Próximo</button>`;
    h += `<button class="icon-btn" id="pFull" aria-label="Tela cheia">${ico('full')}</button>`;
    a.innerHTML = h;
    $('#pFav') && ($('#pFav').onclick = async () => {
      const k = c.item.key, i = S.P.favs.indexOf(k);
      i >= 0 ? S.P.favs.splice(i, 1) : S.P.favs.unshift(k);
      await saveP(); paintActions(); toast(i >= 0 ? 'Removido dos favoritos' : 'Adicionado aos favoritos');
    });
    $('#pPrev') && ($('#pPrev').onclick = () => zap(-1));
    $('#pNext') && ($('#pNext').onclick = () => zap(1));
    $('#pNextEp') && ($('#pNextEp').onclick = nextEpisode);
    $('#pFull').onclick = () => (document.fullscreenElement ? document.exitFullscreen() : player.requestFullscreen?.())?.catch?.(() => { });
  }
  $('#pBack').innerHTML = ico('back');
  $('#pBack').addEventListener('click', () => closePlayer());

  function zap(d) {
    if (!cur || cur.kind !== 'live') return;
    const n = (cur.index + d + cur.list.length) % cur.list.length;
    playLive(cur.list, n);
    toast(`${n + 1} · ${cur.title}`);
  }
  function nextEpisode() { if (cur && cur.kind === 'episode') playEpisode(cur.series, cur.eps, cur.epIndex + 1); }

  function playLive(list, i) {
    const it = list[i]; if (!it) return;
    if (it.kind !== 'live') { location.hash = detailHref(it); return; }
    start({ kind: 'live', item: it, list, index: i, url: it.url, title: it.name, sub: it.catName, logo: it.logo });
  }
  function playMovie(it) {
    const p = S.P.progress[it.key];
    start({ kind: 'movie', item: it, url: it.url, title: it.name, sub: [it.year, it.catName].filter(Boolean).join(' · '), resumeAt: p ? p.t : 0 });
  }
  function playEpisode(series, eps, i) {
    const e = eps[i]; if (!e) return;
    const p = S.P.progress[series.key];
    const resumeAt = p && p.ep && p.ep.url === e.url ? p.t : 0;
    start({ kind: 'episode', item: series, series, eps, epIndex: i, url: e.url, title: series.name, sub: `T${e.season} E${e.num} · ${e.title}`, resumeAt, ep: e });
  }
  async function resumeEntry(key) {
    const it = S.byKey.get(key); if (!it) return;
    if (it.kind === 'movie') return playMovie(it);
    const info = await getInfo(it);
    const eps = info.eps || [];
    const p = S.P.progress[key];
    const i = Math.max(0, eps.findIndex((e) => e.url === p?.ep?.url));
    playEpisode(it, eps, i);
  }
  function saveProgress(force) {
    if (!cur || cur.kind === 'live') return;
    const now = Date.now();
    if (!force && now - saveT < 5000) return;
    saveT = now;
    const t = video.currentTime, d = video.duration;
    if (!d || !isFinite(d) || t < 15) return;
    const key = cur.item.key;
    if (t / d > 0.94) {
      // terminou: em séries, aponta para o próximo episódio
      const nx = cur.kind === 'episode' && cur.eps[cur.epIndex + 1];
      if (nx) S.P.progress[key] = { t: 1, d: 100, ts: now, ep: { url: nx.url, season: nx.season, num: nx.num, title: nx.title, logo: nx.logo } };
      else delete S.P.progress[key];
    } else {
      S.P.progress[key] = { t, d, ts: now, ep: cur.ep ? { url: cur.ep.url, season: cur.ep.season, num: cur.ep.num, title: cur.ep.title, logo: cur.ep.logo } : undefined };
    }
    saveP();
  }

  // Esconde a barra do player quando parado
  function poke() {
    player.classList.remove('idle'); clearTimeout(idleT);
    idleT = setTimeout(() => { if (!video.paused) player.classList.add('idle'); }, 3500);
  }
  ['mousemove', 'touchstart', 'keydown'].forEach((ev) => player.addEventListener(ev, poke, { passive: true }));

  // ================= Controle remoto / teclado =================
  const BACK_KEYS = ['Escape', 'GoBack', 'BrowserBack'];
  function isBackKey(e) { return BACK_KEYS.includes(e.key) || e.keyCode === 10009 || e.keyCode === 461 || (e.key === 'Backspace' && !/INPUT|TEXTAREA/.test(e.target.tagName)); }

  function spatial(dir) {
    const focusables = $$('a[href], button:not([disabled]), input, [tabindex="0"]').filter((el) => {
      if (el.closest('.hidden') || el.closest('dialog:not([open])')) return false;
      if (!$('#drawer').classList.contains('on') && el.closest('#drawer')) return false;
      if ($('#drawer').classList.contains('on') && !el.closest('#drawer')) return false;
      const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0;
    });
    const curEl = document.activeElement;
    if (!curEl || curEl === document.body || !focusables.includes(curEl)) { (focusables.find((el) => el.closest('#view')) || focusables[0])?.focus(); return; }
    const a = curEl.getBoundingClientRect(), ax = a.left + a.width / 2, ay = a.top + a.height / 2;
    let best = null, bestScore = Infinity;
    for (const el of focusables) {
      if (el === curEl) continue;
      const b = el.getBoundingClientRect(), bx = b.left + b.width / 2, by = b.top + b.height / 2;
      const dx = bx - ax, dy = by - ay;
      const ok = dir === 'left' ? dx < -4 : dir === 'right' ? dx > 4 : dir === 'up' ? dy < -4 : dy > 4;
      if (!ok) continue;
      const main = dir === 'left' || dir === 'right' ? Math.abs(dx) : Math.abs(dy);
      const cross = dir === 'left' || dir === 'right' ? Math.abs(dy) : Math.abs(dx);
      const score = main + cross * 2.5;
      if (score < bestScore) { bestScore = score; best = el; }
    }
    if (best) { best.focus({ preventScroll: true }); best.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'smooth' }); }
  }
  document.addEventListener('keydown', (e) => {
    const inPlayer = !player.classList.contains('hidden');
    if (isBackKey(e)) {
      if (dlgP.open) return; // o diálogo fecha sozinho com Esc
      e.preventDefault();
      if (inPlayer) closePlayer();
      else if ($('#drawer').classList.contains('on')) closeDrawer();
      else if (!/^#\/?(home)?$/.test(location.hash || '#/home')) goBack();
      return;
    }
    if (inPlayer) {
      if (e.key === 'ArrowUp' || e.key === 'ChannelUp' || e.keyCode === 427) { if (cur?.kind === 'live') { e.preventDefault(); zap(-1); } }
      else if (e.key === 'ArrowDown' || e.key === 'ChannelDown' || e.keyCode === 428) { if (cur?.kind === 'live') { e.preventDefault(); zap(1); } }
      else if (e.key === 'ArrowRight' && cur?.kind !== 'live') { e.preventDefault(); video.currentTime += 10; toast('+10s'); }
      else if (e.key === 'ArrowLeft' && cur?.kind !== 'live') { e.preventDefault(); video.currentTime -= 10; toast('−10s'); }
      else if (e.key === 'Enter' || e.key === ' ' || e.key === 'MediaPlayPause') { if (e.target === video || e.target === document.body || e.key === 'MediaPlayPause') { e.preventDefault(); video.paused ? video.play() : video.pause(); } }
      return;
    }
    const map = { ArrowLeft: 'left', ArrowRight: 'right', ArrowUp: 'up', ArrowDown: 'down' };
    if (map[e.key] && !dlgP.open) {
      if (e.target.tagName === 'INPUT' && (e.key === 'ArrowLeft' || e.key === 'ArrowRight')) return;
      e.preventDefault(); spatial(map[e.key]);
    }
  });

  // ================= Início =================
  (async () => {
    $('#splashVer').textContent = 'v' + VERSION;
    const t0 = Date.now();
    S.settings = Object.assign(S.settings, await DB.get('settings'));
    if (!S.settings.deviceId) {
      S.settings.deviceId = Array.from(crypto.getRandomValues(new Uint8Array(6)), (b) => b.toString(16).padStart(2, '0')).join(':').toUpperCase();
      await saveSettings();
    }
    const pr = await DB.get('profiles');
    S.profiles = pr && pr.list && pr.list.length ? pr.list : [{ id: 'main', name: 'Meu perfil', color: COLORS[0] }];
    S.profileId = pr && pr.active && S.profiles.some((p) => p.id === pr.active) ? pr.active : S.profiles[0].id;
    S.P = Object.assign({ favs: [], later: [], progress: {} }, await DB.get('p:' + S.profileId));
    S.playlists = (await DB.get('playlists')) || [];
    rebuild();
    buildChrome();
    lastHash = location.hash;
    render();
    setTimeout(() => { $('#splash').classList.add('out'); setTimeout(() => $('#splash').remove(), 500); }, Math.max(0, 1100 - (Date.now() - t0)));
    if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(() => { });
  })();
})();
