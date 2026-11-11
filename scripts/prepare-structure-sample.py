"""Prepare the selected project decomposition from previously extracted PDF text.

Usage: python scripts/prepare-structure-sample.py --cache-dir <extracted-json-dir>
Input: A_pages.json, B_pages.json, C_pages.json, real_records.json.
This is a sample preparation script, not a production AI import pipeline.
"""
import argparse, json, re
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--cache-dir',type=Path,required=True)
args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1]
cache=args.cache_dir
pages={k:json.loads((cache/(k+'_pages.json')).read_text(encoding='utf-8')) for k in ['A','B','C']}
legacy=json.loads((cache/'real_records.json').read_text(encoding='utf-8'))
materials=[];objects=[];groups=[];links=[]
sources={'A':{'name':'A-设计说明-TEKUMA联合体.pdf'},'B':{'name':'B-产业策划及资源导入清单-TEKUMA联合体.pdf'},'JZ':{'name':'方案文册（1正19副）.pdf'}}
layers=[{'id':'brand','name':'品牌认知','subtitle':'价值、人群与地方表达'},{'id':'organization','name':'组织逻辑','subtitle':'核心叙事与行动计划'},{'id':'space','name':'空间项目','subtitle':'空间单元与具体内容'}]
def text(doc,n):return pages['C' if doc=='JZ' else doc][n-1]['text']
def group(project,id,layer,name,open=False):
 groups.append(dict(id=id,project=project,layer=layer,name=name,open=open));return id
def obj(project,id,g,title,description='',parent=None):
 objects.append(dict(id=id,project=project,group=g,title=title,description=description,parent=parent));return id
def mat(oid,title,body,doc,n,kind='文字',basis='原文摘录',locator='',quote=None):
 o=next(o for o in objects if o['id']==oid)
 mid=oid+'-m'+str(sum(m['object']==oid for m in materials)+1)
 materials.append(dict(id=mid,object=oid,project=o['project'],title=title,body=body.strip(),kind=kind,basis=basis,refs=[dict(doc=doc,page=n,locator=locator,quote=(quote if quote is not None else body).strip())]));return mid
def link(a,b,contribution,basis='据原文归纳'):
 links.append(dict(source=a,target=b,contribution=contribution,basis=basis))

# Dongguan: retain a whole-project hierarchy, including all twelve selected products.
for id,layer,name,op in [('dg-context','brand','定位依据与目标人群',False),('dg-theme','brand','品牌母题',True),('dg-expression','brand','语言与视觉表达',False),('dg-narratives','organization','核心叙事',True),('dg-actions','organization','行动计划',False),('dg-units','space','空间单元',False),('dg-projects','space','空间产品与子项目',True)]:group('dg',id,layer,name,op)
obj('dg','DG-V01','dg-context','潮玩产业与地方价值')
mat('DG-V01','产业定位依据',text('B',8).split('东莞为什么要做潮玩文旅？/')[1].split('东莞潮玩产业微生态')[0].split('\n',1)[1], 'B',8,locator='东莞为什么要做潮玩文旅')
mat('DG-V01','产业与文旅的双飞轮','利用全城全要素生产要素的天然优势，构建“产业-文旅”双飞轮，用文旅链拉动产业链的整体完型与延展。','B',10,locator='如何定义“中国潮玩之都”')
obj('dg','DG-U01','dg-context','消费者、品牌与创作者')
mat('DG-U01','服务对象归纳','消费者、品牌、设计师与创作者；具体产品中包括参观研学人群及定制用户。','B',4,basis='原文归纳',locator='前言',quote='它既是城市文旅目的地，也是产业创新平台；既是消费者的沉浸体验场域，也是品牌、设计师与创作者的生长土壤。')
obj('dg','DG-M01','dg-theme','东莞潮玩宇宙','从制造资源到产业创新与文旅体验')
mat('DG-M01','母题原称','东莞潮玩宇宙','B',4,locator='前言末段')
mat('DG-M01','母题释义','把制造资源、工业遗址与古村落转为产业创新与文旅体验，形成东莞的地方辨识。母题归类与释义为本次整理。','B',4,basis='原文归纳',locator='前言核心逻辑',quote='将东莞四十年制造业积累的产业资产、不可复制的工业遗址空间与百年历史的古村落以及产业链各环节的人才与资源系统性地转化为“具有全球竞争力的文旅目的地叙事资产。”')
obj('dg','DG-E01','dg-expression','地方表达与产品品牌')
mat('DG-E01','地方语言表达','中国潮玩之都，世界潮玩坐标。','B',4,locator='前言末段')
mat('DG-E01','十二个空间产品的品牌表达','图面展示十二个空间产品的名称、图形与“中国潮玩之都”的关联表达。本条是图件用途归纳。','B',12,kind='图件',basis='图件归纳',locator='六大产业板块与十二个空间产品体系')
obj('dg','DG-N01','dg-narratives','看见制造，参与创造','本次从原文归纳的核心叙事')
mat('DG-N01','核心叙事','消费者与研学者通过观看生产、参与定制，理解东莞既有制造能力，也能提供智能玩具创新与体验。','B',30,basis='研究归纳',locator='2-2、2-3 行；结合第34页',quote='全链路透明生产线；玻璃幕墙走廊参观动线；消费者自助设计工作站；“看着自己的玩具被做出来”全程直播服务。')
mat('DG-N01','参与方式与预期认识','参与方式：参观制造、学习技术、选择款式与定制。预期认识：生产能力可被体验，并与设计创造连接。该判断未由运营效果验证。','B',34,basis='研究归纳',locator='打开前台及价值闭环',quote='把生产线、定制、直播和住宿转化为消费体验。')
obj('dg','DG-N02','dg-narratives','以首发与消费感知潮玩之都','本次从都市盲盒策划归纳')
mat('DG-N02','核心叙事','游客、消费者与行业参与者通过城市展示、新品首发和品牌活动，理解东莞的潮玩产业与文化形象。','B',32,basis='研究归纳',locator='核心定位、做实首发',quote='承担城市展示、活动首发、品牌消费、产业服务和全片区客流分发五重功能。')
for id,title,page in [('DG-A01','打开前台',34),('DG-A02','做实首发',32)]:
 obj('dg',id,'dg-actions',title)
 t=text('B',page);part=t.split('02 '+title+'\n')[1].split('03 ')[0].strip().replace('\n','')
 mat(id,'行动任务',part,'B',page,kind='任务',locator='三阶段落地路径第02项')
