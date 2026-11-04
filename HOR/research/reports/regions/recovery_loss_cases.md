# A组对照的新增与丢失GT关系清单

变化以Top-50是否命中作为判断。每一行是一条PSG标注关系；索引、图片文件名、GT端点类别、谓词、A组阶段、比较组阶段和端点/预算机制均逐条列出。完整结构化记录见同目录 `recovery_loss_cases.json`。

## 全部968条人相关GT关系

### B_mask2former_thing

恢复26条，丢失74条，命中净变化-48条。

|变化|样本序号|数据集索引|图片|GT人/端点|谓词|GT对象|A组阶段|比较组阶段|机制|
|---|---:|---:|---|---|---|---|---|---|---|
|recovered|385|12|1159501.jpg|0:person|touching|3:laptop|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|494|265|2324812.jpg|3:person|holding|5:cell phone|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|413|280|2325881.jpg|0:person|holding|1:banana|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|364|483|2335916.jpg|1:person|looking at|5:bus|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|373|775|2350750.jpg|3:person|looking at|5:train|endpoint_missing_or_wrong_class|hit50|thing_pair_or_relation_ranking_change|
|recovered|373|775|2350750.jpg|4:person|looking at|5:train|endpoint_missing_or_wrong_class|hit50|thing_pair_or_relation_ranking_change|
|recovered|449|784|2351059.jpg|1:person|wearing|4:baseball glove|endpoint_missing_or_wrong_class|hit50|thing_pair_or_relation_ranking_change|
|recovered|161|859|2354354.jpg|0:person|holding|10:umbrella|endpoint_missing_or_wrong_class|hit50|thing_pair_or_relation_ranking_change|
|recovered|103|989|2360368.jpg|4:bicycle|beside|2:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|23|1055|2363004.jpg|10:train|beside|8:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|194|1135|2367479.jpg|5:person|beside|3:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|369|1390|2380682.jpg|9:person|looking at|5:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|382|1449|2383257.jpg|0:person|standing on|1:bench|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|377|1495|2385674.jpg|1:person|beside|0:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|377|1495|2385674.jpg|3:person|beside|2:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|377|1495|2385674.jpg|3:person|looking at|2:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|253|1589|2389680.jpg|4:person|beside|0:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|253|1589|2389680.jpg|10:handbag|beside|2:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|478|1804|2400822.jpg|0:person|beside|1:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|152|1986|2409643.jpg|1:person|carrying|4:handbag|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|235|2050|2412773.jpg|0:person|on|1:surfboard|endpoint_missing_or_wrong_class|hit50|thing_pair_or_relation_ranking_change|
|recovered|441|2118|2416492.jpg|0:person|cleaning|1:toilet|endpoint_missing_or_wrong_class|hit50|thing_pair_or_relation_ranking_change|
|recovered|60|2159|498242.jpg|0:person|looking at|9:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|60|2159|498242.jpg|1:person|beside|0:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|60|2159|498242.jpg|8:person|beside|5:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|60|2159|498242.jpg|9:person|looking at|0:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|lost|385|12|1159501.jpg|0:person|looking at|3:laptop|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|385|12|1159501.jpg|1:person|looking at|3:laptop|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|321|49|1592294.jpg|1:person|riding|14:bicycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|312|52|1592452.jpg|2:person|talking to|1:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|447|104|2316313.jpg|1:person|in|3:car|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|461|107|2316321.jpg|0:person|wearing|6:skis|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|354|111|2316413.jpg|1:person|holding|3:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|413|280|2325881.jpg|0:person|eating|1:banana|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|331|284|2326073.jpg|1:person|in|2:airplane|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|427|361|2329834.jpg|0:person|looking at|14:laptop|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|472|404|2332502.jpg|2:person|in|14:boat|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|21|411|2332726.jpg|3:person|flying over|5:kite|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|364|483|2335916.jpg|4:person|carrying|7:handbag|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|457|587|2341770.jpg|1:person|in|3:bus|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|262|621|2343341.jpg|0:person|throwing|4:sports ball|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|454|629|2343942.jpg|3:person|sitting on|18:chair|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|396|630|2343959.jpg|9:person|wearing|14:tie|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|396|630|2343959.jpg|10:person|wearing|12:tie|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|95|649|2344605.jpg|0:person|sitting on|9:chair|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|362|651|2344819.jpg|0:person|wearing|1:tie|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|94|664|2345357.jpg|0:person|in|10:train|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|94|664|2345357.jpg|1:person|in|10:train|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|395|758|2350121.jpg|0:person|riding|3:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|395|758|2350121.jpg|1:person|riding|5:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|72|841|2353618.jpg|1:person|wearing|2:skis|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|72|841|2353618.jpg|2:skis|on|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|87|852|2354099.jpg|11:person|on|34:skateboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|106|868|2354820.jpg|0:person|riding|1:skateboard|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|254|896|2356062.jpg|7:person|holding|18:teddy bear|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|166|955|2358756.jpg|0:person|holding|1:frisbee|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|103|989|2360368.jpg|2:person|beside|9:motorcycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|422|1007|2361180.jpg|4:person|talking to|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|456|1089|2365077.jpg|8:person|carrying|16:handbag|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|52|1139|2367625.jpg|0:person|holding|1:spoon|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|281|1203|2371154.jpg|1:person|on|4:snowboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|315|1206|2371236.jpg|5:person|carrying|16:handbag|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|415|1211|2371415.jpg|0:person|holding|1:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|61|1219|2371806.jpg|0:person|wearing|1:baseball glove|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|366|1251|2373084.jpg|3:person|carrying|8:surfboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|127|1293|2375622.jpg|0:person|holding|4:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|406|1324|2377760.jpg|0:person|beside|2:suitcase|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|233|1337|2378360.jpg|0:person|riding|1:surfboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|175|1343|2378563.jpg|0:person|beside|4:motorcycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|175|1343|2378563.jpg|4:motorcycle|beside|0:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|302|1396|2381002.jpg|2:person|riding|5:bicycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|302|1396|2381002.jpg|2:person|carrying|14:backpack|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|63|1445|2383111.jpg|0:person|riding|6:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|63|1445|2383111.jpg|3:person|riding|4:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|16|1466|2384291.jpg|0:person|beside|1:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|16|1466|2384291.jpg|1:person|beside|0:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|75|1505|2386156.jpg|0:person|in|2:car|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|51|1507|2386227.jpg|0:person|beside|1:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|138|1529|2387080.jpg|0:person|sitting on|5:chair|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|465|1540|2387468.jpg|0:person|beside|4:train|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|465|1540|2387468.jpg|2:person|beside|4:train|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|253|1589|2389680.jpg|2:person|sitting on|8:bench|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|253|1589|2389680.jpg|2:person|holding|11:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|243|1591|2389803.jpg|0:person|on|9:boat|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|64|1596|2390113.jpg|0:person|riding|1:elephant|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|172|1608|2390659.jpg|8:person|holding|24:tennis racket|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|53|1627|2391314.jpg|0:person|wearing|1:skis|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|153|1695|2394762.jpg|6:person|catching|12:sports ball|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|484|1699|2394864.jpg|0:person|leaning on|5:dining table|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|122|1729|2396723.jpg|0:person|holding|3:wine glass|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|122|1729|2396723.jpg|1:cat|lying on|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|381|1745|2397343.jpg|0:person|beside|1:dog|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|381|1745|2397343.jpg|2:potted plant|in front of|0:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|399|1835|2402046.jpg|11:person|standing on|13:boat|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|183|1866|2403494.jpg|11:person|wearing|19:skis|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|367|1950|2408290.jpg|0:person|on|1:motorcycle|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|328|2111|2416290.jpg|2:person|cooking|12:pizza|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|228|2144|285721.jpg|0:person|talking to|2:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|60|2159|498242.jpg|9:person|holding|10:umbrella|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|490|2161|498294.jpg|2:person|wearing|7:baseball glove|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|

