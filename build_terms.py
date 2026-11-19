#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成西班牙语日常词汇卡数据（1000 条）。
   高频筛选参考：GirkovArpa/english-spanish-wordlists（源自 oprogramador 多语词频统计），
   本地副本 /tmp/es.json。释义、例句、说明全部人工撰写，不用机器翻译。

   数据结构见 data/terms.js 顶部注释。
   · 42 条人工原稿写在下面的 ORIGINALS；
   · 其余词条按批次写在 data/part1.py … part5.py，每个 part 暴露
     DATA = [(scene, es, zh, pos, ex, exZh, note), ...]；
   · data/term_data.md 是批次写作的原始稿，按 slug 覆盖同词的例句 / 说明
     （写得更口语或改过错的条目这里是最终版）。
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "data", "terms.js")

# 8 个场景 key → 中文标签（标签格式：场景 · 说明）
SCENE_LABELS = {
    "greeting": "问候 · 打招呼",
    "daily": "日常 · 起居动作",
    "food": "饮食 · 吃喝点单",
    "travel": "出行 · 问路交通",
    "shopping": "购物 · 钱与商店",
    "emergency": "应急 · 身体求助",
    "time": "时间 · 日期时段",
    "social": "社交 · 家庭关系",
}
TARGET = {"greeting": 80, "daily": 160, "food": 160, "travel": 140,
          "shopping": 120, "emergency": 100, "time": 120, "social": 120}