units=[('DG-S01','东莞站门户节点',19),('DG-S02','南社古村建筑群节点',19),('DG-S03','生态园—超朗村节点',19),('DG-S04','潮玩古村节点',20),('DG-S05','滨江古采石场节点',20)]
for id,name,p in units:
 obj('dg',id,'dg-units',name)
 mat(id,'节点范围记录',name+'。本条仅定位到方案节点，具体用地与建筑边界未在本次拆解中核定。','B',p,basis='原文归纳',locator='五个城市核心节点',quote=name)
for i,r in enumerate(legacy[:12],1):
 oid=f'DG-PROD-{i:02}';obj('dg',oid,'dg-projects',r['name'],r['place'])
 t=text('B',int(r['page']));n=int(r['page'])
 core=t.split('核心定位\n')[1].split('三阶段落地路径')[0].strip().replace('\n','').rstrip('。')+'。'
 mat(oid,'产品定位',core,'B',n,locator='核心定位')
 functions=t.split('功能构成\n')[1].split('落地原则')[0].strip().replace('\n','')
 mat(oid,'功能构成',functions,'B',n,kind='任务',locator='功能构成')
 for title,body in [('建设量',r.get('area','')),('投资估算',r.get('investment',''))]:
  if body:mat(oid,title,body+'\n沿用该页口径；估算与建议不视为核定结果，不与其他页面自动合计。','B',n,kind='指标',basis='原文摘录＋口径提示',locator=title,quote=body)
 stages=t.split('三阶段落地路径\n')[1].split('建设量')[0]
 for num,title,body in re.findall(r'(0[123]) ([^\n]+)\n(.*?)(?=0[123] |\Z)',stages,re.S):mat(oid,f'阶段{num} · {title}',body.strip().replace('\n',''),'B',n,kind='任务',locator='三阶段落地路径第'+num+'项')
 if i==2:
  for pid,title,body,loc in [('DG-P01','透明超级工厂','任务：AI毛绒玩具全链路透明生产线、玻璃幕墙走廊、情感AI模组植入演示、研学专项课程。','2-2 行'),('DG-P02','潮玩柔性生产与私人定制中心','任务：基础、深度与品牌定制，自助设计工作站、柔性生产线、制作过程直播与娃衣工坊。','2-3 行')]:
   obj('dg',pid,'dg-projects',title,'源子项目编号 '+('2-2' if pid=='DG-P01' else '2-3'),parent=oid)
   mat(pid,'项目任务',body,'B',30,kind='任务',basis='原文归纳',locator=loc)
   mat(pid,'规模（子项目表口径）',('8.7万㎡' if pid=='DG-P01' else '13.5万㎡')+'；此处保留子项目表口径，不与产品落地页自动汇总。','B',30,kind='指标',basis='原文摘录＋口径提示',locator=loc,quote='8.7万㎡' if pid=='DG-P01' else '13.5万㎡')
