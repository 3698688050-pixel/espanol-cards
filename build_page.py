#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""西班牙语日常词汇 · 翻面卡片
   交互骨架复用 comminution-vocab（翻面、键盘、范围筛选、localStorage 进度），
   视觉换成 Linear 口径：#08090A 近黑、单一 Inter 系、白=主信息 灰=解释、紫只在小处。
"""
import os

OUT = "/var/minis/workspace/spanish-cards/index.html"

CSS = """/* Hallmark · Linear 口径 · 近黑底 + 发丝线 + 单一强调色只用于状态 */
:root{
  --ground:#08090A;
  --panel:#0E1013;
  --ink:#F7F8F8;
  --ink-2:#8A8F98;
  --ink-3:#62666D;
  --line:#23252A;
  --line-2:#191B1F;
  --violet:#5E6AD2;
  --violet-soft:rgba(94,106,210,.16);
  --ok:#8FBF9F;
  --ok-line:#26382C;
  --hover-line:#34373E;
  --row-hover:#0B0D10;
  --card-hover:#2C2F35;
  --sans:-apple-system,BlinkMacSystemFont,"PingFang SC","Helvetica Neue","Noto Sans SC",sans-serif;
  --r:6px;
}
html,body{overflow-x:clip}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);
  font-size:15px;line-height:1.55;font-synthesis-weight:none;-webkit-font-smoothing:antialiased;
  -webkit-text-size-adjust:100%;touch-action:manipulation}
::selection{background:var(--violet-soft);color:var(--ink)}
:focus-visible{outline:2px solid var(--violet);outline-offset:2px;border-radius:var(--r)}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
button{font:inherit}

.wrap{max-width:680px;margin:0 auto;padding:0 18px 48px}

/* 顶栏：低、贴边、字小 */
.top{display:flex;align-items:center;gap:14px;height:52px;
  border-bottom:1px solid var(--line-2)}
.brand{display:flex;align-items:baseline;gap:8px;font-size:14px}
.brand .cn{font-weight:500;letter-spacing:-.01em}
.brand .en{font-size:11px;color:var(--ink-3)}
.tabs{margin-left:auto;display:flex;gap:14px}
.tab{appearance:none;background:none;border:0;padding:0;cursor:pointer;
  font-size:13px;color:var(--ink-2)}
.tab[aria-selected="true"]{color:var(--ink)}
.tab:hover{color:var(--ink)}

/* 范围胶囊：低调，选中才有紫 */
.scopes{display:flex;gap:6px;overflow-x:auto;padding:14px 0 2px;
  scrollbar-width:none;-ms-overflow-style:none}
.scopes::-webkit-scrollbar{display:none}
.pill{flex:none;appearance:none;background:transparent;border:1px solid var(--line);
  border-radius:999px;padding:4px 11px;font-size:12.5px;color:var(--ink-2);cursor:pointer;
  transition:border-color .14s ease-out,color .14s ease-out}
.pill[aria-pressed="true"]{color:var(--ink);border-color:var(--violet);
  box-shadow:0 0 0 3px var(--violet-soft)}
.pill:hover{color:var(--ink)}

/* 卡片：靠层次和线条，不靠圆角大块 */
.card{position:relative;display:block;width:100%;margin:18px 0 0;
  min-height:300px;padding:0;appearance:none;text-align:left;cursor:pointer;
  background:var(--panel);border:1px solid var(--line);border-radius:var(--r);
  color:var(--ink);overflow:hidden;
  transition:border-color .16s ease-out}
.card:hover{border-color:var(--card-hover)}
.card:active{transform:scale(.995)}
.card:focus-visible{border-color:var(--violet)}

.face{position:absolute;inset:0;padding:22px 20px;display:flex;flex-direction:column;
  backface-visibility:hidden;transition:opacity .18s ease-out}
.card[data-flipped="true"] .face--front,
.card[data-flipped="false"] .face--back{opacity:0;pointer-events:none}

.head{display:flex;justify-content:space-between;align-items:baseline;font-size:12px;
  color:var(--ink-3)}
.head .scene{color:var(--ink-2)}
.head .idx{font-variant-numeric:tabular-nums}

/* 正面：只给中文，极大留白 */
.front-mid{flex:1;display:flex;flex-direction:column;justify-content:center;gap:8px;
  padding:8px 0}