# ── 42 条人工精写原稿（质量标杆，id 沿用页面已存的写法，保证 localStorage 记忆不失效）──
ORIGINALS = [
    # greeting
    ("hola", "hola", "你好", "感叹", "greeting",
     "Hola, ¿qué tal?", "你好，怎么样？", "最通用的招呼，任何时间、任何人。"),
    ("buenos-dias", "buenos días", "早上好", "短语", "greeting",
     "Buenos días, señora.", "早上好，女士。", "中午两点前用。día 是阳性，所以用 buenos。"),
    ("buenas-noches", "buenas noches", "晚上好 / 晚安", "短语", "greeting",
     "Buenas noches, hasta mañana.", "晚安，明天见。", "见面时说「晚上好」，分开时说「晚安」，同一句。"),
    ("gracias", "gracias", "谢谢", "感叹", "greeting",
     "Muchas gracias por todo.", "非常感谢你做的这一切。", "加 muchas 表示「非常感谢」。"),
    ("por-favor", "por favor", "请 / 麻烦你", "短语", "greeting",
     "Un café, por favor.", "麻烦来杯咖啡。", "放句尾。西语里不加这个会显得生硬。"),
    ("adios", "adiós", "再见", "感叹", "greeting",
     "Adiós, nos vemos.", "再见，回头见。", "正式些；朋友间更常说 hasta luego。"),
    ("hasta-luego", "hasta luego", "回头见", "短语", "greeting",
     "Hasta luego, cuídate.", "回头见，保重。", "不是「待会儿见」的严格意思，就是随口告别。"),
    ("perdon", "perdón", "对不起 / 劳驾", "名词",
     "greeting", "Perdón, ¿tiene un minuto?", "劳驾，您有空吗？", "既能道歉也能插话，比 lo siento 轻。"),
    # daily
    ("agua", "agua", "水", "名词", "daily",
     "¿Me trae un vaso de agua?", "能给我一杯水吗？", "阴性名词：el agua 但说 mucha agua。"),
    ("comer", "comer", "吃", "动词", "daily",
     "¿Qué quieres comer?", "你想吃什么？", "「吃饭」一般用 comer，三餐各有专词（desayunar 等）。"),
    ("beber", "beber", "喝", "动词", "daily",
     "No bebo alcohol.", "我不喝酒。", "日常口语里 tomar 更常用。"),
    ("pan", "pan", "面包", "名词", "daily",
     "Pan con tomate, por favor.", "番茄面包，谢谢。", "餐厅要「一份面包」说 un pan。"),
    ("cafe", "café", "咖啡", "名词", "daily",
     "Un café con leche.", "一杯拿铁。", "café solo 是浓缩，café con leche 是加奶。"),
    ("casa", "casa", "家 / 房子", "名词", "daily",
     "Voy a casa.", "我回家。", "a casa 不加冠词，表示「回自己家」。"),
    ("dormir", "dormir", "睡觉", "动词", "daily",
     "Necesito dormir.", "我需要睡觉。", "不规则动词：duermo、durmió。"),
    ("trabajo", "trabajo", "工作", "名词", "daily",
     "Voy al trabajo.", "我去上班。", "阳性。动词 trabajar 同源。"),
    # travel
    ("donde", "dónde", "在哪里", "副词", "travel",
     "¿Dónde está el baño?", "洗手间在哪里？", "问位置用 dónde está，问去哪用 adónde vas。"),
    ("bano", "baño", "洗手间", "名词", "travel",
     "¿Hay un baño cerca?", "附近有洗手间吗？", "西班牙说 aseo 或 servicio 也很常见。"),
    ("calle", "calle", "街道", "名词", "travel",
     "Vivo en esta calle.", "我住在这条街。", "阴性：la calle。"),
    ("cerca", "cerca", "近 / 附近", "副词", "travel",
     "El hotel está cerca.", "酒店很近。", "反义 lejos。"),
    ("lejos", "lejos", "远", "副词", "travel",
     "¿Está muy lejos?", "很远吗？", "常用搭配：lejos de aquí（离这儿远）。"),
    ("izquierda", "izquierda", "左边", "名词", "travel",
     "Gira a la izquierda.", "向左转。", "阴性；右边是 derecha。"),
    ("derecha", "derecha", "右边", "名词", "travel",
     "La farmacia está a la derecha.", "药房在右边。", "a la derecha 是固定搭配，不要漏冠词。"),
    ("billete", "billete", "票", "名词", "travel",
     "Quiero un billete de ida.", "我要一张单程票。", "ida 单程，ida y vuelta 往返。"),
    # shopping
    ("cuanto", "cuánto", "多少", "副词", "shopping",
     "¿Cuánto cuesta?", "多少钱？", "问价格固定说法。问数量用 cuántos。"),
    ("dinero", "dinero", "钱", "名词", "shopping",
     "No tengo dinero.", "我没钱。", "不可数，不说 dineros。"),
    ("caro", "caro", "贵的", "形容词", "shopping",
     "Es muy caro.", "太贵了。", "反义 barato。跟名词时变化：una casa cara。"),
    ("barato", "barato", "便宜的", "形容词", "shopping",
     "Es bastante barato.", "挺便宜的。", "还表示「廉价劣质」，要分语境。"),
    ("tarjeta", "tarjeta", "卡 / 银行卡", "名词", "shopping",
     "¿Puedo pagar con tarjeta?", "可以刷卡吗？", "tarjeta de crédito 信用卡。"),
    ("tienda", "tienda", "商店", "名词", "shopping",
     "La tienda abre a las diez.", "商店十点开门。", "阴性；店面小摊叫 puesto。"),
    # emergency
    ("ayuda", "ayuda", "帮助", "名词", "emergency",
     "Necesito ayuda.", "我需要帮助。", "动词 ayudar；求助喊 ¡Ayuda!"),
    ("medico", "médico", "医生", "名词", "emergency",
     "Llame a un médico.", "请叫医生。", "阳性；「看医生」是 ir al médico。"),
    ("enfermo", "enfermo", "生病的", "形容词", "emergency",
     "Estoy enfermo.", "我病了。", "女性说 enferma。"),
    ("hospital", "hospital", "医院", "名词", "emergency",
     "¿Dónde está el hospital?", "医院在哪里？", "阳性，重音在最后：hospital。"),
    ("no-entiendo", "no entiendo", "我不懂", "短语", "emergency",
     "No entiendo, más despacio, por favor.", "我不懂，请慢一点。",
     "旅游时最有用的句子之一。"),
    ("hablar", "hablar", "说 / 讲", "动词", "emergency",
     "¿Habla inglés?", "您说英语吗？", "hablo 是我说，habla 是他说 / 您说。"),
    # time
    ("hoy", "hoy", "今天", "副词", "time",
     "Hoy no trabajo.", "我今天不上班。", "不需要介词，直接说 hoy。"),
    ("manana", "mañana", "明天 / 早上", "名词", "time",
     "Hasta mañana.", "明天见。", "同形两义：明天、早上。看冠词和上下文分辨。"),
    ("ayer", "ayer", "昨天", "副词", "time",
     "Ayer llovió.", "昨天下雨了。", "配简单过去时，不配现在时。"),
    ("ahora", "ahora", "现在", "副词", "time",
     "Ahora no puedo.", "我现在不行。", "ahora mismo 是「就现在」。"),
    ("siempre", "siempre", "总是", "副词", "time",
     "Siempre llega tarde.", "他总迟到。", "反义 nunca。"),
    ("nunca", "nunca", "从不", "副词", "time",
     "Nunca he estado allí.", "我从没去过那儿。", "否定句里 nunca 前不再加 no。"),
]

