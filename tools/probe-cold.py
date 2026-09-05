import importlib.util,json
from pathlib import Path
sp=importlib.util.spec_from_file_location('qa',str(Path(__file__).with_name('device-qa.py')));q=importlib.util.module_from_spec(sp);sp.loader.exec_module(q)
l=q.levels[8];wrong=json.loads((q.ROOT/'artifacts/wrong-level-09.json').read_text());c=min(108,536/l['w'],372/l['h']);bx=(720-l['w']*c)/2;by=357+(372-l['h']*c)/2
for i,p in enumerate(l['pieces']):
 s=wrong[p['id']];q.tap(108+i%4*168,880+i//4*126)
 for r in range(s['r']):q.tap(130,1110)
 q.tap(bx+(s['x']+.5)*c,by+(s['y']+.5)*c)
q.shot('cold-wrong-packed');q.tap(360,1200);q.shot('cold-rule-failure');assert '9' not in q.state()['album'];assert len(q.state()['board'])==len(l['pieces'])
q.tap(360,850);q.shot('cold-invalid-highlight');q.key(4);q.shot('android-back-pause');q.tap(215,890);q.shot('reset-confirm');q.tap(360,820);assert q.state()['board']=={}
print('PASS fully packed wrong cold rule, no unlock, editable failure, Android back pause, reset confirmation',flush=True)
