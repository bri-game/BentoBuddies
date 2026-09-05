import importlib.util,time,json
from pathlib import Path
sp=importlib.util.spec_from_file_location('qa',str(Path(__file__).with_name('device-qa.py')));q=importlib.util.module_from_spec(sp);sp.loader.exec_module(q)
# Starts at level 24 win overlay.
q.tap(360,808);q.shot('album-final');s=q.state();assert len(s['album'])==24
q.tap(560,1120);q.shot('album-page-two');q.key(4);q.shot('home-complete')
q.tap(360,1070);q.shot('settings-on');q.tap(360,650);q.tap(360,751);time.sleep(.5);s=q.state();assert s['music']==False and s['sfx']==False;q.shot('settings-muted')
q.tap(360,853);q.shot('tutorial-final');q.tap(360,850)
q.adb('shell','am','force-stop',q.PKG);q.adb('shell','am','start','-n',q.PKG+'/com.cocos.game.AppActivity');time.sleep(2);q.shot('cold-relaunch');s2=q.state();assert s2['album']==s['album'] and s2['music']==False and s2['sfx']==False
q.tap(360,1070);q.shot('settings-muted-persisted');q.tap(360,650);q.tap(360,751);q.key(4)
# Home -> select the first level for an exact-final-binary replay of all opening levels.
q.tap(210,970);q.shot('levels-unlocked');q.tap(120,321)
for n in range(1,9):q.solve(n)
q.key(3);time.sleep(.5);q.adb('shell','am','start','-n',q.PKG+'/com.cocos.game.AppActivity');time.sleep(.8);q.shot('background-resume-paused');q.tap(360,790)
q.shot('resumed-game');q.logs();print('PASS 24 album entries, album pages, tutorial replay, mute switches, cold persistence, final APK levels 1-8, background resume',flush=True)
