"""Temporary campaign fixtures are restricted to Bento's SQLite save and restored in finally."""
import importlib.util,time,json,sqlite3,subprocess,copy,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1];sp=importlib.util.spec_from_file_location('qa',root/'tools/device-qa.py');q=importlib.util.module_from_spec(sp);sp.loader.exec_module(q);q.OUT=root/'artifacts/v3/device';q.OUT.mkdir(exist_ok=True)
basepath=q.OUT/'user-save-before.sqlite';jsonpath=q.OUT/'user-save-before.json'
def guard():assert any(q.PKG in l for l in q.adb('shell','dumpsys','window').decode().splitlines() if 'mCurrentFocus=' in l),'Foreground changed: stopping device input'
def shot(n):time.sleep(.7);guard();q.shot(n)
def tap(x,y):guard();q.tap(x,y)
def launch():q.adb('shell','am','start','-n',q.PKG+'/com.cocos.game.AppActivity');time.sleep(1.5);guard()
def put(save):
 q.adb('shell','am','force-stop',q.PKG);local=q.OUT/'fixture.sqlite';local.write_bytes(basepath.read_bytes())
 with sqlite3.connect(local) as c:c.execute("update data set value=? where key='bento.v1'",(json.dumps(save),));c.commit()
 q.adb('push',local,'/data/local/tmp/bento-campaign-qa.sqlite');q.adb('shell','run-as',q.PKG,'cp','/data/local/tmp/bento-campaign-qa.sqlite','databases/jsb.sqlite');launch()
def fixture(n):
 s=copy.deepcopy(baseline);s.update(current=n,board={},album={str(l['id']):l['solution'] for l in q.levels[:n-1]},unlocked=n,learned=[],seen=True);put(s);tap(360,863);time.sleep(.5)
 if n in [25,37,49]:shot(f'intro-{n}');tap(360,850)
 shot(f'empty-{n}')
def enter(n,board):
 l=q.levels[n-1];c=min(108,536/l['w'],372/l['h']);bx=(720-l['w']*c)/2;by=357+(372-l['h']*c)/2
 for i,p in enumerate(l['pieces']):
  pos=board[p['id']];tap(108+i%4*168,880+i//4*126)
  for r in range(pos['r']):tap(130,1110)
  tap(bx+(pos['x']+.5)*c,by+(pos['y']+.5)*c)
  observed=q.state()
  for _ in range(12):
   if observed['board'].get(p['id'])==pos:break
   time.sleep(.2);observed=q.state()
  if observed['board'].get(p['id'])!=pos:
   (q.OUT/f'mismatch-{n}.json').write_text(json.dumps({'piece':p,'expected':pos,'observed':observed},ensure_ascii=False,indent=2));shot(f'mismatch-{n}');raise AssertionError('Piece mismatch '+str(n)+' '+p['id'])
 state=q.state();assert state['current']==n and state['board']==board, 'Entered board mismatch '+str(n)
def reset():q.key(4);tap(215,890);tap(360,820)
if not basepath.exists():
 guard();basepath.write_bytes(q.adb('exec-out','run-as',q.PKG,'cat','databases/jsb.sqlite'));jsonpath.write_text(json.dumps(q.state(),ensure_ascii=False,indent=2))
baseline=json.loads(jsonpath.read_text());results=json.loads((q.OUT/'campaign-results.json').read_text()) if (q.OUT/'campaign-results.json').exists() else []
try:
 # Real upgrade state: open 25 through the paged map, without injecting progress.
 if len(baseline['album'])==24 and len(sys.argv)==1:
  put(baseline);tap(210,970);shot('map-migration-25');tap(150,416);shot('migration-intro-25');assert q.state()['current']==25 and len(q.state()['album'])==24;results.append('24-to-25 migration')
 probes=json.loads((root/'artifacts/v3/campaign-analysis.json').read_text())['probes']
 for n in (list(map(int,sys.argv[1:])) if len(sys.argv)>1 else [25,37,49,61,78,90,102,107,108]):
  fixture(n)
  if n in [25,49]:
   wrong=next(p['witness'] for p in probes if p['id']==n);assert wrong;enter(n,wrong);tap(360,1200);shot(f'wrong-rule-{n}');assert str(n) not in q.state()['album'];tap(360,850);reset();results.append(f'{n} wrong complete packing rejected')
  if n==37:
   l=q.levels[n-1];i=next(i for i,p in enumerate(l['pieces']) if p.get('fixed'));p=l['pieces'][i];pos=l['solution'][p['id']];tap(108+i%4*168,880+i//4*126);tap(130,1110);shot('fixed-rotation-feedback');c=min(108,536/l['w'],372/l['h']);bx=(720-l['w']*c)/2;by=357+(372-l['h']*c)/2;tap(bx+(pos['x']+.5)*c,by+(pos['y']+.5)*c)
   assert q.state()['board'][p['id']]['r']==0;reset();results.append('37 fixed orientation rejected rotation')
  enter(n,q.levels[n-1]['solution']);shot(f'packed-{n}');tap(360,1200);shot(f'win-{n}');assert str(n) in q.state()['album'];results.append(f'{n} solution entered and win saved');print('PASS level',n,flush=True);(q.OUT/'campaign-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
  if n==102:tap(360,908);tap(645,82);shot('combined-help')
  if n==108:tap(360,808);shot('album-108');q.key(4);tap(210,970);shot('map-108')
 (q.OUT/'campaign-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
finally:
 put(baseline);q.adb('shell','rm','-f','/data/local/tmp/bento-campaign-qa.sqlite');shot('user-progress-restored');assert q.state()==baseline;print('Restored original user save exactly.',flush=True)