POS = {"名词", "动词", "形容词", "副词", "短语", "感叹", "数词", "代词"}


def bare(text):
    """去掉词条开头的冠词，用来配对 md 稿（md 里写「el pan」，DATA 里写「pan」）。"""
    t = text.lower()
    for a in ("el ", "la ", "los ", "las ", "un ", "una "):
        if t.startswith(a):
            return t[len(a):]
    return t


def slug(text):
    """id：小写、去重音、非字母当连字符。"""
    s = text.lower()
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"),
                 ("ü", "u"), ("ñ", "n")):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def load_md():
    """读 data/term_data.md（批次写作的原始稿，每 4 行为一条）：
         scene|es|zh|pos
         - 例句西语
         - 例句中文
         - 用法说明
       这些条目覆盖同名的 DATA 行（正文、note 都比初稿更口语）。"""
    path = os.path.join(ROOT, "data", "term_data.md")
    if not os.path.exists(path):
        return {}
    out = {}
    for b in re.split(r"\n\s*\n", open(path, encoding="utf-8").read()):
        lines = [x.strip() for x in b.strip().split("\n") if x.strip()]
        if not lines:
            continue
        head = lines[0].split("|")
        if len(head) != 4 or head[0].strip() not in SCENE_LABELS:
            continue
        scene, es, zh, pos = [x.strip() for x in head]
        notes = [l[2:].strip() for l in lines[1:] if l.startswith("-")]
        if len(notes) < 3:
            continue
        rec = {"ex": notes[0], "exZh": notes[1], "note": notes[2]}
        out[slug(es)] = rec
        out.setdefault(slug(bare(es)), rec)
    return out


def load_parts():
    """把 data/part1.py … part4.py 的 DATA 依次读进来。"""
    rows = []
    md = load_md()
    for i in range(1, 9):
        path = os.path.join(ROOT, "data", "part%d.py" % i)
        if not os.path.exists(path):
            continue
        ns = {}
        try:
            exec(compile(open(path, encoding="utf-8").read(), path, "exec"), ns)
        except SyntaxError as e:
            print("!! %s 第 %s 行语法错误，跳过" % (path, e.lineno))
            continue
        for r in ns.get("DATA", []):
            if len(r) not in (7, 8):
                print("!! %s 字段数不对，跳过：%r" % (path, r))
                continue
            fixed = list(r[:7])
            fix = md.get(slug(r[1]))
            if fix:
                fixed[4] = fix.get("ex") or fixed[4]
                fixed[5] = fix.get("exZh") or fixed[5]
                fixed[6] = fix.get("note") or fixed[6]
            rows.append(tuple(fixed))
    return rows


def build():
    terms, seen = [], set()

    def add(scene, es, zh, pos, ex, exZh, note, tid=None):
        tid = tid or slug(es)
        if tid in seen:
            print("!! 跳过重复 id：%s（%s）" % (tid, es))
            return
        if scene not in SCENE_LABELS:
            raise SystemExit("场景非法：%s（%s）" % (scene, es))
        if pos not in POS:
            raise SystemExit("词性非法：%s（%s）" % (pos, es))
        seen.add(tid)
        terms.append({
            "id": tid, "es": es, "zh": zh, "pos": pos, "scene": scene,
            "sceneLabel": SCENE_LABELS[scene], "ex": ex, "exZh": exZh, "note": note,
        })

    md = load_md()
    for (tid, es, zh, pos, scene, ex, exZh, note) in ORIGINALS:
        fix = md.get(tid) or md.get(slug(es)) or {}
        add(scene, es, zh, pos, fix.get("ex") or ex, fix.get("exZh") or exZh,
            fix.get("note") or note, tid)
    for row in load_parts():
        scene, es, zh, pos, ex, exZh, note, *_ = row
        add(scene, es, zh, pos, ex, exZh, note)
    return terms


