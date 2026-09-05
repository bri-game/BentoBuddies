import importlib.util,time,re,json,statistics,shlex
from pathlib import Path
sp=importlib.util.spec_from_file_location('qa',str(Path(__file__).with_name('device-qa.py')));q=importlib.util.module_from_spec(sp);sp.loader.exec_module(q)
try:
 q.adb('shell','wm','size','900x1600');q.adb('shell','am','force-stop',q.PKG);q.adb('shell','am','start','-n',q.PKG+'/com.cocos.game.AppActivity');time.sleep(2);q.offset=0
 q.shot('short-16x9-home');q.tap(210,970);q.tap(600,1037);q.shot('short-16x9-dense-empty');q.solve(24);q.tap(360,908);time.sleep(1);q.shot('short-16x9-dense-solved')
 q.key(4);q.shot('short-16x9-pause');q.tap(360,790)
 print('PASS 900x1600 short portrait, dense level24 solve, Back and safe controls',flush=True)
finally:
 q.adb('shell','wm','size','reset');q.adb('shell','am','force-stop',q.PKG);q.adb('shell','am','start','-n',q.PKG+'/com.cocos.game.AppActivity');time.sleep(2);q.offset=215
q.tap(360,863);time.sleep(1);q.shot('tall-dense-solved-final')
surfaces=q.adb('shell','dumpsys','SurfaceFlinger','--list').decode();name=next((line.removeprefix('RequestedLayerState{').removesuffix('}') for line in surfaces.splitlines() if 'SurfaceView['+q.PKG in line and '(BLAST)' in line),None)
if name:
 name=name.split(' parentId=')[0]
 data=q.adb('shell','dumpsys SurfaceFlinger --latency '+shlex.quote(name)).decode();(q.OUT/'frame-latency.txt').write_text(data)
q.logs();q.key(4);q.tap(505,890);q.tap(210,970);q.tap(120,321);q.shot('ready-level-one')
(q.OUT/'final-state.json').write_text(json.dumps(q.state(),ensure_ascii=False,indent=2));print('Restored physical 900x2030; left game at level 1 with QA album retained.',flush=True)