### C_fasterrcnn_thing_plus_stuff

恢复103条，丢失22条，命中净变化+81条。

|变化|样本序号|数据集索引|图片|GT人/端点|谓词|GT对象|A组阶段|比较组阶段|机制|
|---|---:|---:|---|---|---|---|---|---|---|
|recovered|71|10|1159449.jpg|1:person|standing on|23:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|145|23|1159863.jpg|0:person|on|7:road|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|321|49|1592294.jpg|1:person|crossing|38:road|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|312|52|1592452.jpg|8:person|walking on|18:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|29|81|2315729.jpg|2:person|slicing|15:cake|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|210|105|2316316.jpg|6:person|sitting on|17:motorcycle|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|348|205|2321647.jpg|2:person|standing on|21:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|348|205|2321647.jpg|8:person|standing on|21:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|54|237|2323211.jpg|1:person|on|17:grass|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|54|237|2323211.jpg|3:person|on|17:grass|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|54|237|2323211.jpg|8:person|on|17:grass|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|54|237|2323211.jpg|11:person|standing on|17:grass|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|494|265|2324812.jpg|3:person|holding|5:cell phone|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|190|283|2326062.jpg|3:person|on|27:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|190|283|2326062.jpg|9:person|walking on|27:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|6|295|2326503.jpg|0:person|on|1:surfboard|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|6|295|2326503.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|219|316|2327752.jpg|0:person|walking on|15:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|128|323|2328089.jpg|0:person|in front of|5:building|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|184|325|2328153.jpg|1:person|standing on|6:building|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|427|361|2329834.jpg|0:person|beside|16:window|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|346|377|2330880.jpg|0:person|standing on|6:building|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|491|382|2331166.jpg|2:person|on|20:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|491|382|2331166.jpg|3:person|on|20:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|491|382|2331166.jpg|5:person|walking on|20:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|44|489|2336251.jpg|2:person|sitting on|9:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|383|503|2336741.jpg|0:person|standing on|24:floor|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|10|553|2339606.jpg|4:person|standing on|12:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|327|574|2340907.jpg|0:person|standing on|11:floor|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|170|658|2345182.jpg|2:person|standing on|22:grass|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|325|703|2347159.jpg|6:person|standing on|8:railroad|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|446|712|2347578.jpg|0:person|going down|2:snow|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|446|712|2347578.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|400|731|2348722.jpg|8:person|standing on|19:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|449|784|2351059.jpg|2:person|looking at|1:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|448|792|2351247.jpg|7:person|standing on|28:dirt|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|481|797|2351374.jpg|7:person|walking on|14:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|89|813|2352072.jpg|4:sky|over|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|259|826|2352851.jpg|0:person|beside|3:sea|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|259|826|2352851.jpg|0:person|looking at|3:sea|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|161|859|2354354.jpg|4:person|on|16:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|78|910|2356736.jpg|0:person|walking on|13:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|65|915|2356824.jpg|0:person|walking on|18:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|91|926|2357328.jpg|1:person|standing on|5:grass|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|166|955|2358756.jpg|0:person|throwing|1:frisbee|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|166|955|2358756.jpg|0:person|standing on|4:dirt|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|419|962|2359075.jpg|5:person|standing on|12:dirt|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|419|962|2359075.jpg|6:person|standing on|12:dirt|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|201|970|2359437.jpg|0:person|picking|1:pizza|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|158|975|2359797.jpg|3:person|carrying|14:backpack|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|103|989|2360368.jpg|4:bicycle|beside|2:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|422|1007|2361180.jpg|1:person|walking on|6:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|422|1007|2361180.jpg|2:person|walking on|6:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|422|1007|2361180.jpg|4:person|standing on|6:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|135|1163|2368707.jpg|0:person|running on|9:dirt|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|135|1163|2368707.jpg|1:person|running on|9:dirt|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|135|1163|2368707.jpg|3:person|throwing|4:frisbee|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|308|1185|2370070.jpg|6:person|walking on|29:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|360|1205|2371211.jpg|0:person|standing on|8:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|315|1206|2371236.jpg|2:person|walking on|25:floor|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|315|1206|2371236.jpg|5:person|walking on|25:floor|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|315|1206|2371236.jpg|11:person|standing on|25:floor|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|415|1211|2371415.jpg|4:wall|enclosing|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|342|1241|2372547.jpg|0:person|sitting on|3:floor|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|366|1251|2373084.jpg|0:person|standing on|9:sand|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|233|1337|2378360.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|195|1382|2380359.jpg|0:person|walking on|27:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|386|1395|2380947.jpg|6:person|standing on|17:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|302|1396|2381002.jpg|3:person|standing on|19:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|302|1396|2381002.jpg|4:person|standing on|17:road|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|144|1442|2383041.jpg|3:person|flying over|21:sea|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|382|1449|2383257.jpg|5:wall|beside|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|16|1466|2384291.jpg|0:person|on|20:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|16|1466|2384291.jpg|4:person|on|20:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|434|1478|2385010.jpg|0:person|standing on|4:floor|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|41|1485|2385230.jpg|4:wall-wood|beside|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|119|1534|2387240.jpg|9:person|standing on|15:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|227|1607|2390654.jpg|3:person|running on|9:sand|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|172|1608|2390659.jpg|8:person|standing on|29:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|389|1609|2390707.jpg|7:person|standing on|21:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|389|1609|2390707.jpg|9:person|standing on|21:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|125|1673|2393510.jpg|0:person|playing with|2:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|153|1695|2394762.jpg|3:person|running on|13:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|24|1712|2395918.jpg|1:person|sitting on|5:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|430|1713|2395938.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|428|1752|2397624.jpg|0:person|on|5:wall|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|131|1764|2398216.jpg|0:person|standing on|11:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|421|1772|2398484.jpg|2:person|wearing|4:baseball glove|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|101|1796|2400414.jpg|0:person|standing on|6:grass|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|466|1797|2400508.jpg|0:person|on|2:sand|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|466|1797|2400508.jpg|0:person|standing on|2:sand|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|466|1797|2400508.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|478|1804|2400822.jpg|0:person|beside|1:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|478|1804|2400822.jpg|5:sea|beside|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|478|1804|2400822.jpg|5:sea|beside|1:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|347|1854|2402990.jpg|2:person|leaning on|18:fence|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|81|1886|2404565.jpg|0:person|standing on|17:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|152|1986|2409643.jpg|0:person|on|7:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|192|2020|2411218.jpg|2:person|on|15:sand|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|235|2050|2412773.jpg|0:person|in front of|3:rock|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|287|2058|2413475.jpg|0:person|catching|1:frisbee|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|228|2144|285721.jpg|0:person|leaning on|3:wall|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|490|2161|498294.jpg|3:person|standing on|9:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|lost|370|56|1592537.jpg|0:person|riding|1:boat|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|447|104|2316313.jpg|1:person|in|3:car|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|354|111|2316413.jpg|1:person|holding|3:cell phone|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|327|574|2340907.jpg|1:person|looking at|2:person|hit50|rank_below50|correct_predicate_below_top50|
|lost|106|868|2354820.jpg|0:person|riding|1:skateboard|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|166|955|2358756.jpg|0:person|holding|1:frisbee|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|158|975|2359797.jpg|10:person|holding|19:umbrella|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|123|1099|2365844.jpg|0:person|beside|8:person|hit50|rank_below50|correct_predicate_below_top50|
|lost|123|1099|2365844.jpg|9:person|beside|12:person|hit50|rank_below50|correct_predicate_below_top50|
|lost|281|1203|2371154.jpg|2:person|wearing|7:snowboard|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|285|1218|2371757.jpg|0:person|driving|6:bus|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|16|1466|2384291.jpg|0:person|beside|1:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|16|1466|2384291.jpg|1:person|beside|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|465|1540|2387468.jpg|0:person|beside|4:train|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|465|1540|2387468.jpg|2:person|beside|4:train|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|172|1608|2390659.jpg|8:person|holding|24:tennis racket|hit50|rank_below50|correct_predicate_below_top50|
|lost|389|1609|2390707.jpg|8:person|looking at|6:person|hit50|rank_below50|correct_predicate_below_top50|
|lost|125|1673|2393510.jpg|2:person|looking at|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|484|1699|2394864.jpg|4:umbrella|over|0:person|hit50|rank_below50|correct_predicate_below_top50|
|lost|381|1745|2397343.jpg|2:potted plant|in front of|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|428|1752|2397624.jpg|0:person|riding|1:skateboard|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|287|2058|2413475.jpg|0:person|holding|1:frisbee|hit50|wrong_predicate|relation_model_selected_wrong_predicate|

