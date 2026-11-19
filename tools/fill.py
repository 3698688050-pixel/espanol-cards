#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 (scene, es, zh, pos, ex, exZh, note) 行追加到 data/partN.py，自动去重。"""
import re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def slug(text):
    t = text.lower()
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"),
                 ("ü", "u"), ("ñ", "n")):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def existing():
    seen = set()
    for i in range(1, 9):
        p = os.path.join(ROOT, "data", "part%d.py" % i)
        if not os.path.exists(p):
            continue
        ns = {}
        exec(compile(open(p, encoding="utf-8").read(), p, "exec"), ns)
        for r in ns["DATA"]:
            seen.add(slug(r[1]))
    return seen


def q(x):
    return '"' + x.replace("\\", "\\\\").replace('"', '\\"') + '"'


def append(rows, part=3):
    path = os.path.join(ROOT, "data", "part%d.py" % part)
    seen = existing()
    keep, drop = [], []
    for r in rows:
        if len(r) != 7:
            raise SystemExit("字段数不对：%r" % (r,))
        if not all(isinstance(x, str) for x in r):
            raise SystemExit("有非字符串字段：%r" % (r,))
        k = slug(r[1])
        if k in seen:
            drop.append(r[1])
            continue
        seen.add(k)
        keep.append(r)
    body = "\n".join("(" + ", ".join(q(x) for x in r) + ")," for r in keep)
    if os.path.exists(path):
        s = open(path, encoding="utf-8").read()
        s = s.rstrip()
        assert s.endswith("]"), path
        s = s[:-1].rstrip() + "\n" + body + "\n]\n"
    else:
        s = ('"""AI 初稿 · 收尾：补足 1000 条。\n'
             '格式：(scene, es, zh, pos, ex, exZh, note)\n'
             '此文件由 tools/fill.py 生成，人工复核时优先看这里。\n"""\n\n'
             'DATA = [\n' + body + "\n]\n")
    open(path, "w", encoding="utf-8").write(s)
    print("写入 %d 条，跳过重复 %d 条 %s" % (len(keep), len(drop), drop[:8]))