obj('dg','DG-S00','dg-units','片区总体空间','整个片区的总平面表达')
for r in [r for r in legacy if r['doc']=='A']:
 mat('DG-PROD-01' if r['page']=='49' else 'DG-S00',r['name'],r['text'],r['doc'],int(r['page']),kind='图件',basis='图件归纳',locator='图面及标注',quote=r['quote'])
for a,b,d in [('DG-M01','DG-N01','把制造价值转为观看与参与体验'),('DG-N01','DG-A01','为观看、定制提供条件'),('DG-A01','DG-P01','透明工厂让生产可见'),('DG-A01','DG-P02','定制中心让用户参与创造'),('DG-N02','DG-A02','首发活动形成公众感知'),('DG-A02','DG-PROD-01','都市盲盒承载首发与品牌活动')]:link(a,b,d)

# Jingzhang: whole-project categories, selected examples within each category.
for id,layer,name,op in [('jz-context','brand','定位依据与目标人群',False),('jz-theme','brand','品牌母题',True),('jz-expression','brand','宣言与体验原则',False),('jz-narratives','organization','核心叙事',True),('jz-actions','organization','行动计划',False),('jz-units','space','空间单元',False),('jz-projects','space','具体项目',True),('jz-facilities','space','设施配置建议',False)]:group('jz',id,layer,name,op)
obj('jz','JZ-V01','jz-context','资源优势与连接问题')
mat('JZ-V01','定位依据','高校、科研院所、企业之间仍存在物理边界和组织边界；科研成果出校门后，缺少快速概念验证和工程验证空间。','JZ',76,locator='总体城市设计：校内外都是创新力')
obj('jz','JZ-U01','jz-context','创新人群与全龄使用者')
mat('JZ-U01','服务人群归纳','科研人员、师生、创业团队及周边全龄使用者，分别对应协作、创新与持续学习情境。','JZ',104,basis='研究归纳',locator='全龄段才是培育力；结合第9、17、325页',quote='不同年龄、不同职业、不同领域的人群共同生活，把科学家公开课、AI通识教育、职业再成长、青少年科学教育和城市共创嵌入城市日常。')
obj('jz','JZ-M01','jz-theme','海淀·AI 原生城市','组织科研、产业、人才与城市资源')
mat('JZ-M01','母题原称','海淀·AI 原生城市','JZ',4,locator='项目卷首')
mat('JZ-M01','母题释义','通过组织科研、产业、人才、资本和城市资源，形成面向AI时代的新型城市生产关系。“品牌母题”的归类为本次整理。','JZ',4,basis='原文归纳',locator='项目卷首',quote='把海淀已有的科研、产业、人才、资本和城市资源，组织成一种面向AI时代的新型城市生产关系。')
mat('JZ-M01','白皮书的五项主张','真实场景、可信关系、协同共治、智能互联、全龄进化。','JZ',5,locator='AI原生城市白皮书')
for id,title,n,descpage in [('JZ-E01','校内外都是创新力',8,9),('JZ-E02','全龄段才是培育力',16,17)]:
 obj('jz',id,'jz-expression',title)
 mat(id,'宣言原称',title,'JZ',n,locator='海淀宣言')
 body='通过开放实验室、共享科研平台、联合创新中心和“高校创新后街”，让科研成果进入城市，也让真实城市问题进入校园。' if id=='JZ-E01' else '建设成长学苑等终身成长设施，把科学家公开课、AI通识教育、职业再成长、青少年科学教育和城市共创嵌入城市日常。'
 mat(id,'体验与服务要求',body,'JZ',descpage,locator='宣言展开')