### D_mask2former_thing_plus_stuff

恢复107条，丢失77条，命中净变化+30条。

|变化|样本序号|数据集索引|图片|GT人/端点|谓词|GT对象|A组阶段|比较组阶段|机制|
|---|---:|---:|---|---|---|---|---|---|---|
|recovered|71|10|1159449.jpg|1:person|standing on|23:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|385|12|1159501.jpg|0:person|touching|3:laptop|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|145|23|1159863.jpg|0:person|on|7:road|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|210|105|2316316.jpg|1:person|on|22:road|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|348|205|2321647.jpg|2:person|standing on|21:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|348|205|2321647.jpg|8:person|standing on|21:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|54|237|2323211.jpg|1:person|on|17:grass|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|54|237|2323211.jpg|3:person|on|17:grass|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|54|237|2323211.jpg|8:person|on|17:grass|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|54|237|2323211.jpg|11:person|standing on|17:grass|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|494|265|2324812.jpg|3:person|carrying|4:handbag|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|494|265|2324812.jpg|3:person|holding|5:cell phone|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|494|265|2324812.jpg|5:cell phone|touching|3:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|413|280|2325881.jpg|0:person|holding|1:banana|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|190|283|2326062.jpg|0:person|walking on|27:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|190|283|2326062.jpg|3:person|on|27:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|190|283|2326062.jpg|9:person|walking on|27:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|190|283|2326062.jpg|12:person|on|27:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|6|295|2326503.jpg|0:person|on|1:surfboard|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|6|295|2326503.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|219|316|2327752.jpg|0:person|walking on|15:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|128|323|2328089.jpg|0:person|in front of|5:building|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|184|325|2328153.jpg|1:person|standing on|6:building|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|427|361|2329834.jpg|0:person|beside|16:window|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|197|368|2330400.jpg|1:person|holding|2:skis|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|346|377|2330880.jpg|0:person|standing on|6:building|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|491|382|2331166.jpg|2:person|on|20:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|491|382|2331166.jpg|3:person|on|20:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|491|382|2331166.jpg|5:person|walking on|20:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|364|483|2335916.jpg|1:person|looking at|5:bus|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|383|503|2336741.jpg|0:person|standing on|24:floor|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|327|574|2340907.jpg|0:person|standing on|11:floor|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|396|630|2343959.jpg|9:person|looking at|8:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|170|658|2345182.jpg|2:person|standing on|22:grass|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|446|712|2347578.jpg|0:person|going down|2:snow|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|446|712|2347578.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|400|731|2348722.jpg|8:person|standing on|19:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|373|775|2350750.jpg|3:person|looking at|5:train|endpoint_missing_or_wrong_class|hit50|thing_pair_or_relation_ranking_change|
|recovered|373|775|2350750.jpg|4:person|looking at|5:train|endpoint_missing_or_wrong_class|hit50|thing_pair_or_relation_ranking_change|
|recovered|449|784|2351059.jpg|2:person|looking at|1:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|481|797|2351374.jpg|7:person|walking on|14:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|89|813|2352072.jpg|4:sky|over|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|259|826|2352851.jpg|0:person|beside|3:sea|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|259|826|2352851.jpg|0:person|looking at|3:sea|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|72|841|2353618.jpg|1:person|on|3:snow|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|161|859|2354354.jpg|0:person|holding|10:umbrella|endpoint_missing_or_wrong_class|hit50|thing_pair_or_relation_ranking_change|
|recovered|161|859|2354354.jpg|4:person|on|16:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|432|880|2355316.jpg|6:person|in front of|13:building|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|78|910|2356736.jpg|0:person|walking on|13:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|65|915|2356824.jpg|0:person|walking on|18:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|419|962|2359075.jpg|5:person|standing on|12:dirt|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|419|962|2359075.jpg|6:person|standing on|12:dirt|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|103|989|2360368.jpg|4:bicycle|beside|2:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|422|1007|2361180.jpg|1:person|walking on|6:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|422|1007|2361180.jpg|2:person|walking on|6:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|422|1007|2361180.jpg|4:person|standing on|6:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|194|1135|2367479.jpg|5:person|beside|3:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|135|1163|2368707.jpg|2:person|running on|9:dirt|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|308|1185|2370070.jpg|6:person|walking on|29:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|281|1203|2371154.jpg|0:person|on|8:snow|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|360|1205|2371211.jpg|0:person|standing on|8:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|315|1206|2371236.jpg|5:person|walking on|25:floor|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|315|1206|2371236.jpg|11:person|standing on|25:floor|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|415|1211|2371415.jpg|4:wall|enclosing|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|342|1241|2372547.jpg|0:person|sitting on|3:floor|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|366|1251|2373084.jpg|0:person|standing on|9:sand|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|233|1337|2378360.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|195|1382|2380359.jpg|0:person|walking on|27:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|386|1395|2380947.jpg|6:person|standing on|17:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|302|1396|2381002.jpg|4:person|standing on|17:road|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|206|1401|2381176.jpg|4:sky|over|1:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|144|1442|2383041.jpg|3:person|flying over|21:sea|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|382|1449|2383257.jpg|5:wall|beside|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|16|1466|2384291.jpg|0:person|on|20:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|434|1478|2385010.jpg|0:person|standing on|4:floor|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|41|1485|2385230.jpg|4:wall-wood|beside|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|377|1495|2385674.jpg|1:person|beside|0:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|377|1495|2385674.jpg|3:person|beside|2:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|377|1495|2385674.jpg|3:person|looking at|2:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|119|1534|2387240.jpg|9:person|standing on|15:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|227|1607|2390654.jpg|3:person|running on|9:sand|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|172|1608|2390659.jpg|8:person|standing on|29:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|389|1609|2390707.jpg|7:person|standing on|21:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|389|1609|2390707.jpg|9:person|standing on|21:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|125|1673|2393510.jpg|0:person|playing with|2:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|153|1695|2394762.jpg|3:person|running on|13:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|24|1712|2395918.jpg|1:person|sitting on|5:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|430|1713|2395938.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|428|1752|2397624.jpg|0:person|on|5:wall|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|131|1764|2398216.jpg|0:person|standing on|11:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|421|1772|2398484.jpg|2:person|wearing|4:baseball glove|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|101|1796|2400414.jpg|0:person|standing on|6:grass|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|466|1797|2400508.jpg|0:person|on|2:sand|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|466|1797|2400508.jpg|0:person|standing on|2:sand|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|466|1797|2400508.jpg|3:sky|over|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|478|1804|2400822.jpg|0:person|beside|1:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|478|1804|2400822.jpg|5:sea|beside|0:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|478|1804|2400822.jpg|5:sea|beside|1:person|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|81|1886|2404565.jpg|0:person|standing on|17:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|152|1986|2409643.jpg|0:person|on|7:pavement|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|152|1986|2409643.jpg|1:person|carrying|4:handbag|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|235|2050|2412773.jpg|0:person|on|1:surfboard|endpoint_missing_or_wrong_class|hit50|thing_pair_or_relation_ranking_change|
|recovered|235|2050|2412773.jpg|0:person|in front of|3:rock|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|287|2058|2413475.jpg|0:person|catching|1:frisbee|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|441|2118|2416492.jpg|0:person|touching|1:toilet|endpoint_missing_or_wrong_class|hit50|thing_pair_or_relation_ranking_change|
|recovered|228|2144|285721.jpg|0:person|leaning on|3:wall|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|recovered|490|2161|498294.jpg|3:person|standing on|9:playingfield|endpoint_missing_or_wrong_class|hit50|stuff_endpoint_matches_PSG_GT|
|lost|385|12|1159501.jpg|0:person|looking at|3:laptop|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|385|12|1159501.jpg|1:person|looking at|3:laptop|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|321|49|1592294.jpg|1:person|riding|14:bicycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|312|52|1592452.jpg|2:person|talking to|1:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|447|104|2316313.jpg|1:person|in|3:car|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|461|107|2316321.jpg|0:person|wearing|6:skis|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|354|111|2316413.jpg|1:person|holding|3:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|413|280|2325881.jpg|0:person|eating|1:banana|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|331|284|2326073.jpg|1:person|in|2:airplane|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|427|361|2329834.jpg|0:person|looking at|14:laptop|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|197|368|2330400.jpg|1:person|wearing|2:skis|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|472|404|2332502.jpg|2:person|in|14:boat|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|21|411|2332726.jpg|3:person|flying over|5:kite|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|364|483|2335916.jpg|4:person|carrying|7:handbag|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|327|574|2340907.jpg|1:person|looking at|2:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|457|587|2341770.jpg|1:person|in|3:bus|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|262|621|2343341.jpg|0:person|throwing|4:sports ball|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|454|629|2343942.jpg|3:person|sitting on|18:chair|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|396|630|2343959.jpg|9:person|wearing|14:tie|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|396|630|2343959.jpg|10:person|wearing|12:tie|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|95|649|2344605.jpg|0:person|sitting on|9:chair|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|362|651|2344819.jpg|0:person|wearing|1:tie|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|94|664|2345357.jpg|0:person|in|10:train|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|94|664|2345357.jpg|1:person|in|10:train|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|395|758|2350121.jpg|0:person|riding|3:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|395|758|2350121.jpg|1:person|riding|5:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|72|841|2353618.jpg|1:person|wearing|2:skis|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|87|852|2354099.jpg|11:person|on|34:skateboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|106|868|2354820.jpg|0:person|riding|1:skateboard|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|254|896|2356062.jpg|7:person|holding|18:teddy bear|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|166|955|2358756.jpg|0:person|holding|1:frisbee|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|158|975|2359797.jpg|10:person|holding|19:umbrella|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|103|989|2360368.jpg|2:person|beside|9:motorcycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|456|1089|2365077.jpg|8:person|carrying|16:handbag|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|123|1099|2365844.jpg|9:person|beside|12:person|hit50|rank_below50|correct_predicate_below_top50|
|lost|52|1139|2367625.jpg|0:person|holding|1:spoon|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|281|1203|2371154.jpg|1:person|on|4:snowboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|281|1203|2371154.jpg|2:person|wearing|7:snowboard|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|315|1206|2371236.jpg|5:person|carrying|16:handbag|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|415|1211|2371415.jpg|0:person|holding|1:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|285|1218|2371757.jpg|0:person|driving|6:bus|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|366|1251|2373084.jpg|3:person|carrying|8:surfboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|127|1293|2375622.jpg|0:person|holding|4:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|233|1337|2378360.jpg|0:person|riding|1:surfboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|175|1343|2378563.jpg|0:person|beside|4:motorcycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|175|1343|2378563.jpg|4:motorcycle|beside|0:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|302|1396|2381002.jpg|2:person|riding|5:bicycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|302|1396|2381002.jpg|2:person|carrying|14:backpack|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|63|1445|2383111.jpg|0:person|riding|6:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|63|1445|2383111.jpg|3:person|riding|4:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|16|1466|2384291.jpg|0:person|beside|1:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|16|1466|2384291.jpg|1:person|beside|0:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|75|1505|2386156.jpg|0:person|in|2:car|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|51|1507|2386227.jpg|0:person|beside|1:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|138|1529|2387080.jpg|0:person|sitting on|5:chair|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|465|1540|2387468.jpg|0:person|beside|4:train|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|465|1540|2387468.jpg|2:person|beside|4:train|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|465|1540|2387468.jpg|3:person|beside|4:train|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|253|1589|2389680.jpg|2:person|sitting on|8:bench|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|253|1589|2389680.jpg|2:person|holding|11:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|243|1591|2389803.jpg|0:person|on|9:boat|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|64|1596|2390113.jpg|0:person|riding|1:elephant|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|172|1608|2390659.jpg|8:person|holding|24:tennis racket|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|53|1627|2391314.jpg|0:person|wearing|1:skis|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|125|1673|2393510.jpg|2:person|looking at|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|153|1695|2394762.jpg|6:person|catching|12:sports ball|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|122|1729|2396723.jpg|0:person|holding|3:wine glass|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|122|1729|2396723.jpg|1:cat|lying on|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|381|1745|2397343.jpg|0:person|beside|1:dog|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|381|1745|2397343.jpg|2:potted plant|in front of|0:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|399|1835|2402046.jpg|11:person|standing on|13:boat|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|183|1866|2403494.jpg|11:person|wearing|19:skis|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|287|2058|2413475.jpg|0:person|holding|1:frisbee|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|328|2111|2416290.jpg|2:person|cooking|12:pizza|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|228|2144|285721.jpg|0:person|talking to|2:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|60|2159|498242.jpg|9:person|holding|10:umbrella|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|490|2161|498294.jpg|2:person|wearing|7:baseball glove|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|