def interleave(terms):
    """场景交错：相邻两词必属不同场景（按目标配额成比例轮转，余数另排）。"""
    by = {k: [] for k in SCENE_LABELS}
    for t in terms:
        by[t["scene"]].append(t)
    total = len(terms)
    acc, order = 0.0, []
    step = {k: (len(by[k]) / total if total else 0) for k in SCENE_LABELS}
    # 比例轮转：每次取「应出而未出最多」的场景
    ptr = {k: 0 for k in SCENE_LABELS}
    issued = {k: 0 for k in SCENE_LABELS}
    while len(order) < total:
        best, best_key = None, -1.0
        for k in SCENE_LABELS:
            if issued[k] >= len(by[k]):
                continue
            if order and order[-1]["scene"] == k:
                continue
            score = step[k] * (issued[k] + 1) - (len(order) + 1) * step[k] if False else 0
            # 目标位置：issued/len 最小的场景先出
            score = issued[k] / max(len(by[k]), 1)
            if best is None or score < best_key:
                best, best_key = k, score
        if best is None:   # 只剩同一场景的余量，插到中间去
            rest = [by[k][ptr[k]] for k in SCENE_LABELS if ptr[k] < len(by[k])]
            for t in rest:
                order.insert(min(len(order) // 2, len(order)), t)
            break
        order.append(by[best][ptr[best]])
        ptr[best] += 1
        issued[best] += 1
    return order


def main():
    terms = build()
    from collections import Counter
    cnt = Counter(t["scene"] for t in terms)
    problems = []
    for k, want in TARGET.items():
        if cnt.get(k, 0) != want:
            problems.append("%s 实际 %d / 目标 %d" % (k, cnt.get(k, 0), want))
    short_ex = [t["es"] for t in terms if not (6 <= len(t["ex"].split()) <= 18)]
    short_note = [t["es"] for t in terms if len(t["note"]) < 12]
    order = interleave(terms)
    bad = [i for i in range(1, len(order)) if order[i]["scene"] == order[i - 1]["scene"]]

    print("词条", len(terms), "/ 目标", sum(TARGET.values()))
    seen_core = {}
    for t in terms:
        c = t["es"].lower()
        for a in ("el ", "la ", "los ", "las ", "un ", "una "):
            if c.startswith(a):
                c = c[len(a):]
        if c in seen_core and seen_core[c] != t["es"]:
            print("?? 可能重复：%s / %s" % (seen_core[c], t["es"]))
        seen_core.setdefault(c, t["es"])
    for k in SCENE_LABELS:
        print("  %-10s %3d / %d" % (k, cnt.get(k, 0), TARGET[k]))
    if problems:
        print("!! 配额不符：", problems)
    if len(order) != len(terms):
        print("!! 交错丢失", len(terms) - len(order))
    if bad:
        print("!! 相邻同场景位置", bad[:10], "共", len(bad))
    if short_ex:
        print("!! 例句过长/过短", len(short_ex), short_ex[:15])
    if short_note:
        print("!! note 过短", len(short_note), short_note[:15])

    body = "\n".join(
        "  T(" + ", ".join(json.dumps(x, ensure_ascii=False) for x in (
            t["id"], t["es"], t["zh"], t["pos"], t["scene"], t["sceneLabel"],
            t["ex"], t["exZh"], t["note"])) + "),"
        for t in order)
    js = """/* 西班牙语日常词汇 · 词条库
 * 唯一数据源。字段：id / 西语 / 中文 / 词性 / 场景 / 场景名 / 例句 / 例句中文 / 用法说明
 * 高频筛选参考：oprogramador 多语词频统计；释义、例句、说明为人工撰写。
 */
(function (root) {
  const T = (id, es, zh, pos, scene, sceneLabel, ex, exZh, note) =>
    ({ id, es, zh, pos, scene, sceneLabel, ex, exZh, note });

  root.TERMS = [
%s
  ];
})(typeof window !== 'undefined' ? window : globalThis);
""" % body
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(js)
    print("→", OUT, os.path.getsize(OUT), "bytes")
    return 1 if problems or bad else 0


if __name__ == "__main__":
    sys.exit(main())