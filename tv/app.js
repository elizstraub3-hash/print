/* Play TV — player de IPTV (PWA). Não fornece conteúdo: toca listas/links do próprio usuário. */
(() => {
  'use strict';

  // ---------- Armazenamento (IndexedDB, com fallback em memória) ----------
  const DB = (() => {
    let dbp = null;
    const mem = {};
    function open() {
      if (dbp) return dbp;
      dbp = new Promise((res) => {
        try {
          const r = indexedDB.open('playtv', 1);
          r.onupgradeneeded = () => r.result.createObjectStore('kv');
          r.onsuccess = () => res(r.result);
          r.onerror = () => res(null);
        } catch { res(null); }
      });
      return dbp;
    }
    async function get(k) {
      const db = await open();
      if (!db) return mem[k];
      return new Promise((res) => {
        const q = db.transaction('kv').objectStore('kv').get(k);
        q.onsuccess = () => res(q.result);
        q.onerror = () => res(mem[k]);
      });
    }
    async function set(k, v) {
      mem[k] = v;
      const db = await open();
      if (!db) return;
      return new Promise((res) => {
        const t = db.transaction('kv', 'readwrite');
        t.objectStore('kv').put(v, k);
        t.oncomplete = t.onerror = () => res();
      });
    }
    return { get, set };
  })();

  // ---------- Estado ----------
  const state = {
    lists: [],          // {id, name, source:{type,url}, channels:[...], updated}
    favs: new Set(),    // url
    tab: 'live',
    group: '__all',
    query: '',
    page: 1,
    view: [],           // canais filtrados atualmente
    current: -1,
  };
  const PAGE = 120;

  // ---------- Parser M3U ----------
  function attr(line, name) {
    const m = line.match(new RegExp(name + '="([^"]*)"', 'i'));
    return m ? m[1].trim() : '';
  }
  function kindOf(url, group) {
    const u = url.toLowerCase();
    const g = (group || '').toLowerCase();
    if (/\/series\//.test(u) || /s[eé]rie/.test(g)) return 'series';
    if (/\/movie\//.test(u) || /\.(mp4|mkv|avi|mov)(\?|$)/.test(u) || /(filme|movie|vod|cinema)/.test(g)) return 'movie';
    return 'live';
  }
  function parseM3U(text) {
    const lines = text.replace(/\r/g, '').split('\n');
    const out = [];
    let cur = null;
    for (let raw of lines) {
      const line = raw.trim();
      if (!line) continue;
      if (line.startsWith('#EXTINF')) {
        const comma = line.lastIndexOf(',');
        const title = comma >= 0 ? line.slice(comma + 1).trim() : '';
        cur = {
          name: title || attr(line, 'tvg-name') || 'Sem nome',
          logo: attr(line, 'tvg-logo'),
          group: attr(line, 'group-title') || 'Outros',
        };
      } else if (line.startsWith('#EXTGRP:') && cur) {
        cur.group = line.slice(8).trim() || cur.group;
      } else if (!line.startsWith('#')) {
        const c = cur || { name: line.split('/').pop() || 'Canal', logo: '', group: 'Outros' };
        c.url = line;
        c.kind = kindOf(line, c.group);
        out.push(c);
        cur = null;
      }
    }
    return out;
  }

  // ---------- Carregamento de listas ----------
  async function fetchText(url) {
    const r = await fetch(url, { cache: 'no-store' });
    if (!r.ok) throw new Error('O servidor respondeu ' + r.status);
    return r.text();
  }
  function friendlyFetchError(e, url) {
    if (location.protocol === 'https:' && /^http:/i.test(url)) {
      return 'Esse link usa http:// e o app está em https://. O navegador bloqueia por segurança. Peça ao provedor um link https://.';
    }
    if (e instanceof TypeError) {
      return 'Não foi possível baixar a lista. O servidor provavelmente bloqueia acesso pelo navegador (CORS). Tente baixar o arquivo e usar a opção "Arquivo".';
    }
    return e.message || 'Erro ao carregar a lista.';
  }
  const uid = () => Math.random().toString(36).slice(2, 10);

  async function save() {
    await DB.set('lists', state.lists);
    await DB.set('favs', [...state.favs]);
  }

  // ---------- Elementos ----------
  const $ = (s) => document.querySelector(s);
  const grid = $('#grid'), groupsEl = $('#groups'), empty = $('#empty'), more = $('#more');
  const player = $('#player'), video = $('#video'), msg = $('#playerMsg');
  const dlg = $('#dlgLists');

  function allChannels() {
    const seen = new Set();
    const out = [];
    for (const l of state.lists) for (const c of l.channels) {
      if (seen.has(c.url)) continue;
      seen.add(c.url);
      out.push(c);
    }
    return out;
  }

  // ---------- Render ----------
  function esc(s) {
    return String(s).replace(/[&<>"']/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
  }
  function initials(name) {
    return esc(name.replace(/[^\p{L}\p{N} ]/gu, '').split(' ').filter(Boolean).slice(0, 2).map((w) => w[0]).join('').toUpperCase() || 'TV');
  }

  function render() {
    const all = allChannels();
    empty.classList.toggle('hidden', state.lists.length > 0);

    let base = state.tab === 'fav' ? all.filter((c) => state.favs.has(c.url)) : all.filter((c) => c.kind === state.tab);

    // Categorias
    const counts = new Map();
    for (const c of base) counts.set(c.group, (counts.get(c.group) || 0) + 1);
    if (state.group !== '__all' && !counts.has(state.group)) state.group = '__all';
    const groups = [['__all', 'Todos', base.length], ...[...counts].sort((a, b) => a[0].localeCompare(b[0], 'pt')).map(([g, n]) => [g, g, n])];
    groupsEl.innerHTML = groups.map(([id, label, n]) =>
      `<button class="group${id === state.group ? ' active' : ''}" data-group="${esc(id)}"><span>${esc(label)}</span><span>${n}</span></button>`
    ).join('');

    let list = state.group === '__all' ? base : base.filter((c) => c.group === state.group);
    const q = state.query.trim().toLowerCase();
    if (q) list = list.filter((c) => c.name.toLowerCase().includes(q));
    state.view = list;

    const shown = list.slice(0, state.page * PAGE);
    grid.classList.toggle('posters', state.tab === 'movie' || state.tab === 'series');
    grid.innerHTML = shown.map((c, i) => `
      <button class="card" data-i="${i}">
        <div class="thumb">${c.logo
          ? `<img loading="lazy" src="${esc(c.logo)}" alt="" onerror="this.replaceWith(Object.assign(document.createElement('span'),{className:'ph',textContent:'${initials(c.name)}'}))">`
          : `<span class="ph">${initials(c.name)}</span>`}</div>
        <div class="name">${state.favs.has(c.url) ? '<span class="fav">★</span> ' : ''}${esc(c.name)}</div>
      </button>`).join('');

    if (state.lists.length && !list.length) {
      grid.innerHTML = `<p style="color:var(--muted)">${state.tab === 'fav' ? 'Você ainda não tem favoritos. Abra um canal e toque em ☆.' : 'Nada encontrado aqui.'}</p>`;
    }
    more.classList.toggle('hidden', shown.length >= list.length);
  }

  // ---------- Player ----------
  let hls = null, ts = null;
  function stopEngines() {
    if (hls) { hls.destroy(); hls = null; }
    if (ts) { try { ts.destroy(); } catch {} ts = null; }
    video.removeAttribute('src');
    video.load();
  }
  function showMsg(t) { msg.innerHTML = t; msg.classList.remove('hidden'); }
  function hideMsg() { msg.classList.add('hidden'); }

  function playError(url) {
    if (location.protocol === 'https:' && /^http:/i.test(url)) {
      showMsg('<b>Não deu para abrir este canal.</b><br>O link usa <code>http://</code> e o navegador bloqueia em sites seguros. Use um link <code>https://</code> ou o app instalado no aparelho.');
    } else {
      showMsg('<b>Não deu para abrir este canal.</b><br>O link pode estar fora do ar, exigir outro app ou bloquear navegadores (CORS).');
    }
  }

  function play(i) {
    const c = state.view[i];
    if (!c) return;
    state.current = i;
    stopEngines();
    hideMsg();
    player.classList.remove('hidden');
    $('#nowTitle').textContent = c.name;
    const logo = $('#nowLogo');
    if (c.logo) { logo.src = c.logo; logo.classList.remove('hidden'); } else logo.classList.add('hidden');
    $('#btnFav').textContent = state.favs.has(c.url) ? '★' : '☆';
    pushRecent(c);

    const url = c.url;
    const isHls = /\.m3u8(\?|$)/i.test(url) || /type=m3u8|output=m3u8|\/hls\//i.test(url);
    const isTs = /\.ts(\?|$)/i.test(url) || (c.kind === 'live' && !isHls && !/\.(mp4|mkv|webm|mov)(\?|$)/i.test(url));

    const tryPlay = () => video.play().catch(() => {});
    if (isHls && window.Hls && Hls.isSupported()) {
      hls = new Hls({ enableWorker: true, lowLatencyMode: true });
      hls.on(Hls.Events.ERROR, (_, d) => { if (d.fatal) playError(url); });
      hls.loadSource(url);
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, tryPlay);
    } else if (isHls && video.canPlayType('application/vnd.apple.mpegurl')) {
      video.src = url; tryPlay(); // Safari / iOS / algumas TVs
    } else if (isTs && window.mpegts && mpegts.getFeatureList().mseLivePlayback) {
      ts = mpegts.createPlayer({ type: 'mpegts', isLive: c.kind === 'live', url });
      ts.on(mpegts.Events.ERROR, () => playError(url));
      ts.attachMediaElement(video);
      ts.load();
      tryPlay();
    } else {
      video.src = url; tryPlay();
    }
  }
  video.addEventListener('error', () => { if (!hls && !ts && state.current >= 0) playError(state.view[state.current]?.url || ''); });
  video.addEventListener('playing', hideMsg);

  function closePlayer() {
    stopEngines();
    player.classList.add('hidden');
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    const card = grid.querySelector(`[data-i="${state.current}"]`);
    if (card) card.focus();
    render();
  }

  async function pushRecent(c) {
    const r = (await DB.get('recent')) || [];
    const next = [c.url, ...r.filter((u) => u !== c.url)].slice(0, 30);
    DB.set('recent', next);
  }

  // ---------- Listas: UI ----------
  function renderLists() {
    const ul = $('#listItems');
    if (!state.lists.length) { ul.innerHTML = '<li><span class="info"><small>Nenhuma lista ainda.</small></span></li>'; return; }
    ul.innerHTML = state.lists.map((l) => `
      <li>
        <span class="info"><b>${esc(l.name)}</b><br><small>${l.channels.length} itens · atualizada ${new Date(l.updated).toLocaleDateString('pt-BR')}</small></span>
        ${l.source.url ? `<button type="button" class="btn" data-refresh="${l.id}">Atualizar</button>` : ''}
        <button type="button" class="btn" data-remove="${l.id}">Remover</button>
      </li>`).join('');
  }

  let mode = 'url';
  document.querySelectorAll('.seg-btn').forEach((b) => b.addEventListener('click', () => {
    mode = b.dataset.mode;
    document.querySelectorAll('.seg-btn').forEach((x) => x.classList.toggle('active', x === b));
    document.querySelectorAll('.mode').forEach((m) => m.classList.toggle('hidden', m.dataset.mode !== mode));
    $('#addMsg').textContent = '';
  }));

  const f = (n) => dlg.querySelector(`[name="${n}"]`);
  async function addList() {
    const out = $('#addMsg');
    const btn = $('#btnAdd');
    out.textContent = 'Carregando…';
    btn.disabled = true;
    try {
      let list;
      if (mode === 'url') {
        const url = f('urlValue').value.trim();
        if (!url) throw new Error('Cole o link da lista.');
        let text;
        try { text = await fetchText(url); } catch (e) { throw new Error(friendlyFetchError(e, url)); }
        list = { name: f('urlName').value.trim() || 'Lista', source: { type: 'url', url }, channels: parseM3U(text) };
      } else if (mode === 'file') {
        const file = f('fileValue').files[0];
        if (!file) throw new Error('Escolha um arquivo .m3u.');
        list = { name: f('fileName').value.trim() || file.name.replace(/\.[^.]+$/, ''), source: { type: 'file' }, channels: parseM3U(await file.text()) };
      } else if (mode === 'xtream') {
        let server = f('xServer').value.trim().replace(/\/+$/, '');
        const user = f('xUser').value.trim(), pass = f('xPass').value;
        if (!server || !user || !pass) throw new Error('Preencha servidor, usuário e senha.');
        if (!/^https?:\/\//i.test(server)) server = 'http://' + server;
        const url = `${server}/get.php?username=${encodeURIComponent(user)}&password=${encodeURIComponent(pass)}&type=m3u_plus&output=m3u8`;
        let text;
        try { text = await fetchText(url); } catch (e) { throw new Error(friendlyFetchError(e, url)); }
        list = { name: f('xName').value.trim() || 'Xtream', source: { type: 'xtream', url }, channels: parseM3U(text) };
      } else {
        const url = f('sUrl').value.trim();
        if (!url) throw new Error('Cole o link do vídeo.');
        const name = f('sName').value.trim() || 'Canal';
        list = { name, source: { type: 'single' }, channels: [{ name, url, logo: f('sLogo').value.trim(), group: 'Meus canais', kind: kindOf(url, '') }] };
      }
      if (!list.channels.length) throw new Error('Nenhum canal encontrado. Confira se é uma lista M3U válida.');
      list.id = uid();
      list.updated = Date.now();
      state.lists.push(list);
      await save();
      out.textContent = `✓ ${list.channels.length} itens adicionados.`;
      dlg.querySelectorAll('input').forEach((i) => { i.value = ''; });
      renderLists();
      render();
    } catch (e) {
      out.textContent = e.message;
    } finally {
      btn.disabled = false;
    }
  }

  $('#btnAdd').addEventListener('click', addList);
  $('#listItems').addEventListener('click', async (e) => {
    const rm = e.target.closest('[data-remove]');
    const rf = e.target.closest('[data-refresh]');
    if (rm) {
      if (!confirm('Remover esta lista?')) return;
      state.lists = state.lists.filter((l) => l.id !== rm.dataset.remove);
      await save(); renderLists(); render();
    } else if (rf) {
      const l = state.lists.find((x) => x.id === rf.dataset.refresh);
      rf.textContent = '…';
      try {
        l.channels = parseM3U(await fetchText(l.source.url));
        l.updated = Date.now();
        await save();
      } catch (err) { alert(friendlyFetchError(err, l.source.url)); }
      renderLists(); render();
    }
  });

  // ---------- Eventos ----------
  const openLists = () => { renderLists(); dlg.showModal(); };
  $('#btnLists').addEventListener('click', openLists);
  $('#btnEmptyAdd').addEventListener('click', openLists);

  document.querySelectorAll('.tab').forEach((t) => t.addEventListener('click', () => {
    state.tab = t.dataset.tab; state.group = '__all'; state.page = 1;
    document.querySelectorAll('.tab').forEach((x) => x.classList.toggle('active', x === t));
    render();
  }));
  groupsEl.addEventListener('click', (e) => {
    const b = e.target.closest('[data-group]');
    if (!b) return;
    state.group = b.dataset.group; state.page = 1; render();
  });
  let st;
  $('#search').addEventListener('input', (e) => {
    clearTimeout(st);
    st = setTimeout(() => { state.query = e.target.value; state.page = 1; render(); }, 180);
  });
  more.addEventListener('click', () => { state.page++; render(); });
  grid.addEventListener('click', (e) => {
    const c = e.target.closest('.card');
    if (c) play(+c.dataset.i);
  });

  $('#btnClose').addEventListener('click', closePlayer);
  $('#btnPrev').addEventListener('click', () => play((state.current - 1 + state.view.length) % state.view.length));
  $('#btnNext').addEventListener('click', () => play((state.current + 1) % state.view.length));
  $('#btnFav').addEventListener('click', async () => {
    const c = state.view[state.current];
    if (!c) return;
    state.favs.has(c.url) ? state.favs.delete(c.url) : state.favs.add(c.url);
    $('#btnFav').textContent = state.favs.has(c.url) ? '★' : '☆';
    await save();
  });

  // Controle remoto / teclado (Smart TVs, TV Box, PC)
  document.addEventListener('keydown', (e) => {
    const playing = !player.classList.contains('hidden');
    if (playing) {
      if (e.key === 'Escape' || e.key === 'Backspace' || e.key === 'GoBack' || e.keyCode === 10009 || e.keyCode === 461) {
        if (e.target.tagName !== 'INPUT') { e.preventDefault(); closePlayer(); }
      } else if (e.key === 'ArrowUp' || e.key === 'ChannelUp' || e.keyCode === 427) {
        e.preventDefault(); $('#btnPrev').click();
      } else if (e.key === 'ArrowDown' || e.key === 'ChannelDown' || e.keyCode === 428) {
        e.preventDefault(); $('#btnNext').click();
      } else if (e.key === 'f') {
        player.requestFullscreen?.().catch(() => {});
      }
      return;
    }
    // Navegação por setas na grade
    const card = document.activeElement?.closest?.('.card');
    if (!card || !['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) return;
    const cards = [...grid.querySelectorAll('.card')];
    const idx = cards.indexOf(card);
    const cols = Math.max(1, Math.round(grid.clientWidth / card.getBoundingClientRect().width));
    const step = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -cols, ArrowDown: cols }[e.key];
    const next = cards[idx + step];
    if (next) { e.preventDefault(); next.focus(); next.scrollIntoView({ block: 'nearest' }); }
  });

  // ---------- Início ----------
  (async () => {
    state.lists = (await DB.get('lists')) || [];
    state.favs = new Set((await DB.get('favs')) || []);
    render();
    if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(() => {});
  })();
})();