## 固定530条原检测端点有效GT关系

### B_mask2former_thing

恢复20条，丢失74条，命中净变化-54条。

|变化|样本序号|数据集索引|图片|GT人/端点|谓词|GT对象|A组阶段|比较组阶段|机制|
|---|---:|---:|---|---|---|---|---|---|---|
|recovered|385|12|1159501.jpg|0:person|touching|3:laptop|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|494|265|2324812.jpg|3:person|holding|5:cell phone|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|413|280|2325881.jpg|0:person|holding|1:banana|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|364|483|2335916.jpg|1:person|looking at|5:bus|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|103|989|2360368.jpg|4:bicycle|beside|2:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|23|1055|2363004.jpg|10:train|beside|8:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|194|1135|2367479.jpg|5:person|beside|3:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|369|1390|2380682.jpg|9:person|looking at|5:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|382|1449|2383257.jpg|0:person|standing on|1:bench|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|377|1495|2385674.jpg|1:person|beside|0:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|377|1495|2385674.jpg|3:person|beside|2:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|377|1495|2385674.jpg|3:person|looking at|2:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|253|1589|2389680.jpg|4:person|beside|0:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|253|1589|2389680.jpg|10:handbag|beside|2:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|478|1804|2400822.jpg|0:person|beside|1:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|152|1986|2409643.jpg|1:person|carrying|4:handbag|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|60|2159|498242.jpg|0:person|looking at|9:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|60|2159|498242.jpg|1:person|beside|0:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|60|2159|498242.jpg|8:person|beside|5:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|60|2159|498242.jpg|9:person|looking at|0:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|lost|385|12|1159501.jpg|0:person|looking at|3:laptop|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|385|12|1159501.jpg|1:person|looking at|3:laptop|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|321|49|1592294.jpg|1:person|riding|14:bicycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|312|52|1592452.jpg|2:person|talking to|1:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|447|104|2316313.jpg|1:person|in|3:car|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|461|107|2316321.jpg|0:person|wearing|6:skis|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|354|111|2316413.jpg|1:person|holding|3:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|413|280|2325881.jpg|0:person|eating|1:banana|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|331|284|2326073.jpg|1:person|in|2:airplane|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|427|361|2329834.jpg|0:person|looking at|14:laptop|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|472|404|2332502.jpg|2:person|in|14:boat|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|21|411|2332726.jpg|3:person|flying over|5:kite|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|364|483|2335916.jpg|4:person|carrying|7:handbag|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|457|587|2341770.jpg|1:person|in|3:bus|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|262|621|2343341.jpg|0:person|throwing|4:sports ball|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|454|629|2343942.jpg|3:person|sitting on|18:chair|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|396|630|2343959.jpg|9:person|wearing|14:tie|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|396|630|2343959.jpg|10:person|wearing|12:tie|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|95|649|2344605.jpg|0:person|sitting on|9:chair|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|362|651|2344819.jpg|0:person|wearing|1:tie|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|94|664|2345357.jpg|0:person|in|10:train|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|94|664|2345357.jpg|1:person|in|10:train|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|395|758|2350121.jpg|0:person|riding|3:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|395|758|2350121.jpg|1:person|riding|5:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|72|841|2353618.jpg|1:person|wearing|2:skis|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|72|841|2353618.jpg|2:skis|on|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|87|852|2354099.jpg|11:person|on|34:skateboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|106|868|2354820.jpg|0:person|riding|1:skateboard|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|254|896|2356062.jpg|7:person|holding|18:teddy bear|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|166|955|2358756.jpg|0:person|holding|1:frisbee|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|103|989|2360368.jpg|2:person|beside|9:motorcycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|422|1007|2361180.jpg|4:person|talking to|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|456|1089|2365077.jpg|8:person|carrying|16:handbag|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|52|1139|2367625.jpg|0:person|holding|1:spoon|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|281|1203|2371154.jpg|1:person|on|4:snowboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|315|1206|2371236.jpg|5:person|carrying|16:handbag|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|415|1211|2371415.jpg|0:person|holding|1:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|61|1219|2371806.jpg|0:person|wearing|1:baseball glove|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|366|1251|2373084.jpg|3:person|carrying|8:surfboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|127|1293|2375622.jpg|0:person|holding|4:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|406|1324|2377760.jpg|0:person|beside|2:suitcase|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|233|1337|2378360.jpg|0:person|riding|1:surfboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|175|1343|2378563.jpg|0:person|beside|4:motorcycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|175|1343|2378563.jpg|4:motorcycle|beside|0:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|302|1396|2381002.jpg|2:person|riding|5:bicycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|302|1396|2381002.jpg|2:person|carrying|14:backpack|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|63|1445|2383111.jpg|0:person|riding|6:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|63|1445|2383111.jpg|3:person|riding|4:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|16|1466|2384291.jpg|0:person|beside|1:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|16|1466|2384291.jpg|1:person|beside|0:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|75|1505|2386156.jpg|0:person|in|2:car|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|51|1507|2386227.jpg|0:person|beside|1:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|138|1529|2387080.jpg|0:person|sitting on|5:chair|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|465|1540|2387468.jpg|0:person|beside|4:train|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|465|1540|2387468.jpg|2:person|beside|4:train|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|253|1589|2389680.jpg|2:person|sitting on|8:bench|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|253|1589|2389680.jpg|2:person|holding|11:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|243|1591|2389803.jpg|0:person|on|9:boat|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|64|1596|2390113.jpg|0:person|riding|1:elephant|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|172|1608|2390659.jpg|8:person|holding|24:tennis racket|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|53|1627|2391314.jpg|0:person|wearing|1:skis|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|153|1695|2394762.jpg|6:person|catching|12:sports ball|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|484|1699|2394864.jpg|0:person|leaning on|5:dining table|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|122|1729|2396723.jpg|0:person|holding|3:wine glass|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|122|1729|2396723.jpg|1:cat|lying on|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|381|1745|2397343.jpg|0:person|beside|1:dog|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|381|1745|2397343.jpg|2:potted plant|in front of|0:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|399|1835|2402046.jpg|11:person|standing on|13:boat|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|183|1866|2403494.jpg|11:person|wearing|19:skis|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|367|1950|2408290.jpg|0:person|on|1:motorcycle|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|328|2111|2416290.jpg|2:person|cooking|12:pizza|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|228|2144|285721.jpg|0:person|talking to|2:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|60|2159|498242.jpg|9:person|holding|10:umbrella|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|490|2161|498294.jpg|2:person|wearing|7:baseball glove|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|

