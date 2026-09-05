import importlib.util,time,json,sqlite3,copy
from pathlib import Path
root=Path(__file__).resolve().parents[1];sp=importlib.util.spec_from_file_location('qa',root/'tools/device-qa.py');q=importlib.util.module_from_spec(sp);sp.loader.exec_module(q);q.OUT=root/'artifacts/v3/device';original=json.loads((q.OUT/'user-save-before.json').read_text())
def guard():assert any(q.PKG in l for l in q.adb('shell','dumpsys','window').decode().splitlines() if 'mCurrentFocus=' in l),'Foreground changed'
def tap(x,y):guard();q.tap(x,y)
def shot(n):time.sleep(.8);guard();q.shot(n)
def put(s):
 q.adb('shell','am','force-stop',q.PKG);local=q.OUT/'screen-fixture.sqlite';local.write_bytes((q.OUT/'user-save-before.sqlite').read_bytes())
 with sqlite3.connect(local) as c:c.execute("update data set value=? where key='bento.v1'",(json.dumps(s),));c.commit()
 q.adb('push',local,'/data/local/tmp/bento-screen-qa.sqlite');q.adb('shell','run-as',q.PKG,'cp','/data/local/tmp/bento-screen-qa.sqlite','databases/jsb.sqlite');q.adb('shell','am','start','-n',q.PKG+'/com.cocos.game.AppActivity');time.sleep(4);guard()
def setup(n,board):
 s=copy.deepcopy(original);s.update(current=n,board=board,album={str(l['id']):l['solution'] for l in q.levels[:n-1]},unlocked=n,learned=['rice','cold','edge','target','fixed','center']);put(s);shot('loaded-home-'+str(n));tap(360,863);time.sleep(1)
 for _ in range(15):
  q.state()
  with sqlite3.connect(q.OUT/'save-snapshot.sqlite') as c:raw=c.execute("select value from data where key='bento.v1'").fetchone()[0]
  if raw.startswith('{"version":1'):break
  time.sleep(.2)
 else:raise AssertionError('Start button was not processed')
def expect(board):
 for _ in range(15):
  if q.state()['board']==board:return
  time.sleep(.2)
 raise AssertionError('Unexpected board state')
try:
 setup(37,{});l=q.levels[36];i=next(i for i,p in enumerate(l['pieces']) if p.get('fixed'));p=l['pieces'][i];pos=l['solution'][p['id']];c=min(108,536/l['w'],372/l['h']);bx=(720-l['w']*c)/2;by=357+(372-l['h']*c)/2;w=max(a for a,b in p['shape'])+1;h=max(b for a,b in p['shape'])+1
 guard();q.adb('shell','input','swipe',round((108+i%4*168)*q.scale),round((880+i//4*126)*q.scale+q.offset),round((bx+(pos['x']+w/2)*c)*q.scale),round((by+(pos['y']+h/2)*c+70)*q.scale+q.offset),700);expect({p['id']:pos});shot('fixed-drag')
 tap(108+i%4*168,880+i//4*126);tap(360,1110);expect({});tap(590,1110);expect({p['id']:pos});shot('fixed-undo')
 guard();q.adb('shell','wm','size','900x1600');q.offset=0;setup(97,q.levels[96]['solution']);shot('short-dense-97');tap(645,82);shot('short-four-rules-help');tap(360,822);q.key(4);shot('short-pause');tap(505,890);tap(210,970);shot('short-map');print('PASS fixed drag/remove/undo and short dense/help/map',flush=True)
finally:
 q.adb('shell','wm','size','reset');q.offset=215;put(original);q.adb('shell','rm','-f','/data/local/tmp/bento-screen-qa.sqlite');shot('user-progress-restored');assert q.state()==original;print('Restored original save and physical resolution.',flush=True)
