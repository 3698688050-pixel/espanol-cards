/* 西班牙语日常词汇 · 词条库
 * 唯一数据源。字段：id / 西语 / 中文 / 词性 / 场景 / 场景名 / 例句 / 例句中文 / 用法说明
 * 高频筛选参考：oprogramador 多语词频统计；释义、例句、说明为人工撰写。
 */
(function (root) {
  const T = (id, es, zh, pos, scene, sceneLabel, ex, exZh, note) =>
    ({ id, es, zh, pos, scene, sceneLabel, ex, exZh, note });

  root.TERMS = [
  T("hola", "hola", "你好", "感叹", "问候", "问候 · 打招呼", "Hola, ¿qué tal?", "你好，怎么样？", "最通用的招呼，任何时间、任何人。"),
  T("agua", "agua", "水", "名词", "日常", "日常 · 吃喝起居", "¿Me trae un vaso de agua?", "能给我一杯水吗？", "阴性名词：el agua 但说 mucha agua。"),
  T("d-nde", "dónde", "在哪里", "副词", "出行", "出行 · 问路交通", "¿Dónde está el baño?", "洗手间在哪里？", "问位置用 dónde está，问去哪用 adónde vas。"),
  T("cu-nto", "cuánto", "多少", "副词", "购物", "购物 · 付钱议价", "¿Cuánto cuesta?", "多少钱？", "问价格固定说法。问数量用 cuántos。"),
  T("ayuda", "ayuda", "帮助", "名词", "应急", "应急 · 需要帮忙", "Necesito ayuda.", "我需要帮助。", "动词 ayudar；求助喊 ¡Ayuda! "),
  T("hoy", "hoy", "今天", "副词", "时间", "时间 · 今天明天", "Hoy no trabajo.", "我今天不上班。", "不需要介词，直接说 hoy。"),
  T("buenos-d-as", "buenos días", "早上好", "短语", "问候", "问候 · 打招呼", "Buenos días, señora.", "早上好，女士。", "中午两点前用。día 是阳性，所以用 buenos。"),
  T("comer", "comer", "吃", "动词", "日常", "日常 · 吃喝起居", "¿Qué quieres comer?", "你想吃什么？", "「吃饭」一般用 comer，三餐各有专词（desayunar 等）。"),
  T("ba-o", "baño", "洗手间", "名词", "出行", "出行 · 问路交通", "¿Hay un baño cerca?", "附近有洗手间吗？", "西班牙说 aseo 或 servicio 也很常见。"),
  T("dinero", "dinero", "钱", "名词", "购物", "购物 · 付钱议价", "No tengo dinero.", "我没钱。", "不可数，不说 dineros。"),
  T("m-dico", "médico", "医生", "名词", "应急", "应急 · 需要帮忙", "Llame a un médico.", "请叫医生。", "阳性；「看医生」是 ir al médico。"),
  T("ma-ana", "mañana", "明天 / 早上", "名词", "时间", "时间 · 今天明天", "Hasta mañana.", "明天见。", "同形两义：明天、早上。看冠词和上下文分辨。"),
  T("buenas-noches", "buenas noches", "晚上好 / 晚安", "短语", "问候", "问候 · 打招呼", "Buenas noches, hasta mañana.", "晚安，明天见。", "见面时说「晚上好」，分开时说「晚安」，同一句。"),
  T("beber", "beber", "喝", "动词", "日常", "日常 · 吃喝起居", "No bebo alcohol.", "我不喝酒。", "日常口语里 tomar 更常用。"),
  T("calle", "calle", "街道", "名词", "出行", "出行 · 问路交通", "Vivo en esta calle.", "我住在这条街。", "阴性：la calle。"),
  T("caro", "caro", "贵的", "形容词", "购物", "购物 · 付钱议价", "Es muy caro.", "太贵了。", "反义 barato。跟名词时变化：una casa cara。"),
  T("enfermo", "enfermo", "生病的", "形容词", "应急", "应急 · 需要帮忙", "Estoy enfermo.", "我病了。", "女性说 enferma。"),
  T("ayer", "ayer", "昨天", "副词", "时间", "时间 · 今天明天", "Ayer llovió.", "昨天下雨了。", "配简单过去时，不配现在时。"),
  T("gracias", "gracias", "谢谢", "感叹", "问候", "问候 · 打招呼", "Muchas gracias por todo.", "非常感谢你做的这一切。", "加 muchas 表示「非常感谢」。"),
  T("pan", "pan", "面包", "名词", "日常", "日常 · 吃喝起居", "Pan con tomate, por favor.", "番茄面包，谢谢。", "餐厅要「一份面包」说 un pan。"),
  T("cerca", "cerca", "近 / 附近", "副词", "出行", "出行 · 问路交通", "El hotel está cerca.", "酒店很近。", "反义 lejos。"),
  T("barato", "barato", "便宜的", "形容词", "购物", "购物 · 付钱议价", "Es bastante barato.", "挺便宜的。", "还表示「廉价劣质」，要分语境。"),
  T("hospital", "hospital", "医院", "名词", "应急", "应急 · 需要帮忙", "¿Dónde está el hospital?", "医院在哪里？", "阳性，重音在最后：hospital。"),
  T("ahora", "ahora", "现在", "副词", "时间", "时间 · 今天明天", "Ahora no puedo.", "我现在不行。", "ahora mismo 是「就现在」。"),
  T("por-favor", "por favor", "请 / 麻烦你", "短语", "问候", "问候 · 打招呼", "Un café, por favor.", "麻烦来杯咖啡。", "放句尾。西语里不加这个会显得生硬。"),
  T("caf", "café", "咖啡", "名词", "日常", "日常 · 吃喝起居", "Un café con leche.", "一杯拿铁。", "café solo 是浓缩，café con leche 是加奶。"),
  T("lejos", "lejos", "远", "副词", "出行", "出行 · 问路交通", "¿Está muy lejos?", "很远吗？", "常用搭配：lejos de aquí（离这儿远）。"),
  T("tarjeta", "tarjeta", "卡 / 银行卡", "名词", "购物", "购物 · 付钱议价", "¿Puedo pagar con tarjeta?", "可以刷卡吗？", "tarjeta de crédito 信用卡。"),
  T("no-entiendo", "no entiendo", "我不懂", "短语", "应急", "应急 · 需要帮忙", "No entiendo, más despacio, por favor.", "我不懂，请慢一点。", "旅游时最有用的句子之一。"),
  T("siempre", "siempre", "总是", "副词", "时间", "时间 · 今天明天", "Siempre llega tarde.", "他总迟到。", "反义 nunca。"),
  T("adi-s", "adiós", "再见", "感叹", "问候", "问候 · 打招呼", "Adiós, nos vemos.", "再见，回头见。", "正式些；朋友间更常说 hasta luego。"),
  T("casa", "casa", "家 / 房子", "名词", "日常", "日常 · 吃喝起居", "Voy a casa.", "我回家。", "a casa 不加冠词，表示「回自己家」。"),
  T("izquierda", "izquierda", "左边", "名词", "出行", "出行 · 问路交通", "Gira a la izquierda.", "向左转。", "阴性；右边是 derecha。"),
  T("tienda", "tienda", "商店", "名词", "购物", "购物 · 付钱议价", "La tienda abre a las diez.", "商店十点开门。", "阴性；店面小摊叫 puesto。"),
  T("hablar", "hablar", "说 / 讲", "动词", "应急", "应急 · 需要帮忙", "¿Habla inglés?", "您说英语吗？", "hablo 是我说，habla 是他说 / 您说。"),
  T("nunca", "nunca", "从不", "副词", "时间", "时间 · 今天明天", "Nunca he estado allí.", "我从没去过那儿。", "否定句里 nunca 前不再加 no。"),
  T("hasta-luego", "hasta luego", "回头见", "短语", "问候", "问候 · 打招呼", "Hasta luego, cuídate.", "回头见，保重。", "不是「待会儿见」的严格意思，就是随口告别。"),
  T("dormir", "dormir", "睡觉", "动词", "日常", "日常 · 吃喝起居", "Necesito dormir.", "我需要睡觉。", "不规则动词：duermo、durmió。"),
  T("derecha", "derecha", "右边", "名词", "出行", "出行 · 问路交通", "La farmacia está a la derecha.", "药房在右边。", "a la derecha 是固定搭配，不要漏冠词。"),
  T("perd-n", "perdón", "对不起 / 劳驾", "名词", "问候", "问候 · 打招呼", "Perdón, ¿tiene un minuto?", "劳驾，您有空吗？", "既能道歉也能插话，比 lo siento 轻。"),
  T("trabajo", "trabajo", "工作", "名词", "日常", "日常 · 吃喝起居", "Voy al trabajo.", "我去上班。", "阳性。动词 trabajar 同源。"),
  T("billete", "billete", "票", "名词", "出行", "出行 · 问路交通", "Quiero un billete de ida.", "我要一张单程票。", "ida 单程，ida y vuelta 往返。"),
  ];
})(typeof window !== 'undefined' ? window : globalThis);