### C_fasterrcnn_thing_plus_stuff

恢复14条，丢失22条，命中净变化-8条。

|变化|样本序号|数据集索引|图片|GT人/端点|谓词|GT对象|A组阶段|比较组阶段|机制|
|---|---:|---:|---|---|---|---|---|---|---|
|recovered|29|81|2315729.jpg|2:person|slicing|15:cake|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|210|105|2316316.jpg|6:person|sitting on|17:motorcycle|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|494|265|2324812.jpg|3:person|holding|5:cell phone|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|6|295|2326503.jpg|0:person|on|1:surfboard|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|449|784|2351059.jpg|2:person|looking at|1:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|166|955|2358756.jpg|0:person|throwing|1:frisbee|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|201|970|2359437.jpg|0:person|picking|1:pizza|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|158|975|2359797.jpg|3:person|carrying|14:backpack|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|103|989|2360368.jpg|4:bicycle|beside|2:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|135|1163|2368707.jpg|3:person|throwing|4:frisbee|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|125|1673|2393510.jpg|0:person|playing with|2:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|421|1772|2398484.jpg|2:person|wearing|4:baseball glove|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|478|1804|2400822.jpg|0:person|beside|1:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|287|2058|2413475.jpg|0:person|catching|1:frisbee|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|lost|370|56|1592537.jpg|0:person|riding|1:boat|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|447|104|2316313.jpg|1:person|in|3:car|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|354|111|2316413.jpg|1:person|holding|3:cell phone|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|327|574|2340907.jpg|1:person|looking at|2:person|hit50|rank_below50|correct_predicate_below_top50|
|lost|106|868|2354820.jpg|0:person|riding|1:skateboard|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|166|955|2358756.jpg|0:person|holding|1:frisbee|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|158|975|2359797.jpg|10:person|holding|19:umbrella|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|123|1099|2365844.jpg|0:person|beside|8:person|hit50|rank_below50|correct_predicate_below_top50|
|lost|123|1099|2365844.jpg|9:person|beside|12:person|hit50|rank_below50|correct_predicate_below_top50|
|lost|281|1203|2371154.jpg|2:person|wearing|7:snowboard|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|285|1218|2371757.jpg|0:person|driving|6:bus|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|16|1466|2384291.jpg|0:person|beside|1:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|16|1466|2384291.jpg|1:person|beside|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|465|1540|2387468.jpg|0:person|beside|4:train|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|465|1540|2387468.jpg|2:person|beside|4:train|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|172|1608|2390659.jpg|8:person|holding|24:tennis racket|hit50|rank_below50|correct_predicate_below_top50|
|lost|389|1609|2390707.jpg|8:person|looking at|6:person|hit50|rank_below50|correct_predicate_below_top50|
|lost|125|1673|2393510.jpg|2:person|looking at|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|484|1699|2394864.jpg|4:umbrella|over|0:person|hit50|rank_below50|correct_predicate_below_top50|
|lost|381|1745|2397343.jpg|2:potted plant|in front of|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|428|1752|2397624.jpg|0:person|riding|1:skateboard|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|287|2058|2413475.jpg|0:person|holding|1:frisbee|hit50|wrong_predicate|relation_model_selected_wrong_predicate|

