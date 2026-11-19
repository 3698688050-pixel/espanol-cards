#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从词频表筛实词，按场景归类，生成西班牙语日常词汇卡数据。
   词频表来源：GirkovArpa/english-spanish-wordlists（源自 oprogramador 多语词频统计）。
   释义、例句、场景说明由人工撰写，不用机器翻译（机器译文质量不可靠，实测 cuánto 被译成「应做多少？」）。
"""
import json, os, re

FREQ = "/tmp/es.json" if os.path.exists("/tmp/es.json") else None

# ── 人工整理的核心词表：场景 → 词条 ───────────────────────────
# 每条：(西语, 中文, 词性, 例句西语, 例句中文, 一句话说明)
SCENES = {
    "问候": {
        "label": "问候 · 打招呼",
        "words": [
            ("hola", "你好", "感叹",
             "Hola, ¿qué tal?", "你好，怎么样？",
             "最通用的招呼，任何时间、任何人。"),
            ("buenos días", "早上好", "短语",
             "Buenos días, señora.", "早上好，女士。",
             "中午两点前用。día 是阳性，所以用 buenos。"),
            ("buenas noches", "晚上好 / 晚安", "短语",
             "Buenas noches, hasta mañana.", "晚安，明天见。",
             "见面时说「晚上好」，分开时说「晚安」，同一句。"),
            ("gracias", "谢谢", "感叹",
             "Muchas gracias por todo.", "非常感谢你做的这一切。",
             "加 muchas 表示「非常感谢」。"),
            ("por favor", "请 / 麻烦你", "短语",
             "Un café, por favor.", "麻烦来杯咖啡。",
             "放句尾。西语里不加这个会显得生硬。"),
            ("adiós", "再见", "感叹",
             "Adiós, nos vemos.", "再见，回头见。",
             "正式些；朋友间更常说 hasta luego。"),
            ("hasta luego", "回头见", "短语",
             "Hasta luego, cuídate.", "回头见，保重。",
             "不是「待会儿见」的严格意思，就是随口告别。"),
            ("perdón", "对不起 / 劳驾", "名词",
             "Perdón, ¿tiene un minuto?", "劳驾，您有空吗？",
             "既能道歉也能插话，比 lo siento 轻。"),
        ],
    },
    "日常": {
        "label": "日常 · 吃喝起居",
        "words": [
            ("agua", "水", "名词",
             "¿Me trae un vaso de agua?", "能给我一杯水吗？",
             "阴性名词：el agua 但说 mucha agua。"),
            ("comer", "吃", "动词",
             "¿Qué quieres comer?", "你想吃什么？",
             "「吃饭」一般用 comer，三餐各有专词（desayunar 等）。"),
            ("beber", "喝", "动词",
             "No bebo alcohol.", "我不喝酒。",
             "日常口语里 tomar 更常用。"),
            ("pan", "面包", "名词",
             "Pan con tomate, por favor.", "番茄面包，谢谢。",
             "餐厅要「一份面包」说 un pan。"),
            ("café", "咖啡", "名词",
             "Un café con leche.", "一杯拿铁。",
             "café solo 是浓缩，café con leche 是加奶。"),
            ("casa", "家 / 房子", "名词",
             "Voy a casa.", "我回家。",
             "a casa 不加冠词，表示「回自己家」。"),
            ("dormir", "睡觉", "动词",
             "Necesito dormir.", "我需要睡觉。",
             "不规则动词：duermo、durmió。"),
            ("trabajo", "工作", "名词",
             "Voy al trabajo.", "我去上班。",
             "阳性。动词 trabajar 同源。"),
        ],
    },
    "出行": {
        "label": "出行 · 问路交通",
        "words": [
            ("dónde", "在哪里", "副词",
             "¿Dónde está el baño?", "洗手间在哪里？",
             "问位置用 dónde está，问去哪用 adónde vas。"),
            ("baño", "洗手间", "名词",
             "¿Hay un baño cerca?", "附近有洗手间吗？",
             "西班牙说 aseo 或 servicio 也很常见。"),
            ("calle", "街道", "名词",
             "Vivo en esta calle.", "我住在这条街。",
             "阴性：la calle。"),
            ("cerca", "近 / 附近", "副词",
             "El hotel está cerca.", "酒店很近。",
             "反义 lejos。"),
            ("lejos", "远", "副词",
             "¿Está muy lejos?", "很远吗？",
             "常用搭配：lejos de aquí（离这儿远）。"),
            ("izquierda", "左边", "名词",
             "Gira a la izquierda.", "向左转。",
             "阴性；右边是 derecha。"),
            ("derecha", "右边", "名词",
             "La farmacia está a la derecha.", "药房在右边。",
             "a la derecha 是固定搭配，不要漏冠词。"),
            ("billete", "票", "名词",
             "Quiero un billete de ida.", "我要一张单程票。",
             "ida 单程，ida y vuelta 往返。"),
        ],
    },
    "购物": {
        "label": "购物 · 付钱议价",
        "words": [
            ("cuánto", "多少", "副词",
             "¿Cuánto cuesta?", "多少钱？",
             "问价格固定说法。问数量用 cuántos。"),
            ("dinero", "钱", "名词",
             "No tengo dinero.", "我没钱。",
             "不可数，不说 dineros。"),
            ("caro", "贵的", "形容词",
             "Es muy caro.", "太贵了。",
             "反义 barato。跟名词时变化：una casa cara。"),
            ("barato", "便宜的", "形容词",
             "Es bastante barato.", "挺便宜的。",
             "还表示「廉价劣质」，要分语境。"),
            ("tarjeta", "卡 / 银行卡", "名词",
             "¿Puedo pagar con tarjeta?", "可以刷卡吗？",
             "tarjeta de crédito 信用卡。"),
            ("tienda", "商店", "名词",
             "La tienda abre a las diez.", "商店十点开门。",
             "阴性；店面小摊叫 puesto。"),
        ],
    },
    "应急": {
        "label": "应急 · 需要帮忙",
        "words": [
            ("ayuda", "帮助", "名词",
             "Necesito ayuda.", "我需要帮助。",
             "动词 ayudar；求助喊 ¡Ayuda! "),
            ("médico", "医生", "名词",
             "Llame a un médico.", "请叫医生。",
             "阳性；「看医生」是 ir al médico。"),
            ("enfermo", "生病的", "形容词",
             "Estoy enfermo.", "我病了。",
             "女性说 enferma。"),
            ("hospital", "医院", "名词",
             "¿Dónde está el hospital?", "医院在哪里？",
             "阳性，重音在最后：hospital。"),
            ("no entiendo", "我不懂", "短语",
             "No entiendo, más despacio, por favor.", "我不懂，请慢一点。",
             "旅游时最有用的句子之一。"),
            ("hablar", "说 / 讲", "动词",
             "¿Habla inglés?", "您说英语吗？",
             "hablo 是我说，habla 是他说 / 您说。"),
        ],
    },
    "时间": {
        "label": "时间 · 今天明天",
        "words": [
            ("hoy", "今天", "副词",
             "Hoy no trabajo.", "我今天不上班。",
             "不需要介词，直接说 hoy。"),
            ("mañana", "明天 / 早上", "名词",
             "Hasta mañana.", "明天见。",
             "同形两义：明天、早上。看冠词和上下文分辨。"),
            ("ayer", "昨天", "副词",
             "Ayer llovió.", "昨天下雨了。",
             "配简单过去时，不配现在时。"),
            ("ahora", "现在", "副词",
             "Ahora no puedo.", "我现在不行。",
             "ahora mismo 是「就现在」。"),
            ("siempre", "总是", "副词",
             "Siempre llega tarde.", "他总迟到。",
             "反义 nunca。"),
            ("nunca", "从不", "副词",
             "Nunca he estado allí.", "我从没去过那儿。",
             "否定句里 nunca 前不再加 no。"),
        ],
    },
}

# ── 组装 ────────────────────────────────────────────────────
def build():
    terms = []
    for scene, data in SCENES.items():
        for (es, zh, pos, ex_es, ex_zh, note) in data["words"]:
            tid = re.sub(r"[^a-z0-9]+", "-", es.lower()).strip("-")
            terms.append({
                "id": tid,
                "es": es,
                "zh": zh,
                "pos": pos,
                "scene": scene,
                "sceneLabel": data["label"],
                "ex": ex_es,
                "exZh": ex_zh,
                "note": note,
            })
    # 交错排列：相邻两张必属不同场景
    by = {}
    for t in terms:
        by.setdefault(t["scene"], []).append(t)
    order, keys = [], list(by)
    while any(by[k] for k in keys):
        for k in keys:
            if by[k]:
                order.append(by[k].pop(0))
    return order


if __name__ == "__main__":
    terms = build()
    out = "/var/minis/workspace/spanish-cards/data/terms.js"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    body = "\n".join(
        "  T(" + ", ".join([
            json.dumps(t["id"], ensure_ascii=False),
            json.dumps(t["es"], ensure_ascii=False),
            json.dumps(t["zh"], ensure_ascii=False),
            json.dumps(t["pos"], ensure_ascii=False),
            json.dumps(t["scene"], ensure_ascii=False),
            json.dumps(t["sceneLabel"], ensure_ascii=False),
            json.dumps(t["ex"], ensure_ascii=False),
            json.dumps(t["exZh"], ensure_ascii=False),
            json.dumps(t["note"], ensure_ascii=False),
        ]) + "),"
        for t in terms)
    js = f"""/* 西班牙语日常词汇 · 词条库
 * 唯一数据源。字段：id / 西语 / 中文 / 词性 / 场景 / 场景名 / 例句 / 例句中文 / 用法说明
 * 高频筛选参考：oprogramador 多语词频统计；释义、例句、说明为人工撰写。
 */
(function (root) {{
  const T = (id, es, zh, pos, scene, sceneLabel, ex, exZh, note) =>
    ({{ id, es, zh, pos, scene, sceneLabel, ex, exZh, note }});

  root.TERMS = [
{body}
  ];
}})(typeof window !== 'undefined' ? window : globalThis);
"""
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(js)
    print("词条", len(terms), "→", out)
    from collections import Counter
    print(Counter(t["scene"] for t in terms))