"""Create a beginner-readable report copy, preserving the original verbatim."""
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'reproduction/reports'
source=REPORT/'完整实验报告.md'
destination=REPORT/'完整实验报告_附术语解释版.md'
original_bytes=source.read_bytes()
original=original_bytes.decode('utf-8')
appendix=(ROOT/'reproduction/configs/report_glossary.md').read_text(encoding='utf-8')
predicates=json.loads((ROOT/'data/PSG/packed/psg/test/meta.json').read_text(encoding='utf-8'))['predicates']
translations=[
    '在……上方／越过（依语境）','在……前面','在……旁边','在……上面（常含支撑/接触）','在……里面',
    '附着或连接到……','从……悬挂下来','在……背面／背上','从……掉落','沿……向下',
    '画在……上','在……上行走','在……上奔跑','穿过／横穿……','站在……上','躺在……上','坐在……上',
    '飞过……上方','跳过……','从……跳下／跳出','穿戴着……','拿着／握着……','携带／搬运……',
    '看着……','引导……','亲吻……','吃……','喝……','喂养……','咬……','接住／抓住……','采摘／挑取……',
    '与……玩耍／摆弄……','追逐……','攀爬……','清洁……','玩／演奏……（依对象）','触碰……','推……','拉……',
    '打开……','烹饪……','对……说话','投掷……','切……成片','驾驶……','骑着……','停放在……上',
    '在……上行驶','即将撞到／击中……','踢……','挥动／荡动……（依语境）','进入……','离开／从……出来',
    '包围／围住……','倚靠在……上']
assert len(predicates)==len(translations)==56
predicate_table='| 正式词表编号 | 英文谓词 | 中文解释 |\n|---|---|---|\n'
predicate_table+=''.join(f'| {j} | {en} | {zh} |\n' for j,(en,zh) in enumerate(zip(predicates,translations)))
assert appendix.count('<!-- PREDICATE_TRANSLATIONS -->')==1
appendix=appendix.replace('<!-- PREDICATE_TRANSLATIONS -->',predicate_table.rstrip())
(REPORT/'术语解释附录.md').write_text(appendix,encoding='utf-8')
sections=re.findall(r'^## ([A-L]\. .+)$',appendix,re.M)
def anchor(title):
    return re.sub(r'[^\w\- ]','',title.lower()).replace(' ','-')
navigation='\n\n## 本副本的术语附录导航\n\n'
navigation+='本副本完整保留原报告正文与实验结果，仅在前面添加阅读导航、末尾增加术语解释。原报告不修改。建议先读附录A的例子，再按遇到的词查表；可用Ctrl+F搜索GT、logit、mR、query等。\n\n'
navigation+='\n'.join(f'- [{title}](#{anchor(title)})' for title in sections)
navigation+='\n\n附录K包含正式56词表及实验额外短语的中文解释；附录L将正文中几句关键结论改写为白话。\n\n---\n\n'
first,rest=original.split('\n',1)
new=first+'（附术语解释版）'+navigation+rest+'\n\n---\n\n'+appendix
destination.write_text(new,encoding='utf-8')
# The source body must appear exactly after navigation, before the appendix.
assert navigation+rest+'\n\n---\n\n'+appendix in new
assert source.read_bytes()==original_bytes
assert len(sections)==12
refs=re.findall(r'\]\(([^)]+)\)',new)
broken=[]
for ref in refs:
    if ref.startswith(('http:','https:','#','data:')): continue
    if not (REPORT/ref.split('#')[0]).exists(): broken.append(ref)
assert not broken,broken
print(json.dumps({'copy':str(destination),'source_sha256_unchanged':hashlib.sha256(original_bytes).hexdigest(),
    'appendix_sections':len(sections),'predicate_translations':len(predicates),'local_links_checked':len(refs),
    'original_preserved':True},ensure_ascii=False,indent=2))

