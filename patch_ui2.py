#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补齐三块面板的渲染逻辑：进度环 / 场景分布 / 今日痕迹。"""
P = "/var/minis/workspace/spanish-cards/build_page.py"
s = open(P, encoding="utf-8").read()

# ── 追踪今日痕迹：每次翻面、标记都记一条 ──
TRACE = """
  /* ── 今日痕迹：本地记录，不依赖云端 ── */
  const DAY_KEY = STORE_KEY + ':days';
  function todayStr() {
    const d = new Date();
    return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' +
           String(d.getDate()).padStart(2,'0');
  }
  function readDays() {
    try { return JSON.parse(localStorage.getItem(DAY_KEY) || '{}'); } catch (e) { return {}; }
  }
  function touchDay() {
    const d = readDays(), k = todayStr();
    d[k] = d[k] || { seen: {}, known: 0 };
    localStorage.setItem(DAY_KEY, JSON.stringify(d));
    return d[k];
  }
  function markSeen(id) { const t = touchDay(); t.seen[id] = 1;
    localStorage.setItem(DAY_KEY, JSON.stringify(readDays())); }
"""

# 在 deck/current 定义后插入
s = s.replace("  const isFlipped = () => $('card').dataset.flipped === 'true';",
              "  const isFlipped = () => $('card').dataset.flipped === 'true';\n" + TRACE)

# ── 面板渲染函数 ──
PANELS = """
  /* ── 下方三块面板 ── */
  function renderPanels() {
    const d = deck();
    const done = d.filter(t => state.mastered[t.id]).length;
    const pct = d.length ? Math.round(done / d.length * 100) : 0;

    // 进度环
    const C = 2 * Math.PI * 32;
    const fill = $('ringFill');
    fill.setAttribute('stroke-dasharray', C.toFixed(1));
    fill.setAttribute('stroke-dashoffset', (C * (1 - done / (d.length || 1))).toFixed(1));
    $('ringNum').textContent = pct + '%';
    $('ringBig').textContent = done === 0 ? '还没开始'
      : done === d.length ? '这个范围全掌握了' : `已掌握 ${done} 个`;
    $('ringSmall').textContent = done === 0
      ? '标记已掌握的词会算进这里。'
      : `还剩 ${d.length - done} 个没标记，${pct}% 完成。`;

    // 场景分布
    const byScene = {};
    TERMS.forEach(t => {
      byScene[t.scene] = byScene[t.scene] || { total: 0, done: 0, label: t.sceneLabel };
      byScene[t.scene].total++;
      if (state.mastered[t.id]) byScene[t.scene].done++;
    });
    $('bars').innerHTML = Object.keys(byScene).map(k => {
      const v = byScene[k];
      const w = v.total ? (v.done / v.total * 100) : 0;
      return `<div class="b">
        <span class="name">${esc(v.label.split(' · ')[0])}</span>
        <span class="track"><i style="width:${w.toFixed(1)}%"></i></span>
        <span class="v">${v.done}/${v.total}</span>
      </div>`;
    }).join('');

    // 今日
    const days = readDays();
    const td = days[todayStr()] || { seen: {}, known: 0 };
    $('tSeen').textContent = Object.keys(td.seen || {}).length;
    $('tKnown').textContent = td.known || 0;

    const keys = [];
    for (let i = 6; i >= 0; i--) {
      const x = new Date(); x.setDate(x.getDate() - i);
      keys.push(x.getFullYear() + '-' + String(x.getMonth()+1).padStart(2,'0') + '-' + String(x.getDate()).padStart(2,'0'));
    }
    const counts = keys.map(k => Object.keys((days[k] || {}).seen || {}).length);
    const max = Math.max(1, ...counts);
    $('spark').innerHTML = counts.map((n, i) => {
      const h = n ? Math.max(3, Math.round(n / max * 26)) : 2;
      return `<i class="${n ? 'on' : ''}" style="height:${h}px" title="${keys[i]} ${n} 个"></i>`;
    }).join('');
    $('sparkDays').innerHTML = keys.map(k => `<span>${k.slice(8)}</span>`).join('');

    // 连续天数
    let streak = 0;
    for (let i = 0; i < 400; i++) {
      const x = new Date(); x.setDate(x.getDate() - i);
      const k = x.getFullYear() + '-' + String(x.getMonth()+1).padStart(2,'0') + '-' + String(x.getDate()).padStart(2,'0');
      const has = Object.keys((days[k] || {}).seen || {}).length > 0;
      if (has) streak++;
      else if (i === 0) continue;      // 今天还没背，不算断
      else break;
    }
    $('tStreak').textContent = streak;
  }
"""

# 插到 renderCard 函数之前
s = s.replace("  /* 卡片 */\n  function renderCard() {", PANELS + "\n  /* 卡片 */\n  function renderCard() {")

# renderCard 末尾调用 renderPanels
s = s.replace("""    $('card').setAttribute('aria-label', isFlipped()
      ? `${t.zh}，西语 ${t.es}。按空格翻回`
      : `${t.zh}，${t.sceneLabel}。按空格翻面看西语`);""",
"""    $('card').setAttribute('aria-label', isFlipped()
      ? `${t.zh}，西语 ${t.es}。按空格翻回`
      : `${t.zh}，${t.sceneLabel}。按空格翻面看西语`);

    renderPanels();""")

# 翻面时记「看过」；标记掌握时累计
s = s.replace("""  function setFlip(on) {
    $('card').dataset.flipped = String(on);""",
"""  function setFlip(on) {
    if (on) markSeen(current().id);
    $('card').dataset.flipped = String(on);""")

s = s.replace("""    if (was) delete state.mastered[t.id];
    else state.mastered[t.id] = Date.now();
    save(); renderCard(); renderRows();""",
"""    if (was) delete state.mastered[t.id];
    else { state.mastered[t.id] = Date.now(); const td = touchDay(); td.known = (td.known || 0) + 1;
           localStorage.setItem(DAY_KEY, JSON.stringify(readDays())); }
    save(); renderCard(); renderRows();""")

open(P, "w", encoding="utf-8").write(s)
print("面板逻辑已注入")