from PIL import Image,ImageDraw
from pathlib import Path
p=Path(__file__).resolve().parents[1];im=Image.new('RGBA',(1024,1024),'#FFF5E4');d=ImageDraw.Draw(im)
d.rounded_rectangle((135,235,889,851),radius=125,fill='#C99D70');d.rounded_rectangle((147,211,877,813),radius=116,fill='#E9CDA9');d.rounded_rectangle((187,253,837,773),radius=80,fill='#F7E6C8')
d.polygon([(240,511),(404,294),(558,511)],fill='#C5B293');d.polygon([(252,493),(404,292),(543,493)],fill='#FFFCED');d.rounded_rectangle((360,416,448,508),radius=12,fill='#53624C');d.ellipse((355,375,375,395),fill='#51382E');d.ellipse((432,375,452,395),fill='#51382E')
d.rounded_rectangle((642,420,686,524),radius=12,fill='#718B5B')
for x,y,r,c in [(609,371,60,'#718B5B'),(701,367,58,'#789653'),(653,323,68,'#91AD6D')]:d.ellipse((x-r,y-r,x+r,y+r),fill=c)
d.rounded_rectangle((235,566,501,710),radius=32,fill='#EDBE65')
for x in [272,344,416]:d.rounded_rectangle((x,585,x+22,686),radius=9,fill='#FFE2A0')
d.polygon([(562,575),(772,575),(735,668),(669,727),(593,667)],fill='#DC787E');d.ellipse((562,530,772,637),fill='#E88B88');d.polygon([(578,536),(640,550),(669,510),(687,550),(758,536),(704,582),(630,582)],fill='#718B5B')
for x,y in [(614,599),(674,610),(720,597),(645,656),(698,663)]:d.ellipse((x-5,y-9,x+5,y+9),fill='#FFF0C2')
im.save(p/'store-assets/icon-source.png')
res=p/'native/engine/android/res'
for folder,size in [('mdpi',48),('hdpi',72),('xhdpi',96),('xxhdpi',144),('xxxhdpi',192)]:
 dest=res/('mipmap-'+folder);dest.mkdir(exist_ok=True,parents=True)
 for name in ['ic_launcher.png','ic_launcher_round.png']:im.resize((size,size),Image.Resampling.LANCZOS).save(dest/name)
# Fit complete icon inside Android adaptive mask safe zone.
fg=Image.new('RGBA',(432,432),(0,0,0,0));fg.alpha_composite(im.resize((288,288),Image.Resampling.LANCZOS),(72,72));fg.save(res/'drawable-nodpi/ic_launcher_foreground.png')
(res/'values/colors.xml').write_text('<resources><color name="ic_launcher_background">#FFF5E4</color></resources>')
for size in [48,96]:im.resize((size,size),Image.Resampling.LANCZOS).save(p/f'artifacts/icon-{size}.png')