for id,title,body,n,q in [('JZ-N01','校园与城市共同创新','师生、科研人员与企业通过跨越校园边界的连接、共享与共创，感知创新在校园与城市之间持续发生。',78,'突破边界，让科研成果进入城市，也让真实城市问题进入校园。'),('JZ-N02','全龄人群持续成长','不同年龄与职业的人通过学习、公开课、科创实践和交流，把AI与持续成长纳入城市日常。',104,'把科学家公开课、AI通识教育、职业再成长、青少年科学教育和城市共创嵌入城市日常。')]:
 obj('jz',id,'jz-narratives',title,'本次从原文归纳的核心叙事');mat(id,'核心叙事',body,'JZ',n,basis='研究归纳',locator='总体城市设计对应驱动力',quote=q)
for id,title,body,n,q in [('JZ-A01','建设校城互联高线','通过连续慢行系统跨越道路与空间边界，连接清华东北门、生态空间和产业园区，促进人才与知识流动。',79,'通过连续的立体慢行系统跨越现有道路及空间边界。'),('JZ-A02','校城共创与创新服务平台','组织孵化、实验、成果展示和共享交流，为高校与城市的协作提供服务条件。本行动名称为整理归纳，原文未单列同名行动。',325,'JZ-07：依托北航学科优势打造产业创新与创业平台。'),('JZ-A03','全龄学习与成长服务','配置公共学习、科普、职业再成长和城市共创服务，让不同人群在日常中持续学习。',104,'打造5大全民共享的文体公共设施。')]:
 obj('jz',id,'jz-actions',title);mat(id,'行动任务',body,'JZ',n,kind='任务',basis='研究归纳',locator='驱动力说明或项目清单',quote=q)
mat('JZ-A02','实施与开放条件','具体入口、路径、容量、面积、投资和开放时段需结合校方、资产及专项条件核定；专业园区与首发项目为规划建议。','JZ',431,kind='条件',locator='模式选择与空间落位条件')
for id,name,n,body in [('JZ-S01','清华—八家—众智园沿线',325,'方案线位连接清华东北门、八家郊野公园和众智园，具体边界未在本次拆解中核定。'),('JZ-S02','北航西门与京张公园相关范围',325,'方案位置为北京航空航天大学西门和京张遗址公园内；不替代正式用地及授权文件。'),('JZ-S03','一带三港的空间骨架',137,'“一带”提供连续公共空间与创新网络，“三港”形成差异化产业与城市功能，共同构成AI原生城市的空间骨架。')]:
 obj('jz',id,'jz-units',name);mat(id,'空间范围说明',body,'JZ',n,basis='原文归纳',locator='总体空间结构' if n==137 else '项目位置列',quote=body)