.zh{font-size:38px;line-height:1.2;font-weight:500;letter-spacing:-.02em;margin:0;
  text-wrap:balance}
.hint{color:var(--ink-3);font-size:13px;margin:0}
.foot{display:flex;justify-content:space-between;font-size:11.5px;color:var(--ink-3)}

/* 背面：西语为主声部，例句是解释 */
.back-top{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.es{font-size:30px;line-height:1.2;font-weight:500;letter-spacing:-.02em;margin:0}
.pos{font-size:11.5px;color:var(--ink-2);border:1px solid var(--line);
  border-radius:4px;padding:1px 6px}
.back-body{flex:1;display:flex;flex-direction:column;justify-content:center;gap:14px;
  padding:14px 0}
.zh-line{font-size:15px;color:var(--ink-2)}
.rule{height:1px;background:var(--line-2);margin:0}
.ex{margin:0}
.ex .es-ex{font-size:15px;color:var(--ink);line-height:1.5}
.ex .zh-ex{font-size:13px;color:var(--ink-3);margin-top:3px}
.note{font-size:12.5px;color:var(--ink-2);line-height:1.6;margin:0}

/* 操作区 */
.acts{display:flex;gap:8px;margin:14px 0 0;align-items:center}
.btn{appearance:none;border:1px solid var(--line);background:transparent;color:var(--ink);
  border-radius:var(--r);padding:9px 16px;font-size:13.5px;cursor:pointer;
  transition:border-color .14s ease-out}
.btn:hover{border-color:var(--hover-line)}
.btn:active{transform:scale(.97)}
.btn--primary{background:var(--ink);color:var(--ground);border-color:var(--ink);font-weight:500}
.btn--primary:hover{opacity:.9}
.acts .spacer{flex:1}
.meta{display:flex;justify-content:space-between;align-items:baseline;
  margin:14px 0 0;font-size:12.5px;color:var(--ink-2)}
.meta .num{color:var(--ink);font-variant-numeric:tabular-nums}
.linkish{appearance:none;background:none;border:0;padding:0;color:var(--ink-2);
  font-size:12.5px;cursor:pointer;text-decoration:underline;text-underline-offset:3px}
.linkish[data-on="true"]{color:var(--ok)}
.linkish:hover{color:var(--ink)}

/* 词表 */
.search{width:100%;margin:16px 0 0;padding:10px 12px;background:var(--panel);
  border:1px solid var(--line);border-radius:var(--r);color:var(--ink);
  font:inherit;font-size:14px}
.search::placeholder{color:var(--ink-3)}
.count{font-size:12.5px;color:var(--ink-3);margin:10px 0 0}
.rows{list-style:none;margin:8px 0 0;padding:0;border-top:1px solid var(--line-2)}
.rows li{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:baseline;
  padding:11px 0;border-bottom:1px solid var(--line-2);cursor:pointer}
.rows li:hover{background:var(--row-hover)}
.rows .r-es{font-size:14.5px}
.rows .r-zh{color:var(--ink-2);font-size:13px;margin-left:8px}
.rows .r-scene{font-size:11.5px;color:var(--ink-3)}
.rows .r-ok{width:6px;height:6px;border-radius:50%;background:var(--ok);
  display:inline-block;margin-right:6px;vertical-align:middle}
.empty{padding:20px 0;color:var(--ink-3);font-size:13.5px}
"""

BODY = """<div class="wrap">
  <header class="top">
    <div class="brand"><span class="cn">西班牙语日常词汇</span><span class="en">español</span></div>
    <nav class="tabs" role="tablist">
      <button class="tab" id="tabStudy" role="tab" aria-selected="true">背词</button>
      <button class="tab" id="tabIndex" role="tab" aria-selected="false">词表</button>
    </nav>
  </header>

  <div class="scopes" id="scopes" role="group" aria-label="场景筛选"></div>

  <main>
    <section id="viewStudy">
      <button class="card" id="card" data-flipped="false" aria-pressed="false"
              aria-live="polite" aria-label="轻触翻面"></button>

      <div class="acts">
        <button class="btn" id="prev">上一张</button>
        <button class="btn btn--primary" id="next">下一张</button>
      </div>

      <div class="meta">
        <span>已掌握 <span class="num" id="progress">0</span> / <span class="num" id="total">0</span></span>
        <span>
          <button class="linkish" id="mark" data-on="false">标记已掌握</button>
          &nbsp;·&nbsp;
          <button class="linkish" id="reset">清空进度</button>
        </span>
      </div>
    </section>

    <section id="viewIndex" hidden>
      <input class="search" id="search" type="search" placeholder="搜索中文或西语" autocomplete="off">
      <p class="count" id="count" hidden></p>
      <ul class="rows" id="rows"></ul>
      <p class="empty" id="empty" hidden>没有匹配的词条。</p>
    </section>
  </main>
</div>"""

JS = """
(function () {
  'use strict';
  const STORE_KEY = 'espanol-card/v1';
  const $ = id => document.getElementById(id);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

  const TERMS = window.TERMS || [];
  const SCENES = [...new Set(TERMS.map(t => t.scene))];
  const SCENE_LABEL = {};
  TERMS.forEach(t => SCENE_LABEL[t.scene] = t.sceneLabel);

  function load() {
    try {
      const raw = JSON.parse(localStorage.getItem(STORE_KEY) || 'null') || {};
      return { scope: raw.scope || 'all', idx: Math.max(0, raw.idx | 0),
               mastered: raw.mastered && typeof raw.mastered === 'object' ? raw.mastered : {} };
    } catch (e) { return { scope: 'all', idx: 0, mastered: {} }; }
  }
  const state = load();
  const save = () => localStorage.setItem(STORE_KEY, JSON.stringify(state));

  const deck = () => state.scope === 'all' ? TERMS : TERMS.filter(t => t.scene === state.scope);
  const current = () => { const d = deck(); return d[Math.min(state.idx, d.length - 1)] || d[0]; };
  const isFlipped = () => $('card').dataset.flipped === 'true';

  /* 范围胶囊 */
  function renderScopes() {
    const chip = (key, label, n) => `<button class="pill" data-s="${key}"
      aria-pressed="${state.scope === key}">${label} ${n}</button>`;
    $('scopes').innerHTML =
      chip('all', '全部', TERMS.length) +
      SCENES.map(s => chip(s, SCENE_LABEL[s].split(' · ')[0], TERMS.filter(t => t.scene === s).length)).join('');
  }

  function setScope(s) {
    state.scope = s; state.idx = 0; save();
    renderScopes(); renderCard(); renderRows();
  }

  /* 卡片 */
  function renderCard() {
    const t = current(); if (!t) return;
    const d = deck(), pos = Math.min(state.idx, d.length - 1) + 1;
    const on = !!state.mastered[t.id];

    $('card').innerHTML = `
      <div class="face face--front">
        <div class="head"><span class="scene">${esc(t.sceneLabel)}</span><span class="idx">${pos} / ${d.length}</span></div>
        <div class="front-mid">
          <p class="zh">${esc(t.zh)}</p>
          <p class="hint">说出西语说法，再翻面核对。</p>
        </div>
        <div class="foot"><span>轻触或按空格翻面</span><span>${on ? '已掌握' : '未掌握'}</span></div>
      </div>
      <div class="face face--back">
        <div class="head"><span class="scene">${esc(t.sceneLabel)}</span><span class="idx">${pos} / ${d.length}</span></div>
        <div class="back-body">
          <div class="back-top"><h1 class="es">${esc(t.es)}</h1><span class="pos">${esc(t.pos)}</span></div>
          <div class="zh-line">${esc(t.zh)}</div>
          <div class="rule"></div>
          <div class="ex">
            <div class="es-ex">${esc(t.ex)}</div>
            <div class="zh-ex">${esc(t.exZh)}</div>
          </div>
          <p class="note">${esc(t.note)}</p>
        </div>
        <div class="foot"><span>按空格翻回</span><span>${on ? '已掌握' : '未掌握'}</span></div>
      </div>`;

    $('mark').dataset.on = String(on);
    $('mark').textContent = on ? '已掌握，撤销' : '标记已掌握';
    const masteredCount = deck().filter(x => state.mastered[x.id]).length;
    $('progress').textContent = masteredCount;
    $('total').textContent = d.length;
    $('card').setAttribute('aria-label', isFlipped()
      ? `${t.zh}，西语 ${t.es}。按空格翻回`
      : `${t.zh}，${t.sceneLabel}。按空格翻面看西语`);
  }

  function setFlip(on) {
    $('card').dataset.flipped = String(on);
    $('card').setAttribute('aria-pressed', String(on));
    renderCard();
  }
  const toggleFlip = () => setFlip(!isFlipped());

  function go(i) {
    const d = deck();
    state.idx = ((i % d.length) + d.length) % d.length;
    save(); setFlip(false);
  }
  function goNextUnmastered() {
    const d = deck();
    if (d.every(x => state.mastered[x.id])) return;
    let n = d.findIndex((x, i) => i > state.idx && !state.mastered[x.id]);
    if (n === -1) n = d.findIndex(x => !state.mastered[x.id]);
    go(n);
  }

  $('card').addEventListener('click', toggleFlip);
  $('card').addEventListener('keydown', e => {
    if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); toggleFlip(); }
  });
  document.addEventListener('keydown', e => {
    if (e.target.tagName === 'INPUT') return;
    if (e.key === 'ArrowLeft') go(state.idx - 1);
    if (e.key === 'ArrowRight') go(state.idx + 1);
  });
  $('prev').addEventListener('click', () => go(state.idx - 1));
  $('next').addEventListener('click', () => go(state.idx + 1));

  $('mark').addEventListener('click', () => {
    const t = current();
    const was = !!state.mastered[t.id];
    if (was) delete state.mastered[t.id];
    else state.mastered[t.id] = Date.now();
    save(); renderCard(); renderRows();
    if (!was) goNextUnmastered();
  });

  $('reset').addEventListener('click', () => {
    if (!confirm('清空当前范围的进度？')) return;
    deck().forEach(t => delete state.mastered[t.id]);
    save(); renderCard(); renderRows();
  });

  $('scopes').addEventListener('click', e => {
    const b = e.target.closest('.pill');
    if (b) setScope(b.dataset.s);
  });

  /* 视图切换 */
  function showView(name) {
    const study = name === 'study';
    $('viewStudy').hidden = !study;
    $('viewIndex').hidden = study;
    $('tabStudy').setAttribute('aria-selected', String(study));
    $('tabIndex').setAttribute('aria-selected', String(!study));
    if (!study) { renderRows(); $('search').focus(); }
  }
  $('tabStudy').addEventListener('click', () => showView('study'));
  $('tabIndex').addEventListener('click', () => showView('index'));

  /* 词表 */
  function renderRows() {
    const q = ($('search').value || '').trim().toLowerCase();
    const list = q
      ? TERMS.filter(t => t.zh.includes(q) || t.es.toLowerCase().includes(q))
      : TERMS;
    $('count').hidden = !q;
    $('count').textContent = q ? `${list.length} 条匹配` : '';
    $('empty').hidden = list.length > 0;
    $('rows').innerHTML = list.map(t => `
      <li data-id="${t.id}">
        <span><span class="r-es">${esc(t.es)}</span>
          <span class="r-zh">${esc(t.zh)}</span></span>
        <span class="r-scene">${state.mastered[t.id] ? '<i class="r-ok"></i>' : ''}${esc(t.sceneLabel.split(' · ')[0])}</span>
      </li>`).join('');
  }
  $('search').addEventListener('input', renderRows);
  $('rows').addEventListener('click', e => {
    const li = e.target.closest('li'); if (!li) return;
    const i = deck().findIndex(t => t.id === li.dataset.id);
    if (i >= 0) { state.scope = 'all'; }
    const all = TERMS.findIndex(t => t.id === li.dataset.id);
    state.idx = all; save(); showView('study'); setFlip(false); renderScopes();
    $('card').focus();
  });

  renderScopes();
  renderCard();
})();
"""

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>西班牙语日常词汇</title>
<meta name="description" content="按场景分组的高频西班牙语词汇翻面卡片：正面中文，翻面得西语说法、真实例句与用法说明。">
<style>
{CSS}</style>
</head>
<body>
{BODY}
<script src="data/terms.js"></script>
<script>
{JS}</script>
</body>
</html>
"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(HTML)
print("written", OUT, len(HTML))