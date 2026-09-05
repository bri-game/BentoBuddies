"""Scoped ADB interaction with Bento Buddies. Coordinates use the 720x1280 design canvas."""
import subprocess,time,json,sys,pathlib,os,sqlite3
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/device';ADB='/Users/xiu/Library/Android/sdk/platform-tools/adb';SERIAL='323952558406';PKG='com.bentobuddies.game.qa';scale=float(os.environ.get('BENTO_SCALE','1.25'));offset=float(os.environ.get('BENTO_YOFFSET','215'))
levels=json.loads((ROOT/'assets/resources/data/levels.json').read_text())['levels']
def adb(*args):return subprocess.run([ADB,'-s',SERIAL,*map(str,args)],check=True,stdout=subprocess.PIPE).stdout

def tap(x,y):
 adb('shell','input','tap',round(x*scale),round(y*scale+offset));time.sleep(.14)
def shot(name):
 time.sleep(.3);(OUT/(name+'.png')).write_bytes(adb('exec-out','screencap','-p'))
def key(code):adb('shell','input','keyevent',code);time.sleep(.3)
def logs():
 pid=adb('shell','pidof',PKG).decode().strip();assert pid,'Game process died';data=adb('logcat','-d','--pid='+pid).decode(errors='replace');(OUT/'gameplay-logcat.txt').write_text(data);return data

def state():
 target=OUT/'save-snapshot.sqlite';target.write_bytes(adb('exec-out','run-as',PKG,'cat','databases/jsb.sqlite'))
 with sqlite3.connect(target) as conn:
  rows=conn.execute("select value from data where key='bento.v1'").fetchone()
  return json.loads(rows[0])
def solve(n):
 l=levels[n-1];c=min(108,536/l['w'],372/l['h']);bx=(720-l['w']*c)/2;by=357+(372-l['h']*c)/2
 for i,p in enumerate(l['pieces']):
  q=l['solution'][p['id']];tap(108+i%4*168,880+i//4*126)
  for r in range(q['r']):tap(130,1110)
  tap(bx+(q['x']+.5)*c,by+(q['y']+.5)*c)
 if n in [1,2,5,9,13,19,24]:shot(f'level-{n:02}-packed')
 data=state()
 assert data['current']==n and data['board']==l['solution'], 'Current board does not match entered solution for '+str(n)
 tap(360,1200);time.sleep(.2)
 data=state()
 for _ in range(10):
  if str(n) in data['album']:break
  time.sleep(.2);data=state()
 assert str(n) in data['album'], 'No saved win for '+str(n)
 if n in [1,5,9,13,24]:shot(f'level-{n:02}-win')
 print('PASS UI solution level',n,flush=True)
 if n<24:tap(360,808)

if __name__=='__main__':
 cmd=sys.argv[1]
 if cmd=='tap':tap(float(sys.argv[2]),float(sys.argv[3]));shot(sys.argv[4] if len(sys.argv)>4 else 'current')
 elif cmd=='shot':shot(sys.argv[2])
 elif cmd=='solve':
  for n in range(int(sys.argv[2]),int(sys.argv[3])+1):solve(n)
 elif cmd=='key':key(sys.argv[2]);shot(sys.argv[3])
 elif cmd=='logs':print(logs()[-3000:])
 elif cmd=='state':print(json.dumps(state(),ensure_ascii=False))
 elif cmd=='drag':
  x,y,u,v=map(float,sys.argv[2:6]);adb('shell','input','swipe',round(x*scale),round(y*scale+offset),round(u*scale),round(v*scale+offset),700);shot('drag-result')