obj('jz','JZ-P01','jz-projects','清华—众智园创新高线','原项目编号 GJ-01')
mat('JZ-P01','项目目标与任务','建立清华与众智园之间的校城慢行连接，串联清华东北门、八家郊野公园和众智园，使高校知识资源、生态空间与产业园区直接连通。','JZ',325,kind='任务',basis='原文归纳',locator='GJ-01 行')
mat('JZ-P01','建设规模与方案时序','连续慢行步道约3000米；原文计划近期（2026–2027）实施。此为方案时序，不代表已经开工。','JZ',325,kind='指标',basis='原文摘录＋状态提示',locator='GJ-01 行',quote='方案约3000米；近期（2026–2027）。')
mat('JZ-P01','实施与运营安排','区政府牵头，清华与众智园产权单位联合；政府投资、平台公司代建；政府建设、多方共管与市场化活动运营。','JZ',325,kind='任务',basis='原文归纳',locator='GJ-01 行')
mat('JZ-P01','高线的空间设计表达','图面将创新高线与共创街区、创新休闲带、创新后街共同表达，包含连续慢行连接示意。','JZ',79,kind='图件',basis='图件归纳',locator='B 一条校城互联高线')
obj('jz','JZ-P02','jz-projects','北航成长学苑','原项目编号 JZ-07；一个项目主记录')
mat('JZ-P02','项目定位','面向AI时代的未来图书馆，为全年龄段提供终身学习与成长服务，并依托北航学科优势提供产业创新与创业平台。','JZ',325,basis='原文归纳',locator='JZ-07 行')
mat('JZ-P02','创新与学习功能','研发办公、科创孵化、公共服务、实验室、图书室、多功能活动厅；图面另标注创业大厅、创客工坊、户外讲堂和路演讲堂。','JZ',300,kind='任务',basis='原文归纳',locator='图面标注；结合第325页',quote='创业大厅、创客工坊、图书馆、户外讲堂、路演讲堂、共享实验室。')
mat('JZ-P02','规模与方案时序','总建筑面积约6万㎡；原文列为中期（2028–2029）。规模和时序均按方案记录，不视为已核定或已实施。','JZ',325,kind='指标',basis='原文摘录＋状态提示',locator='JZ-07 行',quote='总建筑面积约6万㎡；中期（2028–2029）。')
mat('JZ-P02','主体与运营安排','北航、区政府、区教委与街道联合；方案提出校地共建及高校、政府补贴、低收费运营。','JZ',325,kind='任务',basis='原文归纳',locator='JZ-07 行')
mat('JZ-P02','成长学苑空间图件','图面展示知识环廊、图书馆、工坊、共享实验室、产业办公与户外测试等空间。','JZ',300,kind='图件',basis='图件归纳',locator='北航成长学苑图面')
mat('JZ-P02','终身成长的设计表达','在这里，人们可以学习一项技能，科学家也可以发起一个项目，让学习与创造贯穿一生。这是方案的体验设想。','JZ',301,basis='原文归纳',locator='终身成长学院说明',quote='人们可以学习一项技能，科学家也可以发起一个项目，把真实问题带进城市，让学习与创造贯穿一生。')
for r in legacy[12:29]:
 oid='JZ-F'+str(r['id']);obj('jz',oid,'jz-facilities',r['name'],r['place'])
 # Split the facility row into independently reusable requirements and its scale.
 area=r.get('area','按专项测算');mat(oid,'建议规模',area+'\n面积为共享或平台设施的启动建议区间，不含企业专属研发；具体规模按需求、设备和利用率校核。','JZ',391,kind='指标',basis='原文摘录＋口径提示',locator=r['name']+' 行',quote=area)
 body=r['text'].split('关键空间条件：')[-1].split('\n\n')[0]
 mat(oid,'空间条件',body,'JZ',391,kind='条件',locator=r['name']+' 行',quote=r['quote'])
obj('jz','JZ-P03','jz-projects','众智园公共空间网络','现状与方案成组保留')
for n,title in [(170,'现状图与问题'),(171,'方案图与空间策略')]:
 r=next(r for r in legacy if r['doc']=='JZ' and r['page']==str(n));mat('JZ-P03',title,r['text'],'JZ',n,kind='图件',basis='图件归纳',locator='公共空间规划',quote=text('JZ',n).split('Before the public space plan' if n==170 else 'After planning')[0].strip())
for a,b,d in [('JZ-M01','JZ-N01','母题落实为校城共同创新的体验'),('JZ-M01','JZ-N02','母题落实为全龄持续成长'),('JZ-N01','JZ-A01','慢行连接提供交流条件'),('JZ-N01','JZ-A02','共创平台提供能力与服务'),('JZ-N02','JZ-A03','公共学习承接成长体验'),('JZ-A01','JZ-P01','高线承担空间连接任务'),('JZ-A02','JZ-P02','学苑承担孵化、实验与交流；主归属待确认'),('JZ-A03','JZ-P02','学苑也承担终身学习；协同关系待确认')]:link(a,b,d)

projects=[dict(id='dg',name='东莞潮玩文旅',subtitle='制造资源、产业创新与文旅体验',coverage='12个空间产品及部分子项目；品牌、叙事与行动选取样例。非全册拆解。'),dict(id='jz',name='京张 AI 创新带',subtitle='品牌认知、校城协作与空间更新',coverage='品牌与组织逻辑选取样例，含3项空间项目与17项设施配置。非全册拆解。')]
for o in objects:
 o['open']=o['id'] in ['DG-M01','DG-N01','DG-PROD-01','JZ-M01','JZ-N01','JZ-P02']
data=dict(schemaVersion=2,projects=projects,layers=layers,groups=groups,objects=objects,materials=materials,links=links,sources=sources)
ids=[m['id'] for m in materials];oids={o['id'] for o in objects};gids={g['id'] for g in groups}
assert len(ids)==len(set(ids))
assert all(o['group'] in gids and (o['parent'] is None or o['parent'] in oids) for o in objects)
assert all(m['object'] in oids for m in materials)
assert all(l['source'] in oids and l['target'] in oids for l in links)
(ROOT/'data').mkdir(exist_ok=True)
(ROOT/'data'/'content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(objects)} objects, {len(materials)} materials, {len(links)} support links')