### D_mask2former_thing_plus_stuff

恢复20条，丢失77条，命中净变化-57条。

|变化|样本序号|数据集索引|图片|GT人/端点|谓词|GT对象|A组阶段|比较组阶段|机制|
|---|---:|---:|---|---|---|---|---|---|---|
|recovered|385|12|1159501.jpg|0:person|touching|3:laptop|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|494|265|2324812.jpg|3:person|carrying|4:handbag|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|494|265|2324812.jpg|3:person|holding|5:cell phone|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|494|265|2324812.jpg|5:cell phone|touching|3:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|413|280|2325881.jpg|0:person|holding|1:banana|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|6|295|2326503.jpg|0:person|on|1:surfboard|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|197|368|2330400.jpg|1:person|holding|2:skis|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|364|483|2335916.jpg|1:person|looking at|5:bus|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|396|630|2343959.jpg|9:person|looking at|8:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|449|784|2351059.jpg|2:person|looking at|1:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|103|989|2360368.jpg|4:bicycle|beside|2:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|194|1135|2367479.jpg|5:person|beside|3:person|rank_below50|hit50|thing_pair_or_relation_ranking_change|
|recovered|377|1495|2385674.jpg|1:person|beside|0:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|377|1495|2385674.jpg|3:person|beside|2:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|377|1495|2385674.jpg|3:person|looking at|2:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|125|1673|2393510.jpg|0:person|playing with|2:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|421|1772|2398484.jpg|2:person|wearing|4:baseball glove|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|478|1804|2400822.jpg|0:person|beside|1:person|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|152|1986|2409643.jpg|1:person|carrying|4:handbag|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|recovered|287|2058|2413475.jpg|0:person|catching|1:frisbee|wrong_predicate|hit50|thing_pair_or_relation_ranking_change|
|lost|385|12|1159501.jpg|0:person|looking at|3:laptop|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|385|12|1159501.jpg|1:person|looking at|3:laptop|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|321|49|1592294.jpg|1:person|riding|14:bicycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|312|52|1592452.jpg|2:person|talking to|1:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|447|104|2316313.jpg|1:person|in|3:car|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|461|107|2316321.jpg|0:person|wearing|6:skis|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|354|111|2316413.jpg|1:person|holding|3:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|413|280|2325881.jpg|0:person|eating|1:banana|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|331|284|2326073.jpg|1:person|in|2:airplane|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|427|361|2329834.jpg|0:person|looking at|14:laptop|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|197|368|2330400.jpg|1:person|wearing|2:skis|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|472|404|2332502.jpg|2:person|in|14:boat|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|21|411|2332726.jpg|3:person|flying over|5:kite|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|364|483|2335916.jpg|4:person|carrying|7:handbag|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|327|574|2340907.jpg|1:person|looking at|2:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|457|587|2341770.jpg|1:person|in|3:bus|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|262|621|2343341.jpg|0:person|throwing|4:sports ball|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|454|629|2343942.jpg|3:person|sitting on|18:chair|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|396|630|2343959.jpg|9:person|wearing|14:tie|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|396|630|2343959.jpg|10:person|wearing|12:tie|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|95|649|2344605.jpg|0:person|sitting on|9:chair|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|362|651|2344819.jpg|0:person|wearing|1:tie|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|94|664|2345357.jpg|0:person|in|10:train|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|94|664|2345357.jpg|1:person|in|10:train|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|395|758|2350121.jpg|0:person|riding|3:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|395|758|2350121.jpg|1:person|riding|5:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|72|841|2353618.jpg|1:person|wearing|2:skis|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|87|852|2354099.jpg|11:person|on|34:skateboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|106|868|2354820.jpg|0:person|riding|1:skateboard|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|254|896|2356062.jpg|7:person|holding|18:teddy bear|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|166|955|2358756.jpg|0:person|holding|1:frisbee|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|158|975|2359797.jpg|10:person|holding|19:umbrella|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|103|989|2360368.jpg|2:person|beside|9:motorcycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|456|1089|2365077.jpg|8:person|carrying|16:handbag|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|123|1099|2365844.jpg|9:person|beside|12:person|hit50|rank_below50|correct_predicate_below_top50|
|lost|52|1139|2367625.jpg|0:person|holding|1:spoon|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|281|1203|2371154.jpg|1:person|on|4:snowboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|281|1203|2371154.jpg|2:person|wearing|7:snowboard|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|315|1206|2371236.jpg|5:person|carrying|16:handbag|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|415|1211|2371415.jpg|0:person|holding|1:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|285|1218|2371757.jpg|0:person|driving|6:bus|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|366|1251|2373084.jpg|3:person|carrying|8:surfboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|127|1293|2375622.jpg|0:person|holding|4:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|233|1337|2378360.jpg|0:person|riding|1:surfboard|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|175|1343|2378563.jpg|0:person|beside|4:motorcycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|175|1343|2378563.jpg|4:motorcycle|beside|0:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|302|1396|2381002.jpg|2:person|riding|5:bicycle|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|302|1396|2381002.jpg|2:person|carrying|14:backpack|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|63|1445|2383111.jpg|0:person|riding|6:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|63|1445|2383111.jpg|3:person|riding|4:horse|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|16|1466|2384291.jpg|0:person|beside|1:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|16|1466|2384291.jpg|1:person|beside|0:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|75|1505|2386156.jpg|0:person|in|2:car|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|51|1507|2386227.jpg|0:person|beside|1:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|138|1529|2387080.jpg|0:person|sitting on|5:chair|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|465|1540|2387468.jpg|0:person|beside|4:train|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|465|1540|2387468.jpg|2:person|beside|4:train|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|465|1540|2387468.jpg|3:person|beside|4:train|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|253|1589|2389680.jpg|2:person|sitting on|8:bench|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|253|1589|2389680.jpg|2:person|holding|11:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|243|1591|2389803.jpg|0:person|on|9:boat|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|64|1596|2390113.jpg|0:person|riding|1:elephant|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|172|1608|2390659.jpg|8:person|holding|24:tennis racket|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|53|1627|2391314.jpg|0:person|wearing|1:skis|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|125|1673|2393510.jpg|2:person|looking at|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|153|1695|2394762.jpg|6:person|catching|12:sports ball|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|122|1729|2396723.jpg|0:person|holding|3:wine glass|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|122|1729|2396723.jpg|1:cat|lying on|0:person|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|381|1745|2397343.jpg|0:person|beside|1:dog|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|381|1745|2397343.jpg|2:potted plant|in front of|0:person|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|399|1835|2402046.jpg|11:person|standing on|13:boat|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|183|1866|2403494.jpg|11:person|wearing|19:skis|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|287|2058|2413475.jpg|0:person|holding|1:frisbee|hit50|wrong_predicate|relation_model_selected_wrong_predicate|
|lost|328|2111|2416290.jpg|2:person|cooking|12:pizza|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|228|2144|285721.jpg|0:person|talking to|2:cell phone|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|60|2159|498242.jpg|9:person|holding|10:umbrella|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
|lost|490|2161|498294.jpg|2:person|wearing|7:baseball glove|hit50|endpoint_missing_or_wrong_class|Mask2Former_thing_endpoint_not_matched_to_PSG_GT|
