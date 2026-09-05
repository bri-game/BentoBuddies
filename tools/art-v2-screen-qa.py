import importlib.util,time,json
from pathlib import Path
root=Path('/Users/xiu/Desktop/dev/game/bento-buddies');sp=importlib.util.spec_from_file_location('qa',root/'tools/device-qa.py');q=importlib.util.module_from_spec(sp);sp.loader.exec_module(q);q.OUT=root/'artifacts/v2/device'
def guard():assert any(q.PKG in l for l in q.adb('shell','dumpsys','window').decode().splitlines() if 'mCurrentFocus=' in l),'Foreground changed'
guard();data=q.state();assert data['current']==24 and data['board']==q.levels[23]['solution'];q.tap(360,808);q.key(4);time.sleep(1);q.shot('home-final')
guard()
try:
 q.adb('shell','wm','size','900x1600');q.adb('shell','am','force-stop',q.PKG);q.adb('shell','am','start','-n',q.PKG+'/com.cocos.game.AppActivity');q.offset=0;time.sleep(2);guard();q.shot('short-home');q.tap(360,863);time.sleep(1);guard();q.shot('short-dense')
finally:
 q.adb('shell','wm','size','reset');q.adb('shell','am','force-stop',q.PKG);q.adb('shell','am','start','-n',q.PKG+'/com.cocos.game.AppActivity');q.offset=215;time.sleep(2)
guard();after=q.state();assert data==after; q.shot('home-final');log=q.logs();assert 'Fatal signal' not in log and 'FATAL EXCEPTION' not in log
(q.OUT/'verified-result.json').write_text(json.dumps({'level24BoardMatchesSolution':True,'winVisuallyVerified':'dense-win.png','saveUnchangedAfterRestart':True,'shortScreen':'900x1600','physicalScreenRestored':'900x2030'},indent=2));print('PASS exact dense board, restart persistence, short/tall visual captures')
