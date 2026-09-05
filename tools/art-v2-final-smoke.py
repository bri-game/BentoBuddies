import importlib.util,time,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];sp=importlib.util.spec_from_file_location('qa',root/'tools/device-qa.py');q=importlib.util.module_from_spec(sp);sp.loader.exec_module(q);q.OUT=root/'artifacts/v2/device'
def guard():assert any(q.PKG in l for l in q.adb('shell','dumpsys','window').decode().splitlines() if 'mCurrentFocus=' in l),'Foreground changed'
guard();before=q.state();q.shot('home-final');q.tap(360,863);time.sleep(1);guard();assert q.state()['board']==q.levels[23]['solution'];q.shot('final-packed');q.tap(360,1200);time.sleep(1);guard();q.shot('final-win');q.tap(360,808);q.key(4);guard();q.adb('shell','am','force-stop',q.PKG);q.adb('shell','am','start','-n',q.PKG+'/com.cocos.game.AppActivity');time.sleep(2);guard();assert before==q.state();q.shot('home-final');q.logs();print('PASS final APK: home, saved board, serve, album, Back, restart persistence')
