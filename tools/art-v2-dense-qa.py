import importlib.util,time,json
from pathlib import Path
sp=importlib.util.spec_from_file_location('qa',Path(__file__).with_name('device-qa.py'));q=importlib.util.module_from_spec(sp);sp.loader.exec_module(q);q.OUT=q.ROOT/'artifacts/v2/device'
original=q.tap
def guarded(x,y):
 focus=q.adb('shell','dumpsys','window').decode()
 assert any(q.PKG in l for l in focus.splitlines() if 'mCurrentFocus=' in l), 'Device foreground changed; stop input'
 original(x,y)
q.tap=guarded
q.adb('shell','am','start','-n',q.PKG+'/com.cocos.game.AppActivity');time.sleep(2)
q.adb('logcat','-c');q.tap(210,970);time.sleep(1);q.shot('level-map');q.tap(600,1037);time.sleep(1);q.shot('dense-empty')
q.solve(24);time.sleep(1);q.shot('dense-win');log=q.logs();assert q.state()['board']==q.levels[23]['solution'], 'Dense board mismatch'
q.tap(360,808);time.sleep(1);q.shot('album-complete');q.key(4);time.sleep(1);q.shot('home-final')
(q.OUT/'dense-result.json').write_text(json.dumps({'passed':True,'level24SolutionVerified':True, 'winRequiresScreenshotReview':'dense-win.png','foregroundGuard':True},indent=2));print('PASS guarded dense level24')
