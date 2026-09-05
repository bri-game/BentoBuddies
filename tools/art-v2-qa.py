import importlib.util,time,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('qa',Path(__file__).with_name('device-qa.py'));q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
q.OUT=q.ROOT/'artifacts/v2/device';q.OUT.mkdir(exist_ok=True)
def shot(n):time.sleep(1);q.shot(n)
q.adb('logcat','-c')
q.tap(360,863);shot('play-empty')
q.tap(360,1200);shot('failed');q.tap(360,850)
q.solve(1);shot('level-2')
q.key(4);shot('pause');q.tap(505,890)
q.tap(510,970);shot('album');q.key(4)
q.tap(360,1070);shot('settings');q.tap(360,650);q.tap(360,650);q.tap(360,751);q.tap(360,751);q.tap(360,853);shot('onboarding');q.tap(360,850);q.key(4);q.key(4);q.tap(505,890)
q.tap(210,970);shot('level-map');q.tap(600,1037);shot('dense-empty')
q.solve(24);shot('dense-win');q.tap(360,808);shot('album-complete');q.key(4)
before=q.state();assert len(before['album'])==24
q.adb('shell','am','force-stop',q.PKG);q.adb('shell','monkey','-p',q.PKG,'1');time.sleep(2);shot('home-final');after=q.state();assert after==before
log=q.logs();assert before['current']==24 and before['board']==q.levels[23]['solution']
assert 'FATAL EXCEPTION' not in log and 'Fatal signal' not in log
(q.OUT/'art-v2-result.json').write_text(json.dumps({'passed':True,'savedAlbums':len(after['album']),'winsRequireScreenshotReview':[1,24],'persistence':True},indent=2))
print('PASS visual update device loop, failure, wins 1/24, navigation, audio controls, persistence')
