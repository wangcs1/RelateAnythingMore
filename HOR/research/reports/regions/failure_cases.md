# 全组失败关系逐条审计

以下清单覆盖全部500张固定样本中未命中Top-50的人相关PSG关系。端点来源和候选框编号来自对应组实际输入。完整结构化文件见 `failure_cases.json`。

## A_fasterrcnn_thing

未命中745条。

|序号|索引|图片|GT主语|谓词|GT宾语|失败阶段|匹配主语候选|匹配宾语候选|
|---:|---:|---|---|---|---|---|---|---|
|6|295|2326503.jpg|0:person|on|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|6|295|2326503.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|6|295|2326503.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|7|1675|2393584.jpg|0:person|in|2:tv|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:tv[fasterrcnn_thing]fasterrcnn:000000|
|10|553|2339606.jpg|0:person|running on|16:dirt|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|10|553|2339606.jpg|1:person|standing on|16:dirt|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|10|553|2339606.jpg|4:person|standing on|12:playingfield|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|10|553|2339606.jpg|6:person|wearing|9:baseball glove|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|16|1466|2384291.jpg|0:person|on|20:pavement|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|16|1466|2384291.jpg|2:person|holding|21:paper|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|16|1466|2384291.jpg|3:person|walking on|20:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|16|1466|2384291.jpg|4:person|on|20:pavement|endpoint_missing_or_wrong_class|18:person[fasterrcnn_thing]fasterrcnn:000018||
|18|1983|2409607.jpg|0:person|sitting on|1:horse|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:horse[fasterrcnn_thing]fasterrcnn:000000|
|18|1983|2409607.jpg|0:person|over|5:grass|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|21|411|2332726.jpg|0:person|walking on|8:sand|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|21|411|2332726.jpg|3:person|looking at|5:kite|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:kite[fasterrcnn_thing]fasterrcnn:000005|
|21|411|2332726.jpg|3:person|playing|5:kite|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:kite[fasterrcnn_thing]fasterrcnn:000005|
|21|411|2332726.jpg|3:person|wearing|8:sand|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|22|129|2317125.jpg|2:person|walking on|11:road|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|22|129|2317125.jpg|4:person|standing on|11:road|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|22|129|2317125.jpg|9:house|beside|0:person|endpoint_missing_or_wrong_class||2:person[fasterrcnn_thing]fasterrcnn:000002|
|23|1055|2363004.jpg|0:person|holding|12:handbag|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|6:handbag[fasterrcnn_thing]fasterrcnn:000006|
|23|1055|2363004.jpg|2:person|walking on|21:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|23|1055|2363004.jpg|3:person|walking on|21:pavement|endpoint_missing_or_wrong_class|10:person[fasterrcnn_thing]fasterrcnn:000010||
|23|1055|2363004.jpg|7:person|walking on|21:pavement|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|23|1055|2363004.jpg|8:person|walking on|21:pavement|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|23|1055|2363004.jpg|10:train|beside|8:person|rank_below50|3:train[fasterrcnn_thing]fasterrcnn:000003|1:person[fasterrcnn_thing]fasterrcnn:000001|
|24|1712|2395918.jpg|0:person|crossing|5:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|24|1712|2395918.jpg|1:person|sitting on|5:pavement|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|24|1712|2395918.jpg|1:person|beside|6:grass|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|24|1712|2395918.jpg|2:skateboard|attached to|0:person|wrong_predicate|2:skateboard[fasterrcnn_thing]fasterrcnn:000002|0:person[fasterrcnn_thing]fasterrcnn:000000|
|26|892|2355904.jpg|0:person|touching|10:table|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|27|2018|2411180.jpg|0:person|standing on|6:railroad|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|28|164|2319298.jpg|0:person|driving|1:car|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|0:car[fasterrcnn_thing]fasterrcnn:000000|
|29|81|2315729.jpg|2:person|slicing|15:cake|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|17:cake[fasterrcnn_thing]fasterrcnn:000017|
|29|81|2315729.jpg|3:person|attached to|4:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:person[fasterrcnn_thing]fasterrcnn:000002|
|29|81|2315729.jpg|6:person|attached to|2:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|33|1896|2405341.jpg|0:person|holding|1:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|35|1326|2377788.jpg|0:person|feeding|3:cow|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000; 17:person[fasterrcnn_thing]fasterrcnn:000017|5:cow[fasterrcnn_thing]fasterrcnn:000005|
|35|1326|2377788.jpg|6:cow|in front of|1:person|rank_below50|4:cow[fasterrcnn_thing]fasterrcnn:000004; 16:cow[fasterrcnn_thing]fasterrcnn:000016|0:person[fasterrcnn_thing]fasterrcnn:000000; 3:person[fasterrcnn_thing]fasterrcnn:000003|
|36|922|2357107.jpg|1:person|in|9:boat|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|1:boat[fasterrcnn_thing]fasterrcnn:000001|
|36|922|2357107.jpg|4:person|walking on|14:platform|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|38|1914|2406339.jpg|0:person|beside|3:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002; 6:person[fasterrcnn_thing]fasterrcnn:000006|2:person[fasterrcnn_thing]fasterrcnn:000002|
|38|1914|2406339.jpg|0:person|looking at|22:playingfield|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002; 6:person[fasterrcnn_thing]fasterrcnn:000006||
|38|1914|2406339.jpg|2:person|looking at|22:playingfield|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|38|1914|2406339.jpg|2:person|attached to|26:wall|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|40|208|2321715.jpg|0:person|on|7:motorcycle|endpoint_missing_or_wrong_class||8:motorcycle[fasterrcnn_thing]fasterrcnn:000008|
|40|208|2321715.jpg|0:person|riding|7:motorcycle|endpoint_missing_or_wrong_class||8:motorcycle[fasterrcnn_thing]fasterrcnn:000008|
|40|208|2321715.jpg|3:person|exiting|12:tent|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|40|208|2321715.jpg|3:person|walking on|16:floor|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|41|1485|2385230.jpg|4:wall-wood|beside|0:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|44|489|2336251.jpg|0:person|sitting on|9:pavement|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|44|489|2336251.jpg|1:person|talking to|0:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|44|489|2336251.jpg|1:person|sitting on|9:pavement|endpoint_missing_or_wrong_class|||
|44|489|2336251.jpg|2:person|sitting on|9:pavement|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|44|489|2336251.jpg|3:person|playing|6:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:skateboard[fasterrcnn_thing]fasterrcnn:000003|
|44|489|2336251.jpg|3:person|jumping from|9:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|46|674|2345802.jpg|0:person|sitting on|2:chair|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|46|674|2345802.jpg|0:person|in front of|3:counter|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|51|1507|2386227.jpg|1:person|in|2:tv|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|0:tv[fasterrcnn_thing]fasterrcnn:000000|
|52|1139|2367625.jpg|0:person|in front of|3:oven|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:oven[fasterrcnn_thing]fasterrcnn:000001|
|53|1627|2391314.jpg|0:person|standing on|1:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skis[fasterrcnn_thing]fasterrcnn:000001|
|53|1627|2391314.jpg|0:person|beside|3:tree|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|54|237|2323211.jpg|1:person|on|17:grass|endpoint_missing_or_wrong_class|9:person[fasterrcnn_thing]fasterrcnn:000009||
|54|237|2323211.jpg|3:person|on|17:grass|endpoint_missing_or_wrong_class|11:person[fasterrcnn_thing]fasterrcnn:000011||
|54|237|2323211.jpg|5:person|over|1:person|wrong_predicate|7:person[fasterrcnn_thing]fasterrcnn:000007|9:person[fasterrcnn_thing]fasterrcnn:000009|
|54|237|2323211.jpg|5:person|over|8:person|wrong_predicate|7:person[fasterrcnn_thing]fasterrcnn:000007|6:person[fasterrcnn_thing]fasterrcnn:000006|
|54|237|2323211.jpg|5:person|on|17:grass|endpoint_missing_or_wrong_class|7:person[fasterrcnn_thing]fasterrcnn:000007||
|54|237|2323211.jpg|5:person|jumping from|17:grass|endpoint_missing_or_wrong_class|7:person[fasterrcnn_thing]fasterrcnn:000007||
|54|237|2323211.jpg|8:person|on|17:grass|endpoint_missing_or_wrong_class|6:person[fasterrcnn_thing]fasterrcnn:000006||
|54|237|2323211.jpg|11:person|standing on|17:grass|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|55|166|2319395.jpg|0:person|walking on|6:road|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|55|166|2319395.jpg|1:person|standing on|6:road|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|57|327|2328174.jpg|0:person|in front of|1:car|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:car[fasterrcnn_thing]fasterrcnn:000001|
|57|327|2328174.jpg|0:person|picking|2:umbrella|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:umbrella[fasterrcnn_thing]fasterrcnn:000003|
|57|327|2328174.jpg|0:person|in front of|3:potted plant|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:potted plant[fasterrcnn_thing]fasterrcnn:000002|
|57|327|2328174.jpg|0:person|standing on|6:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|58|617|2343155.jpg|0:person|throwing|3:sports ball|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:sports ball[fasterrcnn_thing]fasterrcnn:000002|
|58|617|2343155.jpg|0:person|about to hit|3:sports ball|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:sports ball[fasterrcnn_thing]fasterrcnn:000002|
|58|617|2343155.jpg|0:person|standing on|6:playingfield|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|60|2159|498242.jpg|0:person|beside|9:person|rank_below50|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|60|2159|498242.jpg|0:person|looking at|9:person|rank_below50|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|60|2159|498242.jpg|1:person|beside|0:person|rank_below50|3:person[fasterrcnn_thing]fasterrcnn:000003|1:person[fasterrcnn_thing]fasterrcnn:000001|
|60|2159|498242.jpg|1:person|looking at|9:person|rank_below50|3:person[fasterrcnn_thing]fasterrcnn:000003|0:person[fasterrcnn_thing]fasterrcnn:000000|
|60|2159|498242.jpg|2:person|standing on|14:pavement|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|60|2159|498242.jpg|3:person|looking at|1:person|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|3:person[fasterrcnn_thing]fasterrcnn:000003|
|60|2159|498242.jpg|3:person|beside|8:person|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|2:person[fasterrcnn_thing]fasterrcnn:000002|
|60|2159|498242.jpg|6:person|beside|4:person|wrong_predicate|14:person[fasterrcnn_thing]fasterrcnn:000014|12:person[fasterrcnn_thing]fasterrcnn:000012|
|60|2159|498242.jpg|8:person|beside|5:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|7:person[fasterrcnn_thing]fasterrcnn:000007|
|60|2159|498242.jpg|8:person|attached to|5:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|7:person[fasterrcnn_thing]fasterrcnn:000007|
|60|2159|498242.jpg|9:person|looking at|0:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:person[fasterrcnn_thing]fasterrcnn:000001|
|61|1219|2371806.jpg|0:person|running on|2:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|63|1445|2383111.jpg|1:person|riding|7:horse|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|65|915|2356824.jpg|0:person|walking on|18:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|66|749|2349334.jpg|1:person|looking at|4:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|66|749|2349334.jpg|2:person|eating|19:pizza|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002; 21:person[fasterrcnn_thing]fasterrcnn:000021||
|66|749|2349334.jpg|6:person|talking to|5:person|rank_below50|4:person[fasterrcnn_thing]fasterrcnn:000004|9:person[fasterrcnn_thing]fasterrcnn:000009|
|66|749|2349334.jpg|23:ceiling|on|4:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|68|1598|2390200.jpg|0:person|swinging|6:remote|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|8:remote[fasterrcnn_thing]fasterrcnn:000008|
|68|1598|2390200.jpg|0:person|holding|9:remote|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|68|1598|2390200.jpg|1:person|holding|3:potted plant|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|68|1598|2390200.jpg|1:person|swinging|8:remote|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|4:remote[fasterrcnn_thing]fasterrcnn:000004|
|68|1598|2390200.jpg|1:person|in front of|16:table|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|70|714|2347722.jpg|0:person|attached to|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|70|714|2347722.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|70|714|2347722.jpg|0:person|touching|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|70|714|2347722.jpg|0:person|looking at|2:sea|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|71|10|1159449.jpg|1:person|looking at|17:sports ball|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|71|10|1159449.jpg|1:person|standing on|23:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|71|10|1159449.jpg|8:person|running on|23:playingfield|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|72|841|2353618.jpg|1:person|standing on|2:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:skis[fasterrcnn_thing]fasterrcnn:000002|
|72|841|2353618.jpg|1:person|on|3:snow|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|75|1505|2386156.jpg|0:person|driving|2:car|wrong_predicate|10:person[fasterrcnn_thing]fasterrcnn:000010|0:car[fasterrcnn_thing]fasterrcnn:000000|
|78|910|2356736.jpg|0:person|walking on|13:pavement|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|81|1886|2404565.jpg|0:person|looking at|3:surfboard|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|7:surfboard[fasterrcnn_thing]fasterrcnn:000007|
|81|1886|2404565.jpg|0:person|standing on|17:pavement|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|82|1497|2385717.jpg|0:person|over|3:pavement|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|83|2176|713850.jpg|0:person|in|5:window|endpoint_missing_or_wrong_class|||
|86|1001|2360816.jpg|1:person|riding|13:bicycle|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|22:bicycle[fasterrcnn_thing]fasterrcnn:000022|
|86|1001|2360816.jpg|5:person|riding|11:bicycle|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|7:bicycle[fasterrcnn_thing]fasterrcnn:000007|
|86|1001|2360816.jpg|10:person|riding|14:bicycle|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|12:bicycle[fasterrcnn_thing]fasterrcnn:000012|
|87|852|2354099.jpg|3:person|crossing|36:pavement|endpoint_missing_or_wrong_class|17:person[fasterrcnn_thing]fasterrcnn:000017||
|87|852|2354099.jpg|9:person|crossing|36:pavement|endpoint_missing_or_wrong_class|21:person[fasterrcnn_thing]fasterrcnn:000021||
|87|852|2354099.jpg|11:person|standing on|34:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|9:skateboard[fasterrcnn_thing]fasterrcnn:000009|
|87|852|2354099.jpg|37:building|beside|11:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|89|813|2352072.jpg|0:person|in front of|3:tree|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|89|813|2352072.jpg|4:sky|over|0:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|91|926|2357328.jpg|0:person|standing on|5:grass|endpoint_missing_or_wrong_class|||
|91|926|2357328.jpg|1:person|standing on|5:grass|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|91|926|2357328.jpg|2:person|holding|3:baseball bat|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:baseball bat[fasterrcnn_thing]fasterrcnn:000002|
|91|926|2357328.jpg|2:person|standing on|5:grass|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|92|1004|2360919.jpg|0:person|in front of|3:book|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|93|227|2322480.jpg|0:person|looking at|1:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|93|227|2322480.jpg|1:person|chasing|2:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:sports ball[fasterrcnn_thing]fasterrcnn:000002|
|93|227|2322480.jpg|1:person|playing|2:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:sports ball[fasterrcnn_thing]fasterrcnn:000002|
|93|227|2322480.jpg|2:sports ball|in front of|1:person|wrong_predicate|2:sports ball[fasterrcnn_thing]fasterrcnn:000002|0:person[fasterrcnn_thing]fasterrcnn:000000|
|95|649|2344605.jpg|0:person|wearing|7:tie|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|95|649|2344605.jpg|0:person|touching|12:laptop|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:laptop[fasterrcnn_thing]fasterrcnn:000002|
|95|649|2344605.jpg|12:laptop|in front of|0:person|wrong_predicate|2:laptop[fasterrcnn_thing]fasterrcnn:000002|0:person[fasterrcnn_thing]fasterrcnn:000000|
|100|1841|2402294.jpg|1:person|driving|6:bus|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|0:bus[fasterrcnn_thing]fasterrcnn:000000|
|101|1796|2400414.jpg|0:person|standing on|6:grass|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|101|1796|2400414.jpg|1:person|playing with|5:sheep|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:sheep[fasterrcnn_thing]fasterrcnn:000003|
|101|1796|2400414.jpg|1:person|touching|5:sheep|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:sheep[fasterrcnn_thing]fasterrcnn:000003|
|101|1796|2400414.jpg|3:person|pulling|4:sheep|endpoint_missing_or_wrong_class||2:sheep[fasterrcnn_thing]fasterrcnn:000002|
|101|1796|2400414.jpg|5:sheep|playing with|1:person|wrong_predicate|3:sheep[fasterrcnn_thing]fasterrcnn:000003|0:person[fasterrcnn_thing]fasterrcnn:000000|
|103|989|2360368.jpg|2:person|standing on|12:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|103|989|2360368.jpg|2:person|in front of|14:dirt|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|103|989|2360368.jpg|4:bicycle|beside|2:person|rank_below50|2:bicycle[fasterrcnn_thing]fasterrcnn:000002|0:person[fasterrcnn_thing]fasterrcnn:000000|
|104|1795|2400390.jpg|10:person|beside|6:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:person[fasterrcnn_thing]fasterrcnn:000003|
|105|1023|2361799.jpg|0:person|looking at|1:bear|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|105|1023|2361799.jpg|0:person|in front of|3:tree|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|106|868|2354820.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|106|868|2354820.jpg|0:person|in front of|2:tree|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|106|868|2354820.jpg|0:person|standing on|4:floor|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|110|979|2359868.jpg|0:person|in|2:train|endpoint_missing_or_wrong_class||0:train[fasterrcnn_thing]fasterrcnn:000000|
|110|979|2359868.jpg|1:person|in|2:train|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|0:train[fasterrcnn_thing]fasterrcnn:000000|
|119|1534|2387240.jpg|4:person|in front of|13:person|endpoint_missing_or_wrong_class|9:person[fasterrcnn_thing]fasterrcnn:000009||
|119|1534|2387240.jpg|9:person|standing on|15:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|121|1300|2376047.jpg|0:person|jumping from|4:playingfield|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|121|1300|2376047.jpg|1:person|chasing|2:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|
|121|1300|2376047.jpg|1:person|playing|2:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|
|121|1300|2376047.jpg|1:person|jumping from|4:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|122|1729|2396723.jpg|0:person|sitting on|4:couch|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|122|1729|2396723.jpg|2:cat|lying on|0:person|wrong_predicate|0:cat[fasterrcnn_thing]fasterrcnn:000000|3:person[fasterrcnn_thing]fasterrcnn:000003|
|122|1729|2396723.jpg|5:pillow|in front of|0:person|endpoint_missing_or_wrong_class||3:person[fasterrcnn_thing]fasterrcnn:000003|
|123|1099|2365844.jpg|10:person|beside|12:person|rank_below50|12:person[fasterrcnn_thing]fasterrcnn:000012|3:person[fasterrcnn_thing]fasterrcnn:000003|
|125|1673|2393510.jpg|0:person|playing with|2:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:person[fasterrcnn_thing]fasterrcnn:000000|
|125|1673|2393510.jpg|1:person|walking on|6:grass|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|125|1673|2393510.jpg|2:person|throwing|3:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:frisbee[fasterrcnn_thing]fasterrcnn:000003|
|126|787|2351136.jpg|0:person|on back of|3:horse|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:horse[fasterrcnn_thing]fasterrcnn:000000|
|127|1293|2375622.jpg|1:person|looking at|2:laptop|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|0:laptop[fasterrcnn_thing]fasterrcnn:000000|
|127|1293|2375622.jpg|1:person|touching|2:laptop|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|0:laptop[fasterrcnn_thing]fasterrcnn:000000|
|128|323|2328089.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|128|323|2328089.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|128|323|2328089.jpg|0:person|in front of|5:building|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|130|2105|2416163.jpg|9:person|sitting on|33:sand|endpoint_missing_or_wrong_class|||
|130|2105|2416163.jpg|11:person|sitting on|33:sand|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|130|2105|2416163.jpg|12:person|sitting on|33:sand|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|131|1764|2398216.jpg|0:person|in front of|1:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|131|1764|2398216.jpg|0:person|standing on|11:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|131|1764|2398216.jpg|2:person|standing on|11:pavement|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|131|1764|2398216.jpg|3:person|standing on|11:pavement|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|134|406|2332593.jpg|0:person|in front of|8:wall-stone|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|134|406|2332593.jpg|0:person|on|12:grass|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|134|406|2332593.jpg|1:person|in front of|0:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|135|1163|2368707.jpg|0:person|running on|9:dirt|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003; 4:person[fasterrcnn_thing]fasterrcnn:000004||
|135|1163|2368707.jpg|1:person|looking at|4:frisbee|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|
|135|1163|2368707.jpg|1:person|running on|9:dirt|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|135|1163|2368707.jpg|2:person|running on|9:dirt|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|135|1163|2368707.jpg|3:person|looking at|4:frisbee|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|
|135|1163|2368707.jpg|3:person|throwing|4:frisbee|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|
|135|1163|2368707.jpg|4:frisbee|over|1:person|rank_below50|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|3:person[fasterrcnn_thing]fasterrcnn:000003|
|136|1375|2379887.jpg|0:person|in front of|5:mountain|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|140|554|2339715.jpg|0:person|holding|14:spoon|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|140|554|2339715.jpg|0:person|eating|14:spoon|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|141|1697|2394828.jpg|0:person|over|3:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|141|1697|2394828.jpg|0:person|jumping from|3:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|141|1697|2394828.jpg|0:person|in front of|4:grass|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|141|1697|2394828.jpg|0:person|in front of|5:rock|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|144|1442|2383041.jpg|3:person|wearing|18:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|20:surfboard[fasterrcnn_thing]fasterrcnn:000020|
|144|1442|2383041.jpg|3:person|flying over|21:sea|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|144|1442|2383041.jpg|4:person|pulling|13:kite|endpoint_missing_or_wrong_class||5:kite[fasterrcnn_thing]fasterrcnn:000005|
|145|23|1159863.jpg|0:person|on|7:road|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|149|1526|2387025.jpg|6:person|carrying|21:handbag|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|32:handbag[fasterrcnn_thing]fasterrcnn:000032|
|149|1526|2387025.jpg|8:person|wearing|24:cardboard|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|152|1986|2409643.jpg|0:person|holding|5:handbag|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|5:handbag[fasterrcnn_thing]fasterrcnn:000005|
|152|1986|2409643.jpg|0:person|on|7:pavement|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|152|1986|2409643.jpg|1:person|carrying|4:handbag|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|4:handbag[fasterrcnn_thing]fasterrcnn:000004|
|153|1695|2394762.jpg|1:person|attached to|16:grass|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|153|1695|2394762.jpg|3:person|looking at|12:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000; 10:person[fasterrcnn_thing]fasterrcnn:000010|8:sports ball[fasterrcnn_thing]fasterrcnn:000008|
|153|1695|2394762.jpg|3:person|running on|13:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000; 10:person[fasterrcnn_thing]fasterrcnn:000010||
|153|1695|2394762.jpg|5:person|pulling|6:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002; 5:person[fasterrcnn_thing]fasterrcnn:000005|2:person[fasterrcnn_thing]fasterrcnn:000002|
|153|1695|2394762.jpg|5:person|jumping from|13:playingfield|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002; 5:person[fasterrcnn_thing]fasterrcnn:000005||
|154|47|1592228.jpg|1:person|standing on|17:platform|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|154|47|1592228.jpg|5:person|carrying|12:handbag|endpoint_missing_or_wrong_class|13:person[fasterrcnn_thing]fasterrcnn:000013||
|154|47|1592228.jpg|5:person|standing on|22:pavement|endpoint_missing_or_wrong_class|13:person[fasterrcnn_thing]fasterrcnn:000013||
|156|1813|2401171.jpg|9:person|walking on|25:pavement|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|157|1286|2375241.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|157|1286|2375241.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|157|1286|2375241.jpg|0:person|looking at|2:sea|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|158|975|2359797.jpg|3:person|carrying|14:backpack|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|7:backpack[fasterrcnn_thing]fasterrcnn:000007|
|158|975|2359797.jpg|8:person|carrying|15:backpack|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|158|975|2359797.jpg|14:backpack|on back of|3:person|wrong_predicate|7:backpack[fasterrcnn_thing]fasterrcnn:000007|3:person[fasterrcnn_thing]fasterrcnn:000003|
|161|859|2354354.jpg|0:person|holding|10:umbrella|endpoint_missing_or_wrong_class||9:umbrella[fasterrcnn_thing]fasterrcnn:000009|
|161|859|2354354.jpg|3:person|running on|16:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|161|859|2354354.jpg|4:person|holding|12:umbrella|rank_below50|4:person[fasterrcnn_thing]fasterrcnn:000004|10:umbrella[fasterrcnn_thing]fasterrcnn:000010|
|161|859|2354354.jpg|4:person|on|16:pavement|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|161|859|2354354.jpg|5:person|walking on|16:pavement|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|165|2125|2416928.jpg|9:person|leaning on|15:truck|endpoint_missing_or_wrong_class||11:truck[fasterrcnn_thing]fasterrcnn:000011|
|165|2125|2416928.jpg|10:person|wearing|16:tree|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|165|2125|2416928.jpg|13:person|standing on|15:truck|endpoint_missing_or_wrong_class||11:truck[fasterrcnn_thing]fasterrcnn:000011|
|166|955|2358756.jpg|0:person|throwing|1:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|
|166|955|2358756.jpg|0:person|holding|2:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:frisbee[fasterrcnn_thing]fasterrcnn:000002|
|166|955|2358756.jpg|0:person|attached to|3:tree|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|166|955|2358756.jpg|0:person|standing on|4:dirt|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|167|2029|2411534.jpg|0:person|looking at|1:sports ball|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:sports ball[fasterrcnn_thing]fasterrcnn:000000|
|167|2029|2411534.jpg|0:person|about to hit|1:sports ball|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:sports ball[fasterrcnn_thing]fasterrcnn:000000|
|167|2029|2411534.jpg|0:person|standing on|3:playingfield|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|170|658|2345182.jpg|2:person|standing on|22:grass|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|170|658|2345182.jpg|6:person|touching|15:kite|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|170|658|2345182.jpg|6:person|holding|18:bottle|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|170|658|2345182.jpg|6:person|holding|19:bottle|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|170|658|2345182.jpg|6:person|walking on|22:grass|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|170|658|2345182.jpg|7:person|in front of|10:person|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|2:person[fasterrcnn_thing]fasterrcnn:000002|
|170|658|2345182.jpg|10:person|beside|6:person|rank_below50|2:person[fasterrcnn_thing]fasterrcnn:000002|1:person[fasterrcnn_thing]fasterrcnn:000001|
|172|1608|2390659.jpg|0:person|lying on|34:rug|endpoint_missing_or_wrong_class|||
|172|1608|2390659.jpg|2:person|lying on|34:rug|endpoint_missing_or_wrong_class|||
|172|1608|2390659.jpg|8:person|standing on|29:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|173|417|2332914.jpg|0:person|standing on|8:pavement|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|173|417|2332914.jpg|0:person|in front of|9:building|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|175|1343|2378563.jpg|0:person|standing on|8:pavement|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|183|1866|2403494.jpg|12:person|standing on|18:skis|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|14:skis[fasterrcnn_thing]fasterrcnn:000014|
|184|325|2328153.jpg|1:person|standing on|6:building|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|184|325|2328153.jpg|2:elephant|in front of|0:person|wrong_predicate|0:elephant[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|185|15|1159597.jpg|0:person|guiding|5:horse|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:horse[fasterrcnn_thing]fasterrcnn:000000|
|188|1302|2376309.jpg|0:person|standing on|1:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skis[fasterrcnn_thing]fasterrcnn:000001|
|188|1302|2376309.jpg|0:person|playing|1:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skis[fasterrcnn_thing]fasterrcnn:000001|
|188|1302|2376309.jpg|0:person|looking at|2:snow|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|190|283|2326062.jpg|0:person|on|27:pavement|endpoint_missing_or_wrong_class|12:person[fasterrcnn_thing]fasterrcnn:000012||
|190|283|2326062.jpg|0:person|walking on|27:pavement|endpoint_missing_or_wrong_class|12:person[fasterrcnn_thing]fasterrcnn:000012||
|190|283|2326062.jpg|3:person|sitting on|13:bench|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|190|283|2326062.jpg|3:person|on|27:pavement|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|190|283|2326062.jpg|9:person|looking at|10:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|21:person[fasterrcnn_thing]fasterrcnn:000021|
|190|283|2326062.jpg|9:person|holding|17:handbag|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:handbag[fasterrcnn_thing]fasterrcnn:000005|
|190|283|2326062.jpg|9:person|walking on|27:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|190|283|2326062.jpg|12:person|on|27:pavement|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|190|283|2326062.jpg|21:handbag|hanging from|3:person|wrong_predicate|8:handbag[fasterrcnn_thing]fasterrcnn:000008|4:person[fasterrcnn_thing]fasterrcnn:000004|
|190|283|2326062.jpg|22:handbag|hanging from|9:person|wrong_predicate|13:handbag[fasterrcnn_thing]fasterrcnn:000013|0:person[fasterrcnn_thing]fasterrcnn:000000|
|190|283|2326062.jpg|28:paper|beside|3:person|endpoint_missing_or_wrong_class||4:person[fasterrcnn_thing]fasterrcnn:000004|
|192|2020|2411218.jpg|2:person|on|15:sand|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|194|1135|2367479.jpg|5:person|beside|3:person|rank_below50|1:person[fasterrcnn_thing]fasterrcnn:000001; 4:person[fasterrcnn_thing]fasterrcnn:000004|3:person[fasterrcnn_thing]fasterrcnn:000003|
|194|1135|2367479.jpg|5:person|looking at|3:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001; 4:person[fasterrcnn_thing]fasterrcnn:000004|3:person[fasterrcnn_thing]fasterrcnn:000003|
|194|1135|2367479.jpg|5:person|holding|7:handbag|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001; 4:person[fasterrcnn_thing]fasterrcnn:000004|9:handbag[fasterrcnn_thing]fasterrcnn:000009|
|194|1135|2367479.jpg|7:handbag|in front of|3:person|wrong_predicate|9:handbag[fasterrcnn_thing]fasterrcnn:000009|3:person[fasterrcnn_thing]fasterrcnn:000003|
|195|1382|2380359.jpg|0:person|walking on|27:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|195|1382|2380359.jpg|1:person|in front of|23:door|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|195|1382|2380359.jpg|1:person|in front of|25:ceiling|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|195|1382|2380359.jpg|2:person|sitting on|4:person|endpoint_missing_or_wrong_class||2:person[fasterrcnn_thing]fasterrcnn:000002|
|197|368|2330400.jpg|0:person|going down|4:snow|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|197|368|2330400.jpg|1:person|holding|2:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|4:skis[fasterrcnn_thing]fasterrcnn:000004|
|197|368|2330400.jpg|1:person|jumping over|4:snow|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|198|1076|2364558.jpg|0:person|about to hit|1:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:sports ball[fasterrcnn_thing]fasterrcnn:000001|
|198|1076|2364558.jpg|0:person|attached to|2:tennis racket|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:tennis racket[fasterrcnn_thing]fasterrcnn:000002|
|198|1076|2364558.jpg|0:person|standing on|3:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|198|1076|2364558.jpg|0:person|in front of|4:wall|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|201|970|2359437.jpg|0:person|picking|1:pizza|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:pizza[fasterrcnn_thing]fasterrcnn:000000|
|203|806|2351780.jpg|1:person|on|12:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|203|806|2351780.jpg|2:person|wearing|11:baseball glove|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|5:baseball glove[fasterrcnn_thing]fasterrcnn:000005|
|203|806|2351780.jpg|2:person|on|12:playingfield|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|203|806|2351780.jpg|3:person|about to hit|9:sports ball|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|203|806|2351780.jpg|3:person|holding|10:baseball bat|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|203|806|2351780.jpg|3:person|swinging|10:baseball bat|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|203|806|2351780.jpg|5:person|on|12:playingfield|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|206|1401|2381176.jpg|4:sky|over|1:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|207|1111|2366320.jpg|0:person|in front of|2:wall|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|210|105|2316316.jpg|1:person|holding|19:handbag|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|24:handbag[fasterrcnn_thing]fasterrcnn:000024|
|210|105|2316316.jpg|1:person|on|22:road|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|210|105|2316316.jpg|1:person|walking on|22:road|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|210|105|2316316.jpg|6:person|in front of|12:person|wrong_predicate|20:person[fasterrcnn_thing]fasterrcnn:000020|11:person[fasterrcnn_thing]fasterrcnn:000011|
|210|105|2316316.jpg|6:person|sitting on|17:motorcycle|wrong_predicate|20:person[fasterrcnn_thing]fasterrcnn:000020|2:motorcycle[fasterrcnn_thing]fasterrcnn:000002|
|210|105|2316316.jpg|11:person|riding|15:bicycle|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|210|105|2316316.jpg|12:person|riding|17:motorcycle|wrong_predicate|11:person[fasterrcnn_thing]fasterrcnn:000011|2:motorcycle[fasterrcnn_thing]fasterrcnn:000002|
|210|105|2316316.jpg|13:person|walking on|22:road|endpoint_missing_or_wrong_class|||
|210|105|2316316.jpg|25:sky|over|6:person|endpoint_missing_or_wrong_class||20:person[fasterrcnn_thing]fasterrcnn:000020|
|211|1563|2388324.jpg|0:person|in|10:tv|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|7:tv[fasterrcnn_thing]fasterrcnn:000007|
|211|1563|2388324.jpg|0:person|playing|10:tv|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|7:tv[fasterrcnn_thing]fasterrcnn:000007|
|211|1563|2388324.jpg|0:person|holding|11:remote|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|8:remote[fasterrcnn_thing]fasterrcnn:000008|
|213|1476|2384904.jpg|0:person|playing with|2:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:frisbee[fasterrcnn_thing]fasterrcnn:000002|
|213|1476|2384904.jpg|1:person|chasing|0:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|216|1890|2404890.jpg|0:person|in|2:train|endpoint_missing_or_wrong_class||3:train[fasterrcnn_thing]fasterrcnn:000003|
|216|1890|2404890.jpg|1:person|driving|2:train|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|3:train[fasterrcnn_thing]fasterrcnn:000003|
|219|316|2327752.jpg|0:person|walking on|15:pavement|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|225|1317|2377220.jpg|1:person|in|10:train|endpoint_missing_or_wrong_class||0:train[fasterrcnn_thing]fasterrcnn:000000|
|225|1317|2377220.jpg|3:person|driving|10:train|endpoint_missing_or_wrong_class||0:train[fasterrcnn_thing]fasterrcnn:000000|
|225|1317|2377220.jpg|6:person|in|10:train|endpoint_missing_or_wrong_class||0:train[fasterrcnn_thing]fasterrcnn:000000|
|225|1317|2377220.jpg|9:person|in|10:train|endpoint_missing_or_wrong_class||0:train[fasterrcnn_thing]fasterrcnn:000000|
|226|2126|2416964.jpg|0:person|picking|14:suitcase|endpoint_missing_or_wrong_class|11:person[fasterrcnn_thing]fasterrcnn:000011||
|227|1607|2390654.jpg|1:person|standing on|9:sand|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|227|1607|2390654.jpg|1:person|in front of|10:sea|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|227|1607|2390654.jpg|3:person|running on|9:sand|endpoint_missing_or_wrong_class|6:person[fasterrcnn_thing]fasterrcnn:000006||
|227|1607|2390654.jpg|4:person|playing with|5:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:person[fasterrcnn_thing]fasterrcnn:000002|
|228|2144|285721.jpg|0:person|holding|2:cell phone|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:cell phone[fasterrcnn_thing]fasterrcnn:000005|
|228|2144|285721.jpg|0:person|carrying|2:cell phone|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:cell phone[fasterrcnn_thing]fasterrcnn:000005|
|228|2144|285721.jpg|0:person|in front of|3:wall|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|228|2144|285721.jpg|0:person|leaning on|3:wall|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|229|1350|2378868.jpg|1:person|in|2:car|endpoint_missing_or_wrong_class||0:car[fasterrcnn_thing]fasterrcnn:000000|
|230|723|2348265.jpg|5:person|on|13:bridge|endpoint_missing_or_wrong_class|||
|230|723|2348265.jpg|6:person|over|14:river|endpoint_missing_or_wrong_class|||
|231|684|2346411.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|231|684|2346411.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|231|684|2346411.jpg|0:person|over|2:sea|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|231|684|2346411.jpg|0:person|looking at|2:sea|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|233|1337|2378360.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|233|1337|2378360.jpg|0:person|on|2:sea|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|233|1337|2378360.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|235|2050|2412773.jpg|0:person|on|1:surfboard|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|235|2050|2412773.jpg|0:person|attached to|1:surfboard|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|235|2050|2412773.jpg|0:person|standing on|1:surfboard|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|235|2050|2412773.jpg|0:person|playing|1:surfboard|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|235|2050|2412773.jpg|0:person|attached to|2:sea|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|235|2050|2412773.jpg|0:person|touching|2:sea|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|235|2050|2412773.jpg|0:person|in front of|3:rock|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|236|561|2340111.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|236|561|2340111.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|236|561|2340111.jpg|0:person|over|2:sea|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|243|1591|2389803.jpg|0:person|sitting on|9:boat|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:boat[fasterrcnn_thing]fasterrcnn:000000|
|243|1591|2389803.jpg|1:person|on|9:boat|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:boat[fasterrcnn_thing]fasterrcnn:000000|
|243|1591|2389803.jpg|1:person|sitting on|9:boat|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:boat[fasterrcnn_thing]fasterrcnn:000000|
|244|603|2342677.jpg|0:person|sitting on|1:bed|endpoint_missing_or_wrong_class||0:bed[fasterrcnn_thing]fasterrcnn:000000; 6:bed[fasterrcnn_thing]fasterrcnn:000006|
|244|603|2342677.jpg|0:person|looking at|2:laptop|endpoint_missing_or_wrong_class||3:laptop[fasterrcnn_thing]fasterrcnn:000003|
|244|603|2342677.jpg|0:person|beside|4:door|endpoint_missing_or_wrong_class|||
|244|603|2342677.jpg|0:person|holding|7:wall|endpoint_missing_or_wrong_class|||
|244|603|2342677.jpg|3:blanket|over|0:person|endpoint_missing_or_wrong_class|||
|244|603|2342677.jpg|7:wall|on back of|0:person|endpoint_missing_or_wrong_class|||
|247|1380|2380325.jpg|0:person|beside|2:car|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|247|1380|2380325.jpg|2:car|beside|0:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|249|520|2337500.jpg|0:person|driving|6:car|wrong_predicate|11:person[fasterrcnn_thing]fasterrcnn:000011; 15:person[fasterrcnn_thing]fasterrcnn:000015|0:car[fasterrcnn_thing]fasterrcnn:000000|
|251|1509|2386257.jpg|0:person|attached to|1:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|251|1509|2386257.jpg|0:person|playing with|2:teddy bear|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:teddy bear[fasterrcnn_thing]fasterrcnn:000002|
|251|1509|2386257.jpg|1:person|attached to|0:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:person[fasterrcnn_thing]fasterrcnn:000001|
|251|1509|2386257.jpg|1:person|attached to|2:teddy bear|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:teddy bear[fasterrcnn_thing]fasterrcnn:000002|
|251|1509|2386257.jpg|2:teddy bear|attached to|1:person|wrong_predicate|2:teddy bear[fasterrcnn_thing]fasterrcnn:000002|0:person[fasterrcnn_thing]fasterrcnn:000000|
|253|1589|2389680.jpg|0:person|beside|12:stairs|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|253|1589|2389680.jpg|0:person|beside|13:water|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|253|1589|2389680.jpg|2:person|looking at|11:cell phone|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|8:cell phone[fasterrcnn_thing]fasterrcnn:000008|
|253|1589|2389680.jpg|4:person|beside|0:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|5:person[fasterrcnn_thing]fasterrcnn:000005|
|253|1589|2389680.jpg|4:person|looking at|0:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|5:person[fasterrcnn_thing]fasterrcnn:000005|
|253|1589|2389680.jpg|4:person|beside|12:stairs|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|253|1589|2389680.jpg|4:person|beside|13:water|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|253|1589|2389680.jpg|10:handbag|beside|2:person|wrong_predicate|4:handbag[fasterrcnn_thing]fasterrcnn:000004|1:person[fasterrcnn_thing]fasterrcnn:000001|
|254|896|2356062.jpg|1:person|beside|25:flower|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|254|896|2356062.jpg|1:person|in front of|26:tree|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|254|896|2356062.jpg|5:person|walking on|28:grass|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|254|896|2356062.jpg|7:person|holding|22:teddy bear|endpoint_missing_or_wrong_class|7:person[fasterrcnn_thing]fasterrcnn:000007||
|254|896|2356062.jpg|8:person|walking on|28:grass|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|254|896|2356062.jpg|10:person|sitting on|24:blanket|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|258|388|2331571.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|258|388|2331571.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|258|388|2331571.jpg|0:person|on|2:sea|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|259|826|2352851.jpg|0:person|standing on|2:sand|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|259|826|2352851.jpg|0:person|beside|3:sea|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|259|826|2352851.jpg|0:person|looking at|3:sea|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|262|621|2343341.jpg|1:person|about to hit|4:sports ball|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|6:sports ball[fasterrcnn_thing]fasterrcnn:000006|
|262|621|2343341.jpg|1:person|standing on|11:dirt|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|263|2037|2412228.jpg|8:motorcycle|in front of|4:person|wrong_predicate|13:motorcycle[fasterrcnn_thing]fasterrcnn:000013|0:person[fasterrcnn_thing]fasterrcnn:000000|
|267|1327|2377789.jpg|12:backpack|beside|3:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|267|1327|2377789.jpg|13:handbag|beside|3:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|269|133|2317501.jpg|1:person|guiding|6:person|wrong_predicate|10:person[fasterrcnn_thing]fasterrcnn:000010|0:person[fasterrcnn_thing]fasterrcnn:000000|
|269|133|2317501.jpg|2:person|beside|0:person|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|7:person[fasterrcnn_thing]fasterrcnn:000007|
|269|133|2317501.jpg|2:person|holding|9:person|endpoints_collapsed_to_same_box|5:person[fasterrcnn_thing]fasterrcnn:000005|5:person[fasterrcnn_thing]fasterrcnn:000005|
|271|1757|2397709.jpg|0:person|playing|1:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:sports ball[fasterrcnn_thing]fasterrcnn:000001|
|271|1757|2397709.jpg|0:person|holding|2:tennis racket|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:tennis racket[fasterrcnn_thing]fasterrcnn:000002|
|271|1757|2397709.jpg|0:person|standing on|3:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|272|1688|2394464.jpg|0:person|sitting on|6:chair|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|276|1693|2394673.jpg|0:person|playing|1:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skis[fasterrcnn_thing]fasterrcnn:000001|
|276|1693|2394673.jpg|1:skis|attached to|0:person|wrong_predicate|1:skis[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|277|1237|2372495.jpg|0:person|holding|15:tennis racket|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|277|1237|2372495.jpg|0:person|standing on|26:playingfield|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|277|1237|2372495.jpg|3:person|looking at|0:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:person[fasterrcnn_thing]fasterrcnn:000001|
|277|1237|2372495.jpg|3:person|talking to|0:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:person[fasterrcnn_thing]fasterrcnn:000001|
|277|1237|2372495.jpg|3:person|holding|14:tennis racket|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:tennis racket[fasterrcnn_thing]fasterrcnn:000002|
|277|1237|2372495.jpg|7:person|beside|9:person|wrong_predicate|17:person[fasterrcnn_thing]fasterrcnn:000017|7:person[fasterrcnn_thing]fasterrcnn:000007|
|281|1203|2371154.jpg|0:person|on|8:snow|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|281|1203|2371154.jpg|1:person|playing|4:snowboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|7:snowboard[fasterrcnn_thing]fasterrcnn:000007|
|281|1203|2371154.jpg|3:person|standing on|5:snowboard|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|4:snowboard[fasterrcnn_thing]fasterrcnn:000004|
|283|673|2345745.jpg|0:person|looking at|3:person|rank_below50|0:person[fasterrcnn_thing]fasterrcnn:000000|10:person[fasterrcnn_thing]fasterrcnn:000010|
|283|673|2345745.jpg|1:person|looking at|3:person|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|10:person[fasterrcnn_thing]fasterrcnn:000010|
|283|673|2345745.jpg|2:person|looking at|3:person|rank_below50|3:person[fasterrcnn_thing]fasterrcnn:000003|10:person[fasterrcnn_thing]fasterrcnn:000010|
|287|2058|2413475.jpg|0:person|catching|1:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|
|287|2058|2413475.jpg|0:person|playing|1:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|
|287|2058|2413475.jpg|0:person|standing on|3:grass|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|292|551|2339515.jpg|0:person|looking at|14:river|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|292|551|2339515.jpg|2:person|looking at|8:cow|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|292|551|2339515.jpg|6:cow|looking at|0:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|293|495|2336518.jpg|2:person|holding|14:cell phone|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|293|495|2336518.jpg|2:person|looking at|14:cell phone|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|293|495|2336518.jpg|7:person|talking to|3:person|endpoint_missing_or_wrong_class|||
|293|495|2336518.jpg|8:person|sitting on|13:couch|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|293|495|2336518.jpg|8:person|looking at|15:table|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|296|1346|2378709.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|296|1346|2378709.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|301|1633|2391614.jpg|0:person|holding|7:food|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|301|1633|2391614.jpg|1:oven|in front of|0:person|wrong_predicate|2:oven[fasterrcnn_thing]fasterrcnn:000002|0:person[fasterrcnn_thing]fasterrcnn:000000|
|302|1396|2381002.jpg|3:person|standing on|19:pavement|endpoint_missing_or_wrong_class|12:person[fasterrcnn_thing]fasterrcnn:000012||
|302|1396|2381002.jpg|4:person|standing on|17:road|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|304|1427|2382463.jpg|0:person|sitting on|2:boat|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|3:boat[fasterrcnn_thing]fasterrcnn:000003|
|304|1427|2382463.jpg|1:person|standing on|2:boat|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|3:boat[fasterrcnn_thing]fasterrcnn:000003|
|304|1427|2382463.jpg|1:person|driving|2:boat|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|3:boat[fasterrcnn_thing]fasterrcnn:000003|
|304|1427|2382463.jpg|1:person|holding|3:cell phone|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|304|1427|2382463.jpg|1:person|wearing|4:sea|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|306|1259|2373413.jpg|0:person|leaning on|1:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|306|1259|2373413.jpg|0:person|on|3:road|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|306|1259|2373413.jpg|1:person|standing on|3:road|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|308|1185|2370070.jpg|1:person|talking to|3:person|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|19:person[fasterrcnn_thing]fasterrcnn:000019|
|308|1185|2370070.jpg|1:person|holding|20:backpack|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|26:backpack[fasterrcnn_thing]fasterrcnn:000026|
|308|1185|2370070.jpg|2:person|looking at|29:pavement|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|308|1185|2370070.jpg|4:person|looking at|29:pavement|endpoint_missing_or_wrong_class|6:person[fasterrcnn_thing]fasterrcnn:000006||
|308|1185|2370070.jpg|6:person|talking to|25:cell phone|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|308|1185|2370070.jpg|6:person|walking on|29:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|308|1185|2370070.jpg|7:person|standing on|29:pavement|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|312|52|1592452.jpg|6:person|in|10:person|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|4:person[fasterrcnn_thing]fasterrcnn:000004|
|312|52|1592452.jpg|7:person|wearing|10:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|4:person[fasterrcnn_thing]fasterrcnn:000004|
|312|52|1592452.jpg|8:person|walking on|18:pavement|endpoint_missing_or_wrong_class|7:person[fasterrcnn_thing]fasterrcnn:000007||
|315|1206|2371236.jpg|2:person|walking on|25:floor|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|315|1206|2371236.jpg|5:person|in front of|2:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:person[fasterrcnn_thing]fasterrcnn:000002|
|315|1206|2371236.jpg|5:person|beside|3:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|17:person[fasterrcnn_thing]fasterrcnn:000017; 35:person[fasterrcnn_thing]fasterrcnn:000035|
|315|1206|2371236.jpg|5:person|walking on|25:floor|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|315|1206|2371236.jpg|9:person|beside|0:person|wrong_predicate|10:person[fasterrcnn_thing]fasterrcnn:000010|8:person[fasterrcnn_thing]fasterrcnn:000008|
|315|1206|2371236.jpg|11:person|standing on|25:floor|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|315|1206|2371236.jpg|24:ceiling|over|11:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|321|49|1592294.jpg|1:person|crossing|38:road|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|321|49|1592294.jpg|3:person|standing on|38:road|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|321|49|1592294.jpg|8:person|walking on|7:person|rank_below50|16:person[fasterrcnn_thing]fasterrcnn:000016|8:person[fasterrcnn_thing]fasterrcnn:000008|
|321|49|1592294.jpg|8:person|looking at|15:bicycle|endpoint_missing_or_wrong_class|16:person[fasterrcnn_thing]fasterrcnn:000016||
|325|703|2347159.jpg|1:person|looking at|8:railroad|endpoint_missing_or_wrong_class|8:person[fasterrcnn_thing]fasterrcnn:000008||
|325|703|2347159.jpg|2:person|walking on|8:railroad|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|325|703|2347159.jpg|6:person|standing on|8:railroad|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|327|574|2340907.jpg|0:person|standing on|11:floor|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|327|574|2340907.jpg|2:person|playing|3:sports ball|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|328|2111|2416290.jpg|0:person|wearing|24:wall-wood|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|328|2111|2416290.jpg|2:person|holding|12:pizza|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|23:pizza[fasterrcnn_thing]fasterrcnn:000023|
|328|2111|2416290.jpg|2:person|wearing|24:wall-wood|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|328|2111|2416290.jpg|3:person|picking|19:cardboard|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|328|2111|2416290.jpg|3:person|wearing|23:towel|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|328|2111|2416290.jpg|6:person|looking at|1:person|wrong_predicate|7:person[fasterrcnn_thing]fasterrcnn:000007|4:person[fasterrcnn_thing]fasterrcnn:000004|
|328|2111|2416290.jpg|6:person|eating|11:pizza|endpoint_missing_or_wrong_class|7:person[fasterrcnn_thing]fasterrcnn:000007||
|330|1919|2406484.jpg|9:person|in front of|11:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|331|284|2326073.jpg|0:person|driving|2:airplane|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:airplane[fasterrcnn_thing]fasterrcnn:000000|
|332|1415|2382040.jpg|2:person|in front of|0:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|332|1415|2382040.jpg|2:person|sitting on|4:chair|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|332|1415|2382040.jpg|5:dining table|in front of|1:person|wrong_predicate|1:dining table[fasterrcnn_thing]fasterrcnn:000001|3:person[fasterrcnn_thing]fasterrcnn:000003|
|333|1739|2397128.jpg|0:person|attached to|1:horse|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:horse[fasterrcnn_thing]fasterrcnn:000000|
|333|1739|2397128.jpg|0:person|sitting on|1:horse|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:horse[fasterrcnn_thing]fasterrcnn:000000|
|335|303|2326982.jpg|1:donut|attached to|0:person|wrong_predicate|0:donut[fasterrcnn_thing]fasterrcnn:000000|1:person[fasterrcnn_thing]fasterrcnn:000001|
|342|1241|2372547.jpg|0:person|touching|1:kite|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:kite[fasterrcnn_thing]fasterrcnn:000002|
|342|1241|2372547.jpg|0:person|sitting on|3:floor|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|342|1241|2372547.jpg|1:kite|in front of|0:person|wrong_predicate|2:kite[fasterrcnn_thing]fasterrcnn:000002|1:person[fasterrcnn_thing]fasterrcnn:000001|
|344|556|2339759.jpg|0:person|holding|1:tennis racket|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:tennis racket[fasterrcnn_thing]fasterrcnn:000001|
|344|556|2339759.jpg|0:person|jumping from|2:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|346|377|2330880.jpg|0:person|standing on|6:building|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|347|1854|2402990.jpg|0:person|wearing|13:baseball glove|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|6:baseball glove[fasterrcnn_thing]fasterrcnn:000006|
|347|1854|2402990.jpg|2:person|leaning on|18:fence|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|347|1854|2402990.jpg|4:person|running on|16:playingfield|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|347|1854|2402990.jpg|5:person|walking on|16:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|348|205|2321647.jpg|2:person|standing on|21:pavement|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|348|205|2321647.jpg|3:person|carrying|18:handbag|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|348|205|2321647.jpg|8:person|in front of|2:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:person[fasterrcnn_thing]fasterrcnn:000005|
|348|205|2321647.jpg|8:person|standing on|21:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|348|205|2321647.jpg|12:person|carrying|16:handbag|endpoint_missing_or_wrong_class|8:person[fasterrcnn_thing]fasterrcnn:000008||
|351|663|2345356.jpg|3:person|riding|21:horse|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:horse[fasterrcnn_thing]fasterrcnn:000000|
|353|1492|2385610.jpg|3:person|beside|15:car|rank_below50|9:person[fasterrcnn_thing]fasterrcnn:000009|18:car[fasterrcnn_thing]fasterrcnn:000018|
|353|1492|2385610.jpg|3:person|crossing|27:road|endpoint_missing_or_wrong_class|9:person[fasterrcnn_thing]fasterrcnn:000009||
|353|1492|2385610.jpg|4:person|walking on|31:pavement|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|353|1492|2385610.jpg|15:car|beside|3:person|wrong_predicate|18:car[fasterrcnn_thing]fasterrcnn:000018|9:person[fasterrcnn_thing]fasterrcnn:000009|
|354|111|2316413.jpg|0:person|walking on|4:stairs|endpoint_missing_or_wrong_class|||
|354|111|2316413.jpg|1:person|going down|4:stairs|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|354|111|2316413.jpg|1:person|wearing|4:stairs|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|354|111|2316413.jpg|2:person|wearing|0:person|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|354|111|2316413.jpg|8:fence|in front of|0:person|endpoint_missing_or_wrong_class|||
|357|726|2348363.jpg|5:person|in front of|14:airplane|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|2:airplane[fasterrcnn_thing]fasterrcnn:000002|
|357|726|2348363.jpg|7:person|looking at|11:person|pair_not_selected|1:person[fasterrcnn_thing]fasterrcnn:000001|5:person[fasterrcnn_thing]fasterrcnn:000005|
|360|1205|2371211.jpg|0:person|holding|3:book|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|360|1205|2371211.jpg|0:person|standing on|8:pavement|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|360|1205|2371211.jpg|6:tree|in front of|0:person|endpoint_missing_or_wrong_class||2:person[fasterrcnn_thing]fasterrcnn:000002|
|362|651|2344819.jpg|3:wall|in front of|0:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|364|483|2335916.jpg|1:person|looking at|5:bus|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:bus[fasterrcnn_thing]fasterrcnn:000001; 7:bus[fasterrcnn_thing]fasterrcnn:000007|
|364|483|2335916.jpg|2:person|standing on|9:dirt|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|366|1251|2373084.jpg|0:person|standing on|9:sand|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|366|1251|2373084.jpg|3:person|talking to|0:person|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|2:person[fasterrcnn_thing]fasterrcnn:000002|
|366|1251|2373084.jpg|4:person|standing on|9:sand|endpoint_missing_or_wrong_class|||
|367|1950|2408290.jpg|0:person|on back of|1:motorcycle|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:motorcycle[fasterrcnn_thing]fasterrcnn:000000|
|369|1390|2380682.jpg|4:person|wearing|10:person|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|0:person[fasterrcnn_thing]fasterrcnn:000000|
|369|1390|2380682.jpg|5:person|standing on|20:snow|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|369|1390|2380682.jpg|8:person|on|10:person|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|0:person[fasterrcnn_thing]fasterrcnn:000000|
|369|1390|2380682.jpg|9:person|looking at|5:person|rank_below50|6:person[fasterrcnn_thing]fasterrcnn:000006; 24:person[fasterrcnn_thing]fasterrcnn:000024|1:person[fasterrcnn_thing]fasterrcnn:000001|
|369|1390|2380682.jpg|10:person|walking on|20:snow|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|369|1390|2380682.jpg|11:person|carrying|19:snowboard|wrong_predicate|7:person[fasterrcnn_thing]fasterrcnn:000007|10:snowboard[fasterrcnn_thing]fasterrcnn:000010|
|370|56|1592537.jpg|14:tree|beside|0:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|371|2103|2416059.jpg|0:person|carrying|2:backpack|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:backpack[fasterrcnn_thing]fasterrcnn:000002|
|371|2103|2416059.jpg|0:person|standing on|3:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skis[fasterrcnn_thing]fasterrcnn:000001|
|371|2103|2416059.jpg|0:person|playing|3:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skis[fasterrcnn_thing]fasterrcnn:000001|
|373|775|2350750.jpg|3:person|looking at|5:train|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|373|775|2350750.jpg|3:person|standing on|7:platform|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|373|775|2350750.jpg|4:person|looking at|5:train|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|373|775|2350750.jpg|4:person|beside|6:suitcase|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|6:suitcase[fasterrcnn_thing]fasterrcnn:000006|
|373|775|2350750.jpg|4:person|standing on|7:platform|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|373|775|2350750.jpg|6:suitcase|beside|4:person|rank_below50|6:suitcase[fasterrcnn_thing]fasterrcnn:000006|2:person[fasterrcnn_thing]fasterrcnn:000002|
|377|1495|2385674.jpg|1:person|beside|0:person|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|10:person[fasterrcnn_thing]fasterrcnn:000010|
|377|1495|2385674.jpg|2:person|looking at|3:person|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|2:person[fasterrcnn_thing]fasterrcnn:000002|
|377|1495|2385674.jpg|3:person|in front of|2:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|3:person[fasterrcnn_thing]fasterrcnn:000003|
|377|1495|2385674.jpg|3:person|beside|2:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|3:person[fasterrcnn_thing]fasterrcnn:000003|
|377|1495|2385674.jpg|3:person|looking at|2:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|3:person[fasterrcnn_thing]fasterrcnn:000003|
|380|581|2341544.jpg|6:person|standing on|29:pavement|endpoint_missing_or_wrong_class|6:person[fasterrcnn_thing]fasterrcnn:000006||
|380|581|2341544.jpg|10:person|carrying|23:handbag|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|15:handbag[fasterrcnn_thing]fasterrcnn:000015|
|381|1745|2397343.jpg|0:person|playing with|1:dog|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|0:dog[fasterrcnn_thing]fasterrcnn:000000|
|381|1745|2397343.jpg|0:person|beside|5:door|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|381|1745|2397343.jpg|0:person|beside|7:table|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|381|1745|2397343.jpg|5:door|in|0:person|endpoint_missing_or_wrong_class||4:person[fasterrcnn_thing]fasterrcnn:000004|
|381|1745|2397343.jpg|7:table|beside|0:person|endpoint_missing_or_wrong_class||4:person[fasterrcnn_thing]fasterrcnn:000004|
|382|1449|2383257.jpg|0:person|standing on|1:bench|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:bench[fasterrcnn_thing]fasterrcnn:000002|
|382|1449|2383257.jpg|0:person|playing|2:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|382|1449|2383257.jpg|3:door|beside|0:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|382|1449|2383257.jpg|5:wall|beside|0:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|383|503|2336741.jpg|0:person|standing on|24:floor|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|385|12|1159501.jpg|0:person|attached to|1:person|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004; 35:person[fasterrcnn_thing]fasterrcnn:000035|4:person[fasterrcnn_thing]fasterrcnn:000004|
|385|12|1159501.jpg|0:person|touching|3:laptop|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004; 35:person[fasterrcnn_thing]fasterrcnn:000035|0:laptop[fasterrcnn_thing]fasterrcnn:000000|
|385|12|1159501.jpg|1:person|attached to|0:person|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|4:person[fasterrcnn_thing]fasterrcnn:000004; 35:person[fasterrcnn_thing]fasterrcnn:000035|
|386|1395|2380947.jpg|3:person|looking at|6:person|rank_below50|4:person[fasterrcnn_thing]fasterrcnn:000004|0:person[fasterrcnn_thing]fasterrcnn:000000|
|386|1395|2380947.jpg|6:person|talking to|11:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:person[fasterrcnn_thing]fasterrcnn:000001|
|386|1395|2380947.jpg|6:person|attached to|14:tennis racket|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|7:tennis racket[fasterrcnn_thing]fasterrcnn:000007|
|386|1395|2380947.jpg|6:person|holding|14:tennis racket|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|7:tennis racket[fasterrcnn_thing]fasterrcnn:000007|
|386|1395|2380947.jpg|6:person|standing on|17:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|386|1395|2380947.jpg|12:person|talking to|4:person|rank_below50|12:person[fasterrcnn_thing]fasterrcnn:000012|13:person[fasterrcnn_thing]fasterrcnn:000013|
|387|1391|2380691.jpg|0:person|looking at|1:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:sports ball[fasterrcnn_thing]fasterrcnn:000001|
|387|1391|2380691.jpg|0:person|chasing|1:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:sports ball[fasterrcnn_thing]fasterrcnn:000001|
|387|1391|2380691.jpg|0:person|about to hit|1:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:sports ball[fasterrcnn_thing]fasterrcnn:000001|
|387|1391|2380691.jpg|0:person|running on|4:floor|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|389|1609|2390707.jpg|6:person|in front of|8:person|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|9:person[fasterrcnn_thing]fasterrcnn:000009|
|389|1609|2390707.jpg|6:person|beside|16:chair|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|27:chair[fasterrcnn_thing]fasterrcnn:000027|
|389|1609|2390707.jpg|6:person|attached to|21:playingfield|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|389|1609|2390707.jpg|6:person|attached to|22:towel|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|389|1609|2390707.jpg|6:person|swinging|22:towel|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|389|1609|2390707.jpg|7:person|standing on|21:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|389|1609|2390707.jpg|9:person|standing on|21:playingfield|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|389|1609|2390707.jpg|16:chair|beside|6:person|wrong_predicate|27:chair[fasterrcnn_thing]fasterrcnn:000027|3:person[fasterrcnn_thing]fasterrcnn:000003|
|394|1496|2385703.jpg|0:person|carrying|6:handbag|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|9:handbag[fasterrcnn_thing]fasterrcnn:000009|
|395|758|2350121.jpg|1:person|on back of|5:horse|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:horse[fasterrcnn_thing]fasterrcnn:000000|
|395|758|2350121.jpg|2:person|on back of|4:horse|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|1:horse[fasterrcnn_thing]fasterrcnn:000001|
|396|630|2343959.jpg|5:person|in front of|8:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|396|630|2343959.jpg|5:person|wearing|15:tie|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|396|630|2343959.jpg|8:person|in front of|19:mirror|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|396|630|2343959.jpg|9:person|looking at|8:person|rank_below50|4:person[fasterrcnn_thing]fasterrcnn:000004|2:person[fasterrcnn_thing]fasterrcnn:000002|
|396|630|2343959.jpg|9:person|beside|10:person|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|1:person[fasterrcnn_thing]fasterrcnn:000001|
|396|630|2343959.jpg|10:person|beside|16:dining table|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|23:dining table[fasterrcnn_thing]fasterrcnn:000023|
|396|630|2343959.jpg|18:light|over|8:person|endpoint_missing_or_wrong_class||2:person[fasterrcnn_thing]fasterrcnn:000002|
|398|1128|2366957.jpg|4:person|looking at|30:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|398|1128|2366957.jpg|13:person|in front of|28:tree|endpoint_missing_or_wrong_class|||
|399|1835|2402046.jpg|1:person|standing on|17:rock|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|399|1835|2402046.jpg|9:person|entering|13:boat|endpoint_missing_or_wrong_class||0:boat[fasterrcnn_thing]fasterrcnn:000000|
|400|731|2348722.jpg|3:person|wearing|17:baseball glove|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|400|731|2348722.jpg|4:person|carrying|16:baseball bat|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|400|731|2348722.jpg|6:person|talking to|5:person|wrong_predicate|19:person[fasterrcnn_thing]fasterrcnn:000019|36:person[fasterrcnn_thing]fasterrcnn:000036|
|400|731|2348722.jpg|7:person|running on|19:playingfield|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|400|731|2348722.jpg|8:person|standing on|19:playingfield|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|404|736|2348945.jpg|0:person|talking to|1:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|404|736|2348945.jpg|0:person|standing on|5:truck|endpoint_missing_or_wrong_class||3:truck[fasterrcnn_thing]fasterrcnn:000003|
|404|736|2348945.jpg|1:person|standing on|9:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|406|1324|2377760.jpg|0:person|on|1:truck|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|406|1324|2377760.jpg|0:person|sitting on|1:truck|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|410|761|2350256.jpg|0:person|in|1:bus|endpoint_missing_or_wrong_class||0:bus[fasterrcnn_thing]fasterrcnn:000000|
|410|761|2350256.jpg|0:person|driving|1:bus|endpoint_missing_or_wrong_class||0:bus[fasterrcnn_thing]fasterrcnn:000000|
|413|280|2325881.jpg|0:person|holding|1:banana|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:banana[fasterrcnn_thing]fasterrcnn:000003|
|413|280|2325881.jpg|0:person|sitting on|2:chair|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|413|280|2325881.jpg|0:person|in front of|4:wall-wood|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|414|1318|2377223.jpg|0:person|in front of|1:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|414|1318|2377223.jpg|0:person|swinging|4:tennis racket|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:tennis racket[fasterrcnn_thing]fasterrcnn:000001|
|414|1318|2377223.jpg|1:person|in front of|6:wall|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|414|1318|2377223.jpg|3:sports ball|beside|2:person|endpoint_missing_or_wrong_class|||
|415|1211|2371415.jpg|4:wall|enclosing|0:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|417|1547|2387788.jpg|0:person|standing on|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|417|1547|2387788.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|417|1547|2387788.jpg|0:person|wearing|2:platform|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|417|1547|2387788.jpg|0:person|wearing|3:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|419|962|2359075.jpg|5:person|standing on|12:dirt|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|419|962|2359075.jpg|6:person|standing on|12:dirt|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|419|962|2359075.jpg|11:fence|in front of|5:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|419|962|2359075.jpg|11:fence|in front of|6:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|421|1772|2398484.jpg|0:person|on back of|2:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:person[fasterrcnn_thing]fasterrcnn:000002|
|421|1772|2398484.jpg|1:person|holding|3:baseball bat|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|4:baseball bat[fasterrcnn_thing]fasterrcnn:000004|
|421|1772|2398484.jpg|1:person|standing on|5:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|421|1772|2398484.jpg|2:person|attached to|0:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|1:person[fasterrcnn_thing]fasterrcnn:000001|
|421|1772|2398484.jpg|2:person|wearing|4:baseball glove|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|3:baseball glove[fasterrcnn_thing]fasterrcnn:000003|
|422|1007|2361180.jpg|1:person|walking on|6:pavement|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|422|1007|2361180.jpg|2:person|walking on|6:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|422|1007|2361180.jpg|3:person|in front of|1:person|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|4:person[fasterrcnn_thing]fasterrcnn:000004|
|422|1007|2361180.jpg|4:person|standing on|6:pavement|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|423|2171|713172.jpg|0:person|in|13:building|endpoint_missing_or_wrong_class|||
|427|361|2329834.jpg|0:person|in front of|15:wall-wood|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|427|361|2329834.jpg|0:person|beside|16:window|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|428|1752|2397624.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|428|1752|2397624.jpg|0:person|looking at|3:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|428|1752|2397624.jpg|0:person|on|5:wall|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|430|1713|2395938.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|430|1713|2395938.jpg|0:person|going down|2:stairs|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|430|1713|2395938.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|432|880|2355316.jpg|0:person|in front of|7:car|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|8:car[fasterrcnn_thing]fasterrcnn:000008|
|432|880|2355316.jpg|0:person|standing on|12:pavement|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|432|880|2355316.jpg|1:person|standing on|12:pavement|endpoint_missing_or_wrong_class|9:person[fasterrcnn_thing]fasterrcnn:000009||
|432|880|2355316.jpg|6:person|in front of|13:building|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|434|1478|2385010.jpg|0:person|standing on|4:floor|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|438|163|2319267.jpg|0:person|on|2:truck|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|438|163|2319267.jpg|0:person|standing on|2:truck|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|439|1357|2379131.jpg|0:person|looking at|8:apple|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:apple[fasterrcnn_thing]fasterrcnn:000000|
|439|1357|2379131.jpg|0:person|catching|8:apple|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:apple[fasterrcnn_thing]fasterrcnn:000000|
|441|2118|2416492.jpg|0:person|beside|1:toilet|endpoint_missing_or_wrong_class||2:toilet[fasterrcnn_thing]fasterrcnn:000002|
|441|2118|2416492.jpg|0:person|cleaning|1:toilet|endpoint_missing_or_wrong_class||2:toilet[fasterrcnn_thing]fasterrcnn:000002|
|441|2118|2416492.jpg|0:person|touching|1:toilet|endpoint_missing_or_wrong_class||2:toilet[fasterrcnn_thing]fasterrcnn:000002|
|443|192|2321324.jpg|0:person|walking on|22:pavement|endpoint_missing_or_wrong_class|7:person[fasterrcnn_thing]fasterrcnn:000007||
|443|192|2321324.jpg|1:person|feeding|11:bird|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|446|712|2347578.jpg|0:person|riding|1:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skis[fasterrcnn_thing]fasterrcnn:000001|
|446|712|2347578.jpg|0:person|going down|2:snow|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|446|712|2347578.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|447|104|2316313.jpg|0:person|in front of|1:person|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|4:person[fasterrcnn_thing]fasterrcnn:000004|
|448|792|2351247.jpg|4:person|beside|8:person|rank_below50|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|448|792|2351247.jpg|7:person|standing on|28:dirt|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|448|792|2351247.jpg|8:person|picking|30:food|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|449|784|2351059.jpg|0:person|running on|6:sand|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|449|784|2351059.jpg|1:person|catching|3:sports ball|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|449|784|2351059.jpg|1:person|wearing|4:baseball glove|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|449|784|2351059.jpg|1:person|running on|6:sand|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|449|784|2351059.jpg|2:person|looking at|1:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|450|1615|2390859.jpg|0:person|looking at|2:cell phone|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:cell phone[fasterrcnn_thing]fasterrcnn:000002|
|450|1615|2390859.jpg|0:person|in front of|3:paper|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|450|1615|2390859.jpg|0:person|in front of|4:building|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|453|1642|2392244.jpg|0:person|looking at|5:bowl|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|12:bowl[fasterrcnn_thing]fasterrcnn:000012|
|453|1642|2392244.jpg|10:dining table|attached to|0:person|wrong_predicate|2:dining table[fasterrcnn_thing]fasterrcnn:000002|1:person[fasterrcnn_thing]fasterrcnn:000001|
|454|629|2343942.jpg|1:person|looking at|23:laptop|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|29:laptop[fasterrcnn_thing]fasterrcnn:000029|
|454|629|2343942.jpg|3:person|wearing|18:chair|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|7:chair[fasterrcnn_thing]fasterrcnn:000007|
|454|629|2343942.jpg|19:chair|in front of|10:person|rank_below50|9:chair[fasterrcnn_thing]fasterrcnn:000009|3:person[fasterrcnn_thing]fasterrcnn:000003; 25:person[fasterrcnn_thing]fasterrcnn:000025|
|456|1089|2365077.jpg|0:person|talking to|2:person|wrong_predicate|14:person[fasterrcnn_thing]fasterrcnn:000014|17:person[fasterrcnn_thing]fasterrcnn:000017; 26:person[fasterrcnn_thing]fasterrcnn:000026|
|457|587|2341770.jpg|0:person|driving|3:bus|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:bus[fasterrcnn_thing]fasterrcnn:000000|
|457|587|2341770.jpg|1:person|sitting on|3:bus|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|0:bus[fasterrcnn_thing]fasterrcnn:000000|
|457|587|2341770.jpg|2:person|sitting on|3:bus|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:bus[fasterrcnn_thing]fasterrcnn:000000|
|458|1575|2388803.jpg|0:person|wearing|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|458|1575|2388803.jpg|0:person|looking at|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|458|1575|2388803.jpg|0:person|catching|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|458|1575|2388803.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|458|1575|2388803.jpg|0:person|jumping over|2:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|458|1575|2388803.jpg|0:person|wearing|2:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|461|107|2316321.jpg|0:person|standing on|6:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|4:skis[fasterrcnn_thing]fasterrcnn:000004|
|461|107|2316321.jpg|2:person|going down|9:snow|endpoint_missing_or_wrong_class|||
|461|107|2316321.jpg|3:person|going down|9:snow|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|463|555|2339725.jpg|0:person|biting|8:toothbrush|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|6:toothbrush[fasterrcnn_thing]fasterrcnn:000006|
|466|1797|2400508.jpg|0:person|playing|1:kite|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:kite[fasterrcnn_thing]fasterrcnn:000001|
|466|1797|2400508.jpg|0:person|on|2:sand|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|466|1797|2400508.jpg|0:person|standing on|2:sand|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|466|1797|2400508.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|470|1101|2365885.jpg|0:person|playing|2:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|4:sports ball[fasterrcnn_thing]fasterrcnn:000004|
|470|1101|2365885.jpg|0:person|holding|3:tennis racket|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:tennis racket[fasterrcnn_thing]fasterrcnn:000002|
|470|1101|2365885.jpg|0:person|running on|4:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|471|1700|2394982.jpg|0:person|in front of|8:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:person[fasterrcnn_thing]fasterrcnn:000002|
|471|1700|2394982.jpg|0:person|attached to|13:fence|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|471|1700|2394982.jpg|8:person|attached to|13:fence|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|472|404|2332502.jpg|1:person|driving|14:boat|wrong_predicate|7:person[fasterrcnn_thing]fasterrcnn:000007|0:boat[fasterrcnn_thing]fasterrcnn:000000|
|472|404|2332502.jpg|2:person|over|18:river|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|473|605|2342711.jpg|0:person|looking at|22:bowl|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|473|605|2342711.jpg|1:person|beside|0:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|478|1804|2400822.jpg|0:person|beside|1:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|478|1804|2400822.jpg|0:person|attached to|3:surfboard|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:surfboard[fasterrcnn_thing]fasterrcnn:000002|
|478|1804|2400822.jpg|0:person|playing|3:surfboard|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:surfboard[fasterrcnn_thing]fasterrcnn:000002|
|478|1804|2400822.jpg|0:person|on|4:sand|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|478|1804|2400822.jpg|0:person|standing on|4:sand|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|478|1804|2400822.jpg|0:person|beside|5:sea|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|478|1804|2400822.jpg|1:person|on|4:sand|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|478|1804|2400822.jpg|1:person|walking on|4:sand|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|478|1804|2400822.jpg|1:person|beside|5:sea|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|478|1804|2400822.jpg|5:sea|beside|0:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|478|1804|2400822.jpg|5:sea|beside|1:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|480|461|2334659.jpg|0:person|in front of|9:house|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|480|461|2334659.jpg|0:person|walking on|13:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|480|461|2334659.jpg|2:person|in front of|9:house|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|480|461|2334659.jpg|2:person|walking on|13:pavement|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|481|797|2351374.jpg|7:person|attached to|14:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|481|797|2351374.jpg|7:person|walking on|14:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|481|797|2351374.jpg|8:person|in front of|9:person|wrong_predicate|14:person[fasterrcnn_thing]fasterrcnn:000014|11:person[fasterrcnn_thing]fasterrcnn:000011|
|481|797|2351374.jpg|10:person|going down|14:pavement|endpoint_missing_or_wrong_class|9:person[fasterrcnn_thing]fasterrcnn:000009||
|481|797|2351374.jpg|12:person|beside|15:building|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|481|797|2351374.jpg|13:sky|on|3:person|endpoint_missing_or_wrong_class||5:person[fasterrcnn_thing]fasterrcnn:000005|
|483|1172|2369539.jpg|0:person|catching|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|483|1172|2369539.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|483|1172|2369539.jpg|0:person|on|2:sea|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|485|57|1592560.jpg|0:person|beside|7:table|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|485|57|1592560.jpg|0:person|in front of|9:wall|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|486|1052|2362836.jpg|0:person|guiding|3:person|wrong_predicate|15:person[fasterrcnn_thing]fasterrcnn:000015|1:person[fasterrcnn_thing]fasterrcnn:000001|
|486|1052|2362836.jpg|3:person|in front of|0:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|15:person[fasterrcnn_thing]fasterrcnn:000015|
|486|1052|2362836.jpg|4:person|on|1:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|486|1052|2362836.jpg|5:person|walking on|8:road|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|489|610|2342847.jpg|2:person|walking on|23:road|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|489|610|2342847.jpg|6:person|driving|11:truck|wrong_predicate|8:person[fasterrcnn_thing]fasterrcnn:000008; 27:person[fasterrcnn_thing]fasterrcnn:000027|18:truck[fasterrcnn_thing]fasterrcnn:000018|
|490|2161|498294.jpg|0:person|in front of|1:person|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|6:person[fasterrcnn_thing]fasterrcnn:000006|
|490|2161|498294.jpg|1:person|wearing|6:baseball glove|wrong_predicate|6:person[fasterrcnn_thing]fasterrcnn:000006|5:baseball glove[fasterrcnn_thing]fasterrcnn:000005|
|490|2161|498294.jpg|3:person|standing on|9:playingfield|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|490|2161|498294.jpg|4:person|wearing|8:baseball glove|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|7:baseball glove[fasterrcnn_thing]fasterrcnn:000007|
|490|2161|498294.jpg|5:person|running on|9:playingfield|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|491|382|2331166.jpg|0:person|on|17:bus|wrong_predicate|14:person[fasterrcnn_thing]fasterrcnn:000014|0:bus[fasterrcnn_thing]fasterrcnn:000000|
|491|382|2331166.jpg|2:person|on|20:pavement|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|491|382|2331166.jpg|3:person|on|20:pavement|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|491|382|2331166.jpg|5:person|walking on|20:pavement|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|491|382|2331166.jpg|8:person|driving|17:bus|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|0:bus[fasterrcnn_thing]fasterrcnn:000000|
|492|1031|2362238.jpg|0:person|playing|2:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|492|1031|2362238.jpg|0:person|on|3:sea|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|493|374|2330610.jpg|0:person|in|1:truck|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|493|374|2330610.jpg|0:person|driving|1:truck|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|494|265|2324812.jpg|0:person|touching|2:person|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|2:person[fasterrcnn_thing]fasterrcnn:000002|
|494|265|2324812.jpg|1:person|attached to|3:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|494|265|2324812.jpg|3:person|carrying|4:handbag|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:handbag[fasterrcnn_thing]fasterrcnn:000005|
|494|265|2324812.jpg|3:person|holding|5:cell phone|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|6:cell phone[fasterrcnn_thing]fasterrcnn:000006|
|494|265|2324812.jpg|3:person|in front of|7:window|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|494|265|2324812.jpg|5:cell phone|touching|3:person|wrong_predicate|6:cell phone[fasterrcnn_thing]fasterrcnn:000006|0:person[fasterrcnn_thing]fasterrcnn:000000|
|496|769|2350508.jpg|1:person|attached to|2:pizza|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|496|769|2350508.jpg|1:person|looking at|2:pizza|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|496|769|2350508.jpg|1:person|eating|2:pizza|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|496|769|2350508.jpg|1:person|in front of|3:wall|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|496|769|2350508.jpg|2:pizza|attached to|1:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|500|1155|2368389.jpg|3:fence|enclosing|0:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|

## B_mask2former_thing

未命中793条。

|序号|索引|图片|GT主语|谓词|GT宾语|失败阶段|匹配主语候选|匹配宾语候选|
|---:|---:|---|---|---|---|---|---|---|
|6|295|2326503.jpg|0:person|on|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000004|
|6|295|2326503.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000004|
|6|295|2326503.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000003|
|7|1675|2393584.jpg|0:person|in|2:tv|endpoint_missing_or_wrong_class||0:tv[mask2former_thing]mask2former:062:000002|
|10|553|2339606.jpg|0:person|running on|16:dirt|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|10|553|2339606.jpg|1:person|standing on|16:dirt|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000008||
|10|553|2339606.jpg|4:person|standing on|12:playingfield|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000007||
|10|553|2339606.jpg|6:person|wearing|9:baseball glove|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|16|1466|2384291.jpg|0:person|beside|1:person|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000010||
|16|1466|2384291.jpg|0:person|on|20:pavement|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000010||
|16|1466|2384291.jpg|1:person|beside|0:person|endpoint_missing_or_wrong_class||2:person[mask2former_thing]mask2former:000:000010|
|16|1466|2384291.jpg|2:person|holding|21:paper|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|16|1466|2384291.jpg|3:person|walking on|20:pavement|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000016||
|16|1466|2384291.jpg|4:person|on|20:pavement|endpoint_missing_or_wrong_class|||
|18|1983|2409607.jpg|0:person|sitting on|1:horse|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:horse[mask2former_thing]mask2former:017:000005|
|18|1983|2409607.jpg|0:person|over|5:grass|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|21|411|2332726.jpg|0:person|walking on|8:sand|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000007||
|21|411|2332726.jpg|3:person|flying over|5:kite|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|21|411|2332726.jpg|3:person|looking at|5:kite|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|21|411|2332726.jpg|3:person|playing|5:kite|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|21|411|2332726.jpg|3:person|wearing|8:sand|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|22|129|2317125.jpg|2:person|walking on|11:road|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000008||
|22|129|2317125.jpg|4:person|standing on|11:road|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|22|129|2317125.jpg|9:house|beside|0:person|endpoint_missing_or_wrong_class||1:person[mask2former_thing]mask2former:000:000005|
|23|1055|2363004.jpg|0:person|holding|12:handbag|wrong_predicate|5:person[mask2former_thing]mask2former:000:000010|9:handbag[mask2former_thing]mask2former:026:000011|
|23|1055|2363004.jpg|2:person|walking on|21:pavement|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000007||
|23|1055|2363004.jpg|3:person|walking on|21:pavement|endpoint_missing_or_wrong_class|||
|23|1055|2363004.jpg|7:person|walking on|21:pavement|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000008||
|23|1055|2363004.jpg|8:person|walking on|21:pavement|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000013||
|24|1712|2395918.jpg|0:person|crossing|5:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|24|1712|2395918.jpg|1:person|sitting on|5:pavement|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|24|1712|2395918.jpg|1:person|beside|6:grass|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|24|1712|2395918.jpg|2:skateboard|attached to|0:person|wrong_predicate|2:skateboard[mask2former_thing]mask2former:036:000002|0:person[mask2former_thing]mask2former:000:000003|
|26|892|2355904.jpg|0:person|touching|10:table|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000006||
|27|2018|2411180.jpg|0:person|standing on|6:railroad|endpoint_missing_or_wrong_class|||
|28|164|2319298.jpg|0:person|driving|1:car|endpoint_missing_or_wrong_class||1:car[mask2former_thing]mask2former:002:000006|
|29|81|2315729.jpg|2:person|slicing|15:cake|wrong_predicate|3:person[mask2former_thing]mask2former:000:000011; 4:person[mask2former_thing]mask2former:000:000013|12:cake[mask2former_thing]mask2former:055:000008|
|29|81|2315729.jpg|3:person|attached to|4:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|2:person[mask2former_thing]mask2former:000:000010|
|29|81|2315729.jpg|6:person|attached to|2:person|endpoint_missing_or_wrong_class||3:person[mask2former_thing]mask2former:000:000011; 4:person[mask2former_thing]mask2former:000:000013|
|33|1896|2405341.jpg|0:person|holding|1:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|0:person[mask2former_thing]mask2former:000:000001|
|35|1326|2377788.jpg|0:person|feeding|3:cow|wrong_predicate|0:person[mask2former_thing]mask2former:000:000007; 1:person[mask2former_thing]mask2former:000:000009|6:cow[mask2former_thing]mask2former:019:000008|
|35|1326|2377788.jpg|6:cow|in front of|1:person|wrong_predicate|8:cow[mask2former_thing]mask2former:019:000013|0:person[mask2former_thing]mask2former:000:000007|
|36|922|2357107.jpg|1:person|in|9:boat|wrong_predicate|2:person[mask2former_thing]mask2former:000:000003|8:boat[mask2former_thing]mask2former:008:000006|
|36|922|2357107.jpg|4:person|walking on|14:platform|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000007||
|38|1914|2406339.jpg|0:person|beside|3:person|endpoint_missing_or_wrong_class|||
|38|1914|2406339.jpg|0:person|looking at|22:playingfield|endpoint_missing_or_wrong_class|||
|38|1914|2406339.jpg|2:person|looking at|22:playingfield|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000006||
|38|1914|2406339.jpg|2:person|attached to|26:wall|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000006||
|40|208|2321715.jpg|0:person|on|7:motorcycle|endpoint_missing_or_wrong_class|||
|40|208|2321715.jpg|0:person|riding|7:motorcycle|endpoint_missing_or_wrong_class|||
|40|208|2321715.jpg|3:person|exiting|12:tent|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000008||
|40|208|2321715.jpg|3:person|walking on|16:floor|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000008||
|41|1485|2385230.jpg|4:wall-wood|beside|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000005|
|44|489|2336251.jpg|0:person|sitting on|9:pavement|endpoint_missing_or_wrong_class|||
|44|489|2336251.jpg|1:person|talking to|0:person|endpoint_missing_or_wrong_class|||
|44|489|2336251.jpg|1:person|sitting on|9:pavement|endpoint_missing_or_wrong_class|||
|44|489|2336251.jpg|2:person|sitting on|9:pavement|endpoint_missing_or_wrong_class|||
|44|489|2336251.jpg|3:person|playing|6:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|3:skateboard[mask2former_thing]mask2former:036:000006|
|44|489|2336251.jpg|3:person|jumping from|9:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|46|674|2345802.jpg|0:person|sitting on|2:chair|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|46|674|2345802.jpg|0:person|in front of|3:counter|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|51|1507|2386227.jpg|0:person|beside|1:person|endpoint_missing_or_wrong_class|||
|51|1507|2386227.jpg|1:person|in|2:tv|endpoint_missing_or_wrong_class||0:tv[mask2former_thing]mask2former:062:000003|
|52|1139|2367625.jpg|0:person|holding|1:spoon|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|52|1139|2367625.jpg|0:person|in front of|3:oven|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|2:oven[mask2former_thing]mask2former:069:000006|
|53|1627|2391314.jpg|0:person|standing on|1:skis|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000005||
|53|1627|2391314.jpg|0:person|wearing|1:skis|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000005||
|53|1627|2391314.jpg|0:person|beside|3:tree|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000005||
|54|237|2323211.jpg|1:person|on|17:grass|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000006||
|54|237|2323211.jpg|3:person|on|17:grass|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000003||
|54|237|2323211.jpg|5:person|over|1:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|3:person[mask2former_thing]mask2former:000:000006|
|54|237|2323211.jpg|5:person|over|8:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|4:person[mask2former_thing]mask2former:000:000007|
|54|237|2323211.jpg|5:person|on|17:grass|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000002||
|54|237|2323211.jpg|5:person|jumping from|17:grass|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000002||
|54|237|2323211.jpg|8:person|on|17:grass|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000007||
|54|237|2323211.jpg|11:person|standing on|17:grass|endpoint_missing_or_wrong_class|11:person[mask2former_thing]mask2former:000:000015||
|55|166|2319395.jpg|0:person|walking on|6:road|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|55|166|2319395.jpg|1:person|standing on|6:road|endpoint_missing_or_wrong_class|||
|57|327|2328174.jpg|0:person|in front of|1:car|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:car[mask2former_thing]mask2former:002:000001|
|57|327|2328174.jpg|0:person|picking|2:umbrella|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:umbrella[mask2former_thing]mask2former:025:000002|
|57|327|2328174.jpg|0:person|in front of|3:potted plant|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|3:potted plant[mask2former_thing]mask2former:058:000004|
|57|327|2328174.jpg|0:person|standing on|6:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|58|617|2343155.jpg|0:person|throwing|3:sports ball|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|58|617|2343155.jpg|0:person|about to hit|3:sports ball|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|58|617|2343155.jpg|0:person|standing on|6:playingfield|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|60|2159|498242.jpg|0:person|beside|9:person|rank_below50|6:person[mask2former_thing]mask2former:000:000008|2:person[mask2former_thing]mask2former:000:000004|
|60|2159|498242.jpg|1:person|looking at|9:person|rank_below50|1:person[mask2former_thing]mask2former:000:000002|2:person[mask2former_thing]mask2former:000:000004|
|60|2159|498242.jpg|2:person|standing on|14:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|60|2159|498242.jpg|3:person|looking at|1:person|rank_below50|4:person[mask2former_thing]mask2former:000:000006|1:person[mask2former_thing]mask2former:000:000002|
|60|2159|498242.jpg|3:person|beside|8:person|rank_below50|4:person[mask2former_thing]mask2former:000:000006|7:person[mask2former_thing]mask2former:000:000010|
|60|2159|498242.jpg|6:person|beside|4:person|endpoint_missing_or_wrong_class|9:person[mask2former_thing]mask2former:000:000013||
|60|2159|498242.jpg|8:person|attached to|5:person|wrong_predicate|7:person[mask2former_thing]mask2former:000:000010|8:person[mask2former_thing]mask2former:000:000011|
|60|2159|498242.jpg|9:person|holding|10:umbrella|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000004||
|61|1219|2371806.jpg|0:person|wearing|1:baseball glove|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:baseball glove[mask2former_thing]mask2former:035:000001|
|61|1219|2371806.jpg|0:person|running on|2:playingfield|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|63|1445|2383111.jpg|0:person|riding|6:horse|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|63|1445|2383111.jpg|1:person|riding|7:horse|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000008||
|63|1445|2383111.jpg|3:person|riding|4:horse|endpoint_missing_or_wrong_class||4:horse[mask2former_thing]mask2former:017:000003|
|64|1596|2390113.jpg|0:person|riding|1:elephant|endpoint_missing_or_wrong_class||2:elephant[mask2former_thing]mask2former:020:000004|
|65|915|2356824.jpg|0:person|walking on|18:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|66|749|2349334.jpg|1:person|looking at|4:person|wrong_predicate|2:person[mask2former_thing]mask2former:000:000006|0:person[mask2former_thing]mask2former:000:000001|
|66|749|2349334.jpg|2:person|eating|19:pizza|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000017||
|66|749|2349334.jpg|6:person|talking to|5:person|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000011||
|66|749|2349334.jpg|23:ceiling|on|4:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000001|
|68|1598|2390200.jpg|0:person|swinging|6:remote|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|68|1598|2390200.jpg|0:person|holding|9:remote|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|68|1598|2390200.jpg|1:person|holding|3:potted plant|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|68|1598|2390200.jpg|1:person|swinging|8:remote|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|68|1598|2390200.jpg|1:person|in front of|16:table|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|70|714|2347722.jpg|0:person|attached to|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:surfboard[mask2former_thing]mask2former:037:000003|
|70|714|2347722.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:surfboard[mask2former_thing]mask2former:037:000003|
|70|714|2347722.jpg|0:person|touching|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:surfboard[mask2former_thing]mask2former:037:000003|
|70|714|2347722.jpg|0:person|looking at|2:sea|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|71|10|1159449.jpg|1:person|looking at|17:sports ball|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000010||
|71|10|1159449.jpg|1:person|standing on|23:playingfield|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000010||
|71|10|1159449.jpg|8:person|running on|23:playingfield|endpoint_missing_or_wrong_class|||
|72|841|2353618.jpg|1:person|standing on|2:skis|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|2:skis[mask2former_thing]mask2former:030:000004|
|72|841|2353618.jpg|1:person|wearing|2:skis|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|2:skis[mask2former_thing]mask2former:030:000004|
|72|841|2353618.jpg|1:person|on|3:snow|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|72|841|2353618.jpg|2:skis|on|0:person|wrong_predicate|2:skis[mask2former_thing]mask2former:030:000004|0:person[mask2former_thing]mask2former:000:000001|
|75|1505|2386156.jpg|0:person|in|2:car|endpoint_missing_or_wrong_class||2:car[mask2former_thing]mask2former:002:000012|
|75|1505|2386156.jpg|0:person|driving|2:car|endpoint_missing_or_wrong_class||2:car[mask2former_thing]mask2former:002:000012|
|78|910|2356736.jpg|0:person|walking on|13:pavement|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000007||
|81|1886|2404565.jpg|0:person|looking at|3:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000010|6:surfboard[mask2former_thing]mask2former:037:000008|
|81|1886|2404565.jpg|0:person|standing on|17:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000010||
|82|1497|2385717.jpg|0:person|over|3:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|83|2176|713850.jpg|0:person|in|5:window|endpoint_missing_or_wrong_class|||
|86|1001|2360816.jpg|1:person|riding|13:bicycle|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|10:bicycle[mask2former_thing]mask2former:001:000023|
|86|1001|2360816.jpg|5:person|riding|11:bicycle|wrong_predicate|2:person[mask2former_thing]mask2former:000:000009|6:bicycle[mask2former_thing]mask2former:001:000007|
|86|1001|2360816.jpg|10:person|riding|14:bicycle|wrong_predicate|4:person[mask2former_thing]mask2former:000:000020|8:bicycle[mask2former_thing]mask2former:001:000013|
|87|852|2354099.jpg|3:person|crossing|36:pavement|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000021||
|87|852|2354099.jpg|9:person|crossing|36:pavement|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000013||
|87|852|2354099.jpg|11:person|on|34:skateboard|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000010||
|87|852|2354099.jpg|11:person|standing on|34:skateboard|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000010||
|87|852|2354099.jpg|37:building|beside|11:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000010|
|89|813|2352072.jpg|0:person|in front of|3:tree|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|89|813|2352072.jpg|4:sky|over|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000004|
|91|926|2357328.jpg|0:person|standing on|5:grass|endpoint_missing_or_wrong_class|||
|91|926|2357328.jpg|1:person|standing on|5:grass|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|91|926|2357328.jpg|2:person|holding|3:baseball bat|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|2:baseball bat[mask2former_thing]mask2former:034:000002|
|91|926|2357328.jpg|2:person|standing on|5:grass|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|92|1004|2360919.jpg|0:person|in front of|3:book|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|93|227|2322480.jpg|0:person|looking at|1:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|0:person[mask2former_thing]mask2former:000:000001|
|93|227|2322480.jpg|1:person|chasing|2:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|2:sports ball[mask2former_thing]mask2former:032:000004|
|93|227|2322480.jpg|1:person|playing|2:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|2:sports ball[mask2former_thing]mask2former:032:000004|
|93|227|2322480.jpg|2:sports ball|in front of|1:person|wrong_predicate|2:sports ball[mask2former_thing]mask2former:032:000004|0:person[mask2former_thing]mask2former:000:000001|
|94|664|2345357.jpg|0:person|in|10:train|endpoint_missing_or_wrong_class||2:train[mask2former_thing]mask2former:006:000004|
|94|664|2345357.jpg|1:person|in|10:train|endpoint_missing_or_wrong_class||2:train[mask2former_thing]mask2former:006:000004|
|95|649|2344605.jpg|0:person|wearing|7:tie|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000009||
|95|649|2344605.jpg|0:person|sitting on|9:chair|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000009||
|95|649|2344605.jpg|0:person|touching|12:laptop|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000009||
|95|649|2344605.jpg|12:laptop|in front of|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000009|
|100|1841|2402294.jpg|1:person|driving|6:bus|endpoint_missing_or_wrong_class||4:bus[mask2former_thing]mask2former:005:000004|
|101|1796|2400414.jpg|0:person|standing on|6:grass|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|101|1796|2400414.jpg|1:person|playing with|5:sheep|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|4:sheep[mask2former_thing]mask2former:018:000006|
|101|1796|2400414.jpg|1:person|touching|5:sheep|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|4:sheep[mask2former_thing]mask2former:018:000006|
|101|1796|2400414.jpg|3:person|pulling|4:sheep|endpoint_missing_or_wrong_class||3:sheep[mask2former_thing]mask2former:018:000003|
|101|1796|2400414.jpg|5:sheep|playing with|1:person|wrong_predicate|4:sheep[mask2former_thing]mask2former:018:000006|1:person[mask2former_thing]mask2former:000:000002|
|103|989|2360368.jpg|2:person|beside|9:motorcycle|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000008||
|103|989|2360368.jpg|2:person|standing on|12:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000008||
|103|989|2360368.jpg|2:person|in front of|14:dirt|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000008||
|104|1795|2400390.jpg|10:person|beside|6:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|3:person[mask2former_thing]mask2former:000:000011|
|105|1023|2361799.jpg|0:person|looking at|1:bear|endpoint_missing_or_wrong_class|||
|105|1023|2361799.jpg|0:person|in front of|3:tree|endpoint_missing_or_wrong_class|||
|106|868|2354820.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:skateboard[mask2former_thing]mask2former:036:000001|
|106|868|2354820.jpg|0:person|riding|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:skateboard[mask2former_thing]mask2former:036:000001|
|106|868|2354820.jpg|0:person|in front of|2:tree|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|106|868|2354820.jpg|0:person|standing on|4:floor|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|110|979|2359868.jpg|0:person|in|2:train|endpoint_missing_or_wrong_class||0:train[mask2former_thing]mask2former:006:000002|
|110|979|2359868.jpg|1:person|in|2:train|endpoint_missing_or_wrong_class||0:train[mask2former_thing]mask2former:006:000002|
|119|1534|2387240.jpg|4:person|in front of|13:person|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000010||
|119|1534|2387240.jpg|9:person|standing on|15:playingfield|endpoint_missing_or_wrong_class|12:person[mask2former_thing]mask2former:000:000018||
|121|1300|2376047.jpg|0:person|jumping from|4:playingfield|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|121|1300|2376047.jpg|1:person|chasing|2:frisbee|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|2:frisbee[mask2former_thing]mask2former:029:000002|
|121|1300|2376047.jpg|1:person|playing|2:frisbee|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|2:frisbee[mask2former_thing]mask2former:029:000002|
|121|1300|2376047.jpg|1:person|jumping from|4:playingfield|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|122|1729|2396723.jpg|0:person|holding|3:wine glass|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|122|1729|2396723.jpg|0:person|sitting on|4:couch|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|122|1729|2396723.jpg|1:cat|lying on|0:person|wrong_predicate|2:cat[mask2former_thing]mask2former:015:000003|0:person[mask2former_thing]mask2former:000:000002|
|122|1729|2396723.jpg|2:cat|lying on|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000002|
|122|1729|2396723.jpg|5:pillow|in front of|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000002|
|123|1099|2365844.jpg|10:person|beside|12:person|wrong_predicate|12:person[mask2former_thing]mask2former:000:000020|0:person[mask2former_thing]mask2former:000:000001|
|125|1673|2393510.jpg|0:person|playing with|2:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000004|2:person[mask2former_thing]mask2former:000:000005|
|125|1673|2393510.jpg|1:person|walking on|6:grass|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|125|1673|2393510.jpg|2:person|throwing|3:frisbee|wrong_predicate|2:person[mask2former_thing]mask2former:000:000005|3:frisbee[mask2former_thing]mask2former:029:000002|
|126|787|2351136.jpg|0:person|on back of|3:horse|wrong_predicate|1:person[mask2former_thing]mask2former:000:000005|3:horse[mask2former_thing]mask2former:017:000004|
|127|1293|2375622.jpg|0:person|holding|4:cell phone|endpoint_missing_or_wrong_class|||
|127|1293|2375622.jpg|1:person|looking at|2:laptop|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|3:laptop[mask2former_thing]mask2former:063:000003|
|127|1293|2375622.jpg|1:person|touching|2:laptop|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|3:laptop[mask2former_thing]mask2former:063:000003|
|128|323|2328089.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:surfboard[mask2former_thing]mask2former:037:000005|
|128|323|2328089.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:surfboard[mask2former_thing]mask2former:037:000005|
|128|323|2328089.jpg|0:person|in front of|5:building|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|130|2105|2416163.jpg|9:person|sitting on|33:sand|endpoint_missing_or_wrong_class|||
|130|2105|2416163.jpg|11:person|sitting on|33:sand|endpoint_missing_or_wrong_class|||
|130|2105|2416163.jpg|12:person|sitting on|33:sand|endpoint_missing_or_wrong_class|||
|131|1764|2398216.jpg|0:person|in front of|1:person|wrong_predicate|2:person[mask2former_thing]mask2former:000:000008|0:person[mask2former_thing]mask2former:000:000005|
|131|1764|2398216.jpg|0:person|standing on|11:pavement|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000008||
|131|1764|2398216.jpg|2:person|standing on|11:pavement|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000009||
|131|1764|2398216.jpg|3:person|standing on|11:pavement|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|134|406|2332593.jpg|0:person|in front of|8:wall-stone|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|134|406|2332593.jpg|0:person|on|12:grass|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|134|406|2332593.jpg|1:person|in front of|0:person|wrong_predicate|2:person[mask2former_thing]mask2former:000:000007|0:person[mask2former_thing]mask2former:000:000001|
|135|1163|2368707.jpg|0:person|running on|9:dirt|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|135|1163|2368707.jpg|1:person|looking at|4:frisbee|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|135|1163|2368707.jpg|1:person|running on|9:dirt|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|135|1163|2368707.jpg|2:person|running on|9:dirt|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000005||
|135|1163|2368707.jpg|3:person|looking at|4:frisbee|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|135|1163|2368707.jpg|3:person|throwing|4:frisbee|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|135|1163|2368707.jpg|4:frisbee|over|1:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000001|
|136|1375|2379887.jpg|0:person|in front of|5:mountain|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|138|1529|2387080.jpg|0:person|sitting on|5:chair|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000008||
|140|554|2339715.jpg|0:person|holding|14:spoon|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000015||
|140|554|2339715.jpg|0:person|eating|14:spoon|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000015||
|141|1697|2394828.jpg|0:person|over|3:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|141|1697|2394828.jpg|0:person|jumping from|3:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|141|1697|2394828.jpg|0:person|in front of|4:grass|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|141|1697|2394828.jpg|0:person|in front of|5:rock|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|144|1442|2383041.jpg|3:person|wearing|18:surfboard|wrong_predicate|1:person[mask2former_thing]mask2former:000:000006|10:surfboard[mask2former_thing]mask2former:037:000002|
|144|1442|2383041.jpg|3:person|flying over|21:sea|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|144|1442|2383041.jpg|4:person|pulling|13:kite|endpoint_missing_or_wrong_class||9:kite[mask2former_thing]mask2former:033:000014|
|145|23|1159863.jpg|0:person|on|7:road|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000007||
|149|1526|2387025.jpg|6:person|carrying|21:handbag|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000010||
|149|1526|2387025.jpg|8:person|wearing|24:cardboard|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000016||
|152|1986|2409643.jpg|0:person|holding|5:handbag|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|6:handbag[mask2former_thing]mask2former:026:000007|
|152|1986|2409643.jpg|0:person|on|7:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|153|1695|2394762.jpg|1:person|attached to|16:grass|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|153|1695|2394762.jpg|3:person|looking at|12:sports ball|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|153|1695|2394762.jpg|3:person|running on|13:playingfield|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|153|1695|2394762.jpg|5:person|pulling|6:person|endpoints_collapsed_to_same_box|2:person[mask2former_thing]mask2former:000:000006|2:person[mask2former_thing]mask2former:000:000006|
|153|1695|2394762.jpg|5:person|jumping from|13:playingfield|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000006||
|153|1695|2394762.jpg|6:person|catching|12:sports ball|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000006||
|154|47|1592228.jpg|1:person|standing on|17:platform|endpoint_missing_or_wrong_class|||
|154|47|1592228.jpg|5:person|carrying|12:handbag|endpoint_missing_or_wrong_class|||
|154|47|1592228.jpg|5:person|standing on|22:pavement|endpoint_missing_or_wrong_class|||
|156|1813|2401171.jpg|9:person|walking on|25:pavement|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000018||
|157|1286|2375241.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|157|1286|2375241.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|157|1286|2375241.jpg|0:person|looking at|2:sea|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|158|975|2359797.jpg|3:person|carrying|14:backpack|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000009||
|158|975|2359797.jpg|8:person|carrying|15:backpack|endpoint_missing_or_wrong_class|11:person[mask2former_thing]mask2former:000:000021||
|158|975|2359797.jpg|14:backpack|on back of|3:person|endpoint_missing_or_wrong_class||3:person[mask2former_thing]mask2former:000:000009|
|161|859|2354354.jpg|3:person|running on|16:pavement|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000007||
|161|859|2354354.jpg|4:person|holding|12:umbrella|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000009||
|161|859|2354354.jpg|4:person|on|16:pavement|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000009||
|161|859|2354354.jpg|5:person|walking on|16:pavement|endpoint_missing_or_wrong_class|9:person[mask2former_thing]mask2former:000:000019||
|165|2125|2416928.jpg|9:person|leaning on|15:truck|wrong_predicate|12:person[mask2former_thing]mask2former:000:000017|13:truck[mask2former_thing]mask2former:007:000004|
|165|2125|2416928.jpg|10:person|wearing|16:tree|endpoint_missing_or_wrong_class|8:person[mask2former_thing]mask2former:000:000012||
|165|2125|2416928.jpg|13:person|standing on|15:truck|endpoint_missing_or_wrong_class||13:truck[mask2former_thing]mask2former:007:000004|
|166|955|2358756.jpg|0:person|holding|1:frisbee|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|166|955|2358756.jpg|0:person|throwing|1:frisbee|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|166|955|2358756.jpg|0:person|holding|2:frisbee|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|166|955|2358756.jpg|0:person|attached to|3:tree|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|166|955|2358756.jpg|0:person|standing on|4:dirt|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|167|2029|2411534.jpg|0:person|looking at|1:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:sports ball[mask2former_thing]mask2former:032:000001|
|167|2029|2411534.jpg|0:person|about to hit|1:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:sports ball[mask2former_thing]mask2former:032:000001|
|167|2029|2411534.jpg|0:person|standing on|3:playingfield|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|170|658|2345182.jpg|2:person|standing on|22:grass|endpoint_missing_or_wrong_class|8:person[mask2former_thing]mask2former:000:000011||
|170|658|2345182.jpg|6:person|touching|15:kite|endpoint_missing_or_wrong_class|15:person[mask2former_thing]mask2former:000:000022||
|170|658|2345182.jpg|6:person|holding|18:bottle|endpoint_missing_or_wrong_class|15:person[mask2former_thing]mask2former:000:000022||
|170|658|2345182.jpg|6:person|holding|19:bottle|endpoint_missing_or_wrong_class|15:person[mask2former_thing]mask2former:000:000022||
|170|658|2345182.jpg|6:person|walking on|22:grass|endpoint_missing_or_wrong_class|15:person[mask2former_thing]mask2former:000:000022||
|170|658|2345182.jpg|7:person|in front of|10:person|wrong_predicate|2:person[mask2former_thing]mask2former:000:000003|0:person[mask2former_thing]mask2former:000:000001|
|170|658|2345182.jpg|10:person|beside|6:person|rank_below50|0:person[mask2former_thing]mask2former:000:000001|15:person[mask2former_thing]mask2former:000:000022|
|172|1608|2390659.jpg|0:person|lying on|34:rug|endpoint_missing_or_wrong_class|||
|172|1608|2390659.jpg|2:person|lying on|34:rug|endpoint_missing_or_wrong_class|||
|172|1608|2390659.jpg|8:person|holding|24:tennis racket|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|172|1608|2390659.jpg|8:person|standing on|29:playingfield|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|173|417|2332914.jpg|0:person|standing on|8:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000006||
|173|417|2332914.jpg|0:person|in front of|9:building|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000006||
|175|1343|2378563.jpg|0:person|beside|4:motorcycle|endpoint_missing_or_wrong_class|||
|175|1343|2378563.jpg|0:person|standing on|8:pavement|endpoint_missing_or_wrong_class|||
|175|1343|2378563.jpg|4:motorcycle|beside|0:person|endpoint_missing_or_wrong_class|||
|183|1866|2403494.jpg|11:person|wearing|19:skis|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000011||
|183|1866|2403494.jpg|12:person|standing on|18:skis|endpoint_missing_or_wrong_class|8:person[mask2former_thing]mask2former:000:000015||
|184|325|2328153.jpg|1:person|standing on|6:building|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|184|325|2328153.jpg|2:elephant|in front of|0:person|wrong_predicate|3:elephant[mask2former_thing]mask2former:020:000004|0:person[mask2former_thing]mask2former:000:000003|
|185|15|1159597.jpg|0:person|guiding|5:horse|wrong_predicate|1:person[mask2former_thing]mask2former:000:000008|4:horse[mask2former_thing]mask2former:017:000007|
|188|1302|2376309.jpg|0:person|standing on|1:skis|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:skis[mask2former_thing]mask2former:030:000003|
|188|1302|2376309.jpg|0:person|playing|1:skis|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:skis[mask2former_thing]mask2former:030:000003|
|188|1302|2376309.jpg|0:person|looking at|2:snow|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|190|283|2326062.jpg|0:person|on|27:pavement|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000011||
|190|283|2326062.jpg|0:person|walking on|27:pavement|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000011||
|190|283|2326062.jpg|3:person|sitting on|13:bench|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000012||
|190|283|2326062.jpg|3:person|on|27:pavement|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000012||
|190|283|2326062.jpg|9:person|looking at|10:person|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000008||
|190|283|2326062.jpg|9:person|holding|17:handbag|wrong_predicate|2:person[mask2former_thing]mask2former:000:000008|11:handbag[mask2former_thing]mask2former:026:000004|
|190|283|2326062.jpg|9:person|walking on|27:pavement|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000008||
|190|283|2326062.jpg|12:person|on|27:pavement|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000002||
|190|283|2326062.jpg|21:handbag|hanging from|3:person|endpoint_missing_or_wrong_class||6:person[mask2former_thing]mask2former:000:000012|
|190|283|2326062.jpg|22:handbag|hanging from|9:person|wrong_predicate|14:handbag[mask2former_thing]mask2former:026:000017|2:person[mask2former_thing]mask2former:000:000008|
|190|283|2326062.jpg|28:paper|beside|3:person|endpoint_missing_or_wrong_class||6:person[mask2former_thing]mask2former:000:000012|
|192|2020|2411218.jpg|2:person|on|15:sand|endpoint_missing_or_wrong_class|||
|194|1135|2367479.jpg|5:person|looking at|3:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|3:person[mask2former_thing]mask2former:000:000005|
|194|1135|2367479.jpg|5:person|holding|7:handbag|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|194|1135|2367479.jpg|7:handbag|in front of|3:person|endpoint_missing_or_wrong_class||3:person[mask2former_thing]mask2former:000:000005|
|195|1382|2380359.jpg|0:person|walking on|27:pavement|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000021||
|195|1382|2380359.jpg|1:person|in front of|23:door|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000015||
|195|1382|2380359.jpg|1:person|in front of|25:ceiling|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000015||
|195|1382|2380359.jpg|2:person|sitting on|4:person|endpoints_collapsed_to_same_box|0:person[mask2former_thing]mask2former:000:000002|0:person[mask2former_thing]mask2former:000:000002|
|197|368|2330400.jpg|0:person|going down|4:snow|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|197|368|2330400.jpg|1:person|holding|2:skis|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|3:skis[mask2former_thing]mask2former:030:000003|
|197|368|2330400.jpg|1:person|jumping over|4:snow|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|198|1076|2364558.jpg|0:person|about to hit|1:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:sports ball[mask2former_thing]mask2former:032:000001|
|198|1076|2364558.jpg|0:person|attached to|2:tennis racket|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:tennis racket[mask2former_thing]mask2former:038:000005|
|198|1076|2364558.jpg|0:person|standing on|3:playingfield|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|198|1076|2364558.jpg|0:person|in front of|4:wall|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|201|970|2359437.jpg|0:person|picking|1:pizza|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|1:pizza[mask2former_thing]mask2former:053:000002|
|203|806|2351780.jpg|1:person|on|12:playingfield|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000003||
|203|806|2351780.jpg|2:person|wearing|11:baseball glove|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|8:baseball glove[mask2former_thing]mask2former:035:000006|
|203|806|2351780.jpg|2:person|on|12:playingfield|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000002||
|203|806|2351780.jpg|3:person|about to hit|9:sports ball|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000004||
|203|806|2351780.jpg|3:person|holding|10:baseball bat|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000004||
|203|806|2351780.jpg|3:person|swinging|10:baseball bat|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000004||
|203|806|2351780.jpg|5:person|on|12:playingfield|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000008||
|206|1401|2381176.jpg|4:sky|over|1:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000001|
|207|1111|2366320.jpg|0:person|in front of|2:wall|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|210|105|2316316.jpg|1:person|holding|19:handbag|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|21:handbag[mask2former_thing]mask2former:026:000007|
|210|105|2316316.jpg|1:person|on|22:road|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000002||
|210|105|2316316.jpg|1:person|walking on|22:road|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000002||
|210|105|2316316.jpg|6:person|in front of|12:person|endpoint_missing_or_wrong_class||6:person[mask2former_thing]mask2former:000:000014|
|210|105|2316316.jpg|6:person|sitting on|17:motorcycle|endpoint_missing_or_wrong_class||20:motorcycle[mask2former_thing]mask2former:003:000013|
|210|105|2316316.jpg|11:person|riding|15:bicycle|endpoint_missing_or_wrong_class|||
|210|105|2316316.jpg|12:person|riding|17:motorcycle|wrong_predicate|6:person[mask2former_thing]mask2former:000:000014|20:motorcycle[mask2former_thing]mask2former:003:000013|
|210|105|2316316.jpg|13:person|walking on|22:road|endpoint_missing_or_wrong_class|||
|210|105|2316316.jpg|25:sky|over|6:person|endpoint_missing_or_wrong_class|||
|211|1563|2388324.jpg|0:person|in|10:tv|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|8:tv[mask2former_thing]mask2former:062:000005|
|211|1563|2388324.jpg|0:person|playing|10:tv|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|8:tv[mask2former_thing]mask2former:062:000005|
|211|1563|2388324.jpg|0:person|holding|11:remote|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|213|1476|2384904.jpg|0:person|playing with|2:frisbee|wrong_predicate|1:person[mask2former_thing]mask2former:000:000005|2:frisbee[mask2former_thing]mask2former:029:000004|
|213|1476|2384904.jpg|1:person|chasing|0:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:person[mask2former_thing]mask2former:000:000005|
|216|1890|2404890.jpg|0:person|in|2:train|endpoint_missing_or_wrong_class||0:train[mask2former_thing]mask2former:006:000003|
|216|1890|2404890.jpg|1:person|driving|2:train|endpoint_missing_or_wrong_class||0:train[mask2former_thing]mask2former:006:000003|
|219|316|2327752.jpg|0:person|walking on|15:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000006||
|225|1317|2377220.jpg|1:person|in|10:train|endpoint_missing_or_wrong_class||1:train[mask2former_thing]mask2former:006:000003|
|225|1317|2377220.jpg|3:person|driving|10:train|endpoint_missing_or_wrong_class||1:train[mask2former_thing]mask2former:006:000003|
|225|1317|2377220.jpg|6:person|in|10:train|endpoint_missing_or_wrong_class||1:train[mask2former_thing]mask2former:006:000003|
|225|1317|2377220.jpg|9:person|in|10:train|endpoint_missing_or_wrong_class||1:train[mask2former_thing]mask2former:006:000003|
|226|2126|2416964.jpg|0:person|picking|14:suitcase|endpoint_missing_or_wrong_class|||
|227|1607|2390654.jpg|1:person|standing on|9:sand|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000007||
|227|1607|2390654.jpg|1:person|in front of|10:sea|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000007||
|227|1607|2390654.jpg|3:person|running on|9:sand|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000006||
|227|1607|2390654.jpg|4:person|playing with|5:person|wrong_predicate|6:person[mask2former_thing]mask2former:000:000012|1:person[mask2former_thing]mask2former:000:000002|
|228|2144|285721.jpg|0:person|holding|2:cell phone|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|228|2144|285721.jpg|0:person|carrying|2:cell phone|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|228|2144|285721.jpg|0:person|talking to|2:cell phone|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|228|2144|285721.jpg|0:person|in front of|3:wall|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|228|2144|285721.jpg|0:person|leaning on|3:wall|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|229|1350|2378868.jpg|1:person|in|2:car|endpoint_missing_or_wrong_class||1:car[mask2former_thing]mask2former:002:000006|
|230|723|2348265.jpg|5:person|on|13:bridge|endpoint_missing_or_wrong_class|||
|230|723|2348265.jpg|6:person|over|14:river|endpoint_missing_or_wrong_class|||
|231|684|2346411.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|231|684|2346411.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|231|684|2346411.jpg|0:person|over|2:sea|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|231|684|2346411.jpg|0:person|looking at|2:sea|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|233|1337|2378360.jpg|0:person|playing|1:surfboard|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|233|1337|2378360.jpg|0:person|riding|1:surfboard|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|233|1337|2378360.jpg|0:person|on|2:sea|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|233|1337|2378360.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000003|
|235|2050|2412773.jpg|0:person|attached to|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|235|2050|2412773.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|235|2050|2412773.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|235|2050|2412773.jpg|0:person|attached to|2:sea|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|235|2050|2412773.jpg|0:person|touching|2:sea|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|235|2050|2412773.jpg|0:person|in front of|3:rock|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|236|561|2340111.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:surfboard[mask2former_thing]mask2former:037:000003|
|236|561|2340111.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:surfboard[mask2former_thing]mask2former:037:000003|
|236|561|2340111.jpg|0:person|over|2:sea|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|243|1591|2389803.jpg|0:person|on|9:boat|endpoint_missing_or_wrong_class||1:boat[mask2former_thing]mask2former:008:000003|
|243|1591|2389803.jpg|0:person|sitting on|9:boat|endpoint_missing_or_wrong_class||1:boat[mask2former_thing]mask2former:008:000003|
|243|1591|2389803.jpg|1:person|on|9:boat|endpoint_missing_or_wrong_class||1:boat[mask2former_thing]mask2former:008:000003|
|243|1591|2389803.jpg|1:person|sitting on|9:boat|endpoint_missing_or_wrong_class||1:boat[mask2former_thing]mask2former:008:000003|
|244|603|2342677.jpg|0:person|sitting on|1:bed|endpoint_missing_or_wrong_class||0:bed[mask2former_thing]mask2former:059:000002|
|244|603|2342677.jpg|0:person|looking at|2:laptop|endpoint_missing_or_wrong_class||1:laptop[mask2former_thing]mask2former:063:000001|
|244|603|2342677.jpg|0:person|beside|4:door|endpoint_missing_or_wrong_class|||
|244|603|2342677.jpg|0:person|holding|7:wall|endpoint_missing_or_wrong_class|||
|244|603|2342677.jpg|3:blanket|over|0:person|endpoint_missing_or_wrong_class|||
|244|603|2342677.jpg|7:wall|on back of|0:person|endpoint_missing_or_wrong_class|||
|247|1380|2380325.jpg|0:person|beside|2:car|endpoint_missing_or_wrong_class|||
|247|1380|2380325.jpg|2:car|beside|0:person|endpoint_missing_or_wrong_class|||
|249|520|2337500.jpg|0:person|driving|6:car|endpoint_missing_or_wrong_class||2:car[mask2former_thing]mask2former:002:000010|
|251|1509|2386257.jpg|0:person|attached to|1:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:person[mask2former_thing]mask2former:000:000003|
|251|1509|2386257.jpg|0:person|playing with|2:teddy bear|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|2:teddy bear[mask2former_thing]mask2former:077:000001|
|251|1509|2386257.jpg|1:person|attached to|0:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|0:person[mask2former_thing]mask2former:000:000002|
|251|1509|2386257.jpg|1:person|attached to|2:teddy bear|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|2:teddy bear[mask2former_thing]mask2former:077:000001|
|251|1509|2386257.jpg|2:teddy bear|attached to|1:person|wrong_predicate|2:teddy bear[mask2former_thing]mask2former:077:000001|1:person[mask2former_thing]mask2former:000:000003|
|253|1589|2389680.jpg|0:person|beside|12:stairs|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000015||
|253|1589|2389680.jpg|0:person|beside|13:water|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000015||
|253|1589|2389680.jpg|2:person|sitting on|8:bench|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000010||
|253|1589|2389680.jpg|2:person|holding|11:cell phone|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000010||
|253|1589|2389680.jpg|2:person|looking at|11:cell phone|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000010||
|253|1589|2389680.jpg|4:person|looking at|0:person|wrong_predicate|3:person[mask2former_thing]mask2former:000:000013|4:person[mask2former_thing]mask2former:000:000015|
|253|1589|2389680.jpg|4:person|beside|12:stairs|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000013||
|253|1589|2389680.jpg|4:person|beside|13:water|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000013||
|254|896|2356062.jpg|1:person|beside|25:flower|endpoint_missing_or_wrong_class|14:person[mask2former_thing]mask2former:000:000022||
|254|896|2356062.jpg|1:person|in front of|26:tree|endpoint_missing_or_wrong_class|14:person[mask2former_thing]mask2former:000:000022||
|254|896|2356062.jpg|5:person|walking on|28:grass|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000005||
|254|896|2356062.jpg|7:person|holding|18:teddy bear|endpoint_missing_or_wrong_class|7:person[mask2former_thing]mask2former:000:000013||
|254|896|2356062.jpg|7:person|holding|22:teddy bear|endpoint_missing_or_wrong_class|7:person[mask2former_thing]mask2former:000:000013||
|254|896|2356062.jpg|8:person|walking on|28:grass|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000009||
|254|896|2356062.jpg|10:person|sitting on|24:blanket|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|258|388|2331571.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000004|
|258|388|2331571.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000004|
|258|388|2331571.jpg|0:person|on|2:sea|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|259|826|2352851.jpg|0:person|standing on|2:sand|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|259|826|2352851.jpg|0:person|beside|3:sea|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|259|826|2352851.jpg|0:person|looking at|3:sea|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|262|621|2343341.jpg|0:person|throwing|4:sports ball|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000005||
|262|621|2343341.jpg|1:person|about to hit|4:sports ball|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000007||
|262|621|2343341.jpg|1:person|standing on|11:dirt|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000007||
|263|2037|2412228.jpg|8:motorcycle|in front of|4:person|wrong_predicate|7:motorcycle[mask2former_thing]mask2former:003:000002|3:person[mask2former_thing]mask2former:000:000007|
|267|1327|2377789.jpg|12:backpack|beside|3:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000004|
|267|1327|2377789.jpg|13:handbag|beside|3:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000004|
|269|133|2317501.jpg|1:person|guiding|6:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|10:person[mask2former_thing]mask2former:000:000016|
|269|133|2317501.jpg|2:person|beside|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000001|
|269|133|2317501.jpg|2:person|holding|9:person|endpoint_missing_or_wrong_class||3:person[mask2former_thing]mask2former:000:000004|
|271|1757|2397709.jpg|0:person|playing|1:sports ball|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|271|1757|2397709.jpg|0:person|holding|2:tennis racket|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:tennis racket[mask2former_thing]mask2former:038:000004|
|271|1757|2397709.jpg|0:person|standing on|3:playingfield|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|272|1688|2394464.jpg|0:person|sitting on|6:chair|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000007||
|276|1693|2394673.jpg|0:person|playing|1:skis|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:skis[mask2former_thing]mask2former:030:000003|
|276|1693|2394673.jpg|1:skis|attached to|0:person|wrong_predicate|1:skis[mask2former_thing]mask2former:030:000003|0:person[mask2former_thing]mask2former:000:000002|
|277|1237|2372495.jpg|0:person|holding|15:tennis racket|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000011||
|277|1237|2372495.jpg|0:person|standing on|26:playingfield|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000011||
|277|1237|2372495.jpg|3:person|looking at|0:person|wrong_predicate|18:person[mask2former_thing]mask2former:000:000032|4:person[mask2former_thing]mask2former:000:000011|
|277|1237|2372495.jpg|3:person|talking to|0:person|wrong_predicate|18:person[mask2former_thing]mask2former:000:000032|4:person[mask2former_thing]mask2former:000:000011|
|277|1237|2372495.jpg|3:person|holding|14:tennis racket|endpoint_missing_or_wrong_class|18:person[mask2former_thing]mask2former:000:000032||
|277|1237|2372495.jpg|7:person|beside|9:person|wrong_predicate|8:person[mask2former_thing]mask2former:000:000017|13:person[mask2former_thing]mask2former:000:000024|
|281|1203|2371154.jpg|0:person|on|8:snow|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|281|1203|2371154.jpg|1:person|on|4:snowboard|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|281|1203|2371154.jpg|1:person|playing|4:snowboard|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|281|1203|2371154.jpg|3:person|standing on|5:snowboard|wrong_predicate|2:person[mask2former_thing]mask2former:000:000007|6:snowboard[mask2former_thing]mask2former:031:000006|
|283|673|2345745.jpg|0:person|looking at|3:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|2:person[mask2former_thing]mask2former:000:000009|
|283|673|2345745.jpg|1:person|looking at|3:person|wrong_predicate|4:person[mask2former_thing]mask2former:000:000019|2:person[mask2former_thing]mask2former:000:000009|
|283|673|2345745.jpg|2:person|looking at|3:person|rank_below50|1:person[mask2former_thing]mask2former:000:000004|2:person[mask2former_thing]mask2former:000:000009|
|287|2058|2413475.jpg|0:person|catching|1:frisbee|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:frisbee[mask2former_thing]mask2former:029:000003|
|287|2058|2413475.jpg|0:person|playing|1:frisbee|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:frisbee[mask2former_thing]mask2former:029:000003|
|287|2058|2413475.jpg|0:person|standing on|3:grass|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|292|551|2339515.jpg|0:person|looking at|14:river|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000014||
|292|551|2339515.jpg|2:person|looking at|8:cow|endpoint_missing_or_wrong_class||8:cow[mask2former_thing]mask2former:019:000012|
|292|551|2339515.jpg|6:cow|looking at|0:person|endpoint_missing_or_wrong_class||1:person[mask2former_thing]mask2former:000:000014|
|293|495|2336518.jpg|2:person|holding|14:cell phone|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000006||
|293|495|2336518.jpg|2:person|looking at|14:cell phone|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000006||
|293|495|2336518.jpg|7:person|talking to|3:person|endpoint_missing_or_wrong_class|||
|293|495|2336518.jpg|8:person|sitting on|13:couch|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|293|495|2336518.jpg|8:person|looking at|15:table|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|296|1346|2378709.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|296|1346|2378709.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|301|1633|2391614.jpg|0:person|holding|7:food|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000005||
|301|1633|2391614.jpg|1:oven|in front of|0:person|wrong_predicate|6:oven[mask2former_thing]mask2former:069:000011|0:person[mask2former_thing]mask2former:000:000005|
|302|1396|2381002.jpg|2:person|riding|5:bicycle|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000016||
|302|1396|2381002.jpg|2:person|carrying|14:backpack|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000016||
|302|1396|2381002.jpg|3:person|standing on|19:pavement|endpoint_missing_or_wrong_class|||
|302|1396|2381002.jpg|4:person|standing on|17:road|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000008||
|304|1427|2382463.jpg|0:person|sitting on|2:boat|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|304|1427|2382463.jpg|1:person|standing on|2:boat|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|304|1427|2382463.jpg|1:person|driving|2:boat|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|304|1427|2382463.jpg|1:person|holding|3:cell phone|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|304|1427|2382463.jpg|1:person|wearing|4:sea|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|306|1259|2373413.jpg|0:person|leaning on|1:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000004|0:person[mask2former_thing]mask2former:000:000001|
|306|1259|2373413.jpg|0:person|on|3:road|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000004||
|306|1259|2373413.jpg|1:person|standing on|3:road|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|308|1185|2370070.jpg|1:person|talking to|3:person|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000012||
|308|1185|2370070.jpg|1:person|holding|20:backpack|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000012||
|308|1185|2370070.jpg|2:person|looking at|29:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|308|1185|2370070.jpg|4:person|looking at|29:pavement|endpoint_missing_or_wrong_class|8:person[mask2former_thing]mask2former:000:000019||
|308|1185|2370070.jpg|6:person|talking to|25:cell phone|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000007||
|308|1185|2370070.jpg|6:person|walking on|29:pavement|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000007||
|308|1185|2370070.jpg|7:person|standing on|29:pavement|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000009||
|312|52|1592452.jpg|2:person|talking to|1:person|endpoint_missing_or_wrong_class|8:person[mask2former_thing]mask2former:000:000015||
|312|52|1592452.jpg|6:person|in|10:person|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000004||
|312|52|1592452.jpg|7:person|wearing|10:person|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000002||
|312|52|1592452.jpg|8:person|walking on|18:pavement|endpoint_missing_or_wrong_class|||
|315|1206|2371236.jpg|2:person|walking on|25:floor|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000009||
|315|1206|2371236.jpg|5:person|in front of|2:person|wrong_predicate|12:person[mask2former_thing]mask2former:000:000020|6:person[mask2former_thing]mask2former:000:000009|
|315|1206|2371236.jpg|5:person|beside|3:person|wrong_predicate|12:person[mask2former_thing]mask2former:000:000020|10:person[mask2former_thing]mask2former:000:000018|
|315|1206|2371236.jpg|5:person|carrying|16:handbag|endpoint_missing_or_wrong_class|12:person[mask2former_thing]mask2former:000:000020||
|315|1206|2371236.jpg|5:person|walking on|25:floor|endpoint_missing_or_wrong_class|12:person[mask2former_thing]mask2former:000:000020||
|315|1206|2371236.jpg|9:person|beside|0:person|endpoint_missing_or_wrong_class||2:person[mask2former_thing]mask2former:000:000004|
|315|1206|2371236.jpg|11:person|standing on|25:floor|endpoint_missing_or_wrong_class|9:person[mask2former_thing]mask2former:000:000014||
|315|1206|2371236.jpg|24:ceiling|over|11:person|endpoint_missing_or_wrong_class||9:person[mask2former_thing]mask2former:000:000014|
|321|49|1592294.jpg|1:person|riding|14:bicycle|endpoint_missing_or_wrong_class||8:bicycle[mask2former_thing]mask2former:001:000018|
|321|49|1592294.jpg|1:person|crossing|38:road|endpoint_missing_or_wrong_class|||
|321|49|1592294.jpg|3:person|standing on|38:road|endpoint_missing_or_wrong_class|||
|321|49|1592294.jpg|8:person|walking on|7:person|endpoint_missing_or_wrong_class||6:person[mask2former_thing]mask2former:000:000026|
|321|49|1592294.jpg|8:person|looking at|15:bicycle|endpoint_missing_or_wrong_class||7:bicycle[mask2former_thing]mask2former:001:000016|
|325|703|2347159.jpg|1:person|looking at|8:railroad|endpoint_missing_or_wrong_class|||
|325|703|2347159.jpg|2:person|walking on|8:railroad|endpoint_missing_or_wrong_class|||
|325|703|2347159.jpg|6:person|standing on|8:railroad|endpoint_missing_or_wrong_class|||
|327|574|2340907.jpg|0:person|standing on|11:floor|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|327|574|2340907.jpg|2:person|playing|3:sports ball|wrong_predicate|2:person[mask2former_thing]mask2former:000:000006|3:sports ball[mask2former_thing]mask2former:032:000003|
|328|2111|2416290.jpg|0:person|wearing|24:wall-wood|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000021||
|328|2111|2416290.jpg|2:person|holding|12:pizza|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|328|2111|2416290.jpg|2:person|cooking|12:pizza|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|328|2111|2416290.jpg|2:person|wearing|24:wall-wood|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|328|2111|2416290.jpg|3:person|picking|19:cardboard|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000012||
|328|2111|2416290.jpg|3:person|wearing|23:towel|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000012||
|328|2111|2416290.jpg|6:person|looking at|1:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000005|3:person[mask2former_thing]mask2former:000:000014|
|328|2111|2416290.jpg|6:person|eating|11:pizza|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|330|1919|2406484.jpg|9:person|in front of|11:person|endpoint_missing_or_wrong_class||2:person[mask2former_thing]mask2former:000:000011|
|331|284|2326073.jpg|0:person|driving|2:airplane|endpoint_missing_or_wrong_class||0:airplane[mask2former_thing]mask2former:004:000005|
|331|284|2326073.jpg|1:person|in|2:airplane|endpoint_missing_or_wrong_class||0:airplane[mask2former_thing]mask2former:004:000005|
|332|1415|2382040.jpg|2:person|in front of|0:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:person[mask2former_thing]mask2former:000:000006|
|332|1415|2382040.jpg|2:person|sitting on|4:chair|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|3:chair[mask2former_thing]mask2former:056:000007|
|332|1415|2382040.jpg|5:dining table|in front of|1:person|wrong_predicate|4:dining table[mask2former_thing]mask2former:060:000002|1:person[mask2former_thing]mask2former:000:000004|
|333|1739|2397128.jpg|0:person|attached to|1:horse|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:horse[mask2former_thing]mask2former:017:000005|
|333|1739|2397128.jpg|0:person|sitting on|1:horse|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:horse[mask2former_thing]mask2former:017:000005|
|335|303|2326982.jpg|1:donut|attached to|0:person|wrong_predicate|1:donut[mask2former_thing]mask2former:054:000002|0:person[mask2former_thing]mask2former:000:000001|
|342|1241|2372547.jpg|0:person|touching|1:kite|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:kite[mask2former_thing]mask2former:033:000004|
|342|1241|2372547.jpg|0:person|sitting on|3:floor|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|342|1241|2372547.jpg|1:kite|in front of|0:person|wrong_predicate|1:kite[mask2former_thing]mask2former:033:000004|0:person[mask2former_thing]mask2former:000:000002|
|344|556|2339759.jpg|0:person|holding|1:tennis racket|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:tennis racket[mask2former_thing]mask2former:038:000003|
|344|556|2339759.jpg|0:person|jumping from|2:playingfield|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|346|377|2330880.jpg|0:person|standing on|6:building|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|347|1854|2402990.jpg|0:person|wearing|13:baseball glove|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000006||
|347|1854|2402990.jpg|2:person|leaning on|18:fence|endpoint_missing_or_wrong_class|||
|347|1854|2402990.jpg|4:person|running on|16:playingfield|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000008||
|347|1854|2402990.jpg|5:person|walking on|16:playingfield|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|348|205|2321647.jpg|2:person|standing on|21:pavement|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000004||
|348|205|2321647.jpg|3:person|carrying|18:handbag|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|15:handbag[mask2former_thing]mask2former:026:000006|
|348|205|2321647.jpg|8:person|in front of|2:person|wrong_predicate|5:person[mask2former_thing]mask2former:000:000007|3:person[mask2former_thing]mask2former:000:000004|
|348|205|2321647.jpg|8:person|standing on|21:pavement|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000007||
|348|205|2321647.jpg|12:person|carrying|16:handbag|endpoint_missing_or_wrong_class|||
|351|663|2345356.jpg|3:person|riding|21:horse|wrong_predicate|0:person[mask2former_thing]mask2former:000:000007|10:horse[mask2former_thing]mask2former:017:000008|
|353|1492|2385610.jpg|3:person|beside|15:car|endpoint_missing_or_wrong_class||9:car[mask2former_thing]mask2former:002:000015|
|353|1492|2385610.jpg|3:person|crossing|27:road|endpoint_missing_or_wrong_class|||
|353|1492|2385610.jpg|4:person|walking on|31:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|353|1492|2385610.jpg|15:car|beside|3:person|endpoint_missing_or_wrong_class|9:car[mask2former_thing]mask2former:002:000015||
|354|111|2316413.jpg|0:person|walking on|4:stairs|endpoint_missing_or_wrong_class|||
|354|111|2316413.jpg|1:person|holding|3:cell phone|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|354|111|2316413.jpg|1:person|going down|4:stairs|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|354|111|2316413.jpg|1:person|wearing|4:stairs|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|354|111|2316413.jpg|2:person|wearing|0:person|endpoint_missing_or_wrong_class|||
|354|111|2316413.jpg|8:fence|in front of|0:person|endpoint_missing_or_wrong_class|||
|357|726|2348363.jpg|5:person|in front of|14:airplane|wrong_predicate|9:person[mask2former_thing]mask2former:000:000014|11:airplane[mask2former_thing]mask2former:004:000009|
|357|726|2348363.jpg|7:person|looking at|11:person|rank_below50|2:person[mask2former_thing]mask2former:000:000003|3:person[mask2former_thing]mask2former:000:000004|
|360|1205|2371211.jpg|0:person|holding|3:book|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000007||
|360|1205|2371211.jpg|0:person|standing on|8:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000007||
|360|1205|2371211.jpg|6:tree|in front of|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000007|
|362|651|2344819.jpg|0:person|wearing|1:tie|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|362|651|2344819.jpg|3:wall|in front of|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000002|
|364|483|2335916.jpg|2:person|standing on|9:dirt|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|364|483|2335916.jpg|4:person|carrying|7:handbag|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|366|1251|2373084.jpg|0:person|standing on|9:sand|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000004||
|366|1251|2373084.jpg|3:person|talking to|0:person|wrong_predicate|3:person[mask2former_thing]mask2former:000:000007|1:person[mask2former_thing]mask2former:000:000004|
|366|1251|2373084.jpg|3:person|carrying|8:surfboard|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000007||
|366|1251|2373084.jpg|4:person|standing on|9:sand|endpoint_missing_or_wrong_class|||
|367|1950|2408290.jpg|0:person|on|1:motorcycle|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:motorcycle[mask2former_thing]mask2former:003:000003|
|367|1950|2408290.jpg|0:person|on back of|1:motorcycle|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:motorcycle[mask2former_thing]mask2former:003:000003|
|369|1390|2380682.jpg|4:person|wearing|10:person|wrong_predicate|5:person[mask2former_thing]mask2former:000:000011|7:person[mask2former_thing]mask2former:000:000014|
|369|1390|2380682.jpg|5:person|standing on|20:snow|endpoint_missing_or_wrong_class|9:person[mask2former_thing]mask2former:000:000018||
|369|1390|2380682.jpg|8:person|on|10:person|wrong_predicate|4:person[mask2former_thing]mask2former:000:000010|7:person[mask2former_thing]mask2former:000:000014|
|369|1390|2380682.jpg|10:person|walking on|20:snow|endpoint_missing_or_wrong_class|7:person[mask2former_thing]mask2former:000:000014||
|369|1390|2380682.jpg|11:person|carrying|19:snowboard|wrong_predicate|8:person[mask2former_thing]mask2former:000:000015|17:snowboard[mask2former_thing]mask2former:031:000016|
|370|56|1592537.jpg|14:tree|beside|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000003|
|371|2103|2416059.jpg|0:person|carrying|2:backpack|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|371|2103|2416059.jpg|0:person|standing on|3:skis|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:skis[mask2former_thing]mask2former:030:000004|
|371|2103|2416059.jpg|0:person|playing|3:skis|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:skis[mask2former_thing]mask2former:030:000004|
|373|775|2350750.jpg|3:person|standing on|7:platform|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000008||
|373|775|2350750.jpg|4:person|beside|6:suitcase|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000007||
|373|775|2350750.jpg|4:person|standing on|7:platform|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000007||
|373|775|2350750.jpg|6:suitcase|beside|4:person|endpoint_missing_or_wrong_class||2:person[mask2former_thing]mask2former:000:000007|
|377|1495|2385674.jpg|2:person|looking at|3:person|wrong_predicate|4:person[mask2former_thing]mask2former:000:000009|0:person[mask2former_thing]mask2former:000:000001|
|377|1495|2385674.jpg|3:person|in front of|2:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|4:person[mask2former_thing]mask2former:000:000009|
|380|581|2341544.jpg|6:person|standing on|29:pavement|endpoint_missing_or_wrong_class|14:person[mask2former_thing]mask2former:000:000021||
|380|581|2341544.jpg|10:person|carrying|23:handbag|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000005||
|381|1745|2397343.jpg|0:person|beside|1:dog|endpoint_missing_or_wrong_class||0:dog[mask2former_thing]mask2former:016:000004|
|381|1745|2397343.jpg|0:person|playing with|1:dog|endpoint_missing_or_wrong_class||0:dog[mask2former_thing]mask2former:016:000004|
|381|1745|2397343.jpg|0:person|beside|5:door|endpoint_missing_or_wrong_class|||
|381|1745|2397343.jpg|0:person|beside|7:table|endpoint_missing_or_wrong_class|||
|381|1745|2397343.jpg|2:potted plant|in front of|0:person|endpoint_missing_or_wrong_class|2:potted plant[mask2former_thing]mask2former:058:000002||
|381|1745|2397343.jpg|5:door|in|0:person|endpoint_missing_or_wrong_class|||
|381|1745|2397343.jpg|7:table|beside|0:person|endpoint_missing_or_wrong_class|||
|382|1449|2383257.jpg|0:person|playing|2:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|2:skateboard[mask2former_thing]mask2former:036:000003|
|382|1449|2383257.jpg|3:door|beside|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000001|
|382|1449|2383257.jpg|5:wall|beside|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000001|
|383|503|2336741.jpg|0:person|standing on|24:floor|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000010||
|385|12|1159501.jpg|0:person|attached to|1:person|endpoints_collapsed_to_same_box|1:person[mask2former_thing]mask2former:000:000010|1:person[mask2former_thing]mask2former:000:000010|
|385|12|1159501.jpg|0:person|looking at|3:laptop|wrong_predicate|1:person[mask2former_thing]mask2former:000:000010|4:laptop[mask2former_thing]mask2former:063:000006|
|385|12|1159501.jpg|1:person|attached to|0:person|endpoints_collapsed_to_same_box|1:person[mask2former_thing]mask2former:000:000010|1:person[mask2former_thing]mask2former:000:000010|
|385|12|1159501.jpg|1:person|looking at|3:laptop|wrong_predicate|1:person[mask2former_thing]mask2former:000:000010|4:laptop[mask2former_thing]mask2former:063:000006|
|386|1395|2380947.jpg|3:person|looking at|6:person|rank_below50|9:person[mask2former_thing]mask2former:000:000023|8:person[mask2former_thing]mask2former:000:000019|
|386|1395|2380947.jpg|6:person|talking to|11:person|wrong_predicate|8:person[mask2former_thing]mask2former:000:000019|6:person[mask2former_thing]mask2former:000:000012|
|386|1395|2380947.jpg|6:person|attached to|14:tennis racket|wrong_predicate|8:person[mask2former_thing]mask2former:000:000019|16:tennis racket[mask2former_thing]mask2former:038:000032|
|386|1395|2380947.jpg|6:person|holding|14:tennis racket|wrong_predicate|8:person[mask2former_thing]mask2former:000:000019|16:tennis racket[mask2former_thing]mask2former:038:000032|
|386|1395|2380947.jpg|6:person|standing on|17:playingfield|endpoint_missing_or_wrong_class|8:person[mask2former_thing]mask2former:000:000019||
|386|1395|2380947.jpg|12:person|talking to|4:person|endpoint_missing_or_wrong_class|10:person[mask2former_thing]mask2former:000:000024||
|387|1391|2380691.jpg|0:person|looking at|1:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:sports ball[mask2former_thing]mask2former:032:000001|
|387|1391|2380691.jpg|0:person|chasing|1:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:sports ball[mask2former_thing]mask2former:032:000001|
|387|1391|2380691.jpg|0:person|about to hit|1:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:sports ball[mask2former_thing]mask2former:032:000001|
|387|1391|2380691.jpg|0:person|running on|4:floor|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|389|1609|2390707.jpg|6:person|in front of|8:person|wrong_predicate|3:person[mask2former_thing]mask2former:000:000008|2:person[mask2former_thing]mask2former:000:000004|
|389|1609|2390707.jpg|6:person|beside|16:chair|wrong_predicate|3:person[mask2former_thing]mask2former:000:000008|17:chair[mask2former_thing]mask2former:056:000011|
|389|1609|2390707.jpg|6:person|attached to|21:playingfield|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000008||
|389|1609|2390707.jpg|6:person|attached to|22:towel|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000008||
|389|1609|2390707.jpg|6:person|swinging|22:towel|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000008||
|389|1609|2390707.jpg|7:person|standing on|21:playingfield|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|389|1609|2390707.jpg|9:person|standing on|21:playingfield|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000017||
|389|1609|2390707.jpg|16:chair|beside|6:person|rank_below50|17:chair[mask2former_thing]mask2former:056:000011|3:person[mask2former_thing]mask2former:000:000008|
|394|1496|2385703.jpg|0:person|carrying|6:handbag|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000005||
|395|758|2350121.jpg|0:person|riding|3:horse|endpoint_missing_or_wrong_class||1:horse[mask2former_thing]mask2former:017:000002|
|395|758|2350121.jpg|1:person|on back of|5:horse|endpoint_missing_or_wrong_class||2:horse[mask2former_thing]mask2former:017:000005|
|395|758|2350121.jpg|1:person|riding|5:horse|endpoint_missing_or_wrong_class||2:horse[mask2former_thing]mask2former:017:000005|
|395|758|2350121.jpg|2:person|on back of|4:horse|endpoint_missing_or_wrong_class||1:horse[mask2former_thing]mask2former:017:000002|
|396|630|2343959.jpg|5:person|in front of|8:person|wrong_predicate|4:person[mask2former_thing]mask2former:000:000006|2:person[mask2former_thing]mask2former:000:000004|
|396|630|2343959.jpg|5:person|wearing|15:tie|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000006||
|396|630|2343959.jpg|8:person|in front of|19:mirror|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000004||
|396|630|2343959.jpg|9:person|looking at|8:person|wrong_predicate|6:person[mask2former_thing]mask2former:000:000010|2:person[mask2former_thing]mask2former:000:000004|
|396|630|2343959.jpg|9:person|beside|10:person|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000010||
|396|630|2343959.jpg|9:person|wearing|14:tie|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000010||
|396|630|2343959.jpg|10:person|wearing|12:tie|endpoint_missing_or_wrong_class|||
|396|630|2343959.jpg|10:person|beside|16:dining table|endpoint_missing_or_wrong_class|||
|396|630|2343959.jpg|18:light|over|8:person|endpoint_missing_or_wrong_class||2:person[mask2former_thing]mask2former:000:000004|
|398|1128|2366957.jpg|4:person|looking at|30:pavement|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000015||
|398|1128|2366957.jpg|13:person|in front of|28:tree|endpoint_missing_or_wrong_class|||
|399|1835|2402046.jpg|1:person|standing on|17:rock|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000008||
|399|1835|2402046.jpg|9:person|entering|13:boat|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|5:boat[mask2former_thing]mask2former:008:000005|
|399|1835|2402046.jpg|11:person|standing on|13:boat|endpoint_missing_or_wrong_class||5:boat[mask2former_thing]mask2former:008:000005|
|400|731|2348722.jpg|3:person|wearing|17:baseball glove|endpoint_missing_or_wrong_class|15:person[mask2former_thing]mask2former:000:000021||
|400|731|2348722.jpg|4:person|carrying|16:baseball bat|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000009||
|400|731|2348722.jpg|6:person|talking to|5:person|endpoint_missing_or_wrong_class|||
|400|731|2348722.jpg|7:person|running on|19:playingfield|endpoint_missing_or_wrong_class|8:person[mask2former_thing]mask2former:000:000012||
|400|731|2348722.jpg|8:person|standing on|19:playingfield|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000002||
|404|736|2348945.jpg|0:person|talking to|1:person|endpoint_missing_or_wrong_class||1:person[mask2former_thing]mask2former:000:000008|
|404|736|2348945.jpg|0:person|standing on|5:truck|endpoint_missing_or_wrong_class||4:truck[mask2former_thing]mask2former:007:000006|
|404|736|2348945.jpg|1:person|standing on|9:pavement|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000008||
|406|1324|2377760.jpg|0:person|on|1:truck|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|406|1324|2377760.jpg|0:person|sitting on|1:truck|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|406|1324|2377760.jpg|0:person|beside|2:suitcase|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:suitcase[mask2former_thing]mask2former:028:000008|
|410|761|2350256.jpg|0:person|in|1:bus|endpoint_missing_or_wrong_class||1:bus[mask2former_thing]mask2former:005:000006|
|410|761|2350256.jpg|0:person|driving|1:bus|endpoint_missing_or_wrong_class||1:bus[mask2former_thing]mask2former:005:000006|
|413|280|2325881.jpg|0:person|eating|1:banana|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:banana[mask2former_thing]mask2former:046:000001|
|413|280|2325881.jpg|0:person|sitting on|2:chair|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|413|280|2325881.jpg|0:person|in front of|4:wall-wood|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|414|1318|2377223.jpg|0:person|in front of|1:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000004|2:person[mask2former_thing]mask2former:000:000006|
|414|1318|2377223.jpg|0:person|swinging|4:tennis racket|wrong_predicate|1:person[mask2former_thing]mask2former:000:000004|7:tennis racket[mask2former_thing]mask2former:038:000002|
|414|1318|2377223.jpg|1:person|in front of|6:wall|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000006||
|414|1318|2377223.jpg|3:sports ball|beside|2:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000001|
|415|1211|2371415.jpg|0:person|holding|1:cell phone|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|415|1211|2371415.jpg|4:wall|enclosing|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000001|
|417|1547|2387788.jpg|0:person|standing on|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|1:skateboard[mask2former_thing]mask2former:036:000003|
|417|1547|2387788.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|1:skateboard[mask2former_thing]mask2former:036:000003|
|417|1547|2387788.jpg|0:person|wearing|2:platform|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|417|1547|2387788.jpg|0:person|wearing|3:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|419|962|2359075.jpg|5:person|standing on|12:dirt|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000006||
|419|962|2359075.jpg|6:person|standing on|12:dirt|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|419|962|2359075.jpg|11:fence|in front of|5:person|endpoint_missing_or_wrong_class||2:person[mask2former_thing]mask2former:000:000006|
|419|962|2359075.jpg|11:fence|in front of|6:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000001|
|421|1772|2398484.jpg|0:person|on back of|2:person|wrong_predicate|2:person[mask2former_thing]mask2former:000:000005|0:person[mask2former_thing]mask2former:000:000001|
|421|1772|2398484.jpg|1:person|holding|3:baseball bat|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|3:baseball bat[mask2former_thing]mask2former:034:000006|
|421|1772|2398484.jpg|1:person|standing on|5:playingfield|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|421|1772|2398484.jpg|2:person|attached to|0:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|2:person[mask2former_thing]mask2former:000:000005|
|421|1772|2398484.jpg|2:person|wearing|4:baseball glove|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|4:baseball glove[mask2former_thing]mask2former:035:000004|
|422|1007|2361180.jpg|1:person|walking on|6:pavement|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000010||
|422|1007|2361180.jpg|2:person|walking on|6:pavement|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000006||
|422|1007|2361180.jpg|3:person|in front of|1:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000005|6:person[mask2former_thing]mask2former:000:000010|
|422|1007|2361180.jpg|4:person|talking to|0:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|7:person[mask2former_thing]mask2former:000:000012|
|422|1007|2361180.jpg|4:person|standing on|6:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|423|2171|713172.jpg|0:person|in|13:building|endpoint_missing_or_wrong_class|||
|427|361|2329834.jpg|0:person|looking at|14:laptop|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000008||
|427|361|2329834.jpg|0:person|in front of|15:wall-wood|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000008||
|427|361|2329834.jpg|0:person|beside|16:window|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000008||
|428|1752|2397624.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:skateboard[mask2former_thing]mask2former:036:000003|
|428|1752|2397624.jpg|0:person|looking at|3:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|428|1752|2397624.jpg|0:person|on|5:wall|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|430|1713|2395938.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:skateboard[mask2former_thing]mask2former:036:000004|
|430|1713|2395938.jpg|0:person|going down|2:stairs|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|430|1713|2395938.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000003|
|432|880|2355316.jpg|0:person|in front of|7:car|wrong_predicate|2:person[mask2former_thing]mask2former:000:000008|4:car[mask2former_thing]mask2former:002:000006|
|432|880|2355316.jpg|0:person|standing on|12:pavement|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000008||
|432|880|2355316.jpg|1:person|standing on|12:pavement|endpoint_missing_or_wrong_class|||
|432|880|2355316.jpg|6:person|in front of|13:building|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|434|1478|2385010.jpg|0:person|standing on|4:floor|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|438|163|2319267.jpg|0:person|on|2:truck|endpoint_missing_or_wrong_class|||
|438|163|2319267.jpg|0:person|standing on|2:truck|endpoint_missing_or_wrong_class|||
|439|1357|2379131.jpg|0:person|looking at|8:apple|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:apple[mask2former_thing]mask2former:047:000004|
|439|1357|2379131.jpg|0:person|catching|8:apple|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:apple[mask2former_thing]mask2former:047:000004|
|441|2118|2416492.jpg|0:person|beside|1:toilet|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:toilet[mask2former_thing]mask2former:061:000003|
|441|2118|2416492.jpg|0:person|touching|1:toilet|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:toilet[mask2former_thing]mask2former:061:000003|
|443|192|2321324.jpg|0:person|walking on|22:pavement|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000013||
|443|192|2321324.jpg|1:person|feeding|11:bird|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000008||
|446|712|2347578.jpg|0:person|riding|1:skis|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:skis[mask2former_thing]mask2former:030:000004|
|446|712|2347578.jpg|0:person|going down|2:snow|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|446|712|2347578.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000003|
|447|104|2316313.jpg|0:person|in front of|1:person|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|447|104|2316313.jpg|1:person|in|3:car|endpoint_missing_or_wrong_class||4:car[mask2former_thing]mask2former:002:000004|
|448|792|2351247.jpg|4:person|beside|8:person|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000008||
|448|792|2351247.jpg|7:person|standing on|28:dirt|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000011||
|448|792|2351247.jpg|8:person|picking|30:food|endpoint_missing_or_wrong_class|||
|449|784|2351059.jpg|0:person|running on|6:sand|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000004||
|449|784|2351059.jpg|1:person|catching|3:sports ball|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|449|784|2351059.jpg|1:person|running on|6:sand|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|449|784|2351059.jpg|2:person|looking at|1:person|wrong_predicate|2:person[mask2former_thing]mask2former:000:000005|0:person[mask2former_thing]mask2former:000:000001|
|450|1615|2390859.jpg|0:person|looking at|2:cell phone|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|2:cell phone[mask2former_thing]mask2former:067:000003|
|450|1615|2390859.jpg|0:person|in front of|3:paper|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|450|1615|2390859.jpg|0:person|in front of|4:building|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|453|1642|2392244.jpg|0:person|looking at|5:bowl|wrong_predicate|1:person[mask2former_thing]mask2former:000:000007|8:bowl[mask2former_thing]mask2former:045:000012|
|453|1642|2392244.jpg|10:dining table|attached to|0:person|wrong_predicate|11:dining table[mask2former_thing]mask2former:060:000005|1:person[mask2former_thing]mask2former:000:000007|
|454|629|2343942.jpg|1:person|looking at|23:laptop|wrong_predicate|5:person[mask2former_thing]mask2former:000:000016|21:laptop[mask2former_thing]mask2former:063:000009|
|454|629|2343942.jpg|3:person|sitting on|18:chair|endpoint_missing_or_wrong_class|||
|454|629|2343942.jpg|3:person|wearing|18:chair|endpoint_missing_or_wrong_class|||
|454|629|2343942.jpg|19:chair|in front of|10:person|rank_below50|19:chair[mask2former_thing]mask2former:056:000027|11:person[mask2former_thing]mask2former:000:000025|
|456|1089|2365077.jpg|0:person|talking to|2:person|endpoint_missing_or_wrong_class|||
|456|1089|2365077.jpg|8:person|carrying|16:handbag|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000013||
|457|587|2341770.jpg|0:person|driving|3:bus|wrong_predicate|1:person[mask2former_thing]mask2former:000:000005|2:bus[mask2former_thing]mask2former:005:000003|
|457|587|2341770.jpg|1:person|in|3:bus|endpoint_missing_or_wrong_class||2:bus[mask2former_thing]mask2former:005:000003|
|457|587|2341770.jpg|1:person|sitting on|3:bus|endpoint_missing_or_wrong_class||2:bus[mask2former_thing]mask2former:005:000003|
|457|587|2341770.jpg|2:person|sitting on|3:bus|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|2:bus[mask2former_thing]mask2former:005:000003|
|458|1575|2388803.jpg|0:person|wearing|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:skateboard[mask2former_thing]mask2former:036:000001|
|458|1575|2388803.jpg|0:person|looking at|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:skateboard[mask2former_thing]mask2former:036:000001|
|458|1575|2388803.jpg|0:person|catching|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:skateboard[mask2former_thing]mask2former:036:000001|
|458|1575|2388803.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:skateboard[mask2former_thing]mask2former:036:000001|
|458|1575|2388803.jpg|0:person|jumping over|2:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|458|1575|2388803.jpg|0:person|wearing|2:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|461|107|2316321.jpg|0:person|standing on|6:skis|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|461|107|2316321.jpg|0:person|wearing|6:skis|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|461|107|2316321.jpg|2:person|going down|9:snow|endpoint_missing_or_wrong_class|||
|461|107|2316321.jpg|3:person|going down|9:snow|endpoint_missing_or_wrong_class|||
|463|555|2339725.jpg|0:person|biting|8:toothbrush|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000005||
|465|1540|2387468.jpg|0:person|beside|4:train|endpoint_missing_or_wrong_class||3:train[mask2former_thing]mask2former:006:000003|
|465|1540|2387468.jpg|2:person|beside|4:train|wrong_predicate|1:person[mask2former_thing]mask2former:000:000007|3:train[mask2former_thing]mask2former:006:000003|
|466|1797|2400508.jpg|0:person|playing|1:kite|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|466|1797|2400508.jpg|0:person|on|2:sand|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|466|1797|2400508.jpg|0:person|standing on|2:sand|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|466|1797|2400508.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000003|
|470|1101|2365885.jpg|0:person|playing|2:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:sports ball[mask2former_thing]mask2former:032:000004|
|470|1101|2365885.jpg|0:person|holding|3:tennis racket|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:tennis racket[mask2former_thing]mask2former:038:000001|
|470|1101|2365885.jpg|0:person|running on|4:playingfield|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|471|1700|2394982.jpg|0:person|in front of|8:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:person[mask2former_thing]mask2former:000:000007|
|471|1700|2394982.jpg|0:person|attached to|13:fence|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|471|1700|2394982.jpg|8:person|attached to|13:fence|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000007||
|472|404|2332502.jpg|1:person|driving|14:boat|wrong_predicate|0:person[mask2former_thing]mask2former:000:000011|5:boat[mask2former_thing]mask2former:008:000008|
|472|404|2332502.jpg|2:person|in|14:boat|endpoint_missing_or_wrong_class||5:boat[mask2former_thing]mask2former:008:000008|
|472|404|2332502.jpg|2:person|over|18:river|endpoint_missing_or_wrong_class|||
|473|605|2342711.jpg|0:person|looking at|22:bowl|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000015||
|473|605|2342711.jpg|1:person|beside|0:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|2:person[mask2former_thing]mask2former:000:000015|
|478|1804|2400822.jpg|0:person|attached to|3:surfboard|wrong_predicate|1:person[mask2former_thing]mask2former:000:000004|2:surfboard[mask2former_thing]mask2former:037:000002|
|478|1804|2400822.jpg|0:person|playing|3:surfboard|wrong_predicate|1:person[mask2former_thing]mask2former:000:000004|2:surfboard[mask2former_thing]mask2former:037:000002|
|478|1804|2400822.jpg|0:person|on|4:sand|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000004||
|478|1804|2400822.jpg|0:person|standing on|4:sand|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000004||
|478|1804|2400822.jpg|0:person|beside|5:sea|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000004||
|478|1804|2400822.jpg|1:person|on|4:sand|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|478|1804|2400822.jpg|1:person|walking on|4:sand|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|478|1804|2400822.jpg|1:person|beside|5:sea|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|478|1804|2400822.jpg|5:sea|beside|0:person|endpoint_missing_or_wrong_class||1:person[mask2former_thing]mask2former:000:000004|
|478|1804|2400822.jpg|5:sea|beside|1:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000001|
|480|461|2334659.jpg|0:person|in front of|9:house|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000005||
|480|461|2334659.jpg|0:person|walking on|13:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000005||
|480|461|2334659.jpg|2:person|in front of|9:house|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000009||
|480|461|2334659.jpg|2:person|walking on|13:pavement|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000009||
|481|797|2351374.jpg|7:person|attached to|14:pavement|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000009||
|481|797|2351374.jpg|7:person|walking on|14:pavement|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000009||
|481|797|2351374.jpg|8:person|in front of|9:person|endpoint_missing_or_wrong_class|||
|481|797|2351374.jpg|10:person|going down|14:pavement|endpoint_missing_or_wrong_class|9:person[mask2former_thing]mask2former:000:000017||
|481|797|2351374.jpg|12:person|beside|15:building|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000011||
|481|797|2351374.jpg|13:sky|on|3:person|endpoint_missing_or_wrong_class||7:person[mask2former_thing]mask2former:000:000015|
|483|1172|2369539.jpg|0:person|catching|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000004|
|483|1172|2369539.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000004|
|483|1172|2369539.jpg|0:person|on|2:sea|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|484|1699|2394864.jpg|0:person|leaning on|5:dining table|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|5:dining table[mask2former_thing]mask2former:060:000001|
|485|57|1592560.jpg|0:person|beside|7:table|endpoint_missing_or_wrong_class|||
|485|57|1592560.jpg|0:person|in front of|9:wall|endpoint_missing_or_wrong_class|||
|486|1052|2362836.jpg|0:person|guiding|3:person|endpoint_missing_or_wrong_class||1:person[mask2former_thing]mask2former:000:000004|
|486|1052|2362836.jpg|3:person|in front of|0:person|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000004||
|486|1052|2362836.jpg|4:person|on|1:person|endpoint_missing_or_wrong_class||3:person[mask2former_thing]mask2former:000:000007|
|486|1052|2362836.jpg|5:person|walking on|8:road|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|489|610|2342847.jpg|2:person|walking on|23:road|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000018||
|489|610|2342847.jpg|6:person|driving|11:truck|wrong_predicate|2:person[mask2former_thing]mask2former:000:000013|11:truck[mask2former_thing]mask2former:007:000009|
|490|2161|498294.jpg|0:person|in front of|1:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|3:person[mask2former_thing]mask2former:000:000007|
|490|2161|498294.jpg|1:person|wearing|6:baseball glove|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000007||
|490|2161|498294.jpg|2:person|wearing|7:baseball glove|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000010||
|490|2161|498294.jpg|3:person|standing on|9:playingfield|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000006||
|490|2161|498294.jpg|4:person|wearing|8:baseball glove|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000008||
|490|2161|498294.jpg|5:person|running on|9:playingfield|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|491|382|2331166.jpg|0:person|on|17:bus|endpoint_missing_or_wrong_class||8:bus[mask2former_thing]mask2former:005:000009|
|491|382|2331166.jpg|2:person|on|20:pavement|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000010||
|491|382|2331166.jpg|3:person|on|20:pavement|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000006||
|491|382|2331166.jpg|5:person|walking on|20:pavement|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|491|382|2331166.jpg|8:person|driving|17:bus|endpoint_missing_or_wrong_class||8:bus[mask2former_thing]mask2former:005:000009|
|492|1031|2362238.jpg|0:person|playing|2:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:surfboard[mask2former_thing]mask2former:037:000004|
|492|1031|2362238.jpg|0:person|on|3:sea|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|493|374|2330610.jpg|0:person|in|1:truck|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|493|374|2330610.jpg|0:person|driving|1:truck|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|494|265|2324812.jpg|0:person|touching|2:person|wrong_predicate|3:person[mask2former_thing]mask2former:000:000006|2:person[mask2former_thing]mask2former:000:000005|
|494|265|2324812.jpg|1:person|attached to|3:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|1:person[mask2former_thing]mask2former:000:000003|
|494|265|2324812.jpg|3:person|carrying|4:handbag|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|4:handbag[mask2former_thing]mask2former:026:000004|
|494|265|2324812.jpg|3:person|in front of|7:window|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|494|265|2324812.jpg|5:cell phone|touching|3:person|wrong_predicate|5:cell phone[mask2former_thing]mask2former:067:000002|1:person[mask2former_thing]mask2former:000:000003|
|496|769|2350508.jpg|1:person|attached to|2:pizza|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|496|769|2350508.jpg|1:person|looking at|2:pizza|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|496|769|2350508.jpg|1:person|eating|2:pizza|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|496|769|2350508.jpg|1:person|in front of|3:wall|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|496|769|2350508.jpg|2:pizza|attached to|1:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000002|
|500|1155|2368389.jpg|3:fence|enclosing|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000002|

## C_fasterrcnn_thing_plus_stuff

未命中664条。

|序号|索引|图片|GT主语|谓词|GT宾语|失败阶段|匹配主语候选|匹配宾语候选|
|---:|---:|---|---|---|---|---|---|---|
|6|295|2326503.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|7|1675|2393584.jpg|0:person|in|2:tv|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:tv[fasterrcnn_thing]fasterrcnn:000000|
|10|553|2339606.jpg|0:person|running on|16:dirt|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|10|553|2339606.jpg|1:person|standing on|16:dirt|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|10|553|2339606.jpg|6:person|wearing|9:baseball glove|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|16|1466|2384291.jpg|0:person|beside|1:person|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|12:person[fasterrcnn_thing]fasterrcnn:000012|
|16|1466|2384291.jpg|1:person|beside|0:person|wrong_predicate|12:person[fasterrcnn_thing]fasterrcnn:000012|4:person[fasterrcnn_thing]fasterrcnn:000004|
|16|1466|2384291.jpg|2:person|holding|21:paper|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|16|1466|2384291.jpg|3:person|walking on|20:pavement|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|25:pavement[mask2former_stuff]mask2former:123:000013|
|18|1983|2409607.jpg|0:person|sitting on|1:horse|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:horse[fasterrcnn_thing]fasterrcnn:000000|
|18|1983|2409607.jpg|0:person|over|5:grass|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|6:grass[mask2former_stuff]mask2former:125:000007|
|21|411|2332726.jpg|0:person|walking on|8:sand|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|14:sand[mask2former_stuff]mask2former:102:000006|
|21|411|2332726.jpg|3:person|looking at|5:kite|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:kite[fasterrcnn_thing]fasterrcnn:000005|
|21|411|2332726.jpg|3:person|playing|5:kite|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:kite[fasterrcnn_thing]fasterrcnn:000005|
|21|411|2332726.jpg|3:person|wearing|8:sand|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|14:sand[mask2former_stuff]mask2former:102:000006|
|22|129|2317125.jpg|2:person|walking on|11:road|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|13:road[mask2former_stuff]mask2former:100:000009|
|22|129|2317125.jpg|4:person|standing on|11:road|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|13:road[mask2former_stuff]mask2former:100:000009|
|22|129|2317125.jpg|9:house|beside|0:person|rank_below50|12:house[mask2former_stuff]mask2former:091:000013|2:person[fasterrcnn_thing]fasterrcnn:000002|
|23|1055|2363004.jpg|0:person|holding|12:handbag|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|6:handbag[fasterrcnn_thing]fasterrcnn:000006|
|23|1055|2363004.jpg|2:person|walking on|21:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|23|1055|2363004.jpg|3:person|walking on|21:pavement|endpoint_missing_or_wrong_class|10:person[fasterrcnn_thing]fasterrcnn:000010||
|23|1055|2363004.jpg|7:person|walking on|21:pavement|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|23|1055|2363004.jpg|8:person|walking on|21:pavement|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|23|1055|2363004.jpg|10:train|beside|8:person|rank_below50|3:train[fasterrcnn_thing]fasterrcnn:000003|1:person[fasterrcnn_thing]fasterrcnn:000001|
|24|1712|2395918.jpg|0:person|crossing|5:pavement|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|7:pavement[mask2former_stuff]mask2former:123:000007|
|24|1712|2395918.jpg|1:person|beside|6:grass|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|8:grass[mask2former_stuff]mask2former:125:000006|
|24|1712|2395918.jpg|2:skateboard|attached to|0:person|wrong_predicate|2:skateboard[fasterrcnn_thing]fasterrcnn:000002|0:person[fasterrcnn_thing]fasterrcnn:000000|
|26|892|2355904.jpg|0:person|touching|10:table|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|27|2018|2411180.jpg|0:person|standing on|6:railroad|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|9:railroad[mask2former_stuff]mask2former:098:000007|
|28|164|2319298.jpg|0:person|driving|1:car|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|0:car[fasterrcnn_thing]fasterrcnn:000000|
|29|81|2315729.jpg|3:person|attached to|4:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:person[fasterrcnn_thing]fasterrcnn:000002|
|29|81|2315729.jpg|6:person|attached to|2:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|33|1896|2405341.jpg|0:person|holding|1:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|35|1326|2377788.jpg|0:person|feeding|3:cow|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000; 17:person[fasterrcnn_thing]fasterrcnn:000017|5:cow[fasterrcnn_thing]fasterrcnn:000005|
|35|1326|2377788.jpg|6:cow|in front of|1:person|wrong_predicate|4:cow[fasterrcnn_thing]fasterrcnn:000004; 16:cow[fasterrcnn_thing]fasterrcnn:000016|0:person[fasterrcnn_thing]fasterrcnn:000000; 3:person[fasterrcnn_thing]fasterrcnn:000003|
|36|922|2357107.jpg|1:person|in|9:boat|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|1:boat[fasterrcnn_thing]fasterrcnn:000001|
|36|922|2357107.jpg|4:person|walking on|14:platform|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|38|1914|2406339.jpg|0:person|beside|3:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002; 6:person[fasterrcnn_thing]fasterrcnn:000006|2:person[fasterrcnn_thing]fasterrcnn:000002|
|38|1914|2406339.jpg|0:person|looking at|22:playingfield|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002; 6:person[fasterrcnn_thing]fasterrcnn:000006||
|38|1914|2406339.jpg|2:person|looking at|22:playingfield|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|38|1914|2406339.jpg|2:person|attached to|26:wall|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|14:wall[mask2former_stuff]mask2former:131:000011|
|40|208|2321715.jpg|0:person|on|7:motorcycle|endpoint_missing_or_wrong_class||8:motorcycle[fasterrcnn_thing]fasterrcnn:000008|
|40|208|2321715.jpg|0:person|riding|7:motorcycle|endpoint_missing_or_wrong_class||8:motorcycle[fasterrcnn_thing]fasterrcnn:000008|
|40|208|2321715.jpg|3:person|exiting|12:tent|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|40|208|2321715.jpg|3:person|walking on|16:floor|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|44|489|2336251.jpg|0:person|sitting on|9:pavement|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|10:pavement[mask2former_stuff]mask2former:123:000008|
|44|489|2336251.jpg|1:person|talking to|0:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|44|489|2336251.jpg|1:person|sitting on|9:pavement|endpoint_missing_or_wrong_class||10:pavement[mask2former_stuff]mask2former:123:000008|
|44|489|2336251.jpg|3:person|playing|6:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:skateboard[fasterrcnn_thing]fasterrcnn:000003|
|44|489|2336251.jpg|3:person|jumping from|9:pavement|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|10:pavement[mask2former_stuff]mask2former:123:000008|
|46|674|2345802.jpg|0:person|sitting on|2:chair|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|46|674|2345802.jpg|0:person|in front of|3:counter|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|51|1507|2386227.jpg|1:person|in|2:tv|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|0:tv[fasterrcnn_thing]fasterrcnn:000000|
|52|1139|2367625.jpg|0:person|in front of|3:oven|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:oven[fasterrcnn_thing]fasterrcnn:000001|
|53|1627|2391314.jpg|0:person|standing on|1:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skis[fasterrcnn_thing]fasterrcnn:000001|
|53|1627|2391314.jpg|0:person|beside|3:tree|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|4:tree[mask2former_stuff]mask2former:116:000001|
|54|237|2323211.jpg|5:person|over|1:person|wrong_predicate|7:person[fasterrcnn_thing]fasterrcnn:000007|9:person[fasterrcnn_thing]fasterrcnn:000009|
|54|237|2323211.jpg|5:person|over|8:person|wrong_predicate|7:person[fasterrcnn_thing]fasterrcnn:000007|6:person[fasterrcnn_thing]fasterrcnn:000006|
|54|237|2323211.jpg|5:person|on|17:grass|rank_below50|7:person[fasterrcnn_thing]fasterrcnn:000007|27:grass[mask2former_stuff]mask2former:125:000014|
|54|237|2323211.jpg|5:person|jumping from|17:grass|wrong_predicate|7:person[fasterrcnn_thing]fasterrcnn:000007|27:grass[mask2former_stuff]mask2former:125:000014|
|55|166|2319395.jpg|0:person|walking on|6:road|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|14:road[mask2former_stuff]mask2former:100:000007|
|55|166|2319395.jpg|1:person|standing on|6:road|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|14:road[mask2former_stuff]mask2former:100:000007|
|57|327|2328174.jpg|0:person|in front of|1:car|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:car[fasterrcnn_thing]fasterrcnn:000001|
|57|327|2328174.jpg|0:person|picking|2:umbrella|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:umbrella[fasterrcnn_thing]fasterrcnn:000003|
|57|327|2328174.jpg|0:person|in front of|3:potted plant|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:potted plant[fasterrcnn_thing]fasterrcnn:000002|
|57|327|2328174.jpg|0:person|standing on|6:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|58|617|2343155.jpg|0:person|throwing|3:sports ball|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:sports ball[fasterrcnn_thing]fasterrcnn:000002|
|58|617|2343155.jpg|0:person|about to hit|3:sports ball|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:sports ball[fasterrcnn_thing]fasterrcnn:000002|
|58|617|2343155.jpg|0:person|standing on|6:playingfield|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|60|2159|498242.jpg|0:person|beside|9:person|rank_below50|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|60|2159|498242.jpg|0:person|looking at|9:person|rank_below50|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|60|2159|498242.jpg|1:person|beside|0:person|rank_below50|3:person[fasterrcnn_thing]fasterrcnn:000003|1:person[fasterrcnn_thing]fasterrcnn:000001|
|60|2159|498242.jpg|1:person|looking at|9:person|rank_below50|3:person[fasterrcnn_thing]fasterrcnn:000003|0:person[fasterrcnn_thing]fasterrcnn:000000|
|60|2159|498242.jpg|2:person|standing on|14:pavement|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|24:pavement[mask2former_stuff]mask2former:123:000015|
|60|2159|498242.jpg|3:person|looking at|1:person|rank_below50|4:person[fasterrcnn_thing]fasterrcnn:000004|3:person[fasterrcnn_thing]fasterrcnn:000003|
|60|2159|498242.jpg|3:person|beside|8:person|rank_below50|4:person[fasterrcnn_thing]fasterrcnn:000004|2:person[fasterrcnn_thing]fasterrcnn:000002|
|60|2159|498242.jpg|6:person|beside|4:person|wrong_predicate|14:person[fasterrcnn_thing]fasterrcnn:000014|12:person[fasterrcnn_thing]fasterrcnn:000012|
|60|2159|498242.jpg|8:person|beside|5:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|7:person[fasterrcnn_thing]fasterrcnn:000007|
|60|2159|498242.jpg|8:person|attached to|5:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|7:person[fasterrcnn_thing]fasterrcnn:000007|
|60|2159|498242.jpg|9:person|looking at|0:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:person[fasterrcnn_thing]fasterrcnn:000001|
|61|1219|2371806.jpg|0:person|running on|2:playingfield|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|8:playingfield[mask2former_stuff]mask2former:097:000003|
|63|1445|2383111.jpg|1:person|riding|7:horse|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|66|749|2349334.jpg|1:person|looking at|4:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|66|749|2349334.jpg|2:person|eating|19:pizza|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002; 21:person[fasterrcnn_thing]fasterrcnn:000021||
|66|749|2349334.jpg|6:person|talking to|5:person|rank_below50|4:person[fasterrcnn_thing]fasterrcnn:000004|9:person[fasterrcnn_thing]fasterrcnn:000009|
|66|749|2349334.jpg|23:ceiling|on|4:person|wrong_predicate|34:ceiling[mask2former_stuff]mask2former:118:000018|0:person[fasterrcnn_thing]fasterrcnn:000000|
|68|1598|2390200.jpg|0:person|swinging|6:remote|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|8:remote[fasterrcnn_thing]fasterrcnn:000008|
|68|1598|2390200.jpg|0:person|holding|9:remote|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|68|1598|2390200.jpg|1:person|holding|3:potted plant|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|68|1598|2390200.jpg|1:person|swinging|8:remote|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|4:remote[fasterrcnn_thing]fasterrcnn:000004|
|68|1598|2390200.jpg|1:person|in front of|16:table|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|70|714|2347722.jpg|0:person|attached to|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|70|714|2347722.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|70|714|2347722.jpg|0:person|touching|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|70|714|2347722.jpg|0:person|looking at|2:sea|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:sea[mask2former_stuff]mask2former:103:000001|
|71|10|1159449.jpg|1:person|looking at|17:sports ball|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|71|10|1159449.jpg|8:person|running on|23:playingfield|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|29:playingfield[mask2former_stuff]mask2former:097:000004|
|72|841|2353618.jpg|1:person|standing on|2:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:skis[fasterrcnn_thing]fasterrcnn:000002|
|72|841|2353618.jpg|1:person|on|3:snow|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|4:snow[mask2former_stuff]mask2former:105:000002|
|75|1505|2386156.jpg|0:person|driving|2:car|wrong_predicate|10:person[fasterrcnn_thing]fasterrcnn:000010|0:car[fasterrcnn_thing]fasterrcnn:000000|
|81|1886|2404565.jpg|0:person|looking at|3:surfboard|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|7:surfboard[fasterrcnn_thing]fasterrcnn:000007|
|82|1497|2385717.jpg|0:person|over|3:pavement|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|7:pavement[mask2former_stuff]mask2former:123:000005|
|83|2176|713850.jpg|0:person|in|5:window|endpoint_missing_or_wrong_class|||
|86|1001|2360816.jpg|1:person|riding|13:bicycle|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|22:bicycle[fasterrcnn_thing]fasterrcnn:000022|
|86|1001|2360816.jpg|5:person|riding|11:bicycle|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|7:bicycle[fasterrcnn_thing]fasterrcnn:000007|
|86|1001|2360816.jpg|10:person|riding|14:bicycle|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|12:bicycle[fasterrcnn_thing]fasterrcnn:000012|
|87|852|2354099.jpg|3:person|crossing|36:pavement|endpoint_missing_or_wrong_class|17:person[fasterrcnn_thing]fasterrcnn:000017||
|87|852|2354099.jpg|9:person|crossing|36:pavement|endpoint_missing_or_wrong_class|21:person[fasterrcnn_thing]fasterrcnn:000021||
|87|852|2354099.jpg|11:person|standing on|34:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|9:skateboard[fasterrcnn_thing]fasterrcnn:000009|
|87|852|2354099.jpg|37:building|beside|11:person|wrong_predicate|39:building[mask2former_stuff]mask2former:129:000003|0:person[fasterrcnn_thing]fasterrcnn:000000|
|89|813|2352072.jpg|0:person|in front of|3:tree|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|8:tree[mask2former_stuff]mask2former:116:000001|
|91|926|2357328.jpg|0:person|standing on|5:grass|endpoint_missing_or_wrong_class||5:grass[mask2former_stuff]mask2former:125:000004|
|91|926|2357328.jpg|2:person|holding|3:baseball bat|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:baseball bat[fasterrcnn_thing]fasterrcnn:000002|
|91|926|2357328.jpg|2:person|standing on|5:grass|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|5:grass[mask2former_stuff]mask2former:125:000004|
|92|1004|2360919.jpg|0:person|in front of|3:book|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|93|227|2322480.jpg|0:person|looking at|1:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|93|227|2322480.jpg|1:person|chasing|2:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:sports ball[fasterrcnn_thing]fasterrcnn:000002|
|93|227|2322480.jpg|1:person|playing|2:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:sports ball[fasterrcnn_thing]fasterrcnn:000002|
|93|227|2322480.jpg|2:sports ball|in front of|1:person|wrong_predicate|2:sports ball[fasterrcnn_thing]fasterrcnn:000002|0:person[fasterrcnn_thing]fasterrcnn:000000|
|95|649|2344605.jpg|0:person|wearing|7:tie|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|95|649|2344605.jpg|0:person|touching|12:laptop|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:laptop[fasterrcnn_thing]fasterrcnn:000002|
|95|649|2344605.jpg|12:laptop|in front of|0:person|wrong_predicate|2:laptop[fasterrcnn_thing]fasterrcnn:000002|0:person[fasterrcnn_thing]fasterrcnn:000000|
|100|1841|2402294.jpg|1:person|driving|6:bus|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|0:bus[fasterrcnn_thing]fasterrcnn:000000|
|101|1796|2400414.jpg|1:person|playing with|5:sheep|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:sheep[fasterrcnn_thing]fasterrcnn:000003|
|101|1796|2400414.jpg|1:person|touching|5:sheep|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:sheep[fasterrcnn_thing]fasterrcnn:000003|
|101|1796|2400414.jpg|3:person|pulling|4:sheep|endpoint_missing_or_wrong_class||2:sheep[fasterrcnn_thing]fasterrcnn:000002|
|101|1796|2400414.jpg|5:sheep|playing with|1:person|wrong_predicate|3:sheep[fasterrcnn_thing]fasterrcnn:000003|0:person[fasterrcnn_thing]fasterrcnn:000000|
|103|989|2360368.jpg|2:person|standing on|12:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|103|989|2360368.jpg|2:person|in front of|14:dirt|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|21:dirt[mask2former_stuff]mask2former:126:000010|
|104|1795|2400390.jpg|10:person|beside|6:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:person[fasterrcnn_thing]fasterrcnn:000003|
|105|1023|2361799.jpg|0:person|looking at|1:bear|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|105|1023|2361799.jpg|0:person|in front of|3:tree|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:tree[mask2former_stuff]mask2former:116:000001|
|106|868|2354820.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|106|868|2354820.jpg|0:person|riding|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|106|868|2354820.jpg|0:person|in front of|2:tree|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:tree[mask2former_stuff]mask2former:116:000002|
|106|868|2354820.jpg|0:person|standing on|4:floor|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|110|979|2359868.jpg|0:person|in|2:train|endpoint_missing_or_wrong_class||0:train[fasterrcnn_thing]fasterrcnn:000000|
|110|979|2359868.jpg|1:person|in|2:train|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|0:train[fasterrcnn_thing]fasterrcnn:000000|
|119|1534|2387240.jpg|4:person|in front of|13:person|endpoint_missing_or_wrong_class|9:person[fasterrcnn_thing]fasterrcnn:000009||
|121|1300|2376047.jpg|0:person|jumping from|4:playingfield|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|121|1300|2376047.jpg|1:person|chasing|2:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|
|121|1300|2376047.jpg|1:person|playing|2:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|
|121|1300|2376047.jpg|1:person|jumping from|4:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|122|1729|2396723.jpg|0:person|sitting on|4:couch|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|122|1729|2396723.jpg|2:cat|lying on|0:person|wrong_predicate|0:cat[fasterrcnn_thing]fasterrcnn:000000|3:person[fasterrcnn_thing]fasterrcnn:000003|
|122|1729|2396723.jpg|5:pillow|in front of|0:person|endpoint_missing_or_wrong_class||3:person[fasterrcnn_thing]fasterrcnn:000003|
|123|1099|2365844.jpg|0:person|beside|8:person|rank_below50|6:person[fasterrcnn_thing]fasterrcnn:000006|1:person[fasterrcnn_thing]fasterrcnn:000001|
|123|1099|2365844.jpg|9:person|beside|12:person|rank_below50|0:person[fasterrcnn_thing]fasterrcnn:000000|3:person[fasterrcnn_thing]fasterrcnn:000003|
|123|1099|2365844.jpg|10:person|beside|12:person|rank_below50|12:person[fasterrcnn_thing]fasterrcnn:000012|3:person[fasterrcnn_thing]fasterrcnn:000003|
|125|1673|2393510.jpg|1:person|walking on|6:grass|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|5:grass[mask2former_stuff]mask2former:125:000006|
|125|1673|2393510.jpg|2:person|looking at|0:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|125|1673|2393510.jpg|2:person|throwing|3:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:frisbee[fasterrcnn_thing]fasterrcnn:000003|
|126|787|2351136.jpg|0:person|on back of|3:horse|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:horse[fasterrcnn_thing]fasterrcnn:000000|
|127|1293|2375622.jpg|1:person|looking at|2:laptop|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|0:laptop[fasterrcnn_thing]fasterrcnn:000000|
|127|1293|2375622.jpg|1:person|touching|2:laptop|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|0:laptop[fasterrcnn_thing]fasterrcnn:000000|
|128|323|2328089.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|128|323|2328089.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|130|2105|2416163.jpg|9:person|sitting on|33:sand|endpoint_missing_or_wrong_class||35:sand[mask2former_stuff]mask2former:102:000023|
|130|2105|2416163.jpg|11:person|sitting on|33:sand|rank_below50|2:person[fasterrcnn_thing]fasterrcnn:000002|35:sand[mask2former_stuff]mask2former:102:000023|
|130|2105|2416163.jpg|12:person|sitting on|33:sand|rank_below50|4:person[fasterrcnn_thing]fasterrcnn:000004|35:sand[mask2former_stuff]mask2former:102:000023|
|131|1764|2398216.jpg|0:person|in front of|1:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|131|1764|2398216.jpg|2:person|standing on|11:pavement|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|9:pavement[mask2former_stuff]mask2former:123:000011|
|131|1764|2398216.jpg|3:person|standing on|11:pavement|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|9:pavement[mask2former_stuff]mask2former:123:000011|
|134|406|2332593.jpg|0:person|in front of|8:wall-stone|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|14:wall-stone[mask2former_stuff]mask2former:110:000005|
|134|406|2332593.jpg|0:person|on|12:grass|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|17:grass[mask2former_stuff]mask2former:125:000009|
|134|406|2332593.jpg|1:person|in front of|0:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|135|1163|2368707.jpg|1:person|looking at|4:frisbee|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|
|135|1163|2368707.jpg|2:person|running on|9:dirt|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|12:dirt[mask2former_stuff]mask2former:126:000007|
|135|1163|2368707.jpg|3:person|looking at|4:frisbee|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|
|135|1163|2368707.jpg|4:frisbee|over|1:person|rank_below50|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|3:person[fasterrcnn_thing]fasterrcnn:000003|
|136|1375|2379887.jpg|0:person|in front of|5:mountain|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:mountain[mask2former_stuff]mask2former:124:000004|
|140|554|2339715.jpg|0:person|holding|14:spoon|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|140|554|2339715.jpg|0:person|eating|14:spoon|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|141|1697|2394828.jpg|0:person|over|3:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|141|1697|2394828.jpg|0:person|jumping from|3:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|141|1697|2394828.jpg|0:person|in front of|4:grass|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:grass[mask2former_stuff]mask2former:125:000004|
|141|1697|2394828.jpg|0:person|in front of|5:rock|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|144|1442|2383041.jpg|3:person|wearing|18:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|20:surfboard[fasterrcnn_thing]fasterrcnn:000020|
|144|1442|2383041.jpg|4:person|pulling|13:kite|endpoint_missing_or_wrong_class||5:kite[fasterrcnn_thing]fasterrcnn:000005|
|149|1526|2387025.jpg|6:person|carrying|21:handbag|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|32:handbag[fasterrcnn_thing]fasterrcnn:000032|
|149|1526|2387025.jpg|8:person|wearing|24:cardboard|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|152|1986|2409643.jpg|0:person|holding|5:handbag|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|5:handbag[fasterrcnn_thing]fasterrcnn:000005|
|152|1986|2409643.jpg|1:person|carrying|4:handbag|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|4:handbag[fasterrcnn_thing]fasterrcnn:000004|
|153|1695|2394762.jpg|1:person|attached to|16:grass|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|153|1695|2394762.jpg|3:person|looking at|12:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000; 10:person[fasterrcnn_thing]fasterrcnn:000010|8:sports ball[fasterrcnn_thing]fasterrcnn:000008|
|153|1695|2394762.jpg|5:person|pulling|6:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002; 5:person[fasterrcnn_thing]fasterrcnn:000005|2:person[fasterrcnn_thing]fasterrcnn:000002|
|153|1695|2394762.jpg|5:person|jumping from|13:playingfield|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002; 5:person[fasterrcnn_thing]fasterrcnn:000005|14:playingfield[mask2former_stuff]mask2former:097:000005|
|154|47|1592228.jpg|1:person|standing on|17:platform|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|154|47|1592228.jpg|5:person|carrying|12:handbag|endpoint_missing_or_wrong_class|13:person[fasterrcnn_thing]fasterrcnn:000013||
|154|47|1592228.jpg|5:person|standing on|22:pavement|endpoint_missing_or_wrong_class|13:person[fasterrcnn_thing]fasterrcnn:000013||
|156|1813|2401171.jpg|9:person|walking on|25:pavement|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|157|1286|2375241.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|157|1286|2375241.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|157|1286|2375241.jpg|0:person|looking at|2:sea|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:sea[mask2former_stuff]mask2former:103:000001|
|158|975|2359797.jpg|8:person|carrying|15:backpack|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|158|975|2359797.jpg|10:person|holding|19:umbrella|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|4:umbrella[fasterrcnn_thing]fasterrcnn:000004|
|158|975|2359797.jpg|14:backpack|on back of|3:person|wrong_predicate|7:backpack[fasterrcnn_thing]fasterrcnn:000007|3:person[fasterrcnn_thing]fasterrcnn:000003|
|161|859|2354354.jpg|0:person|holding|10:umbrella|endpoint_missing_or_wrong_class||9:umbrella[fasterrcnn_thing]fasterrcnn:000009|
|161|859|2354354.jpg|3:person|running on|16:pavement|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|27:pavement[mask2former_stuff]mask2former:123:000014|
|161|859|2354354.jpg|4:person|holding|12:umbrella|rank_below50|4:person[fasterrcnn_thing]fasterrcnn:000004|10:umbrella[fasterrcnn_thing]fasterrcnn:000010|
|161|859|2354354.jpg|5:person|walking on|16:pavement|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|27:pavement[mask2former_stuff]mask2former:123:000014|
|165|2125|2416928.jpg|9:person|leaning on|15:truck|endpoint_missing_or_wrong_class||11:truck[fasterrcnn_thing]fasterrcnn:000011|
|165|2125|2416928.jpg|10:person|wearing|16:tree|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|18:tree[mask2former_stuff]mask2former:116:000002|
|165|2125|2416928.jpg|13:person|standing on|15:truck|endpoint_missing_or_wrong_class||11:truck[fasterrcnn_thing]fasterrcnn:000011|
|166|955|2358756.jpg|0:person|holding|1:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|
|166|955|2358756.jpg|0:person|holding|2:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:frisbee[fasterrcnn_thing]fasterrcnn:000002|
|166|955|2358756.jpg|0:person|attached to|3:tree|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|4:tree[mask2former_stuff]mask2former:116:000001|
|167|2029|2411534.jpg|0:person|looking at|1:sports ball|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:sports ball[fasterrcnn_thing]fasterrcnn:000000|
|167|2029|2411534.jpg|0:person|about to hit|1:sports ball|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:sports ball[fasterrcnn_thing]fasterrcnn:000000|
|167|2029|2411534.jpg|0:person|standing on|3:playingfield|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|3:playingfield[mask2former_stuff]mask2former:097:000002|
|170|658|2345182.jpg|6:person|touching|15:kite|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|170|658|2345182.jpg|6:person|holding|18:bottle|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|170|658|2345182.jpg|6:person|holding|19:bottle|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|170|658|2345182.jpg|6:person|walking on|22:grass|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|39:grass[mask2former_stuff]mask2former:125:000019|
|170|658|2345182.jpg|7:person|in front of|10:person|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|2:person[fasterrcnn_thing]fasterrcnn:000002|
|170|658|2345182.jpg|10:person|beside|6:person|rank_below50|2:person[fasterrcnn_thing]fasterrcnn:000002|1:person[fasterrcnn_thing]fasterrcnn:000001|
|172|1608|2390659.jpg|0:person|lying on|34:rug|endpoint_missing_or_wrong_class|||
|172|1608|2390659.jpg|2:person|lying on|34:rug|endpoint_missing_or_wrong_class|||
|172|1608|2390659.jpg|8:person|holding|24:tennis racket|rank_below50|0:person[fasterrcnn_thing]fasterrcnn:000000|2:tennis racket[fasterrcnn_thing]fasterrcnn:000002|
|173|417|2332914.jpg|0:person|standing on|8:pavement|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|10:pavement[mask2former_stuff]mask2former:123:000009|
|173|417|2332914.jpg|0:person|in front of|9:building|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|11:building[mask2former_stuff]mask2former:129:000001|
|175|1343|2378563.jpg|0:person|standing on|8:pavement|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|183|1866|2403494.jpg|12:person|standing on|18:skis|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|14:skis[fasterrcnn_thing]fasterrcnn:000014|
|184|325|2328153.jpg|2:elephant|in front of|0:person|wrong_predicate|0:elephant[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|185|15|1159597.jpg|0:person|guiding|5:horse|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:horse[fasterrcnn_thing]fasterrcnn:000000|
|188|1302|2376309.jpg|0:person|standing on|1:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skis[fasterrcnn_thing]fasterrcnn:000001|
|188|1302|2376309.jpg|0:person|playing|1:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skis[fasterrcnn_thing]fasterrcnn:000001|
|188|1302|2376309.jpg|0:person|looking at|2:snow|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:snow[mask2former_stuff]mask2former:105:000002|
|190|283|2326062.jpg|0:person|on|27:pavement|rank_below50|12:person[fasterrcnn_thing]fasterrcnn:000012|38:pavement[mask2former_stuff]mask2former:123:000019|
|190|283|2326062.jpg|0:person|walking on|27:pavement|rank_below50|12:person[fasterrcnn_thing]fasterrcnn:000012|38:pavement[mask2former_stuff]mask2former:123:000019|
|190|283|2326062.jpg|3:person|sitting on|13:bench|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|190|283|2326062.jpg|9:person|looking at|10:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|21:person[fasterrcnn_thing]fasterrcnn:000021|
|190|283|2326062.jpg|9:person|holding|17:handbag|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:handbag[fasterrcnn_thing]fasterrcnn:000005|
|190|283|2326062.jpg|12:person|on|27:pavement|rank_below50|2:person[fasterrcnn_thing]fasterrcnn:000002|38:pavement[mask2former_stuff]mask2former:123:000019|
|190|283|2326062.jpg|21:handbag|hanging from|3:person|wrong_predicate|8:handbag[fasterrcnn_thing]fasterrcnn:000008|4:person[fasterrcnn_thing]fasterrcnn:000004|
|190|283|2326062.jpg|22:handbag|hanging from|9:person|rank_below50|13:handbag[fasterrcnn_thing]fasterrcnn:000013|0:person[fasterrcnn_thing]fasterrcnn:000000|
|190|283|2326062.jpg|28:paper|beside|3:person|endpoint_missing_or_wrong_class||4:person[fasterrcnn_thing]fasterrcnn:000004|
|194|1135|2367479.jpg|5:person|beside|3:person|rank_below50|1:person[fasterrcnn_thing]fasterrcnn:000001; 4:person[fasterrcnn_thing]fasterrcnn:000004|3:person[fasterrcnn_thing]fasterrcnn:000003|
|194|1135|2367479.jpg|5:person|looking at|3:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001; 4:person[fasterrcnn_thing]fasterrcnn:000004|3:person[fasterrcnn_thing]fasterrcnn:000003|
|194|1135|2367479.jpg|5:person|holding|7:handbag|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001; 4:person[fasterrcnn_thing]fasterrcnn:000004|9:handbag[fasterrcnn_thing]fasterrcnn:000009|
|194|1135|2367479.jpg|7:handbag|in front of|3:person|wrong_predicate|9:handbag[fasterrcnn_thing]fasterrcnn:000009|3:person[fasterrcnn_thing]fasterrcnn:000003|
|195|1382|2380359.jpg|1:person|in front of|23:door|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|29:door[mask2former_stuff]mask2former:086:000010|
|195|1382|2380359.jpg|1:person|in front of|25:ceiling|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|195|1382|2380359.jpg|2:person|sitting on|4:person|endpoint_missing_or_wrong_class||2:person[fasterrcnn_thing]fasterrcnn:000002|
|197|368|2330400.jpg|0:person|going down|4:snow|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|6:snow[mask2former_stuff]mask2former:105:000001|
|197|368|2330400.jpg|1:person|holding|2:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|4:skis[fasterrcnn_thing]fasterrcnn:000004|
|197|368|2330400.jpg|1:person|jumping over|4:snow|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|6:snow[mask2former_stuff]mask2former:105:000001|
|198|1076|2364558.jpg|0:person|about to hit|1:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:sports ball[fasterrcnn_thing]fasterrcnn:000001|
|198|1076|2364558.jpg|0:person|attached to|2:tennis racket|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:tennis racket[fasterrcnn_thing]fasterrcnn:000002|
|198|1076|2364558.jpg|0:person|standing on|3:playingfield|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|4:playingfield[mask2former_stuff]mask2former:097:000002|
|198|1076|2364558.jpg|0:person|in front of|4:wall|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|203|806|2351780.jpg|1:person|on|12:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|203|806|2351780.jpg|2:person|wearing|11:baseball glove|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|5:baseball glove[fasterrcnn_thing]fasterrcnn:000005|
|203|806|2351780.jpg|2:person|on|12:playingfield|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|203|806|2351780.jpg|3:person|about to hit|9:sports ball|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|203|806|2351780.jpg|3:person|holding|10:baseball bat|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|203|806|2351780.jpg|3:person|swinging|10:baseball bat|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|203|806|2351780.jpg|5:person|on|12:playingfield|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|206|1401|2381176.jpg|4:sky|over|1:person|rank_below50|14:sky[mask2former_stuff]mask2former:119:000004|1:person[fasterrcnn_thing]fasterrcnn:000001|
|207|1111|2366320.jpg|0:person|in front of|2:wall|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|7:wall[mask2former_stuff]mask2former:131:000005|
|210|105|2316316.jpg|1:person|holding|19:handbag|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|24:handbag[fasterrcnn_thing]fasterrcnn:000024|
|210|105|2316316.jpg|1:person|on|22:road|rank_below50|0:person[fasterrcnn_thing]fasterrcnn:000000|36:road[mask2former_stuff]mask2former:100:000019|
|210|105|2316316.jpg|1:person|walking on|22:road|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|36:road[mask2former_stuff]mask2former:100:000019|
|210|105|2316316.jpg|6:person|in front of|12:person|wrong_predicate|20:person[fasterrcnn_thing]fasterrcnn:000020|11:person[fasterrcnn_thing]fasterrcnn:000011|
|210|105|2316316.jpg|11:person|riding|15:bicycle|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|210|105|2316316.jpg|12:person|riding|17:motorcycle|wrong_predicate|11:person[fasterrcnn_thing]fasterrcnn:000011|2:motorcycle[fasterrcnn_thing]fasterrcnn:000002|
|210|105|2316316.jpg|13:person|walking on|22:road|endpoint_missing_or_wrong_class||36:road[mask2former_stuff]mask2former:100:000019|
|210|105|2316316.jpg|25:sky|over|6:person|pair_not_selected|37:sky[mask2former_stuff]mask2former:119:000006|20:person[fasterrcnn_thing]fasterrcnn:000020|
|211|1563|2388324.jpg|0:person|in|10:tv|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|7:tv[fasterrcnn_thing]fasterrcnn:000007|
|211|1563|2388324.jpg|0:person|playing|10:tv|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|7:tv[fasterrcnn_thing]fasterrcnn:000007|
|211|1563|2388324.jpg|0:person|holding|11:remote|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|8:remote[fasterrcnn_thing]fasterrcnn:000008|
|213|1476|2384904.jpg|0:person|playing with|2:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:frisbee[fasterrcnn_thing]fasterrcnn:000002|
|213|1476|2384904.jpg|1:person|chasing|0:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|216|1890|2404890.jpg|0:person|in|2:train|endpoint_missing_or_wrong_class||3:train[fasterrcnn_thing]fasterrcnn:000003|
|216|1890|2404890.jpg|1:person|driving|2:train|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|3:train[fasterrcnn_thing]fasterrcnn:000003|
|225|1317|2377220.jpg|1:person|in|10:train|endpoint_missing_or_wrong_class||0:train[fasterrcnn_thing]fasterrcnn:000000|
|225|1317|2377220.jpg|3:person|driving|10:train|endpoint_missing_or_wrong_class||0:train[fasterrcnn_thing]fasterrcnn:000000|
|225|1317|2377220.jpg|6:person|in|10:train|endpoint_missing_or_wrong_class||0:train[fasterrcnn_thing]fasterrcnn:000000|
|225|1317|2377220.jpg|9:person|in|10:train|endpoint_missing_or_wrong_class||0:train[fasterrcnn_thing]fasterrcnn:000000|
|226|2126|2416964.jpg|0:person|picking|14:suitcase|endpoint_missing_or_wrong_class|11:person[fasterrcnn_thing]fasterrcnn:000011||
|227|1607|2390654.jpg|1:person|standing on|9:sand|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|10:sand[mask2former_stuff]mask2former:102:000009|
|227|1607|2390654.jpg|1:person|in front of|10:sea|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|11:sea[mask2former_stuff]mask2former:103:000004|
|227|1607|2390654.jpg|4:person|playing with|5:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:person[fasterrcnn_thing]fasterrcnn:000002|
|228|2144|285721.jpg|0:person|holding|2:cell phone|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:cell phone[fasterrcnn_thing]fasterrcnn:000005|
|228|2144|285721.jpg|0:person|carrying|2:cell phone|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:cell phone[fasterrcnn_thing]fasterrcnn:000005|
|228|2144|285721.jpg|0:person|in front of|3:wall|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|6:wall[mask2former_stuff]mask2former:131:000003|
|229|1350|2378868.jpg|1:person|in|2:car|endpoint_missing_or_wrong_class||0:car[fasterrcnn_thing]fasterrcnn:000000|
|230|723|2348265.jpg|5:person|on|13:bridge|endpoint_missing_or_wrong_class|||
|230|723|2348265.jpg|6:person|over|14:river|endpoint_missing_or_wrong_class||2:river[mask2former_stuff]mask2former:099:000004|
|231|684|2346411.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|231|684|2346411.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|231|684|2346411.jpg|0:person|over|2:sea|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:sea[mask2former_stuff]mask2former:103:000001|
|231|684|2346411.jpg|0:person|looking at|2:sea|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:sea[mask2former_stuff]mask2former:103:000001|
|233|1337|2378360.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|233|1337|2378360.jpg|0:person|on|2:sea|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:sea[mask2former_stuff]mask2former:103:000002|
|235|2050|2412773.jpg|0:person|on|1:surfboard|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|235|2050|2412773.jpg|0:person|attached to|1:surfboard|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|235|2050|2412773.jpg|0:person|standing on|1:surfboard|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|235|2050|2412773.jpg|0:person|playing|1:surfboard|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|235|2050|2412773.jpg|0:person|attached to|2:sea|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:sea[mask2former_stuff]mask2former:103:000001|
|235|2050|2412773.jpg|0:person|touching|2:sea|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:sea[mask2former_stuff]mask2former:103:000001|
|236|561|2340111.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|236|561|2340111.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|236|561|2340111.jpg|0:person|over|2:sea|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:sea[mask2former_stuff]mask2former:103:000001|
|243|1591|2389803.jpg|0:person|sitting on|9:boat|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:boat[fasterrcnn_thing]fasterrcnn:000000|
|243|1591|2389803.jpg|1:person|on|9:boat|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:boat[fasterrcnn_thing]fasterrcnn:000000|
|243|1591|2389803.jpg|1:person|sitting on|9:boat|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:boat[fasterrcnn_thing]fasterrcnn:000000|
|244|603|2342677.jpg|0:person|sitting on|1:bed|endpoint_missing_or_wrong_class||0:bed[fasterrcnn_thing]fasterrcnn:000000; 6:bed[fasterrcnn_thing]fasterrcnn:000006|
|244|603|2342677.jpg|0:person|looking at|2:laptop|endpoint_missing_or_wrong_class||3:laptop[fasterrcnn_thing]fasterrcnn:000003|
|244|603|2342677.jpg|0:person|beside|4:door|endpoint_missing_or_wrong_class|||
|244|603|2342677.jpg|0:person|holding|7:wall|endpoint_missing_or_wrong_class|||
|244|603|2342677.jpg|3:blanket|over|0:person|endpoint_missing_or_wrong_class|||
|244|603|2342677.jpg|7:wall|on back of|0:person|endpoint_missing_or_wrong_class|||
|247|1380|2380325.jpg|0:person|beside|2:car|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|247|1380|2380325.jpg|2:car|beside|0:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|249|520|2337500.jpg|0:person|driving|6:car|wrong_predicate|11:person[fasterrcnn_thing]fasterrcnn:000011; 15:person[fasterrcnn_thing]fasterrcnn:000015|0:car[fasterrcnn_thing]fasterrcnn:000000|
|251|1509|2386257.jpg|0:person|attached to|1:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|251|1509|2386257.jpg|0:person|playing with|2:teddy bear|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:teddy bear[fasterrcnn_thing]fasterrcnn:000002|
|251|1509|2386257.jpg|1:person|attached to|0:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:person[fasterrcnn_thing]fasterrcnn:000001|
|251|1509|2386257.jpg|1:person|attached to|2:teddy bear|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:teddy bear[fasterrcnn_thing]fasterrcnn:000002|
|251|1509|2386257.jpg|2:teddy bear|attached to|1:person|wrong_predicate|2:teddy bear[fasterrcnn_thing]fasterrcnn:000002|0:person[fasterrcnn_thing]fasterrcnn:000000|
|253|1589|2389680.jpg|0:person|beside|12:stairs|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|253|1589|2389680.jpg|0:person|beside|13:water|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|21:water[mask2former_stuff]mask2former:113:000009|
|253|1589|2389680.jpg|2:person|looking at|11:cell phone|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|8:cell phone[fasterrcnn_thing]fasterrcnn:000008|
|253|1589|2389680.jpg|4:person|beside|0:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|5:person[fasterrcnn_thing]fasterrcnn:000005|
|253|1589|2389680.jpg|4:person|looking at|0:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|5:person[fasterrcnn_thing]fasterrcnn:000005|
|253|1589|2389680.jpg|4:person|beside|12:stairs|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|253|1589|2389680.jpg|4:person|beside|13:water|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|21:water[mask2former_stuff]mask2former:113:000009|
|253|1589|2389680.jpg|10:handbag|beside|2:person|wrong_predicate|4:handbag[fasterrcnn_thing]fasterrcnn:000004|1:person[fasterrcnn_thing]fasterrcnn:000001|
|254|896|2356062.jpg|1:person|beside|25:flower|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|35:flower[mask2former_stuff]mask2former:088:000002|
|254|896|2356062.jpg|1:person|in front of|26:tree|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|37:tree[mask2former_stuff]mask2former:116:000006|
|254|896|2356062.jpg|5:person|walking on|28:grass|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|39:grass[mask2former_stuff]mask2former:125:000017|
|254|896|2356062.jpg|7:person|holding|22:teddy bear|endpoint_missing_or_wrong_class|7:person[fasterrcnn_thing]fasterrcnn:000007||
|254|896|2356062.jpg|8:person|walking on|28:grass|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|39:grass[mask2former_stuff]mask2former:125:000017|
|254|896|2356062.jpg|10:person|sitting on|24:blanket|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|258|388|2331571.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|258|388|2331571.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|258|388|2331571.jpg|0:person|on|2:sea|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:sea[mask2former_stuff]mask2former:103:000002|
|259|826|2352851.jpg|0:person|standing on|2:sand|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|262|621|2343341.jpg|1:person|about to hit|4:sports ball|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|6:sports ball[fasterrcnn_thing]fasterrcnn:000006|
|262|621|2343341.jpg|1:person|standing on|11:dirt|rank_below50|5:person[fasterrcnn_thing]fasterrcnn:000005|18:dirt[mask2former_stuff]mask2former:126:000009|
|263|2037|2412228.jpg|8:motorcycle|in front of|4:person|wrong_predicate|13:motorcycle[fasterrcnn_thing]fasterrcnn:000013|0:person[fasterrcnn_thing]fasterrcnn:000000|
|267|1327|2377789.jpg|12:backpack|beside|3:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|267|1327|2377789.jpg|13:handbag|beside|3:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|269|133|2317501.jpg|1:person|guiding|6:person|wrong_predicate|10:person[fasterrcnn_thing]fasterrcnn:000010|0:person[fasterrcnn_thing]fasterrcnn:000000|
|269|133|2317501.jpg|2:person|beside|0:person|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|7:person[fasterrcnn_thing]fasterrcnn:000007|
|269|133|2317501.jpg|2:person|holding|9:person|endpoints_collapsed_to_same_box|5:person[fasterrcnn_thing]fasterrcnn:000005|5:person[fasterrcnn_thing]fasterrcnn:000005|
|271|1757|2397709.jpg|0:person|playing|1:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:sports ball[fasterrcnn_thing]fasterrcnn:000001|
|271|1757|2397709.jpg|0:person|holding|2:tennis racket|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:tennis racket[fasterrcnn_thing]fasterrcnn:000002|
|271|1757|2397709.jpg|0:person|standing on|3:playingfield|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:playingfield[mask2former_stuff]mask2former:097:000002|
|272|1688|2394464.jpg|0:person|sitting on|6:chair|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|276|1693|2394673.jpg|0:person|playing|1:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skis[fasterrcnn_thing]fasterrcnn:000001|
|276|1693|2394673.jpg|1:skis|attached to|0:person|wrong_predicate|1:skis[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|277|1237|2372495.jpg|0:person|holding|15:tennis racket|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|277|1237|2372495.jpg|0:person|standing on|26:playingfield|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|36:playingfield[mask2former_stuff]mask2former:097:000023|
|277|1237|2372495.jpg|3:person|looking at|0:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:person[fasterrcnn_thing]fasterrcnn:000001|
|277|1237|2372495.jpg|3:person|talking to|0:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:person[fasterrcnn_thing]fasterrcnn:000001|
|277|1237|2372495.jpg|3:person|holding|14:tennis racket|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:tennis racket[fasterrcnn_thing]fasterrcnn:000002|
|277|1237|2372495.jpg|7:person|beside|9:person|rank_below50|17:person[fasterrcnn_thing]fasterrcnn:000017|7:person[fasterrcnn_thing]fasterrcnn:000007|
|281|1203|2371154.jpg|0:person|on|8:snow|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|10:snow[mask2former_stuff]mask2former:105:000002|
|281|1203|2371154.jpg|1:person|playing|4:snowboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|7:snowboard[fasterrcnn_thing]fasterrcnn:000007|
|281|1203|2371154.jpg|2:person|wearing|7:snowboard|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|5:snowboard[fasterrcnn_thing]fasterrcnn:000005|
|281|1203|2371154.jpg|3:person|standing on|5:snowboard|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|4:snowboard[fasterrcnn_thing]fasterrcnn:000004|
|283|673|2345745.jpg|0:person|looking at|3:person|rank_below50|0:person[fasterrcnn_thing]fasterrcnn:000000|10:person[fasterrcnn_thing]fasterrcnn:000010|
|283|673|2345745.jpg|1:person|looking at|3:person|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|10:person[fasterrcnn_thing]fasterrcnn:000010|
|283|673|2345745.jpg|2:person|looking at|3:person|rank_below50|3:person[fasterrcnn_thing]fasterrcnn:000003|10:person[fasterrcnn_thing]fasterrcnn:000010|
|285|1218|2371757.jpg|0:person|driving|6:bus|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|0:bus[fasterrcnn_thing]fasterrcnn:000000|
|287|2058|2413475.jpg|0:person|holding|1:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|
|287|2058|2413475.jpg|0:person|playing|1:frisbee|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:frisbee[fasterrcnn_thing]fasterrcnn:000001|
|287|2058|2413475.jpg|0:person|standing on|3:grass|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|4:grass[mask2former_stuff]mask2former:125:000004|
|292|551|2339515.jpg|0:person|looking at|14:river|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|292|551|2339515.jpg|2:person|looking at|8:cow|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|292|551|2339515.jpg|6:cow|looking at|0:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|293|495|2336518.jpg|2:person|holding|14:cell phone|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|293|495|2336518.jpg|2:person|looking at|14:cell phone|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|293|495|2336518.jpg|7:person|talking to|3:person|endpoint_missing_or_wrong_class|||
|293|495|2336518.jpg|8:person|sitting on|13:couch|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|293|495|2336518.jpg|8:person|looking at|15:table|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|296|1346|2378709.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|296|1346|2378709.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|301|1633|2391614.jpg|0:person|holding|7:food|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|301|1633|2391614.jpg|1:oven|in front of|0:person|wrong_predicate|2:oven[fasterrcnn_thing]fasterrcnn:000002|0:person[fasterrcnn_thing]fasterrcnn:000000|
|304|1427|2382463.jpg|0:person|sitting on|2:boat|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|3:boat[fasterrcnn_thing]fasterrcnn:000003|
|304|1427|2382463.jpg|1:person|standing on|2:boat|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|3:boat[fasterrcnn_thing]fasterrcnn:000003|
|304|1427|2382463.jpg|1:person|driving|2:boat|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|3:boat[fasterrcnn_thing]fasterrcnn:000003|
|304|1427|2382463.jpg|1:person|holding|3:cell phone|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|304|1427|2382463.jpg|1:person|wearing|4:sea|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|4:sea[mask2former_stuff]mask2former:103:000002|
|306|1259|2373413.jpg|0:person|leaning on|1:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|306|1259|2373413.jpg|0:person|on|3:road|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|306|1259|2373413.jpg|1:person|standing on|3:road|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|308|1185|2370070.jpg|1:person|talking to|3:person|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|19:person[fasterrcnn_thing]fasterrcnn:000019|
|308|1185|2370070.jpg|1:person|holding|20:backpack|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|26:backpack[fasterrcnn_thing]fasterrcnn:000026|
|308|1185|2370070.jpg|2:person|looking at|29:pavement|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|37:pavement[mask2former_stuff]mask2former:123:000014|
|308|1185|2370070.jpg|4:person|looking at|29:pavement|wrong_predicate|6:person[fasterrcnn_thing]fasterrcnn:000006|37:pavement[mask2former_stuff]mask2former:123:000014|
|308|1185|2370070.jpg|6:person|talking to|25:cell phone|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|308|1185|2370070.jpg|7:person|standing on|29:pavement|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|37:pavement[mask2former_stuff]mask2former:123:000014|
|312|52|1592452.jpg|6:person|in|10:person|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|4:person[fasterrcnn_thing]fasterrcnn:000004|
|312|52|1592452.jpg|7:person|wearing|10:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|4:person[fasterrcnn_thing]fasterrcnn:000004|
|315|1206|2371236.jpg|5:person|in front of|2:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:person[fasterrcnn_thing]fasterrcnn:000002|
|315|1206|2371236.jpg|5:person|beside|3:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|17:person[fasterrcnn_thing]fasterrcnn:000017|
|315|1206|2371236.jpg|9:person|beside|0:person|wrong_predicate|10:person[fasterrcnn_thing]fasterrcnn:000010|8:person[fasterrcnn_thing]fasterrcnn:000008|
|315|1206|2371236.jpg|24:ceiling|over|11:person|pair_not_selected|37:ceiling[mask2former_stuff]mask2former:118:000022|0:person[fasterrcnn_thing]fasterrcnn:000000|
|321|49|1592294.jpg|3:person|standing on|38:road|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|36:road[mask2former_stuff]mask2former:100:000017|
|321|49|1592294.jpg|8:person|walking on|7:person|rank_below50|16:person[fasterrcnn_thing]fasterrcnn:000016|8:person[fasterrcnn_thing]fasterrcnn:000008|
|321|49|1592294.jpg|8:person|looking at|15:bicycle|endpoint_missing_or_wrong_class|16:person[fasterrcnn_thing]fasterrcnn:000016||
|325|703|2347159.jpg|1:person|looking at|8:railroad|wrong_predicate|8:person[fasterrcnn_thing]fasterrcnn:000008|10:railroad[mask2former_stuff]mask2former:098:000006|
|325|703|2347159.jpg|2:person|walking on|8:railroad|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|10:railroad[mask2former_stuff]mask2former:098:000006|
|327|574|2340907.jpg|1:person|looking at|2:person|rank_below50|2:person[fasterrcnn_thing]fasterrcnn:000002|0:person[fasterrcnn_thing]fasterrcnn:000000|
|327|574|2340907.jpg|2:person|playing|3:sports ball|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|328|2111|2416290.jpg|0:person|wearing|24:wall-wood|endpoint_missing_or_wrong_class|5:person[fasterrcnn_thing]fasterrcnn:000005||
|328|2111|2416290.jpg|2:person|holding|12:pizza|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|23:pizza[fasterrcnn_thing]fasterrcnn:000023|
|328|2111|2416290.jpg|2:person|wearing|24:wall-wood|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|328|2111|2416290.jpg|3:person|picking|19:cardboard|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|328|2111|2416290.jpg|3:person|wearing|23:towel|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|328|2111|2416290.jpg|6:person|looking at|1:person|wrong_predicate|7:person[fasterrcnn_thing]fasterrcnn:000007|4:person[fasterrcnn_thing]fasterrcnn:000004|
|328|2111|2416290.jpg|6:person|eating|11:pizza|endpoint_missing_or_wrong_class|7:person[fasterrcnn_thing]fasterrcnn:000007||
|330|1919|2406484.jpg|9:person|in front of|11:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|331|284|2326073.jpg|0:person|driving|2:airplane|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:airplane[fasterrcnn_thing]fasterrcnn:000000|
|332|1415|2382040.jpg|2:person|in front of|0:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|332|1415|2382040.jpg|2:person|sitting on|4:chair|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|332|1415|2382040.jpg|5:dining table|in front of|1:person|wrong_predicate|1:dining table[fasterrcnn_thing]fasterrcnn:000001|3:person[fasterrcnn_thing]fasterrcnn:000003|
|333|1739|2397128.jpg|0:person|attached to|1:horse|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:horse[fasterrcnn_thing]fasterrcnn:000000|
|333|1739|2397128.jpg|0:person|sitting on|1:horse|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:horse[fasterrcnn_thing]fasterrcnn:000000|
|335|303|2326982.jpg|1:donut|attached to|0:person|wrong_predicate|0:donut[fasterrcnn_thing]fasterrcnn:000000|1:person[fasterrcnn_thing]fasterrcnn:000001|
|342|1241|2372547.jpg|0:person|touching|1:kite|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:kite[fasterrcnn_thing]fasterrcnn:000002|
|342|1241|2372547.jpg|1:kite|in front of|0:person|wrong_predicate|2:kite[fasterrcnn_thing]fasterrcnn:000002|1:person[fasterrcnn_thing]fasterrcnn:000001|
|344|556|2339759.jpg|0:person|holding|1:tennis racket|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:tennis racket[fasterrcnn_thing]fasterrcnn:000001|
|344|556|2339759.jpg|0:person|jumping from|2:playingfield|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:playingfield[mask2former_stuff]mask2former:097:000001|
|347|1854|2402990.jpg|0:person|wearing|13:baseball glove|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|6:baseball glove[fasterrcnn_thing]fasterrcnn:000006|
|347|1854|2402990.jpg|4:person|running on|16:playingfield|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|347|1854|2402990.jpg|5:person|walking on|16:playingfield|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|348|205|2321647.jpg|3:person|carrying|18:handbag|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|348|205|2321647.jpg|8:person|in front of|2:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:person[fasterrcnn_thing]fasterrcnn:000005|
|348|205|2321647.jpg|12:person|carrying|16:handbag|endpoint_missing_or_wrong_class|8:person[fasterrcnn_thing]fasterrcnn:000008||
|351|663|2345356.jpg|3:person|riding|21:horse|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:horse[fasterrcnn_thing]fasterrcnn:000000|
|353|1492|2385610.jpg|3:person|beside|15:car|wrong_predicate|9:person[fasterrcnn_thing]fasterrcnn:000009|18:car[fasterrcnn_thing]fasterrcnn:000018|
|353|1492|2385610.jpg|3:person|crossing|27:road|rank_below50|9:person[fasterrcnn_thing]fasterrcnn:000009|34:road[mask2former_stuff]mask2former:100:000014|
|353|1492|2385610.jpg|4:person|walking on|31:pavement|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|353|1492|2385610.jpg|15:car|beside|3:person|rank_below50|18:car[fasterrcnn_thing]fasterrcnn:000018|9:person[fasterrcnn_thing]fasterrcnn:000009|
|354|111|2316413.jpg|0:person|walking on|4:stairs|endpoint_missing_or_wrong_class||4:stairs[mask2former_stuff]mask2former:106:000005|
|354|111|2316413.jpg|1:person|holding|3:cell phone|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:cell phone[fasterrcnn_thing]fasterrcnn:000002|
|354|111|2316413.jpg|1:person|going down|4:stairs|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|4:stairs[mask2former_stuff]mask2former:106:000005|
|354|111|2316413.jpg|1:person|wearing|4:stairs|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|4:stairs[mask2former_stuff]mask2former:106:000005|
|354|111|2316413.jpg|2:person|wearing|0:person|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|354|111|2316413.jpg|8:fence|in front of|0:person|endpoint_missing_or_wrong_class|7:fence[mask2former_stuff]mask2former:117:000008||
|357|726|2348363.jpg|5:person|in front of|14:airplane|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|2:airplane[fasterrcnn_thing]fasterrcnn:000002|
|357|726|2348363.jpg|7:person|looking at|11:person|pair_not_selected|1:person[fasterrcnn_thing]fasterrcnn:000001|5:person[fasterrcnn_thing]fasterrcnn:000005|
|360|1205|2371211.jpg|0:person|holding|3:book|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|360|1205|2371211.jpg|6:tree|in front of|0:person|wrong_predicate|5:tree[mask2former_stuff]mask2former:116:000002|2:person[fasterrcnn_thing]fasterrcnn:000002|
|362|651|2344819.jpg|3:wall|in front of|0:person|wrong_predicate|3:wall[mask2former_stuff]mask2former:131:000003|1:person[fasterrcnn_thing]fasterrcnn:000001|
|364|483|2335916.jpg|1:person|looking at|5:bus|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:bus[fasterrcnn_thing]fasterrcnn:000001; 7:bus[fasterrcnn_thing]fasterrcnn:000007|
|364|483|2335916.jpg|2:person|standing on|9:dirt|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|366|1251|2373084.jpg|3:person|talking to|0:person|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|2:person[fasterrcnn_thing]fasterrcnn:000002|
|366|1251|2373084.jpg|4:person|standing on|9:sand|endpoint_missing_or_wrong_class||7:sand[mask2former_stuff]mask2former:102:000008|
|367|1950|2408290.jpg|0:person|on back of|1:motorcycle|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:motorcycle[fasterrcnn_thing]fasterrcnn:000000|
|369|1390|2380682.jpg|4:person|wearing|10:person|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|0:person[fasterrcnn_thing]fasterrcnn:000000|
|369|1390|2380682.jpg|5:person|standing on|20:snow|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|369|1390|2380682.jpg|8:person|on|10:person|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|0:person[fasterrcnn_thing]fasterrcnn:000000|
|369|1390|2380682.jpg|9:person|looking at|5:person|wrong_predicate|6:person[fasterrcnn_thing]fasterrcnn:000006; 24:person[fasterrcnn_thing]fasterrcnn:000024|1:person[fasterrcnn_thing]fasterrcnn:000001|
|369|1390|2380682.jpg|10:person|walking on|20:snow|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|369|1390|2380682.jpg|11:person|carrying|19:snowboard|wrong_predicate|7:person[fasterrcnn_thing]fasterrcnn:000007|10:snowboard[fasterrcnn_thing]fasterrcnn:000010|
|370|56|1592537.jpg|0:person|riding|1:boat|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:boat[fasterrcnn_thing]fasterrcnn:000000|
|370|56|1592537.jpg|14:tree|beside|0:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|371|2103|2416059.jpg|0:person|carrying|2:backpack|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:backpack[fasterrcnn_thing]fasterrcnn:000002|
|371|2103|2416059.jpg|0:person|standing on|3:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skis[fasterrcnn_thing]fasterrcnn:000001|
|371|2103|2416059.jpg|0:person|playing|3:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skis[fasterrcnn_thing]fasterrcnn:000001|
|373|775|2350750.jpg|3:person|looking at|5:train|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|373|775|2350750.jpg|3:person|standing on|7:platform|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|373|775|2350750.jpg|4:person|looking at|5:train|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|373|775|2350750.jpg|4:person|beside|6:suitcase|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|6:suitcase[fasterrcnn_thing]fasterrcnn:000006|
|373|775|2350750.jpg|4:person|standing on|7:platform|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|373|775|2350750.jpg|6:suitcase|beside|4:person|rank_below50|6:suitcase[fasterrcnn_thing]fasterrcnn:000006|2:person[fasterrcnn_thing]fasterrcnn:000002|
|377|1495|2385674.jpg|1:person|beside|0:person|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|10:person[fasterrcnn_thing]fasterrcnn:000010|
|377|1495|2385674.jpg|2:person|looking at|3:person|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|2:person[fasterrcnn_thing]fasterrcnn:000002|
|377|1495|2385674.jpg|3:person|in front of|2:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|3:person[fasterrcnn_thing]fasterrcnn:000003|
|377|1495|2385674.jpg|3:person|beside|2:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|3:person[fasterrcnn_thing]fasterrcnn:000003|
|377|1495|2385674.jpg|3:person|looking at|2:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|3:person[fasterrcnn_thing]fasterrcnn:000003|
|380|581|2341544.jpg|6:person|standing on|29:pavement|wrong_predicate|6:person[fasterrcnn_thing]fasterrcnn:000006|38:pavement[mask2former_stuff]mask2former:123:000019|
|380|581|2341544.jpg|10:person|carrying|23:handbag|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|15:handbag[fasterrcnn_thing]fasterrcnn:000015|
|381|1745|2397343.jpg|0:person|playing with|1:dog|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|0:dog[fasterrcnn_thing]fasterrcnn:000000|
|381|1745|2397343.jpg|0:person|beside|5:door|endpoint_missing_or_wrong_class|4:person[fasterrcnn_thing]fasterrcnn:000004||
|381|1745|2397343.jpg|0:person|beside|7:table|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|19:table[mask2former_stuff]mask2former:121:000008|
|381|1745|2397343.jpg|2:potted plant|in front of|0:person|wrong_predicate|2:potted plant[fasterrcnn_thing]fasterrcnn:000002|4:person[fasterrcnn_thing]fasterrcnn:000004|
|381|1745|2397343.jpg|5:door|in|0:person|endpoint_missing_or_wrong_class||4:person[fasterrcnn_thing]fasterrcnn:000004|
|381|1745|2397343.jpg|7:table|beside|0:person|wrong_predicate|19:table[mask2former_stuff]mask2former:121:000008|4:person[fasterrcnn_thing]fasterrcnn:000004|
|382|1449|2383257.jpg|0:person|standing on|1:bench|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:bench[fasterrcnn_thing]fasterrcnn:000002|
|382|1449|2383257.jpg|0:person|playing|2:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|382|1449|2383257.jpg|3:door|beside|0:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|385|12|1159501.jpg|0:person|attached to|1:person|endpoints_collapsed_to_same_box|4:person[fasterrcnn_thing]fasterrcnn:000004|4:person[fasterrcnn_thing]fasterrcnn:000004|
|385|12|1159501.jpg|0:person|touching|3:laptop|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|0:laptop[fasterrcnn_thing]fasterrcnn:000000|
|385|12|1159501.jpg|1:person|attached to|0:person|endpoints_collapsed_to_same_box|4:person[fasterrcnn_thing]fasterrcnn:000004|4:person[fasterrcnn_thing]fasterrcnn:000004|
|386|1395|2380947.jpg|3:person|looking at|6:person|rank_below50|4:person[fasterrcnn_thing]fasterrcnn:000004|0:person[fasterrcnn_thing]fasterrcnn:000000|
|386|1395|2380947.jpg|6:person|talking to|11:person|rank_below50|0:person[fasterrcnn_thing]fasterrcnn:000000|1:person[fasterrcnn_thing]fasterrcnn:000001|
|386|1395|2380947.jpg|6:person|attached to|14:tennis racket|pair_not_selected|0:person[fasterrcnn_thing]fasterrcnn:000000|7:tennis racket[fasterrcnn_thing]fasterrcnn:000007|
|386|1395|2380947.jpg|6:person|holding|14:tennis racket|pair_not_selected|0:person[fasterrcnn_thing]fasterrcnn:000000|7:tennis racket[fasterrcnn_thing]fasterrcnn:000007|
|386|1395|2380947.jpg|12:person|talking to|4:person|rank_below50|12:person[fasterrcnn_thing]fasterrcnn:000012|13:person[fasterrcnn_thing]fasterrcnn:000013|
|387|1391|2380691.jpg|0:person|looking at|1:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:sports ball[fasterrcnn_thing]fasterrcnn:000001|
|387|1391|2380691.jpg|0:person|chasing|1:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:sports ball[fasterrcnn_thing]fasterrcnn:000001|
|387|1391|2380691.jpg|0:person|about to hit|1:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:sports ball[fasterrcnn_thing]fasterrcnn:000001|
|387|1391|2380691.jpg|0:person|running on|4:floor|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|389|1609|2390707.jpg|6:person|in front of|8:person|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|9:person[fasterrcnn_thing]fasterrcnn:000009|
|389|1609|2390707.jpg|6:person|beside|16:chair|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|27:chair[fasterrcnn_thing]fasterrcnn:000027|
|389|1609|2390707.jpg|6:person|attached to|21:playingfield|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|28:playingfield[mask2former_stuff]mask2former:097:000005|
|389|1609|2390707.jpg|6:person|attached to|22:towel|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|389|1609|2390707.jpg|6:person|swinging|22:towel|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|389|1609|2390707.jpg|8:person|looking at|6:person|rank_below50|9:person[fasterrcnn_thing]fasterrcnn:000009|3:person[fasterrcnn_thing]fasterrcnn:000003|
|389|1609|2390707.jpg|16:chair|beside|6:person|rank_below50|27:chair[fasterrcnn_thing]fasterrcnn:000027|3:person[fasterrcnn_thing]fasterrcnn:000003|
|394|1496|2385703.jpg|0:person|carrying|6:handbag|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|9:handbag[fasterrcnn_thing]fasterrcnn:000009|
|395|758|2350121.jpg|1:person|on back of|5:horse|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:horse[fasterrcnn_thing]fasterrcnn:000000|
|395|758|2350121.jpg|2:person|on back of|4:horse|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|1:horse[fasterrcnn_thing]fasterrcnn:000001|
|396|630|2343959.jpg|5:person|in front of|8:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|396|630|2343959.jpg|5:person|wearing|15:tie|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|396|630|2343959.jpg|8:person|in front of|19:mirror|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|396|630|2343959.jpg|9:person|looking at|8:person|rank_below50|4:person[fasterrcnn_thing]fasterrcnn:000004|2:person[fasterrcnn_thing]fasterrcnn:000002|
|396|630|2343959.jpg|9:person|beside|10:person|rank_below50|4:person[fasterrcnn_thing]fasterrcnn:000004|1:person[fasterrcnn_thing]fasterrcnn:000001|
|396|630|2343959.jpg|10:person|beside|16:dining table|rank_below50|1:person[fasterrcnn_thing]fasterrcnn:000001|23:dining table[fasterrcnn_thing]fasterrcnn:000023|
|396|630|2343959.jpg|18:light|over|8:person|endpoint_missing_or_wrong_class||2:person[fasterrcnn_thing]fasterrcnn:000002|
|398|1128|2366957.jpg|4:person|looking at|30:pavement|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|36:pavement[mask2former_stuff]mask2former:123:000026|
|398|1128|2366957.jpg|13:person|in front of|28:tree|endpoint_missing_or_wrong_class||33:tree[mask2former_stuff]mask2former:116:000007|
|399|1835|2402046.jpg|1:person|standing on|17:rock|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|399|1835|2402046.jpg|9:person|entering|13:boat|endpoint_missing_or_wrong_class||0:boat[fasterrcnn_thing]fasterrcnn:000000|
|400|731|2348722.jpg|3:person|wearing|17:baseball glove|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|400|731|2348722.jpg|4:person|carrying|16:baseball bat|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|400|731|2348722.jpg|6:person|talking to|5:person|endpoint_missing_or_wrong_class|19:person[fasterrcnn_thing]fasterrcnn:000019||
|400|731|2348722.jpg|7:person|running on|19:playingfield|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|32:playingfield[mask2former_stuff]mask2former:097:000016|
|404|736|2348945.jpg|0:person|talking to|1:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|404|736|2348945.jpg|0:person|standing on|5:truck|endpoint_missing_or_wrong_class||3:truck[fasterrcnn_thing]fasterrcnn:000003|
|404|736|2348945.jpg|1:person|standing on|9:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|406|1324|2377760.jpg|0:person|on|1:truck|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|406|1324|2377760.jpg|0:person|sitting on|1:truck|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|410|761|2350256.jpg|0:person|in|1:bus|endpoint_missing_or_wrong_class||0:bus[fasterrcnn_thing]fasterrcnn:000000|
|410|761|2350256.jpg|0:person|driving|1:bus|endpoint_missing_or_wrong_class||0:bus[fasterrcnn_thing]fasterrcnn:000000|
|413|280|2325881.jpg|0:person|holding|1:banana|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:banana[fasterrcnn_thing]fasterrcnn:000003|
|413|280|2325881.jpg|0:person|sitting on|2:chair|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|413|280|2325881.jpg|0:person|in front of|4:wall-wood|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|414|1318|2377223.jpg|0:person|in front of|1:person|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|414|1318|2377223.jpg|0:person|swinging|4:tennis racket|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:tennis racket[fasterrcnn_thing]fasterrcnn:000001|
|414|1318|2377223.jpg|1:person|in front of|6:wall|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|16:wall[mask2former_stuff]mask2former:131:000010|
|414|1318|2377223.jpg|3:sports ball|beside|2:person|endpoint_missing_or_wrong_class|||
|417|1547|2387788.jpg|0:person|standing on|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|417|1547|2387788.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|417|1547|2387788.jpg|0:person|wearing|2:platform|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|417|1547|2387788.jpg|0:person|wearing|3:pavement|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:pavement[mask2former_stuff]mask2former:123:000002|
|419|962|2359075.jpg|11:fence|in front of|5:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|419|962|2359075.jpg|11:fence|in front of|6:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|421|1772|2398484.jpg|0:person|on back of|2:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:person[fasterrcnn_thing]fasterrcnn:000002|
|421|1772|2398484.jpg|1:person|holding|3:baseball bat|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|4:baseball bat[fasterrcnn_thing]fasterrcnn:000004|
|421|1772|2398484.jpg|1:person|standing on|5:playingfield|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:playingfield[mask2former_stuff]mask2former:097:000002|
|421|1772|2398484.jpg|2:person|attached to|0:person|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|1:person[fasterrcnn_thing]fasterrcnn:000001|
|422|1007|2361180.jpg|3:person|in front of|1:person|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|4:person[fasterrcnn_thing]fasterrcnn:000004|
|423|2171|713172.jpg|0:person|in|13:building|endpoint_missing_or_wrong_class|||
|427|361|2329834.jpg|0:person|in front of|15:wall-wood|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|428|1752|2397624.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|428|1752|2397624.jpg|0:person|riding|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|428|1752|2397624.jpg|0:person|looking at|3:pavement|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:pavement[mask2former_stuff]mask2former:123:000004|
|430|1713|2395938.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|430|1713|2395938.jpg|0:person|going down|2:stairs|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|432|880|2355316.jpg|0:person|in front of|7:car|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|8:car[fasterrcnn_thing]fasterrcnn:000008|
|432|880|2355316.jpg|0:person|standing on|12:pavement|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|19:pavement[mask2former_stuff]mask2former:123:000009|
|432|880|2355316.jpg|1:person|standing on|12:pavement|wrong_predicate|9:person[fasterrcnn_thing]fasterrcnn:000009|19:pavement[mask2former_stuff]mask2former:123:000009|
|432|880|2355316.jpg|6:person|in front of|13:building|rank_below50|0:person[fasterrcnn_thing]fasterrcnn:000000|20:building[mask2former_stuff]mask2former:129:000001|
|438|163|2319267.jpg|0:person|on|2:truck|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|438|163|2319267.jpg|0:person|standing on|2:truck|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|439|1357|2379131.jpg|0:person|looking at|8:apple|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:apple[fasterrcnn_thing]fasterrcnn:000000|
|439|1357|2379131.jpg|0:person|catching|8:apple|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:apple[fasterrcnn_thing]fasterrcnn:000000|
|441|2118|2416492.jpg|0:person|beside|1:toilet|endpoint_missing_or_wrong_class||2:toilet[fasterrcnn_thing]fasterrcnn:000002|
|441|2118|2416492.jpg|0:person|cleaning|1:toilet|endpoint_missing_or_wrong_class||2:toilet[fasterrcnn_thing]fasterrcnn:000002|
|441|2118|2416492.jpg|0:person|touching|1:toilet|endpoint_missing_or_wrong_class||2:toilet[fasterrcnn_thing]fasterrcnn:000002|
|443|192|2321324.jpg|0:person|walking on|22:pavement|endpoint_missing_or_wrong_class|7:person[fasterrcnn_thing]fasterrcnn:000007||
|443|192|2321324.jpg|1:person|feeding|11:bird|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|446|712|2347578.jpg|0:person|riding|1:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skis[fasterrcnn_thing]fasterrcnn:000001|
|447|104|2316313.jpg|0:person|in front of|1:person|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|4:person[fasterrcnn_thing]fasterrcnn:000004|
|447|104|2316313.jpg|1:person|in|3:car|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|0:car[fasterrcnn_thing]fasterrcnn:000000|
|448|792|2351247.jpg|4:person|beside|8:person|rank_below50|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|448|792|2351247.jpg|8:person|picking|30:food|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|449|784|2351059.jpg|0:person|running on|6:sand|endpoint_missing_or_wrong_class|2:person[fasterrcnn_thing]fasterrcnn:000002||
|449|784|2351059.jpg|1:person|catching|3:sports ball|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|449|784|2351059.jpg|1:person|wearing|4:baseball glove|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|449|784|2351059.jpg|1:person|running on|6:sand|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|450|1615|2390859.jpg|0:person|looking at|2:cell phone|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:cell phone[fasterrcnn_thing]fasterrcnn:000002|
|450|1615|2390859.jpg|0:person|in front of|3:paper|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|450|1615|2390859.jpg|0:person|in front of|4:building|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|453|1642|2392244.jpg|0:person|looking at|5:bowl|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|12:bowl[fasterrcnn_thing]fasterrcnn:000012|
|453|1642|2392244.jpg|10:dining table|attached to|0:person|wrong_predicate|2:dining table[fasterrcnn_thing]fasterrcnn:000002|1:person[fasterrcnn_thing]fasterrcnn:000001|
|454|629|2343942.jpg|1:person|looking at|23:laptop|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|29:laptop[fasterrcnn_thing]fasterrcnn:000029|
|454|629|2343942.jpg|3:person|wearing|18:chair|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|7:chair[fasterrcnn_thing]fasterrcnn:000007|
|454|629|2343942.jpg|19:chair|in front of|10:person|rank_below50|9:chair[fasterrcnn_thing]fasterrcnn:000009|3:person[fasterrcnn_thing]fasterrcnn:000003; 25:person[fasterrcnn_thing]fasterrcnn:000025|
|456|1089|2365077.jpg|0:person|talking to|2:person|wrong_predicate|14:person[fasterrcnn_thing]fasterrcnn:000014|17:person[fasterrcnn_thing]fasterrcnn:000017; 26:person[fasterrcnn_thing]fasterrcnn:000026|
|457|587|2341770.jpg|0:person|driving|3:bus|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:bus[fasterrcnn_thing]fasterrcnn:000000|
|457|587|2341770.jpg|1:person|sitting on|3:bus|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|0:bus[fasterrcnn_thing]fasterrcnn:000000|
|457|587|2341770.jpg|2:person|sitting on|3:bus|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:bus[fasterrcnn_thing]fasterrcnn:000000|
|458|1575|2388803.jpg|0:person|wearing|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|458|1575|2388803.jpg|0:person|looking at|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|458|1575|2388803.jpg|0:person|catching|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|458|1575|2388803.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:skateboard[fasterrcnn_thing]fasterrcnn:000001|
|458|1575|2388803.jpg|0:person|jumping over|2:pavement|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:pavement[mask2former_stuff]mask2former:123:000003|
|458|1575|2388803.jpg|0:person|wearing|2:pavement|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:pavement[mask2former_stuff]mask2former:123:000003|
|461|107|2316321.jpg|0:person|standing on|6:skis|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|4:skis[fasterrcnn_thing]fasterrcnn:000004|
|461|107|2316321.jpg|2:person|going down|9:snow|endpoint_missing_or_wrong_class||13:snow[mask2former_stuff]mask2former:105:000002|
|461|107|2316321.jpg|3:person|going down|9:snow|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|13:snow[mask2former_stuff]mask2former:105:000002|
|463|555|2339725.jpg|0:person|biting|8:toothbrush|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|6:toothbrush[fasterrcnn_thing]fasterrcnn:000006|
|465|1540|2387468.jpg|0:person|beside|4:train|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|0:train[fasterrcnn_thing]fasterrcnn:000000|
|465|1540|2387468.jpg|2:person|beside|4:train|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|0:train[fasterrcnn_thing]fasterrcnn:000000|
|466|1797|2400508.jpg|0:person|playing|1:kite|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:kite[fasterrcnn_thing]fasterrcnn:000001|
|470|1101|2365885.jpg|0:person|playing|2:sports ball|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|4:sports ball[fasterrcnn_thing]fasterrcnn:000004|
|470|1101|2365885.jpg|0:person|holding|3:tennis racket|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|2:tennis racket[fasterrcnn_thing]fasterrcnn:000002|
|470|1101|2365885.jpg|0:person|running on|4:playingfield|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|6:playingfield[mask2former_stuff]mask2former:097:000002|
|471|1700|2394982.jpg|0:person|in front of|8:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:person[fasterrcnn_thing]fasterrcnn:000002|
|471|1700|2394982.jpg|0:person|attached to|13:fence|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|22:fence[mask2former_stuff]mask2former:117:000009|
|471|1700|2394982.jpg|8:person|attached to|13:fence|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|22:fence[mask2former_stuff]mask2former:117:000009|
|472|404|2332502.jpg|1:person|driving|14:boat|wrong_predicate|7:person[fasterrcnn_thing]fasterrcnn:000007|0:boat[fasterrcnn_thing]fasterrcnn:000000|
|472|404|2332502.jpg|2:person|over|18:river|wrong_predicate|5:person[fasterrcnn_thing]fasterrcnn:000005|23:river[mask2former_stuff]mask2former:099:000007|
|473|605|2342711.jpg|0:person|looking at|22:bowl|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|473|605|2342711.jpg|1:person|beside|0:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|478|1804|2400822.jpg|0:person|attached to|3:surfboard|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:surfboard[fasterrcnn_thing]fasterrcnn:000002|
|478|1804|2400822.jpg|0:person|playing|3:surfboard|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|2:surfboard[fasterrcnn_thing]fasterrcnn:000002|
|478|1804|2400822.jpg|0:person|on|4:sand|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|478|1804|2400822.jpg|0:person|standing on|4:sand|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|478|1804|2400822.jpg|0:person|beside|5:sea|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|5:sea[mask2former_stuff]mask2former:103:000003|
|478|1804|2400822.jpg|1:person|on|4:sand|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|478|1804|2400822.jpg|1:person|walking on|4:sand|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|478|1804|2400822.jpg|1:person|beside|5:sea|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:sea[mask2former_stuff]mask2former:103:000003|
|480|461|2334659.jpg|0:person|in front of|9:house|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|480|461|2334659.jpg|0:person|walking on|13:pavement|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|480|461|2334659.jpg|2:person|in front of|9:house|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|480|461|2334659.jpg|2:person|walking on|13:pavement|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|481|797|2351374.jpg|7:person|attached to|14:pavement|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|23:pavement[mask2former_stuff]mask2former:123:000014|
|481|797|2351374.jpg|8:person|in front of|9:person|wrong_predicate|14:person[fasterrcnn_thing]fasterrcnn:000014|11:person[fasterrcnn_thing]fasterrcnn:000011|
|481|797|2351374.jpg|10:person|going down|14:pavement|wrong_predicate|9:person[fasterrcnn_thing]fasterrcnn:000009|23:pavement[mask2former_stuff]mask2former:123:000014|
|481|797|2351374.jpg|12:person|beside|15:building|wrong_predicate|2:person[fasterrcnn_thing]fasterrcnn:000002|24:building[mask2former_stuff]mask2former:129:000003|
|481|797|2351374.jpg|13:sky|on|3:person|wrong_predicate|22:sky[mask2former_stuff]mask2former:119:000007|5:person[fasterrcnn_thing]fasterrcnn:000005|
|483|1172|2369539.jpg|0:person|catching|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|483|1172|2369539.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|483|1172|2369539.jpg|0:person|on|2:sea|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:sea[mask2former_stuff]mask2former:103:000002|
|484|1699|2394864.jpg|4:umbrella|over|0:person|rank_below50|0:umbrella[fasterrcnn_thing]fasterrcnn:000000|2:person[fasterrcnn_thing]fasterrcnn:000002|
|485|57|1592560.jpg|0:person|beside|7:table|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|19:table[mask2former_stuff]mask2former:121:000008|
|485|57|1592560.jpg|0:person|in front of|9:wall|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|20:wall[mask2former_stuff]mask2former:131:000010|
|486|1052|2362836.jpg|0:person|guiding|3:person|wrong_predicate|15:person[fasterrcnn_thing]fasterrcnn:000015|1:person[fasterrcnn_thing]fasterrcnn:000001|
|486|1052|2362836.jpg|3:person|in front of|0:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|15:person[fasterrcnn_thing]fasterrcnn:000015|
|486|1052|2362836.jpg|4:person|on|1:person|endpoint_missing_or_wrong_class||0:person[fasterrcnn_thing]fasterrcnn:000000|
|486|1052|2362836.jpg|5:person|walking on|8:road|endpoint_missing_or_wrong_class|3:person[fasterrcnn_thing]fasterrcnn:000003||
|489|610|2342847.jpg|2:person|walking on|23:road|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|28:road[mask2former_stuff]mask2former:100:000015|
|489|610|2342847.jpg|6:person|driving|11:truck|wrong_predicate|8:person[fasterrcnn_thing]fasterrcnn:000008; 27:person[fasterrcnn_thing]fasterrcnn:000027|18:truck[fasterrcnn_thing]fasterrcnn:000018|
|490|2161|498294.jpg|0:person|in front of|1:person|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|6:person[fasterrcnn_thing]fasterrcnn:000006|
|490|2161|498294.jpg|1:person|wearing|6:baseball glove|wrong_predicate|6:person[fasterrcnn_thing]fasterrcnn:000006|5:baseball glove[fasterrcnn_thing]fasterrcnn:000005|
|490|2161|498294.jpg|4:person|wearing|8:baseball glove|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|7:baseball glove[fasterrcnn_thing]fasterrcnn:000007|
|490|2161|498294.jpg|5:person|running on|9:playingfield|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|13:playingfield[mask2former_stuff]mask2former:097:000003|
|491|382|2331166.jpg|0:person|on|17:bus|wrong_predicate|14:person[fasterrcnn_thing]fasterrcnn:000014|0:bus[fasterrcnn_thing]fasterrcnn:000000|
|491|382|2331166.jpg|8:person|driving|17:bus|wrong_predicate|4:person[fasterrcnn_thing]fasterrcnn:000004|0:bus[fasterrcnn_thing]fasterrcnn:000000|
|492|1031|2362238.jpg|0:person|playing|2:surfboard|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|1:surfboard[fasterrcnn_thing]fasterrcnn:000001|
|492|1031|2362238.jpg|0:person|on|3:sea|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|3:sea[mask2former_stuff]mask2former:103:000002|
|493|374|2330610.jpg|0:person|in|1:truck|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|493|374|2330610.jpg|0:person|driving|1:truck|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|494|265|2324812.jpg|0:person|touching|2:person|wrong_predicate|3:person[fasterrcnn_thing]fasterrcnn:000003|2:person[fasterrcnn_thing]fasterrcnn:000002|
|494|265|2324812.jpg|1:person|attached to|3:person|wrong_predicate|1:person[fasterrcnn_thing]fasterrcnn:000001|0:person[fasterrcnn_thing]fasterrcnn:000000|
|494|265|2324812.jpg|3:person|carrying|4:handbag|wrong_predicate|0:person[fasterrcnn_thing]fasterrcnn:000000|5:handbag[fasterrcnn_thing]fasterrcnn:000005|
|494|265|2324812.jpg|3:person|in front of|7:window|endpoint_missing_or_wrong_class|0:person[fasterrcnn_thing]fasterrcnn:000000||
|494|265|2324812.jpg|5:cell phone|touching|3:person|wrong_predicate|6:cell phone[fasterrcnn_thing]fasterrcnn:000006|0:person[fasterrcnn_thing]fasterrcnn:000000|
|496|769|2350508.jpg|1:person|attached to|2:pizza|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|496|769|2350508.jpg|1:person|looking at|2:pizza|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|496|769|2350508.jpg|1:person|eating|2:pizza|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|496|769|2350508.jpg|1:person|in front of|3:wall|endpoint_missing_or_wrong_class|1:person[fasterrcnn_thing]fasterrcnn:000001||
|496|769|2350508.jpg|2:pizza|attached to|1:person|endpoint_missing_or_wrong_class||1:person[fasterrcnn_thing]fasterrcnn:000001|
|500|1155|2368389.jpg|3:fence|enclosing|0:person|wrong_predicate|5:fence[mask2former_stuff]mask2former:117:000005|0:person[fasterrcnn_thing]fasterrcnn:000000|

## D_mask2former_thing_plus_stuff

未命中715条。

|序号|索引|图片|GT主语|谓词|GT宾语|失败阶段|匹配主语候选|匹配宾语候选|
|---:|---:|---|---|---|---|---|---|---|
|6|295|2326503.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000004|
|7|1675|2393584.jpg|0:person|in|2:tv|endpoint_missing_or_wrong_class||0:tv[mask2former_thing]mask2former:062:000002|
|10|553|2339606.jpg|0:person|running on|16:dirt|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|10|553|2339606.jpg|1:person|standing on|16:dirt|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000008||
|10|553|2339606.jpg|4:person|standing on|12:playingfield|wrong_predicate|2:person[mask2former_thing]mask2former:000:000007|6:playingfield[mask2former_stuff]mask2former:097:000004|
|10|553|2339606.jpg|6:person|wearing|9:baseball glove|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|16|1466|2384291.jpg|0:person|beside|1:person|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000010||
|16|1466|2384291.jpg|1:person|beside|0:person|endpoint_missing_or_wrong_class||2:person[mask2former_thing]mask2former:000:000010|
|16|1466|2384291.jpg|2:person|holding|21:paper|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|16|1466|2384291.jpg|3:person|walking on|20:pavement|wrong_predicate|3:person[mask2former_thing]mask2former:000:000016|18:pavement[mask2former_stuff]mask2former:123:000013|
|16|1466|2384291.jpg|4:person|on|20:pavement|endpoint_missing_or_wrong_class||18:pavement[mask2former_stuff]mask2former:123:000013|
|18|1983|2409607.jpg|0:person|sitting on|1:horse|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:horse[mask2former_thing]mask2former:017:000005|
|18|1983|2409607.jpg|0:person|over|5:grass|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|6:grass[mask2former_stuff]mask2former:125:000007|
|21|411|2332726.jpg|0:person|walking on|8:sand|wrong_predicate|2:person[mask2former_thing]mask2former:000:000007|4:sand[mask2former_stuff]mask2former:102:000006|
|21|411|2332726.jpg|3:person|flying over|5:kite|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|21|411|2332726.jpg|3:person|looking at|5:kite|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|21|411|2332726.jpg|3:person|playing|5:kite|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|21|411|2332726.jpg|3:person|wearing|8:sand|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|4:sand[mask2former_stuff]mask2former:102:000006|
|22|129|2317125.jpg|2:person|walking on|11:road|wrong_predicate|2:person[mask2former_thing]mask2former:000:000008|9:road[mask2former_stuff]mask2former:100:000009|
|22|129|2317125.jpg|4:person|standing on|11:road|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|9:road[mask2former_stuff]mask2former:100:000009|
|22|129|2317125.jpg|9:house|beside|0:person|rank_below50|8:house[mask2former_stuff]mask2former:091:000013|1:person[mask2former_thing]mask2former:000:000005|
|23|1055|2363004.jpg|0:person|holding|12:handbag|wrong_predicate|5:person[mask2former_thing]mask2former:000:000010|9:handbag[mask2former_thing]mask2former:026:000011|
|23|1055|2363004.jpg|2:person|walking on|21:pavement|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000007||
|23|1055|2363004.jpg|3:person|walking on|21:pavement|endpoint_missing_or_wrong_class|||
|23|1055|2363004.jpg|7:person|walking on|21:pavement|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000008||
|23|1055|2363004.jpg|8:person|walking on|21:pavement|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000013||
|23|1055|2363004.jpg|10:train|beside|8:person|rank_below50|8:train[mask2former_thing]mask2former:006:000006|6:person[mask2former_thing]mask2former:000:000013|
|24|1712|2395918.jpg|0:person|crossing|5:pavement|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|5:pavement[mask2former_stuff]mask2former:123:000007|
|24|1712|2395918.jpg|1:person|beside|6:grass|wrong_predicate|1:person[mask2former_thing]mask2former:000:000005|6:grass[mask2former_stuff]mask2former:125:000006|
|24|1712|2395918.jpg|2:skateboard|attached to|0:person|wrong_predicate|2:skateboard[mask2former_thing]mask2former:036:000002|0:person[mask2former_thing]mask2former:000:000003|
|26|892|2355904.jpg|0:person|touching|10:table|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000006||
|27|2018|2411180.jpg|0:person|standing on|6:railroad|endpoint_missing_or_wrong_class||4:railroad[mask2former_stuff]mask2former:098:000007|
|28|164|2319298.jpg|0:person|driving|1:car|endpoint_missing_or_wrong_class||1:car[mask2former_thing]mask2former:002:000006|
|29|81|2315729.jpg|2:person|slicing|15:cake|wrong_predicate|3:person[mask2former_thing]mask2former:000:000011; 4:person[mask2former_thing]mask2former:000:000013|12:cake[mask2former_thing]mask2former:055:000008|
|29|81|2315729.jpg|3:person|attached to|4:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|2:person[mask2former_thing]mask2former:000:000010|
|29|81|2315729.jpg|6:person|attached to|2:person|endpoint_missing_or_wrong_class||3:person[mask2former_thing]mask2former:000:000011; 4:person[mask2former_thing]mask2former:000:000013|
|33|1896|2405341.jpg|0:person|holding|1:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|0:person[mask2former_thing]mask2former:000:000001|
|35|1326|2377788.jpg|0:person|feeding|3:cow|wrong_predicate|0:person[mask2former_thing]mask2former:000:000007; 1:person[mask2former_thing]mask2former:000:000009|6:cow[mask2former_thing]mask2former:019:000008|
|35|1326|2377788.jpg|6:cow|in front of|1:person|wrong_predicate|8:cow[mask2former_thing]mask2former:019:000013|0:person[mask2former_thing]mask2former:000:000007|
|36|922|2357107.jpg|1:person|in|9:boat|wrong_predicate|2:person[mask2former_thing]mask2former:000:000003|8:boat[mask2former_thing]mask2former:008:000006|
|36|922|2357107.jpg|4:person|walking on|14:platform|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000007||
|38|1914|2406339.jpg|0:person|beside|3:person|endpoint_missing_or_wrong_class|||
|38|1914|2406339.jpg|0:person|looking at|22:playingfield|endpoint_missing_or_wrong_class|||
|38|1914|2406339.jpg|2:person|looking at|22:playingfield|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000006||
|38|1914|2406339.jpg|2:person|attached to|26:wall|wrong_predicate|2:person[mask2former_thing]mask2former:000:000006|10:wall[mask2former_stuff]mask2former:131:000011|
|40|208|2321715.jpg|0:person|on|7:motorcycle|endpoint_missing_or_wrong_class|||
|40|208|2321715.jpg|0:person|riding|7:motorcycle|endpoint_missing_or_wrong_class|||
|40|208|2321715.jpg|3:person|exiting|12:tent|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000008||
|40|208|2321715.jpg|3:person|walking on|16:floor|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000008||
|44|489|2336251.jpg|0:person|sitting on|9:pavement|endpoint_missing_or_wrong_class||7:pavement[mask2former_stuff]mask2former:123:000008|
|44|489|2336251.jpg|1:person|talking to|0:person|endpoint_missing_or_wrong_class|||
|44|489|2336251.jpg|1:person|sitting on|9:pavement|endpoint_missing_or_wrong_class||7:pavement[mask2former_stuff]mask2former:123:000008|
|44|489|2336251.jpg|2:person|sitting on|9:pavement|endpoint_missing_or_wrong_class||7:pavement[mask2former_stuff]mask2former:123:000008|
|44|489|2336251.jpg|3:person|playing|6:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|3:skateboard[mask2former_thing]mask2former:036:000006|
|44|489|2336251.jpg|3:person|jumping from|9:pavement|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|7:pavement[mask2former_stuff]mask2former:123:000008|
|46|674|2345802.jpg|0:person|sitting on|2:chair|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|46|674|2345802.jpg|0:person|in front of|3:counter|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|51|1507|2386227.jpg|0:person|beside|1:person|endpoint_missing_or_wrong_class|||
|51|1507|2386227.jpg|1:person|in|2:tv|endpoint_missing_or_wrong_class||0:tv[mask2former_thing]mask2former:062:000003|
|52|1139|2367625.jpg|0:person|holding|1:spoon|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|52|1139|2367625.jpg|0:person|in front of|3:oven|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|2:oven[mask2former_thing]mask2former:069:000006|
|53|1627|2391314.jpg|0:person|standing on|1:skis|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000005||
|53|1627|2391314.jpg|0:person|wearing|1:skis|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000005||
|53|1627|2391314.jpg|0:person|beside|3:tree|wrong_predicate|0:person[mask2former_thing]mask2former:000:000005|4:tree[mask2former_stuff]mask2former:116:000001|
|54|237|2323211.jpg|5:person|over|1:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|3:person[mask2former_thing]mask2former:000:000006|
|54|237|2323211.jpg|5:person|over|8:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|4:person[mask2former_thing]mask2former:000:000007|
|54|237|2323211.jpg|5:person|on|17:grass|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|18:grass[mask2former_stuff]mask2former:125:000014|
|54|237|2323211.jpg|5:person|jumping from|17:grass|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|18:grass[mask2former_stuff]mask2former:125:000014|
|55|166|2319395.jpg|0:person|walking on|6:road|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|4:road[mask2former_stuff]mask2former:100:000007|
|55|166|2319395.jpg|1:person|standing on|6:road|endpoint_missing_or_wrong_class||4:road[mask2former_stuff]mask2former:100:000007|
|57|327|2328174.jpg|0:person|in front of|1:car|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:car[mask2former_thing]mask2former:002:000001|
|57|327|2328174.jpg|0:person|picking|2:umbrella|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:umbrella[mask2former_thing]mask2former:025:000002|
|57|327|2328174.jpg|0:person|in front of|3:potted plant|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|3:potted plant[mask2former_thing]mask2former:058:000004|
|57|327|2328174.jpg|0:person|standing on|6:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|58|617|2343155.jpg|0:person|throwing|3:sports ball|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|58|617|2343155.jpg|0:person|about to hit|3:sports ball|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|58|617|2343155.jpg|0:person|standing on|6:playingfield|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|60|2159|498242.jpg|0:person|beside|9:person|rank_below50|6:person[mask2former_thing]mask2former:000:000008|2:person[mask2former_thing]mask2former:000:000004|
|60|2159|498242.jpg|0:person|looking at|9:person|rank_below50|6:person[mask2former_thing]mask2former:000:000008|2:person[mask2former_thing]mask2former:000:000004|
|60|2159|498242.jpg|1:person|beside|0:person|rank_below50|1:person[mask2former_thing]mask2former:000:000002|6:person[mask2former_thing]mask2former:000:000008|
|60|2159|498242.jpg|1:person|looking at|9:person|rank_below50|1:person[mask2former_thing]mask2former:000:000002|2:person[mask2former_thing]mask2former:000:000004|
|60|2159|498242.jpg|2:person|standing on|14:pavement|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|15:pavement[mask2former_stuff]mask2former:123:000015|
|60|2159|498242.jpg|3:person|looking at|1:person|rank_below50|4:person[mask2former_thing]mask2former:000:000006|1:person[mask2former_thing]mask2former:000:000002|
|60|2159|498242.jpg|3:person|beside|8:person|rank_below50|4:person[mask2former_thing]mask2former:000:000006|7:person[mask2former_thing]mask2former:000:000010|
|60|2159|498242.jpg|6:person|beside|4:person|endpoint_missing_or_wrong_class|9:person[mask2former_thing]mask2former:000:000013||
|60|2159|498242.jpg|8:person|beside|5:person|rank_below50|7:person[mask2former_thing]mask2former:000:000010|8:person[mask2former_thing]mask2former:000:000011|
|60|2159|498242.jpg|8:person|attached to|5:person|wrong_predicate|7:person[mask2former_thing]mask2former:000:000010|8:person[mask2former_thing]mask2former:000:000011|
|60|2159|498242.jpg|9:person|looking at|0:person|wrong_predicate|2:person[mask2former_thing]mask2former:000:000004|6:person[mask2former_thing]mask2former:000:000008|
|60|2159|498242.jpg|9:person|holding|10:umbrella|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000004||
|61|1219|2371806.jpg|0:person|running on|2:playingfield|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|2:playingfield[mask2former_stuff]mask2former:097:000003|
|63|1445|2383111.jpg|0:person|riding|6:horse|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|63|1445|2383111.jpg|1:person|riding|7:horse|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000008||
|63|1445|2383111.jpg|3:person|riding|4:horse|endpoint_missing_or_wrong_class||4:horse[mask2former_thing]mask2former:017:000003|
|64|1596|2390113.jpg|0:person|riding|1:elephant|endpoint_missing_or_wrong_class||2:elephant[mask2former_thing]mask2former:020:000004|
|66|749|2349334.jpg|1:person|looking at|4:person|wrong_predicate|2:person[mask2former_thing]mask2former:000:000006|0:person[mask2former_thing]mask2former:000:000001|
|66|749|2349334.jpg|2:person|eating|19:pizza|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000017||
|66|749|2349334.jpg|6:person|talking to|5:person|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000011||
|66|749|2349334.jpg|23:ceiling|on|4:person|wrong_predicate|18:ceiling[mask2former_stuff]mask2former:118:000018|0:person[mask2former_thing]mask2former:000:000001|
|68|1598|2390200.jpg|0:person|swinging|6:remote|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|68|1598|2390200.jpg|0:person|holding|9:remote|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|68|1598|2390200.jpg|1:person|holding|3:potted plant|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|68|1598|2390200.jpg|1:person|swinging|8:remote|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|68|1598|2390200.jpg|1:person|in front of|16:table|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|70|714|2347722.jpg|0:person|attached to|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:surfboard[mask2former_thing]mask2former:037:000003|
|70|714|2347722.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:surfboard[mask2former_thing]mask2former:037:000003|
|70|714|2347722.jpg|0:person|touching|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:surfboard[mask2former_thing]mask2former:037:000003|
|70|714|2347722.jpg|0:person|looking at|2:sea|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|2:sea[mask2former_stuff]mask2former:103:000001|
|71|10|1159449.jpg|1:person|looking at|17:sports ball|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000010||
|71|10|1159449.jpg|8:person|running on|23:playingfield|endpoint_missing_or_wrong_class||12:playingfield[mask2former_stuff]mask2former:097:000004|
|72|841|2353618.jpg|1:person|standing on|2:skis|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|2:skis[mask2former_thing]mask2former:030:000004|
|72|841|2353618.jpg|1:person|wearing|2:skis|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|2:skis[mask2former_thing]mask2former:030:000004|
|75|1505|2386156.jpg|0:person|in|2:car|endpoint_missing_or_wrong_class||2:car[mask2former_thing]mask2former:002:000012|
|75|1505|2386156.jpg|0:person|driving|2:car|endpoint_missing_or_wrong_class||2:car[mask2former_thing]mask2former:002:000012|
|81|1886|2404565.jpg|0:person|looking at|3:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000010|6:surfboard[mask2former_thing]mask2former:037:000008|
|82|1497|2385717.jpg|0:person|over|3:pavement|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|3:pavement[mask2former_stuff]mask2former:123:000005|
|83|2176|713850.jpg|0:person|in|5:window|endpoint_missing_or_wrong_class|||
|86|1001|2360816.jpg|1:person|riding|13:bicycle|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|10:bicycle[mask2former_thing]mask2former:001:000023|
|86|1001|2360816.jpg|5:person|riding|11:bicycle|wrong_predicate|2:person[mask2former_thing]mask2former:000:000009|6:bicycle[mask2former_thing]mask2former:001:000007|
|86|1001|2360816.jpg|10:person|riding|14:bicycle|wrong_predicate|4:person[mask2former_thing]mask2former:000:000020|8:bicycle[mask2former_thing]mask2former:001:000013|
|87|852|2354099.jpg|3:person|crossing|36:pavement|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000021||
|87|852|2354099.jpg|9:person|crossing|36:pavement|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000013||
|87|852|2354099.jpg|11:person|on|34:skateboard|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000010||
|87|852|2354099.jpg|11:person|standing on|34:skateboard|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000010||
|87|852|2354099.jpg|37:building|beside|11:person|wrong_predicate|22:building[mask2former_stuff]mask2former:129:000003|0:person[mask2former_thing]mask2former:000:000010|
|89|813|2352072.jpg|0:person|in front of|3:tree|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|2:tree[mask2former_stuff]mask2former:116:000001|
|91|926|2357328.jpg|0:person|standing on|5:grass|endpoint_missing_or_wrong_class||3:grass[mask2former_stuff]mask2former:125:000004|
|91|926|2357328.jpg|1:person|standing on|5:grass|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|3:grass[mask2former_stuff]mask2former:125:000004|
|91|926|2357328.jpg|2:person|holding|3:baseball bat|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|2:baseball bat[mask2former_thing]mask2former:034:000002|
|91|926|2357328.jpg|2:person|standing on|5:grass|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|3:grass[mask2former_stuff]mask2former:125:000004|
|92|1004|2360919.jpg|0:person|in front of|3:book|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|93|227|2322480.jpg|0:person|looking at|1:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|0:person[mask2former_thing]mask2former:000:000001|
|93|227|2322480.jpg|1:person|chasing|2:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|2:sports ball[mask2former_thing]mask2former:032:000004|
|93|227|2322480.jpg|1:person|playing|2:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|2:sports ball[mask2former_thing]mask2former:032:000004|
|93|227|2322480.jpg|2:sports ball|in front of|1:person|wrong_predicate|2:sports ball[mask2former_thing]mask2former:032:000004|0:person[mask2former_thing]mask2former:000:000001|
|94|664|2345357.jpg|0:person|in|10:train|endpoint_missing_or_wrong_class||2:train[mask2former_thing]mask2former:006:000004|
|94|664|2345357.jpg|1:person|in|10:train|endpoint_missing_or_wrong_class||2:train[mask2former_thing]mask2former:006:000004|
|95|649|2344605.jpg|0:person|wearing|7:tie|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000009||
|95|649|2344605.jpg|0:person|sitting on|9:chair|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000009||
|95|649|2344605.jpg|0:person|touching|12:laptop|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000009||
|95|649|2344605.jpg|12:laptop|in front of|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000009|
|100|1841|2402294.jpg|1:person|driving|6:bus|endpoint_missing_or_wrong_class||4:bus[mask2former_thing]mask2former:005:000004|
|101|1796|2400414.jpg|1:person|playing with|5:sheep|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|4:sheep[mask2former_thing]mask2former:018:000006|
|101|1796|2400414.jpg|1:person|touching|5:sheep|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|4:sheep[mask2former_thing]mask2former:018:000006|
|101|1796|2400414.jpg|3:person|pulling|4:sheep|endpoint_missing_or_wrong_class||3:sheep[mask2former_thing]mask2former:018:000003|
|101|1796|2400414.jpg|5:sheep|playing with|1:person|wrong_predicate|4:sheep[mask2former_thing]mask2former:018:000006|1:person[mask2former_thing]mask2former:000:000002|
|103|989|2360368.jpg|2:person|beside|9:motorcycle|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000008||
|103|989|2360368.jpg|2:person|standing on|12:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000008||
|103|989|2360368.jpg|2:person|in front of|14:dirt|wrong_predicate|0:person[mask2former_thing]mask2former:000:000008|13:dirt[mask2former_stuff]mask2former:126:000010|
|104|1795|2400390.jpg|10:person|beside|6:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|3:person[mask2former_thing]mask2former:000:000011|
|105|1023|2361799.jpg|0:person|looking at|1:bear|endpoint_missing_or_wrong_class|||
|105|1023|2361799.jpg|0:person|in front of|3:tree|endpoint_missing_or_wrong_class||1:tree[mask2former_stuff]mask2former:116:000001|
|106|868|2354820.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:skateboard[mask2former_thing]mask2former:036:000001|
|106|868|2354820.jpg|0:person|riding|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:skateboard[mask2former_thing]mask2former:036:000001|
|106|868|2354820.jpg|0:person|in front of|2:tree|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|2:tree[mask2former_stuff]mask2former:116:000002|
|106|868|2354820.jpg|0:person|standing on|4:floor|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|110|979|2359868.jpg|0:person|in|2:train|endpoint_missing_or_wrong_class||0:train[mask2former_thing]mask2former:006:000002|
|110|979|2359868.jpg|1:person|in|2:train|endpoint_missing_or_wrong_class||0:train[mask2former_thing]mask2former:006:000002|
|119|1534|2387240.jpg|4:person|in front of|13:person|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000010||
|121|1300|2376047.jpg|0:person|jumping from|4:playingfield|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|121|1300|2376047.jpg|1:person|chasing|2:frisbee|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|2:frisbee[mask2former_thing]mask2former:029:000002|
|121|1300|2376047.jpg|1:person|playing|2:frisbee|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|2:frisbee[mask2former_thing]mask2former:029:000002|
|121|1300|2376047.jpg|1:person|jumping from|4:playingfield|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|122|1729|2396723.jpg|0:person|holding|3:wine glass|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|122|1729|2396723.jpg|0:person|sitting on|4:couch|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|122|1729|2396723.jpg|1:cat|lying on|0:person|wrong_predicate|2:cat[mask2former_thing]mask2former:015:000003|0:person[mask2former_thing]mask2former:000:000002|
|122|1729|2396723.jpg|2:cat|lying on|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000002|
|122|1729|2396723.jpg|5:pillow|in front of|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000002|
|123|1099|2365844.jpg|9:person|beside|12:person|rank_below50|2:person[mask2former_thing]mask2former:000:000003|0:person[mask2former_thing]mask2former:000:000001|
|123|1099|2365844.jpg|10:person|beside|12:person|rank_below50|12:person[mask2former_thing]mask2former:000:000020|0:person[mask2former_thing]mask2former:000:000001|
|125|1673|2393510.jpg|1:person|walking on|6:grass|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|5:grass[mask2former_stuff]mask2former:125:000006|
|125|1673|2393510.jpg|2:person|looking at|0:person|wrong_predicate|2:person[mask2former_thing]mask2former:000:000005|1:person[mask2former_thing]mask2former:000:000004|
|125|1673|2393510.jpg|2:person|throwing|3:frisbee|wrong_predicate|2:person[mask2former_thing]mask2former:000:000005|3:frisbee[mask2former_thing]mask2former:029:000002|
|126|787|2351136.jpg|0:person|on back of|3:horse|wrong_predicate|1:person[mask2former_thing]mask2former:000:000005|3:horse[mask2former_thing]mask2former:017:000004|
|127|1293|2375622.jpg|0:person|holding|4:cell phone|endpoint_missing_or_wrong_class|||
|127|1293|2375622.jpg|1:person|looking at|2:laptop|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|3:laptop[mask2former_thing]mask2former:063:000003|
|127|1293|2375622.jpg|1:person|touching|2:laptop|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|3:laptop[mask2former_thing]mask2former:063:000003|
|128|323|2328089.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:surfboard[mask2former_thing]mask2former:037:000005|
|128|323|2328089.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:surfboard[mask2former_thing]mask2former:037:000005|
|130|2105|2416163.jpg|9:person|sitting on|33:sand|endpoint_missing_or_wrong_class||27:sand[mask2former_stuff]mask2former:102:000023|
|130|2105|2416163.jpg|11:person|sitting on|33:sand|endpoint_missing_or_wrong_class||27:sand[mask2former_stuff]mask2former:102:000023|
|130|2105|2416163.jpg|12:person|sitting on|33:sand|endpoint_missing_or_wrong_class||27:sand[mask2former_stuff]mask2former:102:000023|
|131|1764|2398216.jpg|0:person|in front of|1:person|wrong_predicate|2:person[mask2former_thing]mask2former:000:000008|0:person[mask2former_thing]mask2former:000:000005|
|131|1764|2398216.jpg|2:person|standing on|11:pavement|wrong_predicate|3:person[mask2former_thing]mask2former:000:000009|10:pavement[mask2former_stuff]mask2former:123:000011|
|131|1764|2398216.jpg|3:person|standing on|11:pavement|wrong_predicate|1:person[mask2former_thing]mask2former:000:000006|10:pavement[mask2former_stuff]mask2former:123:000011|
|134|406|2332593.jpg|0:person|in front of|8:wall-stone|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|8:wall-stone[mask2former_stuff]mask2former:110:000005|
|134|406|2332593.jpg|0:person|on|12:grass|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|11:grass[mask2former_stuff]mask2former:125:000009|
|134|406|2332593.jpg|1:person|in front of|0:person|wrong_predicate|2:person[mask2former_thing]mask2former:000:000007|0:person[mask2former_thing]mask2former:000:000001|
|135|1163|2368707.jpg|0:person|running on|9:dirt|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|6:dirt[mask2former_stuff]mask2former:126:000007|
|135|1163|2368707.jpg|1:person|looking at|4:frisbee|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|135|1163|2368707.jpg|1:person|running on|9:dirt|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|6:dirt[mask2former_stuff]mask2former:126:000007|
|135|1163|2368707.jpg|3:person|looking at|4:frisbee|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|135|1163|2368707.jpg|3:person|throwing|4:frisbee|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|135|1163|2368707.jpg|4:frisbee|over|1:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000001|
|136|1375|2379887.jpg|0:person|in front of|5:mountain|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|4:mountain[mask2former_stuff]mask2former:124:000004|
|138|1529|2387080.jpg|0:person|sitting on|5:chair|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000008||
|140|554|2339715.jpg|0:person|holding|14:spoon|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000015||
|140|554|2339715.jpg|0:person|eating|14:spoon|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000015||
|141|1697|2394828.jpg|0:person|over|3:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|141|1697|2394828.jpg|0:person|jumping from|3:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|141|1697|2394828.jpg|0:person|in front of|4:grass|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|5:grass[mask2former_stuff]mask2former:125:000004|
|141|1697|2394828.jpg|0:person|in front of|5:rock|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|144|1442|2383041.jpg|3:person|wearing|18:surfboard|wrong_predicate|1:person[mask2former_thing]mask2former:000:000006|10:surfboard[mask2former_thing]mask2former:037:000002|
|144|1442|2383041.jpg|4:person|pulling|13:kite|endpoint_missing_or_wrong_class||9:kite[mask2former_thing]mask2former:033:000014|
|149|1526|2387025.jpg|6:person|carrying|21:handbag|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000010||
|149|1526|2387025.jpg|8:person|wearing|24:cardboard|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000016||
|152|1986|2409643.jpg|0:person|holding|5:handbag|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|6:handbag[mask2former_thing]mask2former:026:000007|
|153|1695|2394762.jpg|1:person|attached to|16:grass|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|153|1695|2394762.jpg|3:person|looking at|12:sports ball|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|153|1695|2394762.jpg|5:person|pulling|6:person|endpoints_collapsed_to_same_box|2:person[mask2former_thing]mask2former:000:000006|2:person[mask2former_thing]mask2former:000:000006|
|153|1695|2394762.jpg|5:person|jumping from|13:playingfield|wrong_predicate|2:person[mask2former_thing]mask2former:000:000006|7:playingfield[mask2former_stuff]mask2former:097:000005|
|153|1695|2394762.jpg|6:person|catching|12:sports ball|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000006||
|154|47|1592228.jpg|1:person|standing on|17:platform|endpoint_missing_or_wrong_class|||
|154|47|1592228.jpg|5:person|carrying|12:handbag|endpoint_missing_or_wrong_class|||
|154|47|1592228.jpg|5:person|standing on|22:pavement|endpoint_missing_or_wrong_class|||
|156|1813|2401171.jpg|9:person|walking on|25:pavement|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000018||
|157|1286|2375241.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|157|1286|2375241.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|157|1286|2375241.jpg|0:person|looking at|2:sea|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:sea[mask2former_stuff]mask2former:103:000001|
|158|975|2359797.jpg|3:person|carrying|14:backpack|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000009||
|158|975|2359797.jpg|8:person|carrying|15:backpack|endpoint_missing_or_wrong_class|11:person[mask2former_thing]mask2former:000:000021||
|158|975|2359797.jpg|10:person|holding|19:umbrella|wrong_predicate|8:person[mask2former_thing]mask2former:000:000017|17:umbrella[mask2former_thing]mask2former:025:000022|
|158|975|2359797.jpg|14:backpack|on back of|3:person|endpoint_missing_or_wrong_class||3:person[mask2former_thing]mask2former:000:000009|
|161|859|2354354.jpg|3:person|running on|16:pavement|wrong_predicate|3:person[mask2former_thing]mask2former:000:000007|17:pavement[mask2former_stuff]mask2former:123:000014|
|161|859|2354354.jpg|4:person|holding|12:umbrella|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000009||
|161|859|2354354.jpg|5:person|walking on|16:pavement|wrong_predicate|9:person[mask2former_thing]mask2former:000:000019|17:pavement[mask2former_stuff]mask2former:123:000014|
|165|2125|2416928.jpg|9:person|leaning on|15:truck|wrong_predicate|12:person[mask2former_thing]mask2former:000:000017|13:truck[mask2former_thing]mask2former:007:000004|
|165|2125|2416928.jpg|10:person|wearing|16:tree|wrong_predicate|8:person[mask2former_thing]mask2former:000:000012|14:tree[mask2former_stuff]mask2former:116:000002|
|165|2125|2416928.jpg|13:person|standing on|15:truck|endpoint_missing_or_wrong_class||13:truck[mask2former_thing]mask2former:007:000004|
|166|955|2358756.jpg|0:person|holding|1:frisbee|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|166|955|2358756.jpg|0:person|throwing|1:frisbee|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|166|955|2358756.jpg|0:person|holding|2:frisbee|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|166|955|2358756.jpg|0:person|attached to|3:tree|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:tree[mask2former_stuff]mask2former:116:000001|
|166|955|2358756.jpg|0:person|standing on|4:dirt|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|2:dirt[mask2former_stuff]mask2former:126:000003|
|167|2029|2411534.jpg|0:person|looking at|1:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:sports ball[mask2former_thing]mask2former:032:000001|
|167|2029|2411534.jpg|0:person|about to hit|1:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:sports ball[mask2former_thing]mask2former:032:000001|
|167|2029|2411534.jpg|0:person|standing on|3:playingfield|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|3:playingfield[mask2former_stuff]mask2former:097:000002|
|170|658|2345182.jpg|6:person|touching|15:kite|endpoint_missing_or_wrong_class|15:person[mask2former_thing]mask2former:000:000022||
|170|658|2345182.jpg|6:person|holding|18:bottle|endpoint_missing_or_wrong_class|15:person[mask2former_thing]mask2former:000:000022||
|170|658|2345182.jpg|6:person|holding|19:bottle|endpoint_missing_or_wrong_class|15:person[mask2former_thing]mask2former:000:000022||
|170|658|2345182.jpg|6:person|walking on|22:grass|wrong_predicate|15:person[mask2former_thing]mask2former:000:000022|24:grass[mask2former_stuff]mask2former:125:000019|
|170|658|2345182.jpg|7:person|in front of|10:person|wrong_predicate|2:person[mask2former_thing]mask2former:000:000003|0:person[mask2former_thing]mask2former:000:000001|
|170|658|2345182.jpg|10:person|beside|6:person|rank_below50|0:person[mask2former_thing]mask2former:000:000001|15:person[mask2former_thing]mask2former:000:000022|
|172|1608|2390659.jpg|0:person|lying on|34:rug|endpoint_missing_or_wrong_class|||
|172|1608|2390659.jpg|2:person|lying on|34:rug|endpoint_missing_or_wrong_class|||
|172|1608|2390659.jpg|8:person|holding|24:tennis racket|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|173|417|2332914.jpg|0:person|standing on|8:pavement|wrong_predicate|0:person[mask2former_thing]mask2former:000:000006|9:pavement[mask2former_stuff]mask2former:123:000009|
|173|417|2332914.jpg|0:person|in front of|9:building|wrong_predicate|0:person[mask2former_thing]mask2former:000:000006|10:building[mask2former_stuff]mask2former:129:000001|
|175|1343|2378563.jpg|0:person|beside|4:motorcycle|endpoint_missing_or_wrong_class|||
|175|1343|2378563.jpg|0:person|standing on|8:pavement|endpoint_missing_or_wrong_class|||
|175|1343|2378563.jpg|4:motorcycle|beside|0:person|endpoint_missing_or_wrong_class|||
|183|1866|2403494.jpg|11:person|wearing|19:skis|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000011||
|183|1866|2403494.jpg|12:person|standing on|18:skis|endpoint_missing_or_wrong_class|8:person[mask2former_thing]mask2former:000:000015||
|184|325|2328153.jpg|2:elephant|in front of|0:person|wrong_predicate|3:elephant[mask2former_thing]mask2former:020:000004|0:person[mask2former_thing]mask2former:000:000003|
|185|15|1159597.jpg|0:person|guiding|5:horse|wrong_predicate|1:person[mask2former_thing]mask2former:000:000008|4:horse[mask2former_thing]mask2former:017:000007|
|188|1302|2376309.jpg|0:person|standing on|1:skis|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:skis[mask2former_thing]mask2former:030:000003|
|188|1302|2376309.jpg|0:person|playing|1:skis|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:skis[mask2former_thing]mask2former:030:000003|
|188|1302|2376309.jpg|0:person|looking at|2:snow|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|3:snow[mask2former_stuff]mask2former:105:000002|
|190|283|2326062.jpg|0:person|on|27:pavement|rank_below50|5:person[mask2former_thing]mask2former:000:000011|18:pavement[mask2former_stuff]mask2former:123:000019|
|190|283|2326062.jpg|3:person|sitting on|13:bench|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000012||
|190|283|2326062.jpg|9:person|looking at|10:person|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000008||
|190|283|2326062.jpg|9:person|holding|17:handbag|wrong_predicate|2:person[mask2former_thing]mask2former:000:000008|11:handbag[mask2former_thing]mask2former:026:000004|
|190|283|2326062.jpg|21:handbag|hanging from|3:person|endpoint_missing_or_wrong_class||6:person[mask2former_thing]mask2former:000:000012|
|190|283|2326062.jpg|22:handbag|hanging from|9:person|wrong_predicate|14:handbag[mask2former_thing]mask2former:026:000017|2:person[mask2former_thing]mask2former:000:000008|
|190|283|2326062.jpg|28:paper|beside|3:person|endpoint_missing_or_wrong_class||6:person[mask2former_thing]mask2former:000:000012|
|192|2020|2411218.jpg|2:person|on|15:sand|endpoint_missing_or_wrong_class||2:sand[mask2former_stuff]mask2former:102:000005|
|194|1135|2367479.jpg|5:person|looking at|3:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|3:person[mask2former_thing]mask2former:000:000005|
|194|1135|2367479.jpg|5:person|holding|7:handbag|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|194|1135|2367479.jpg|7:handbag|in front of|3:person|endpoint_missing_or_wrong_class||3:person[mask2former_thing]mask2former:000:000005|
|195|1382|2380359.jpg|1:person|in front of|23:door|wrong_predicate|4:person[mask2former_thing]mask2former:000:000015|19:door[mask2former_stuff]mask2former:086:000010|
|195|1382|2380359.jpg|1:person|in front of|25:ceiling|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000015||
|195|1382|2380359.jpg|2:person|sitting on|4:person|endpoints_collapsed_to_same_box|0:person[mask2former_thing]mask2former:000:000002|0:person[mask2former_thing]mask2former:000:000002|
|197|368|2330400.jpg|0:person|going down|4:snow|wrong_predicate|1:person[mask2former_thing]mask2former:000:000005|4:snow[mask2former_stuff]mask2former:105:000001|
|197|368|2330400.jpg|1:person|wearing|2:skis|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|3:skis[mask2former_thing]mask2former:030:000003|
|197|368|2330400.jpg|1:person|jumping over|4:snow|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|4:snow[mask2former_stuff]mask2former:105:000001|
|198|1076|2364558.jpg|0:person|about to hit|1:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:sports ball[mask2former_thing]mask2former:032:000001|
|198|1076|2364558.jpg|0:person|attached to|2:tennis racket|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:tennis racket[mask2former_thing]mask2former:038:000005|
|198|1076|2364558.jpg|0:person|standing on|3:playingfield|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|4:playingfield[mask2former_stuff]mask2former:097:000002|
|198|1076|2364558.jpg|0:person|in front of|4:wall|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|201|970|2359437.jpg|0:person|picking|1:pizza|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|1:pizza[mask2former_thing]mask2former:053:000002|
|203|806|2351780.jpg|1:person|on|12:playingfield|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000003||
|203|806|2351780.jpg|2:person|wearing|11:baseball glove|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|8:baseball glove[mask2former_thing]mask2former:035:000006|
|203|806|2351780.jpg|2:person|on|12:playingfield|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000002||
|203|806|2351780.jpg|3:person|about to hit|9:sports ball|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000004||
|203|806|2351780.jpg|3:person|holding|10:baseball bat|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000004||
|203|806|2351780.jpg|3:person|swinging|10:baseball bat|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000004||
|203|806|2351780.jpg|5:person|on|12:playingfield|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000008||
|207|1111|2366320.jpg|0:person|in front of|2:wall|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|4:wall[mask2former_stuff]mask2former:131:000005|
|210|105|2316316.jpg|1:person|holding|19:handbag|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|21:handbag[mask2former_thing]mask2former:026:000007|
|210|105|2316316.jpg|1:person|walking on|22:road|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|22:road[mask2former_stuff]mask2former:100:000019|
|210|105|2316316.jpg|6:person|in front of|12:person|endpoint_missing_or_wrong_class||6:person[mask2former_thing]mask2former:000:000014|
|210|105|2316316.jpg|6:person|sitting on|17:motorcycle|endpoint_missing_or_wrong_class||20:motorcycle[mask2former_thing]mask2former:003:000013|
|210|105|2316316.jpg|11:person|riding|15:bicycle|endpoint_missing_or_wrong_class|||
|210|105|2316316.jpg|12:person|riding|17:motorcycle|wrong_predicate|6:person[mask2former_thing]mask2former:000:000014|20:motorcycle[mask2former_thing]mask2former:003:000013|
|210|105|2316316.jpg|13:person|walking on|22:road|endpoint_missing_or_wrong_class||22:road[mask2former_stuff]mask2former:100:000019|
|210|105|2316316.jpg|25:sky|over|6:person|endpoint_missing_or_wrong_class|23:sky[mask2former_stuff]mask2former:119:000006||
|211|1563|2388324.jpg|0:person|in|10:tv|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|8:tv[mask2former_thing]mask2former:062:000005|
|211|1563|2388324.jpg|0:person|playing|10:tv|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|8:tv[mask2former_thing]mask2former:062:000005|
|211|1563|2388324.jpg|0:person|holding|11:remote|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|213|1476|2384904.jpg|0:person|playing with|2:frisbee|wrong_predicate|1:person[mask2former_thing]mask2former:000:000005|2:frisbee[mask2former_thing]mask2former:029:000004|
|213|1476|2384904.jpg|1:person|chasing|0:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:person[mask2former_thing]mask2former:000:000005|
|216|1890|2404890.jpg|0:person|in|2:train|endpoint_missing_or_wrong_class||0:train[mask2former_thing]mask2former:006:000003|
|216|1890|2404890.jpg|1:person|driving|2:train|endpoint_missing_or_wrong_class||0:train[mask2former_thing]mask2former:006:000003|
|225|1317|2377220.jpg|1:person|in|10:train|endpoint_missing_or_wrong_class||1:train[mask2former_thing]mask2former:006:000003|
|225|1317|2377220.jpg|3:person|driving|10:train|endpoint_missing_or_wrong_class||1:train[mask2former_thing]mask2former:006:000003|
|225|1317|2377220.jpg|6:person|in|10:train|endpoint_missing_or_wrong_class||1:train[mask2former_thing]mask2former:006:000003|
|225|1317|2377220.jpg|9:person|in|10:train|endpoint_missing_or_wrong_class||1:train[mask2former_thing]mask2former:006:000003|
|226|2126|2416964.jpg|0:person|picking|14:suitcase|endpoint_missing_or_wrong_class|||
|227|1607|2390654.jpg|1:person|standing on|9:sand|wrong_predicate|4:person[mask2former_thing]mask2former:000:000007|8:sand[mask2former_stuff]mask2former:102:000009|
|227|1607|2390654.jpg|1:person|in front of|10:sea|wrong_predicate|4:person[mask2former_thing]mask2former:000:000007|9:sea[mask2former_stuff]mask2former:103:000004|
|227|1607|2390654.jpg|4:person|playing with|5:person|wrong_predicate|6:person[mask2former_thing]mask2former:000:000012|1:person[mask2former_thing]mask2former:000:000002|
|228|2144|285721.jpg|0:person|holding|2:cell phone|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|228|2144|285721.jpg|0:person|carrying|2:cell phone|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|228|2144|285721.jpg|0:person|talking to|2:cell phone|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|228|2144|285721.jpg|0:person|in front of|3:wall|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|2:wall[mask2former_stuff]mask2former:131:000003|
|229|1350|2378868.jpg|1:person|in|2:car|endpoint_missing_or_wrong_class||1:car[mask2former_thing]mask2former:002:000006|
|230|723|2348265.jpg|5:person|on|13:bridge|endpoint_missing_or_wrong_class|||
|230|723|2348265.jpg|6:person|over|14:river|endpoint_missing_or_wrong_class||2:river[mask2former_stuff]mask2former:099:000004|
|231|684|2346411.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|231|684|2346411.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|231|684|2346411.jpg|0:person|over|2:sea|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:sea[mask2former_stuff]mask2former:103:000001|
|231|684|2346411.jpg|0:person|looking at|2:sea|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:sea[mask2former_stuff]mask2former:103:000001|
|233|1337|2378360.jpg|0:person|playing|1:surfboard|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|233|1337|2378360.jpg|0:person|riding|1:surfboard|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|233|1337|2378360.jpg|0:person|on|2:sea|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:sea[mask2former_stuff]mask2former:103:000002|
|235|2050|2412773.jpg|0:person|attached to|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|235|2050|2412773.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|235|2050|2412773.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|235|2050|2412773.jpg|0:person|attached to|2:sea|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:sea[mask2former_stuff]mask2former:103:000001|
|235|2050|2412773.jpg|0:person|touching|2:sea|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:sea[mask2former_stuff]mask2former:103:000001|
|236|561|2340111.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:surfboard[mask2former_thing]mask2former:037:000003|
|236|561|2340111.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:surfboard[mask2former_thing]mask2former:037:000003|
|236|561|2340111.jpg|0:person|over|2:sea|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|2:sea[mask2former_stuff]mask2former:103:000001|
|243|1591|2389803.jpg|0:person|on|9:boat|endpoint_missing_or_wrong_class||1:boat[mask2former_thing]mask2former:008:000003|
|243|1591|2389803.jpg|0:person|sitting on|9:boat|endpoint_missing_or_wrong_class||1:boat[mask2former_thing]mask2former:008:000003|
|243|1591|2389803.jpg|1:person|on|9:boat|endpoint_missing_or_wrong_class||1:boat[mask2former_thing]mask2former:008:000003|
|243|1591|2389803.jpg|1:person|sitting on|9:boat|endpoint_missing_or_wrong_class||1:boat[mask2former_thing]mask2former:008:000003|
|244|603|2342677.jpg|0:person|sitting on|1:bed|endpoint_missing_or_wrong_class||0:bed[mask2former_thing]mask2former:059:000002|
|244|603|2342677.jpg|0:person|looking at|2:laptop|endpoint_missing_or_wrong_class||1:laptop[mask2former_thing]mask2former:063:000001|
|244|603|2342677.jpg|0:person|beside|4:door|endpoint_missing_or_wrong_class|||
|244|603|2342677.jpg|0:person|holding|7:wall|endpoint_missing_or_wrong_class|||
|244|603|2342677.jpg|3:blanket|over|0:person|endpoint_missing_or_wrong_class|||
|244|603|2342677.jpg|7:wall|on back of|0:person|endpoint_missing_or_wrong_class|||
|247|1380|2380325.jpg|0:person|beside|2:car|endpoint_missing_or_wrong_class|||
|247|1380|2380325.jpg|2:car|beside|0:person|endpoint_missing_or_wrong_class|||
|249|520|2337500.jpg|0:person|driving|6:car|endpoint_missing_or_wrong_class||2:car[mask2former_thing]mask2former:002:000010|
|251|1509|2386257.jpg|0:person|attached to|1:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:person[mask2former_thing]mask2former:000:000003|
|251|1509|2386257.jpg|0:person|playing with|2:teddy bear|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|2:teddy bear[mask2former_thing]mask2former:077:000001|
|251|1509|2386257.jpg|1:person|attached to|0:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|0:person[mask2former_thing]mask2former:000:000002|
|251|1509|2386257.jpg|1:person|attached to|2:teddy bear|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|2:teddy bear[mask2former_thing]mask2former:077:000001|
|251|1509|2386257.jpg|2:teddy bear|attached to|1:person|wrong_predicate|2:teddy bear[mask2former_thing]mask2former:077:000001|1:person[mask2former_thing]mask2former:000:000003|
|253|1589|2389680.jpg|0:person|beside|12:stairs|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000015||
|253|1589|2389680.jpg|0:person|beside|13:water|wrong_predicate|4:person[mask2former_thing]mask2former:000:000015|11:water[mask2former_stuff]mask2former:113:000009|
|253|1589|2389680.jpg|2:person|sitting on|8:bench|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000010||
|253|1589|2389680.jpg|2:person|holding|11:cell phone|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000010||
|253|1589|2389680.jpg|2:person|looking at|11:cell phone|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000010||
|253|1589|2389680.jpg|4:person|beside|0:person|wrong_predicate|3:person[mask2former_thing]mask2former:000:000013|4:person[mask2former_thing]mask2former:000:000015|
|253|1589|2389680.jpg|4:person|looking at|0:person|wrong_predicate|3:person[mask2former_thing]mask2former:000:000013|4:person[mask2former_thing]mask2former:000:000015|
|253|1589|2389680.jpg|4:person|beside|12:stairs|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000013||
|253|1589|2389680.jpg|4:person|beside|13:water|wrong_predicate|3:person[mask2former_thing]mask2former:000:000013|11:water[mask2former_stuff]mask2former:113:000009|
|253|1589|2389680.jpg|10:handbag|beside|2:person|wrong_predicate|9:handbag[mask2former_thing]mask2former:026:000007|1:person[mask2former_thing]mask2former:000:000010|
|254|896|2356062.jpg|1:person|beside|25:flower|wrong_predicate|14:person[mask2former_thing]mask2former:000:000022|18:flower[mask2former_stuff]mask2former:088:000002|
|254|896|2356062.jpg|1:person|in front of|26:tree|wrong_predicate|14:person[mask2former_thing]mask2former:000:000022|20:tree[mask2former_stuff]mask2former:116:000006|
|254|896|2356062.jpg|5:person|walking on|28:grass|wrong_predicate|3:person[mask2former_thing]mask2former:000:000005|22:grass[mask2former_stuff]mask2former:125:000017|
|254|896|2356062.jpg|7:person|holding|18:teddy bear|endpoint_missing_or_wrong_class|7:person[mask2former_thing]mask2former:000:000013||
|254|896|2356062.jpg|7:person|holding|22:teddy bear|endpoint_missing_or_wrong_class|7:person[mask2former_thing]mask2former:000:000013||
|254|896|2356062.jpg|8:person|walking on|28:grass|wrong_predicate|5:person[mask2former_thing]mask2former:000:000009|22:grass[mask2former_stuff]mask2former:125:000017|
|254|896|2356062.jpg|10:person|sitting on|24:blanket|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|258|388|2331571.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000004|
|258|388|2331571.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000004|
|258|388|2331571.jpg|0:person|on|2:sea|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:sea[mask2former_stuff]mask2former:103:000002|
|259|826|2352851.jpg|0:person|standing on|2:sand|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|262|621|2343341.jpg|0:person|throwing|4:sports ball|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000005||
|262|621|2343341.jpg|1:person|about to hit|4:sports ball|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000007||
|262|621|2343341.jpg|1:person|standing on|11:dirt|rank_below50|3:person[mask2former_thing]mask2former:000:000007|10:dirt[mask2former_stuff]mask2former:126:000009|
|263|2037|2412228.jpg|8:motorcycle|in front of|4:person|wrong_predicate|7:motorcycle[mask2former_thing]mask2former:003:000002|3:person[mask2former_thing]mask2former:000:000007|
|267|1327|2377789.jpg|12:backpack|beside|3:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000004|
|267|1327|2377789.jpg|13:handbag|beside|3:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000004|
|269|133|2317501.jpg|1:person|guiding|6:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|10:person[mask2former_thing]mask2former:000:000016|
|269|133|2317501.jpg|2:person|beside|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000001|
|269|133|2317501.jpg|2:person|holding|9:person|endpoint_missing_or_wrong_class||3:person[mask2former_thing]mask2former:000:000004|
|271|1757|2397709.jpg|0:person|playing|1:sports ball|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|271|1757|2397709.jpg|0:person|holding|2:tennis racket|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:tennis racket[mask2former_thing]mask2former:038:000004|
|271|1757|2397709.jpg|0:person|standing on|3:playingfield|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:playingfield[mask2former_stuff]mask2former:097:000002|
|272|1688|2394464.jpg|0:person|sitting on|6:chair|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000007||
|276|1693|2394673.jpg|0:person|playing|1:skis|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:skis[mask2former_thing]mask2former:030:000003|
|276|1693|2394673.jpg|1:skis|attached to|0:person|wrong_predicate|1:skis[mask2former_thing]mask2former:030:000003|0:person[mask2former_thing]mask2former:000:000002|
|277|1237|2372495.jpg|0:person|holding|15:tennis racket|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000011||
|277|1237|2372495.jpg|0:person|standing on|26:playingfield|wrong_predicate|4:person[mask2former_thing]mask2former:000:000011|36:playingfield[mask2former_stuff]mask2former:097:000023|
|277|1237|2372495.jpg|3:person|looking at|0:person|wrong_predicate|18:person[mask2former_thing]mask2former:000:000032|4:person[mask2former_thing]mask2former:000:000011|
|277|1237|2372495.jpg|3:person|talking to|0:person|wrong_predicate|18:person[mask2former_thing]mask2former:000:000032|4:person[mask2former_thing]mask2former:000:000011|
|277|1237|2372495.jpg|3:person|holding|14:tennis racket|endpoint_missing_or_wrong_class|18:person[mask2former_thing]mask2former:000:000032||
|277|1237|2372495.jpg|7:person|beside|9:person|rank_below50|8:person[mask2former_thing]mask2former:000:000017|13:person[mask2former_thing]mask2former:000:000024|
|281|1203|2371154.jpg|1:person|on|4:snowboard|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|281|1203|2371154.jpg|1:person|playing|4:snowboard|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|281|1203|2371154.jpg|2:person|wearing|7:snowboard|wrong_predicate|3:person[mask2former_thing]mask2former:000:000008|5:snowboard[mask2former_thing]mask2former:031:000004|
|281|1203|2371154.jpg|3:person|standing on|5:snowboard|wrong_predicate|2:person[mask2former_thing]mask2former:000:000007|6:snowboard[mask2former_thing]mask2former:031:000006|
|283|673|2345745.jpg|0:person|looking at|3:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|2:person[mask2former_thing]mask2former:000:000009|
|283|673|2345745.jpg|1:person|looking at|3:person|wrong_predicate|4:person[mask2former_thing]mask2former:000:000019|2:person[mask2former_thing]mask2former:000:000009|
|283|673|2345745.jpg|2:person|looking at|3:person|rank_below50|1:person[mask2former_thing]mask2former:000:000004|2:person[mask2former_thing]mask2former:000:000009|
|285|1218|2371757.jpg|0:person|driving|6:bus|wrong_predicate|0:person[mask2former_thing]mask2former:000:000006|4:bus[mask2former_thing]mask2former:005:000010|
|287|2058|2413475.jpg|0:person|holding|1:frisbee|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:frisbee[mask2former_thing]mask2former:029:000003|
|287|2058|2413475.jpg|0:person|playing|1:frisbee|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:frisbee[mask2former_thing]mask2former:029:000003|
|287|2058|2413475.jpg|0:person|standing on|3:grass|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|3:grass[mask2former_stuff]mask2former:125:000004|
|292|551|2339515.jpg|0:person|looking at|14:river|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000014||
|292|551|2339515.jpg|2:person|looking at|8:cow|endpoint_missing_or_wrong_class||8:cow[mask2former_thing]mask2former:019:000012|
|292|551|2339515.jpg|6:cow|looking at|0:person|endpoint_missing_or_wrong_class||1:person[mask2former_thing]mask2former:000:000014|
|293|495|2336518.jpg|2:person|holding|14:cell phone|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000006||
|293|495|2336518.jpg|2:person|looking at|14:cell phone|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000006||
|293|495|2336518.jpg|7:person|talking to|3:person|endpoint_missing_or_wrong_class|||
|293|495|2336518.jpg|8:person|sitting on|13:couch|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|293|495|2336518.jpg|8:person|looking at|15:table|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|296|1346|2378709.jpg|0:person|standing on|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|296|1346|2378709.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000002|
|301|1633|2391614.jpg|0:person|holding|7:food|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000005||
|301|1633|2391614.jpg|1:oven|in front of|0:person|wrong_predicate|6:oven[mask2former_thing]mask2former:069:000011|0:person[mask2former_thing]mask2former:000:000005|
|302|1396|2381002.jpg|2:person|riding|5:bicycle|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000016||
|302|1396|2381002.jpg|2:person|carrying|14:backpack|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000016||
|302|1396|2381002.jpg|3:person|standing on|19:pavement|endpoint_missing_or_wrong_class||16:pavement[mask2former_stuff]mask2former:123:000012|
|304|1427|2382463.jpg|0:person|sitting on|2:boat|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|304|1427|2382463.jpg|1:person|standing on|2:boat|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|304|1427|2382463.jpg|1:person|driving|2:boat|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|304|1427|2382463.jpg|1:person|holding|3:cell phone|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|304|1427|2382463.jpg|1:person|wearing|4:sea|wrong_predicate|1:person[mask2former_thing]mask2former:000:000006|3:sea[mask2former_stuff]mask2former:103:000002|
|306|1259|2373413.jpg|0:person|leaning on|1:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000004|0:person[mask2former_thing]mask2former:000:000001|
|306|1259|2373413.jpg|0:person|on|3:road|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000004||
|306|1259|2373413.jpg|1:person|standing on|3:road|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|308|1185|2370070.jpg|1:person|talking to|3:person|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000012||
|308|1185|2370070.jpg|1:person|holding|20:backpack|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000012||
|308|1185|2370070.jpg|2:person|looking at|29:pavement|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|19:pavement[mask2former_stuff]mask2former:123:000014|
|308|1185|2370070.jpg|4:person|looking at|29:pavement|wrong_predicate|8:person[mask2former_thing]mask2former:000:000019|19:pavement[mask2former_stuff]mask2former:123:000014|
|308|1185|2370070.jpg|6:person|talking to|25:cell phone|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000007||
|308|1185|2370070.jpg|7:person|standing on|29:pavement|wrong_predicate|5:person[mask2former_thing]mask2former:000:000009|19:pavement[mask2former_stuff]mask2former:123:000014|
|312|52|1592452.jpg|2:person|talking to|1:person|endpoint_missing_or_wrong_class|8:person[mask2former_thing]mask2former:000:000015||
|312|52|1592452.jpg|6:person|in|10:person|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000004||
|312|52|1592452.jpg|7:person|wearing|10:person|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000002||
|312|52|1592452.jpg|8:person|walking on|18:pavement|endpoint_missing_or_wrong_class||14:pavement[mask2former_stuff]mask2former:123:000011|
|315|1206|2371236.jpg|2:person|walking on|25:floor|wrong_predicate|6:person[mask2former_thing]mask2former:000:000009|22:floor[mask2former_stuff]mask2former:122:000017|
|315|1206|2371236.jpg|5:person|in front of|2:person|wrong_predicate|12:person[mask2former_thing]mask2former:000:000020|6:person[mask2former_thing]mask2former:000:000009|
|315|1206|2371236.jpg|5:person|beside|3:person|wrong_predicate|12:person[mask2former_thing]mask2former:000:000020|10:person[mask2former_thing]mask2former:000:000018|
|315|1206|2371236.jpg|5:person|carrying|16:handbag|endpoint_missing_or_wrong_class|12:person[mask2former_thing]mask2former:000:000020||
|315|1206|2371236.jpg|9:person|beside|0:person|endpoint_missing_or_wrong_class||2:person[mask2former_thing]mask2former:000:000004|
|315|1206|2371236.jpg|24:ceiling|over|11:person|rank_below50|21:ceiling[mask2former_stuff]mask2former:118:000022|9:person[mask2former_thing]mask2former:000:000014|
|321|49|1592294.jpg|1:person|riding|14:bicycle|endpoint_missing_or_wrong_class||8:bicycle[mask2former_thing]mask2former:001:000018|
|321|49|1592294.jpg|1:person|crossing|38:road|endpoint_missing_or_wrong_class||25:road[mask2former_stuff]mask2former:100:000017|
|321|49|1592294.jpg|3:person|standing on|38:road|endpoint_missing_or_wrong_class||25:road[mask2former_stuff]mask2former:100:000017|
|321|49|1592294.jpg|8:person|walking on|7:person|endpoint_missing_or_wrong_class||6:person[mask2former_thing]mask2former:000:000026|
|321|49|1592294.jpg|8:person|looking at|15:bicycle|endpoint_missing_or_wrong_class||7:bicycle[mask2former_thing]mask2former:001:000016|
|325|703|2347159.jpg|1:person|looking at|8:railroad|endpoint_missing_or_wrong_class||3:railroad[mask2former_stuff]mask2former:098:000006|
|325|703|2347159.jpg|2:person|walking on|8:railroad|endpoint_missing_or_wrong_class||3:railroad[mask2former_stuff]mask2former:098:000006|
|325|703|2347159.jpg|6:person|standing on|8:railroad|endpoint_missing_or_wrong_class||3:railroad[mask2former_stuff]mask2former:098:000006|
|327|574|2340907.jpg|1:person|looking at|2:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|2:person[mask2former_thing]mask2former:000:000006|
|327|574|2340907.jpg|2:person|playing|3:sports ball|wrong_predicate|2:person[mask2former_thing]mask2former:000:000006|3:sports ball[mask2former_thing]mask2former:032:000003|
|328|2111|2416290.jpg|0:person|wearing|24:wall-wood|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000021||
|328|2111|2416290.jpg|2:person|holding|12:pizza|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|328|2111|2416290.jpg|2:person|cooking|12:pizza|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|328|2111|2416290.jpg|2:person|wearing|24:wall-wood|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|328|2111|2416290.jpg|3:person|picking|19:cardboard|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000012||
|328|2111|2416290.jpg|3:person|wearing|23:towel|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000012||
|328|2111|2416290.jpg|6:person|looking at|1:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000005|3:person[mask2former_thing]mask2former:000:000014|
|328|2111|2416290.jpg|6:person|eating|11:pizza|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|330|1919|2406484.jpg|9:person|in front of|11:person|endpoint_missing_or_wrong_class||2:person[mask2former_thing]mask2former:000:000011|
|331|284|2326073.jpg|0:person|driving|2:airplane|endpoint_missing_or_wrong_class||0:airplane[mask2former_thing]mask2former:004:000005|
|331|284|2326073.jpg|1:person|in|2:airplane|endpoint_missing_or_wrong_class||0:airplane[mask2former_thing]mask2former:004:000005|
|332|1415|2382040.jpg|2:person|in front of|0:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:person[mask2former_thing]mask2former:000:000006|
|332|1415|2382040.jpg|2:person|sitting on|4:chair|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|3:chair[mask2former_thing]mask2former:056:000007|
|332|1415|2382040.jpg|5:dining table|in front of|1:person|wrong_predicate|4:dining table[mask2former_thing]mask2former:060:000002|1:person[mask2former_thing]mask2former:000:000004|
|333|1739|2397128.jpg|0:person|attached to|1:horse|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:horse[mask2former_thing]mask2former:017:000005|
|333|1739|2397128.jpg|0:person|sitting on|1:horse|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:horse[mask2former_thing]mask2former:017:000005|
|335|303|2326982.jpg|1:donut|attached to|0:person|wrong_predicate|1:donut[mask2former_thing]mask2former:054:000002|0:person[mask2former_thing]mask2former:000:000001|
|342|1241|2372547.jpg|0:person|touching|1:kite|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:kite[mask2former_thing]mask2former:033:000004|
|342|1241|2372547.jpg|1:kite|in front of|0:person|wrong_predicate|1:kite[mask2former_thing]mask2former:033:000004|0:person[mask2former_thing]mask2former:000:000002|
|344|556|2339759.jpg|0:person|holding|1:tennis racket|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:tennis racket[mask2former_thing]mask2former:038:000003|
|344|556|2339759.jpg|0:person|jumping from|2:playingfield|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|2:playingfield[mask2former_stuff]mask2former:097:000001|
|347|1854|2402990.jpg|0:person|wearing|13:baseball glove|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000006||
|347|1854|2402990.jpg|2:person|leaning on|18:fence|endpoint_missing_or_wrong_class||12:fence[mask2former_stuff]mask2former:117:000014|
|347|1854|2402990.jpg|4:person|running on|16:playingfield|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000008||
|347|1854|2402990.jpg|5:person|walking on|16:playingfield|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|348|205|2321647.jpg|3:person|carrying|18:handbag|wrong_predicate|1:person[mask2former_thing]mask2former:000:000002|15:handbag[mask2former_thing]mask2former:026:000006|
|348|205|2321647.jpg|8:person|in front of|2:person|wrong_predicate|5:person[mask2former_thing]mask2former:000:000007|3:person[mask2former_thing]mask2former:000:000004|
|348|205|2321647.jpg|12:person|carrying|16:handbag|endpoint_missing_or_wrong_class|||
|351|663|2345356.jpg|3:person|riding|21:horse|wrong_predicate|0:person[mask2former_thing]mask2former:000:000007|10:horse[mask2former_thing]mask2former:017:000008|
|353|1492|2385610.jpg|3:person|beside|15:car|endpoint_missing_or_wrong_class||9:car[mask2former_thing]mask2former:002:000015|
|353|1492|2385610.jpg|3:person|crossing|27:road|endpoint_missing_or_wrong_class||19:road[mask2former_stuff]mask2former:100:000014|
|353|1492|2385610.jpg|4:person|walking on|31:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|353|1492|2385610.jpg|15:car|beside|3:person|endpoint_missing_or_wrong_class|9:car[mask2former_thing]mask2former:002:000015||
|354|111|2316413.jpg|0:person|walking on|4:stairs|endpoint_missing_or_wrong_class||2:stairs[mask2former_stuff]mask2former:106:000005|
|354|111|2316413.jpg|1:person|holding|3:cell phone|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|354|111|2316413.jpg|1:person|going down|4:stairs|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|2:stairs[mask2former_stuff]mask2former:106:000005|
|354|111|2316413.jpg|1:person|wearing|4:stairs|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|2:stairs[mask2former_stuff]mask2former:106:000005|
|354|111|2316413.jpg|2:person|wearing|0:person|endpoint_missing_or_wrong_class|||
|354|111|2316413.jpg|8:fence|in front of|0:person|endpoint_missing_or_wrong_class|5:fence[mask2former_stuff]mask2former:117:000008||
|357|726|2348363.jpg|5:person|in front of|14:airplane|wrong_predicate|9:person[mask2former_thing]mask2former:000:000014|11:airplane[mask2former_thing]mask2former:004:000009|
|357|726|2348363.jpg|7:person|looking at|11:person|wrong_predicate|2:person[mask2former_thing]mask2former:000:000003|3:person[mask2former_thing]mask2former:000:000004|
|360|1205|2371211.jpg|0:person|holding|3:book|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000007||
|360|1205|2371211.jpg|6:tree|in front of|0:person|wrong_predicate|4:tree[mask2former_stuff]mask2former:116:000002|0:person[mask2former_thing]mask2former:000:000007|
|362|651|2344819.jpg|0:person|wearing|1:tie|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|362|651|2344819.jpg|3:wall|in front of|0:person|wrong_predicate|2:wall[mask2former_stuff]mask2former:131:000003|0:person[mask2former_thing]mask2former:000:000002|
|364|483|2335916.jpg|2:person|standing on|9:dirt|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000006||
|364|483|2335916.jpg|4:person|carrying|7:handbag|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|366|1251|2373084.jpg|3:person|talking to|0:person|wrong_predicate|3:person[mask2former_thing]mask2former:000:000007|1:person[mask2former_thing]mask2former:000:000004|
|366|1251|2373084.jpg|3:person|carrying|8:surfboard|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000007||
|366|1251|2373084.jpg|4:person|standing on|9:sand|endpoint_missing_or_wrong_class||7:sand[mask2former_stuff]mask2former:102:000008|
|367|1950|2408290.jpg|0:person|on back of|1:motorcycle|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:motorcycle[mask2former_thing]mask2former:003:000003|
|369|1390|2380682.jpg|4:person|wearing|10:person|wrong_predicate|5:person[mask2former_thing]mask2former:000:000011|7:person[mask2former_thing]mask2former:000:000014|
|369|1390|2380682.jpg|5:person|standing on|20:snow|endpoint_missing_or_wrong_class|9:person[mask2former_thing]mask2former:000:000018||
|369|1390|2380682.jpg|8:person|on|10:person|wrong_predicate|4:person[mask2former_thing]mask2former:000:000010|7:person[mask2former_thing]mask2former:000:000014|
|369|1390|2380682.jpg|9:person|looking at|5:person|rank_below50|2:person[mask2former_thing]mask2former:000:000006|9:person[mask2former_thing]mask2former:000:000018|
|369|1390|2380682.jpg|10:person|walking on|20:snow|endpoint_missing_or_wrong_class|7:person[mask2former_thing]mask2former:000:000014||
|369|1390|2380682.jpg|11:person|carrying|19:snowboard|wrong_predicate|8:person[mask2former_thing]mask2former:000:000015|17:snowboard[mask2former_thing]mask2former:031:000016|
|370|56|1592537.jpg|14:tree|beside|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000003|
|371|2103|2416059.jpg|0:person|carrying|2:backpack|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|371|2103|2416059.jpg|0:person|standing on|3:skis|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:skis[mask2former_thing]mask2former:030:000004|
|371|2103|2416059.jpg|0:person|playing|3:skis|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:skis[mask2former_thing]mask2former:030:000004|
|373|775|2350750.jpg|3:person|standing on|7:platform|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000008||
|373|775|2350750.jpg|4:person|beside|6:suitcase|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000007||
|373|775|2350750.jpg|4:person|standing on|7:platform|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000007||
|373|775|2350750.jpg|6:suitcase|beside|4:person|endpoint_missing_or_wrong_class||2:person[mask2former_thing]mask2former:000:000007|
|377|1495|2385674.jpg|2:person|looking at|3:person|wrong_predicate|4:person[mask2former_thing]mask2former:000:000009|0:person[mask2former_thing]mask2former:000:000001|
|377|1495|2385674.jpg|3:person|in front of|2:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|4:person[mask2former_thing]mask2former:000:000009|
|380|581|2341544.jpg|6:person|standing on|29:pavement|wrong_predicate|14:person[mask2former_thing]mask2former:000:000021|21:pavement[mask2former_stuff]mask2former:123:000019|
|380|581|2341544.jpg|10:person|carrying|23:handbag|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000005||
|381|1745|2397343.jpg|0:person|beside|1:dog|endpoint_missing_or_wrong_class||0:dog[mask2former_thing]mask2former:016:000004|
|381|1745|2397343.jpg|0:person|playing with|1:dog|endpoint_missing_or_wrong_class||0:dog[mask2former_thing]mask2former:016:000004|
|381|1745|2397343.jpg|0:person|beside|5:door|endpoint_missing_or_wrong_class|||
|381|1745|2397343.jpg|0:person|beside|7:table|endpoint_missing_or_wrong_class||7:table[mask2former_stuff]mask2former:121:000008|
|381|1745|2397343.jpg|2:potted plant|in front of|0:person|endpoint_missing_or_wrong_class|2:potted plant[mask2former_thing]mask2former:058:000002||
|381|1745|2397343.jpg|5:door|in|0:person|endpoint_missing_or_wrong_class|||
|381|1745|2397343.jpg|7:table|beside|0:person|endpoint_missing_or_wrong_class|7:table[mask2former_stuff]mask2former:121:000008||
|382|1449|2383257.jpg|0:person|standing on|1:bench|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|1:bench[mask2former_thing]mask2former:013:000002|
|382|1449|2383257.jpg|0:person|playing|2:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|2:skateboard[mask2former_thing]mask2former:036:000003|
|382|1449|2383257.jpg|3:door|beside|0:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000001|
|385|12|1159501.jpg|0:person|attached to|1:person|endpoints_collapsed_to_same_box|1:person[mask2former_thing]mask2former:000:000010|1:person[mask2former_thing]mask2former:000:000010|
|385|12|1159501.jpg|0:person|looking at|3:laptop|wrong_predicate|1:person[mask2former_thing]mask2former:000:000010|4:laptop[mask2former_thing]mask2former:063:000006|
|385|12|1159501.jpg|1:person|attached to|0:person|endpoints_collapsed_to_same_box|1:person[mask2former_thing]mask2former:000:000010|1:person[mask2former_thing]mask2former:000:000010|
|385|12|1159501.jpg|1:person|looking at|3:laptop|wrong_predicate|1:person[mask2former_thing]mask2former:000:000010|4:laptop[mask2former_thing]mask2former:063:000006|
|386|1395|2380947.jpg|3:person|looking at|6:person|rank_below50|9:person[mask2former_thing]mask2former:000:000023|8:person[mask2former_thing]mask2former:000:000019|
|386|1395|2380947.jpg|6:person|talking to|11:person|rank_below50|8:person[mask2former_thing]mask2former:000:000019|6:person[mask2former_thing]mask2former:000:000012|
|386|1395|2380947.jpg|6:person|attached to|14:tennis racket|pair_not_selected|8:person[mask2former_thing]mask2former:000:000019|16:tennis racket[mask2former_thing]mask2former:038:000032|
|386|1395|2380947.jpg|6:person|holding|14:tennis racket|pair_not_selected|8:person[mask2former_thing]mask2former:000:000019|16:tennis racket[mask2former_thing]mask2former:038:000032|
|386|1395|2380947.jpg|12:person|talking to|4:person|endpoint_missing_or_wrong_class|10:person[mask2former_thing]mask2former:000:000024||
|387|1391|2380691.jpg|0:person|looking at|1:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:sports ball[mask2former_thing]mask2former:032:000001|
|387|1391|2380691.jpg|0:person|chasing|1:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:sports ball[mask2former_thing]mask2former:032:000001|
|387|1391|2380691.jpg|0:person|about to hit|1:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:sports ball[mask2former_thing]mask2former:032:000001|
|387|1391|2380691.jpg|0:person|running on|4:floor|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|389|1609|2390707.jpg|6:person|in front of|8:person|wrong_predicate|3:person[mask2former_thing]mask2former:000:000008|2:person[mask2former_thing]mask2former:000:000004|
|389|1609|2390707.jpg|6:person|beside|16:chair|wrong_predicate|3:person[mask2former_thing]mask2former:000:000008|17:chair[mask2former_thing]mask2former:056:000011|
|389|1609|2390707.jpg|6:person|attached to|21:playingfield|wrong_predicate|3:person[mask2former_thing]mask2former:000:000008|21:playingfield[mask2former_stuff]mask2former:097:000005|
|389|1609|2390707.jpg|6:person|attached to|22:towel|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000008||
|389|1609|2390707.jpg|6:person|swinging|22:towel|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000008||
|389|1609|2390707.jpg|16:chair|beside|6:person|rank_below50|17:chair[mask2former_thing]mask2former:056:000011|3:person[mask2former_thing]mask2former:000:000008|
|394|1496|2385703.jpg|0:person|carrying|6:handbag|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000005||
|395|758|2350121.jpg|0:person|riding|3:horse|endpoint_missing_or_wrong_class||1:horse[mask2former_thing]mask2former:017:000002|
|395|758|2350121.jpg|1:person|on back of|5:horse|endpoint_missing_or_wrong_class||2:horse[mask2former_thing]mask2former:017:000005|
|395|758|2350121.jpg|1:person|riding|5:horse|endpoint_missing_or_wrong_class||2:horse[mask2former_thing]mask2former:017:000005|
|395|758|2350121.jpg|2:person|on back of|4:horse|endpoint_missing_or_wrong_class||1:horse[mask2former_thing]mask2former:017:000002|
|396|630|2343959.jpg|5:person|in front of|8:person|wrong_predicate|4:person[mask2former_thing]mask2former:000:000006|2:person[mask2former_thing]mask2former:000:000004|
|396|630|2343959.jpg|5:person|wearing|15:tie|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000006||
|396|630|2343959.jpg|8:person|in front of|19:mirror|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000004||
|396|630|2343959.jpg|9:person|beside|10:person|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000010||
|396|630|2343959.jpg|9:person|wearing|14:tie|endpoint_missing_or_wrong_class|6:person[mask2former_thing]mask2former:000:000010||
|396|630|2343959.jpg|10:person|wearing|12:tie|endpoint_missing_or_wrong_class|||
|396|630|2343959.jpg|10:person|beside|16:dining table|endpoint_missing_or_wrong_class|||
|396|630|2343959.jpg|18:light|over|8:person|endpoint_missing_or_wrong_class||2:person[mask2former_thing]mask2former:000:000004|
|398|1128|2366957.jpg|4:person|looking at|30:pavement|wrong_predicate|6:person[mask2former_thing]mask2former:000:000015|23:pavement[mask2former_stuff]mask2former:123:000026|
|398|1128|2366957.jpg|13:person|in front of|28:tree|endpoint_missing_or_wrong_class||20:tree[mask2former_stuff]mask2former:116:000007|
|399|1835|2402046.jpg|1:person|standing on|17:rock|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000008||
|399|1835|2402046.jpg|9:person|entering|13:boat|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|5:boat[mask2former_thing]mask2former:008:000005|
|399|1835|2402046.jpg|11:person|standing on|13:boat|endpoint_missing_or_wrong_class||5:boat[mask2former_thing]mask2former:008:000005|
|400|731|2348722.jpg|3:person|wearing|17:baseball glove|endpoint_missing_or_wrong_class|15:person[mask2former_thing]mask2former:000:000021||
|400|731|2348722.jpg|4:person|carrying|16:baseball bat|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000009||
|400|731|2348722.jpg|6:person|talking to|5:person|endpoint_missing_or_wrong_class|||
|400|731|2348722.jpg|7:person|running on|19:playingfield|wrong_predicate|8:person[mask2former_thing]mask2former:000:000012|17:playingfield[mask2former_stuff]mask2former:097:000016|
|404|736|2348945.jpg|0:person|talking to|1:person|endpoint_missing_or_wrong_class||1:person[mask2former_thing]mask2former:000:000008|
|404|736|2348945.jpg|0:person|standing on|5:truck|endpoint_missing_or_wrong_class||4:truck[mask2former_thing]mask2former:007:000006|
|404|736|2348945.jpg|1:person|standing on|9:pavement|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000008||
|406|1324|2377760.jpg|0:person|on|1:truck|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|406|1324|2377760.jpg|0:person|sitting on|1:truck|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|410|761|2350256.jpg|0:person|in|1:bus|endpoint_missing_or_wrong_class||1:bus[mask2former_thing]mask2former:005:000006|
|410|761|2350256.jpg|0:person|driving|1:bus|endpoint_missing_or_wrong_class||1:bus[mask2former_thing]mask2former:005:000006|
|413|280|2325881.jpg|0:person|eating|1:banana|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:banana[mask2former_thing]mask2former:046:000001|
|413|280|2325881.jpg|0:person|sitting on|2:chair|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|413|280|2325881.jpg|0:person|in front of|4:wall-wood|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|414|1318|2377223.jpg|0:person|in front of|1:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000004|2:person[mask2former_thing]mask2former:000:000006|
|414|1318|2377223.jpg|0:person|swinging|4:tennis racket|wrong_predicate|1:person[mask2former_thing]mask2former:000:000004|7:tennis racket[mask2former_thing]mask2former:038:000002|
|414|1318|2377223.jpg|1:person|in front of|6:wall|wrong_predicate|2:person[mask2former_thing]mask2former:000:000006|9:wall[mask2former_stuff]mask2former:131:000010|
|414|1318|2377223.jpg|3:sports ball|beside|2:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000001|
|415|1211|2371415.jpg|0:person|holding|1:cell phone|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|417|1547|2387788.jpg|0:person|standing on|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|1:skateboard[mask2former_thing]mask2former:036:000003|
|417|1547|2387788.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|1:skateboard[mask2former_thing]mask2former:036:000003|
|417|1547|2387788.jpg|0:person|wearing|2:platform|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|417|1547|2387788.jpg|0:person|wearing|3:pavement|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|2:pavement[mask2former_stuff]mask2former:123:000002|
|419|962|2359075.jpg|11:fence|in front of|5:person|endpoint_missing_or_wrong_class||2:person[mask2former_thing]mask2former:000:000006|
|419|962|2359075.jpg|11:fence|in front of|6:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000001|
|421|1772|2398484.jpg|0:person|on back of|2:person|wrong_predicate|2:person[mask2former_thing]mask2former:000:000005|0:person[mask2former_thing]mask2former:000:000001|
|421|1772|2398484.jpg|1:person|holding|3:baseball bat|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|3:baseball bat[mask2former_thing]mask2former:034:000006|
|421|1772|2398484.jpg|1:person|standing on|5:playingfield|wrong_predicate|1:person[mask2former_thing]mask2former:000:000003|5:playingfield[mask2former_stuff]mask2former:097:000002|
|421|1772|2398484.jpg|2:person|attached to|0:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|2:person[mask2former_thing]mask2former:000:000005|
|422|1007|2361180.jpg|3:person|in front of|1:person|wrong_predicate|1:person[mask2former_thing]mask2former:000:000005|6:person[mask2former_thing]mask2former:000:000010|
|423|2171|713172.jpg|0:person|in|13:building|endpoint_missing_or_wrong_class|||
|427|361|2329834.jpg|0:person|looking at|14:laptop|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000008||
|427|361|2329834.jpg|0:person|in front of|15:wall-wood|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000008||
|428|1752|2397624.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:skateboard[mask2former_thing]mask2former:036:000003|
|428|1752|2397624.jpg|0:person|looking at|3:pavement|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|3:pavement[mask2former_stuff]mask2former:123:000004|
|430|1713|2395938.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:skateboard[mask2former_thing]mask2former:036:000004|
|430|1713|2395938.jpg|0:person|going down|2:stairs|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|432|880|2355316.jpg|0:person|in front of|7:car|wrong_predicate|2:person[mask2former_thing]mask2former:000:000008|4:car[mask2former_thing]mask2former:002:000006|
|432|880|2355316.jpg|0:person|standing on|12:pavement|wrong_predicate|2:person[mask2former_thing]mask2former:000:000008|9:pavement[mask2former_stuff]mask2former:123:000009|
|432|880|2355316.jpg|1:person|standing on|12:pavement|endpoint_missing_or_wrong_class||9:pavement[mask2former_stuff]mask2former:123:000009|
|438|163|2319267.jpg|0:person|on|2:truck|endpoint_missing_or_wrong_class|||
|438|163|2319267.jpg|0:person|standing on|2:truck|endpoint_missing_or_wrong_class|||
|439|1357|2379131.jpg|0:person|looking at|8:apple|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:apple[mask2former_thing]mask2former:047:000004|
|439|1357|2379131.jpg|0:person|catching|8:apple|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:apple[mask2former_thing]mask2former:047:000004|
|441|2118|2416492.jpg|0:person|beside|1:toilet|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:toilet[mask2former_thing]mask2former:061:000003|
|441|2118|2416492.jpg|0:person|cleaning|1:toilet|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:toilet[mask2former_thing]mask2former:061:000003|
|443|192|2321324.jpg|0:person|walking on|22:pavement|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000013||
|443|192|2321324.jpg|1:person|feeding|11:bird|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000008||
|446|712|2347578.jpg|0:person|riding|1:skis|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:skis[mask2former_thing]mask2former:030:000004|
|447|104|2316313.jpg|0:person|in front of|1:person|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000005||
|447|104|2316313.jpg|1:person|in|3:car|endpoint_missing_or_wrong_class||4:car[mask2former_thing]mask2former:002:000004|
|448|792|2351247.jpg|4:person|beside|8:person|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000008||
|448|792|2351247.jpg|7:person|standing on|28:dirt|wrong_predicate|5:person[mask2former_thing]mask2former:000:000011|16:dirt[mask2former_stuff]mask2former:126:000016|
|448|792|2351247.jpg|8:person|picking|30:food|endpoint_missing_or_wrong_class|||
|449|784|2351059.jpg|0:person|running on|6:sand|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000004||
|449|784|2351059.jpg|1:person|catching|3:sports ball|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|449|784|2351059.jpg|1:person|wearing|4:baseball glove|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|3:baseball glove[mask2former_thing]mask2former:035:000006|
|449|784|2351059.jpg|1:person|running on|6:sand|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|450|1615|2390859.jpg|0:person|looking at|2:cell phone|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|2:cell phone[mask2former_thing]mask2former:067:000003|
|450|1615|2390859.jpg|0:person|in front of|3:paper|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|450|1615|2390859.jpg|0:person|in front of|4:building|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|453|1642|2392244.jpg|0:person|looking at|5:bowl|wrong_predicate|1:person[mask2former_thing]mask2former:000:000007|8:bowl[mask2former_thing]mask2former:045:000012|
|453|1642|2392244.jpg|10:dining table|attached to|0:person|wrong_predicate|11:dining table[mask2former_thing]mask2former:060:000005|1:person[mask2former_thing]mask2former:000:000007|
|454|629|2343942.jpg|1:person|looking at|23:laptop|wrong_predicate|5:person[mask2former_thing]mask2former:000:000016|21:laptop[mask2former_thing]mask2former:063:000009|
|454|629|2343942.jpg|3:person|sitting on|18:chair|endpoint_missing_or_wrong_class|||
|454|629|2343942.jpg|3:person|wearing|18:chair|endpoint_missing_or_wrong_class|||
|454|629|2343942.jpg|19:chair|in front of|10:person|rank_below50|19:chair[mask2former_thing]mask2former:056:000027|11:person[mask2former_thing]mask2former:000:000025|
|456|1089|2365077.jpg|0:person|talking to|2:person|endpoint_missing_or_wrong_class|||
|456|1089|2365077.jpg|8:person|carrying|16:handbag|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000013||
|457|587|2341770.jpg|0:person|driving|3:bus|wrong_predicate|1:person[mask2former_thing]mask2former:000:000005|2:bus[mask2former_thing]mask2former:005:000003|
|457|587|2341770.jpg|1:person|in|3:bus|endpoint_missing_or_wrong_class||2:bus[mask2former_thing]mask2former:005:000003|
|457|587|2341770.jpg|1:person|sitting on|3:bus|endpoint_missing_or_wrong_class||2:bus[mask2former_thing]mask2former:005:000003|
|457|587|2341770.jpg|2:person|sitting on|3:bus|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|2:bus[mask2former_thing]mask2former:005:000003|
|458|1575|2388803.jpg|0:person|wearing|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:skateboard[mask2former_thing]mask2former:036:000001|
|458|1575|2388803.jpg|0:person|looking at|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:skateboard[mask2former_thing]mask2former:036:000001|
|458|1575|2388803.jpg|0:person|catching|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:skateboard[mask2former_thing]mask2former:036:000001|
|458|1575|2388803.jpg|0:person|playing|1:skateboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|1:skateboard[mask2former_thing]mask2former:036:000001|
|458|1575|2388803.jpg|0:person|jumping over|2:pavement|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|2:pavement[mask2former_stuff]mask2former:123:000003|
|458|1575|2388803.jpg|0:person|wearing|2:pavement|wrong_predicate|0:person[mask2former_thing]mask2former:000:000002|2:pavement[mask2former_stuff]mask2former:123:000003|
|461|107|2316321.jpg|0:person|standing on|6:skis|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|461|107|2316321.jpg|0:person|wearing|6:skis|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000004||
|461|107|2316321.jpg|2:person|going down|9:snow|endpoint_missing_or_wrong_class||3:snow[mask2former_stuff]mask2former:105:000002|
|461|107|2316321.jpg|3:person|going down|9:snow|endpoint_missing_or_wrong_class||3:snow[mask2former_stuff]mask2former:105:000002|
|463|555|2339725.jpg|0:person|biting|8:toothbrush|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000005||
|465|1540|2387468.jpg|0:person|beside|4:train|endpoint_missing_or_wrong_class||3:train[mask2former_thing]mask2former:006:000003|
|465|1540|2387468.jpg|2:person|beside|4:train|wrong_predicate|1:person[mask2former_thing]mask2former:000:000007|3:train[mask2former_thing]mask2former:006:000003|
|465|1540|2387468.jpg|3:person|beside|4:train|wrong_predicate|0:person[mask2former_thing]mask2former:000:000005|3:train[mask2former_thing]mask2former:006:000003|
|466|1797|2400508.jpg|0:person|playing|1:kite|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000003||
|470|1101|2365885.jpg|0:person|playing|2:sports ball|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:sports ball[mask2former_thing]mask2former:032:000004|
|470|1101|2365885.jpg|0:person|holding|3:tennis racket|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:tennis racket[mask2former_thing]mask2former:038:000001|
|470|1101|2365885.jpg|0:person|running on|4:playingfield|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|3:playingfield[mask2former_stuff]mask2former:097:000002|
|471|1700|2394982.jpg|0:person|in front of|8:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|1:person[mask2former_thing]mask2former:000:000007|
|471|1700|2394982.jpg|0:person|attached to|13:fence|wrong_predicate|0:person[mask2former_thing]mask2former:000:000004|4:fence[mask2former_stuff]mask2former:117:000009|
|471|1700|2394982.jpg|8:person|attached to|13:fence|wrong_predicate|1:person[mask2former_thing]mask2former:000:000007|4:fence[mask2former_stuff]mask2former:117:000009|
|472|404|2332502.jpg|1:person|driving|14:boat|wrong_predicate|0:person[mask2former_thing]mask2former:000:000011|5:boat[mask2former_thing]mask2former:008:000008|
|472|404|2332502.jpg|2:person|in|14:boat|endpoint_missing_or_wrong_class||5:boat[mask2former_thing]mask2former:008:000008|
|472|404|2332502.jpg|2:person|over|18:river|endpoint_missing_or_wrong_class||7:river[mask2former_stuff]mask2former:099:000007|
|473|605|2342711.jpg|0:person|looking at|22:bowl|endpoint_missing_or_wrong_class|2:person[mask2former_thing]mask2former:000:000015||
|473|605|2342711.jpg|1:person|beside|0:person|rank_below50|1:person[mask2former_thing]mask2former:000:000003|2:person[mask2former_thing]mask2former:000:000015|
|478|1804|2400822.jpg|0:person|attached to|3:surfboard|wrong_predicate|1:person[mask2former_thing]mask2former:000:000004|2:surfboard[mask2former_thing]mask2former:037:000002|
|478|1804|2400822.jpg|0:person|playing|3:surfboard|wrong_predicate|1:person[mask2former_thing]mask2former:000:000004|2:surfboard[mask2former_thing]mask2former:037:000002|
|478|1804|2400822.jpg|0:person|on|4:sand|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000004||
|478|1804|2400822.jpg|0:person|standing on|4:sand|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000004||
|478|1804|2400822.jpg|0:person|beside|5:sea|wrong_predicate|1:person[mask2former_thing]mask2former:000:000004|4:sea[mask2former_stuff]mask2former:103:000003|
|478|1804|2400822.jpg|1:person|on|4:sand|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|478|1804|2400822.jpg|1:person|walking on|4:sand|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|478|1804|2400822.jpg|1:person|beside|5:sea|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|4:sea[mask2former_stuff]mask2former:103:000003|
|480|461|2334659.jpg|0:person|in front of|9:house|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000005||
|480|461|2334659.jpg|0:person|walking on|13:pavement|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000005||
|480|461|2334659.jpg|2:person|in front of|9:house|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000009||
|480|461|2334659.jpg|2:person|walking on|13:pavement|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000009||
|481|797|2351374.jpg|7:person|attached to|14:pavement|wrong_predicate|4:person[mask2former_thing]mask2former:000:000009|16:pavement[mask2former_stuff]mask2former:123:000014|
|481|797|2351374.jpg|8:person|in front of|9:person|endpoint_missing_or_wrong_class|||
|481|797|2351374.jpg|10:person|going down|14:pavement|wrong_predicate|9:person[mask2former_thing]mask2former:000:000017|16:pavement[mask2former_stuff]mask2former:123:000014|
|481|797|2351374.jpg|12:person|beside|15:building|wrong_predicate|6:person[mask2former_thing]mask2former:000:000011|17:building[mask2former_stuff]mask2former:129:000003|
|481|797|2351374.jpg|13:sky|on|3:person|wrong_predicate|15:sky[mask2former_stuff]mask2former:119:000007|7:person[mask2former_thing]mask2former:000:000015|
|483|1172|2369539.jpg|0:person|catching|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000004|
|483|1172|2369539.jpg|0:person|playing|1:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|1:surfboard[mask2former_thing]mask2former:037:000004|
|483|1172|2369539.jpg|0:person|on|2:sea|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:sea[mask2former_stuff]mask2former:103:000002|
|485|57|1592560.jpg|0:person|beside|7:table|endpoint_missing_or_wrong_class||7:table[mask2former_stuff]mask2former:121:000008|
|485|57|1592560.jpg|0:person|in front of|9:wall|endpoint_missing_or_wrong_class||8:wall[mask2former_stuff]mask2former:131:000010|
|486|1052|2362836.jpg|0:person|guiding|3:person|endpoint_missing_or_wrong_class||1:person[mask2former_thing]mask2former:000:000004|
|486|1052|2362836.jpg|3:person|in front of|0:person|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000004||
|486|1052|2362836.jpg|4:person|on|1:person|endpoint_missing_or_wrong_class||3:person[mask2former_thing]mask2former:000:000007|
|486|1052|2362836.jpg|5:person|walking on|8:road|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000001||
|489|610|2342847.jpg|2:person|walking on|23:road|wrong_predicate|3:person[mask2former_thing]mask2former:000:000018|18:road[mask2former_stuff]mask2former:100:000015|
|489|610|2342847.jpg|6:person|driving|11:truck|wrong_predicate|2:person[mask2former_thing]mask2former:000:000013|11:truck[mask2former_thing]mask2former:007:000009|
|490|2161|498294.jpg|0:person|in front of|1:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|3:person[mask2former_thing]mask2former:000:000007|
|490|2161|498294.jpg|1:person|wearing|6:baseball glove|endpoint_missing_or_wrong_class|3:person[mask2former_thing]mask2former:000:000007||
|490|2161|498294.jpg|2:person|wearing|7:baseball glove|endpoint_missing_or_wrong_class|5:person[mask2former_thing]mask2former:000:000010||
|490|2161|498294.jpg|4:person|wearing|8:baseball glove|endpoint_missing_or_wrong_class|4:person[mask2former_thing]mask2former:000:000008||
|490|2161|498294.jpg|5:person|running on|9:playingfield|wrong_predicate|1:person[mask2former_thing]mask2former:000:000005|7:playingfield[mask2former_stuff]mask2former:097:000003|
|491|382|2331166.jpg|0:person|on|17:bus|endpoint_missing_or_wrong_class||8:bus[mask2former_thing]mask2former:005:000009|
|491|382|2331166.jpg|8:person|driving|17:bus|endpoint_missing_or_wrong_class||8:bus[mask2former_thing]mask2former:005:000009|
|492|1031|2362238.jpg|0:person|playing|2:surfboard|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|2:surfboard[mask2former_thing]mask2former:037:000004|
|492|1031|2362238.jpg|0:person|on|3:sea|wrong_predicate|0:person[mask2former_thing]mask2former:000:000003|3:sea[mask2former_stuff]mask2former:103:000002|
|493|374|2330610.jpg|0:person|in|1:truck|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|493|374|2330610.jpg|0:person|driving|1:truck|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|494|265|2324812.jpg|0:person|touching|2:person|wrong_predicate|3:person[mask2former_thing]mask2former:000:000006|2:person[mask2former_thing]mask2former:000:000005|
|494|265|2324812.jpg|1:person|attached to|3:person|wrong_predicate|0:person[mask2former_thing]mask2former:000:000001|1:person[mask2former_thing]mask2former:000:000003|
|494|265|2324812.jpg|3:person|in front of|7:window|endpoint_missing_or_wrong_class|1:person[mask2former_thing]mask2former:000:000003||
|496|769|2350508.jpg|1:person|attached to|2:pizza|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|496|769|2350508.jpg|1:person|looking at|2:pizza|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|496|769|2350508.jpg|1:person|eating|2:pizza|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|496|769|2350508.jpg|1:person|in front of|3:wall|endpoint_missing_or_wrong_class|0:person[mask2former_thing]mask2former:000:000002||
|496|769|2350508.jpg|2:pizza|attached to|1:person|endpoint_missing_or_wrong_class||0:person[mask2former_thing]mask2former:000:000002|
|500|1155|2368389.jpg|3:fence|enclosing|0:person|wrong_predicate|4:fence[mask2former_stuff]mask2former:117:000005|0:person[mask2former_thing]mask2former:000:000002|
