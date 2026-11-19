#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UI 优化：补齐卡片下方的视觉重量。
   加三块有实际用途的内容：
   1. 进度环（掌握比例，SVG 绘制）
   2. 场景分布条（每个场景学了多少，一眼看出偏科）
   3. 今日痕迹（翻了几张、新掌握几个，有无数据都有对应状态）
"""
import os, re

P = "/var/minis/workspace/spanish-cards/build_page.py"
s = open(P, encoding="utf-8").read()

# ── 1) 追加 CSS ─────────────────────────────────────────────
NEW_CSS = """
/* ── 下方信息区：补足页面下半部分的视觉重量 ── */
.panel{margin:18px 0 0;padding:16px 0 0;border-top:1px solid var(--line-2)}
.panel h2{font-size:12px;font-weight:400;color:var(--ink-3);margin:0 0 12px;letter-spacing:.01em}

/* 进度环 + 一句话 */
.ring-row{display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:center}
.ring{position:relative;width:74px;height:74px;flex:none}
.ring svg{display:block;transform:rotate(-90deg)}
.ring .track{stroke:var(--line);stroke-width:5;fill:none}
.ring .fill{stroke:var(--violet);stroke-width:5;fill:none;stroke-linecap:round;
  transition:stroke-dashoffset .5s cubic-bezier(.16,1,.3,1)}
.ring .num{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
  font-size:16px;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.ring-txt{min-width:0}
.ring-txt .big{font-size:15px;color:var(--ink);margin:0 0 3px}
.ring-txt .small{font-size:12.5px;color:var(--ink-3);margin:0;line-height:1.5}

/* 场景分布：横向小条，一眼看偏科 */
.bars{display:grid;gap:9px}
.bars .b{display:grid;grid-template-columns:4.6em 1fr auto;gap:9px;align-items:center;
  font-size:12px}
.bars .b .name{color:var(--ink-2)}
.bars .b .track{height:5px;background:var(--line-2);border-radius:3px;overflow:hidden}
.bars .b .track i{display:block;height:5px;background:var(--violet);border-radius:3px;
  transition:width .5s cubic-bezier(.16,1,.3,1)}
.bars .b .v{color:var(--ink-3);font-variant-numeric:tabular-nums;font-size:11.5px;
  min-width:3.4em;text-align:right}

/* 今日：三个小读数 + 一条迷你轨迹 */
.today-row{display:flex;gap:22px;margin:0 0 10px}
.today-row div{display:flex;flex-direction:column;gap:1px}
.today-row .k{font-size:11.5px;color:var(--ink-3)}
.today-row .v{font-size:17px;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.spark{display:flex;align-items:flex-end;gap:4px;height:26px;margin-top:2px}
.spark i{flex:1;background:var(--line);border-radius:1px 1px 0 0;min-height:2px;
  transition:height .4s ease-out}
.spark i.on{background:var(--violet)}
.spark-days{display:flex;gap:4px;margin-top:4px}
.spark-days span{flex:1;text-align:center;font-size:9.5px;color:var(--ink-3)}
"""

s = s.replace('.empty{padding:20px 0;color:var(--ink-3);font-size:13.5px}\n"""',
              '.empty{padding:20px 0;color:var(--ink-3);font-size:13.5px}' + NEW_CSS + '"""')

# ── 2) 追加 HTML ────────────────────────────────────────────
NEW_HTML = '''
      <div class="panel">
        <h2>进度</h2>
        <div class="ring-row">
          <div class="ring" id="ring" role="img" aria-label="掌握进度">
            <svg width="74" height="74" viewBox="0 0 74 74" aria-hidden="true">
              <circle class="track" cx="37" cy="37" r="32"/>
              <circle class="fill" id="ringFill" cx="37" cy="37" r="32"
                      stroke-dasharray="201" stroke-dashoffset="201"/>
            </svg>
            <span class="num" id="ringNum">0%</span>
          </div>
          <div class="ring-txt">
            <p class="big" id="ringBig">还没开始</p>
            <p class="small" id="ringSmall">标记已掌握的词会算进这里。</p>
          </div>
        </div>
      </div>

      <div class="panel">
        <h2>场景分布</h2>
        <div class="bars" id="bars"></div>
      </div>

      <div class="panel">
        <h2>今天</h2>
        <div class="today-row">
          <div><span class="k">翻过</span><span class="v" id="tSeen">0</span></div>
          <div><span class="k">新掌握</span><span class="v" id="tKnown">0</span></div>
          <div><span class="k">连续</span><span class="v" id="tStreak">0</span></div>
        </div>
        <div class="spark" id="spark" aria-label="近七天翻过的词数"></div>
        <div class="spark-days" id="sparkDays"></div>
      </div>
'''

s = s.replace('''    </section>

    <section id="viewIndex" hidden>''','''    </section>

    <section id="viewIndex" hidden>''')
# 面板放在 viewStudy 里，meta 之后
s = s.replace('''        </span>
      </div>
    </section>

    <section id="viewIndex" hidden>''','''        </span>
      </div>
''' + NEW_HTML + '''    </section>

    <section id="viewIndex" hidden>''')

open(P, "w", encoding="utf-8").write(s)
print("CSS/HTML 已注入")