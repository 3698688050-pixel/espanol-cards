"""AI 初稿 · 收尾：补足 1000 条。
格式：(scene, es, zh, pos, ex, exZh, note)
此文件由 tools/fill.py 生成，人工复核时优先看这里。
"""

DATA = [
("daily", "el grifo", "水龙头", "名词", "El grifo de la cocina sigue goteando, hay que avisar al casero.", "厨房水龙头还在滴水，得告诉房东。", "阳性；「关紧水龙头」cerrar el grifo，租房常见话题。"),
("food", "el pan rallado", "面包糠", "短语", "Para las albóndigas necesito pan rallado y huevo.", "做肉丸我需要面包糠和鸡蛋。", "rallado 阳性配 pan；「擦丝」rallar，同一词根。"),
("travel", "el paseo marítimo", "海滨大道", "短语", "Cenamos en un bar del paseo marítimo.", "我们在海滨大道一家酒吧吃的晚饭。", "paseo 阳性，marítimo 修饰；西班牙海滨城市标配。"),
("shopping", "la bolsa de tela", "布袋", "短语", "Llevo una bolsa de tela porque el plástico se paga.", "我带布袋，塑料袋要付钱。", "tela 阴性；西班牙超市塑料袋要收费，这个说法很实用。"),
("emergency", "la quemadura de sol", "晒伤", "短语", "Me ha dado una quemadura de sol en la espalda.", "我背上晒伤了。", "quemadura 阴性，de sol 修饰；「防晒霜」crema solar。"),
("social", "el primo hermano", "亲表兄弟", "短语", "Mi primo hermano vive a dos calles de aquí.", "我亲表弟住在这两条街外。", "primo hermano 表示「亲的」堂表兄弟，不是普通 primo。"),
("daily", "la persiana", "卷帘", "名词", "Baja la persiana, que entra mucha luz.", "把卷帘放下来，光太足了。", "阴性；西班牙房子几乎都装 persiana，放下来用 bajar。"),
("time", "el fin de semana largo", "长周末", "短语", "Aprovechamos el fin de semana largo para subir a la montaña.", "我们利用长周末上山。", "largo 阳性配 fin；西班牙常把假期「架桥」成连休。"),
("daily", "el pañal", "尿布", "名词", "Se ha acabado el pañal, hay que comprar esta tarde.", "尿布用完了，下午得去买。", "阳性，复数 pañales；西班牙说 pañal，拉美也说同一词。"),
("time", "el reloj de pared", "挂钟", "短语", "El reloj de pared está parado, hay que cambiar la pila.", "挂钟停了，得换电池。", "reloj 阳性；de pared 表示「挂墙的」，pila 是电池。"),
("travel", "el carril bici", "自行车道", "短语", "Ve por el carril bici, es más seguro que la calle.", "走自行车道，比马路安全。", "carril 阳性；西班牙城市新修了很多 carril bici。"),
("shopping", "la bolsa de papel", "纸袋", "短语", "¿Me lo pone en una bolsa de papel, por favor?", "能给我装纸袋里吗？", "papel 阳性；纸袋不收钱时西班牙店员会问 ¿con bolsa?。"),
("daily", "el edificio", "楼房", "名词", "El edificio tiene seis plantas y no hay ascensor.", "这楼六层，还没电梯。", "阳性；「楼层」planta（阴性），「楼」edificio（阳性），两个别混。"),
("social", "la personalidad", "个性", "名词", "Tiene mucha personalidad y nunca pasa desapercibido.", "他很有个性，从不被人忽视。", "阴性，-dad 结尾重音在最后；形容人用 tener personalidad。"),
]
