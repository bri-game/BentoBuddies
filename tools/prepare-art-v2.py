"""Inspect ImageGen alpha and record sprite rectangles; original atlases remain unchanged."""
from PIL import Image
from pathlib import Path
import json
p=Path(__file__).resolve().parents[1];root=p/'assets/resources/art/v2';data={}
def rects(name,regions,keys):
 im=Image.open(root/(name+'.png')).convert('RGBA');alpha=im.getchannel('A');out={}
 for key,(x,y,x2,y2) in zip(keys,regions):
  a=alpha.crop((x,y,x2,y2));box=a.point(lambda v:255 if v>32 else 0).getbbox();assert box,key
  l,t,r,b=box;l=max(0,l-2);t=max(0,t-2);r=min(x2-x,r+2);b=min(y2-y,b+2)
  out[key]=[x+l,y+t,r-l,b-t]
 data[name]=out
rects('ui',[(x,y,x2,y2) for y,y2 in [(0,285),(285,575),(575,895),(895,1254)] for x,x2 in [(0,627),(627,1254)]],['primary','secondary','sign','panel','tile','selected','tray','scrapbook'])
rects('icons',[(int(c*1254/4),int(r*1254/4),int((c+1)*1254/4),int((r+1)*1254/4)) for r in range(4) for c in range(4)],['back','help','rotate','remove','undo','play','album','map','music','sound','home','reset','check','lock','next','star'])
rects('food',[(0,0,320,410),(320,0,642,410),(642,0,932,410),(932,0,1254,410),(0,410,320,762),(320,410,640,762),(640,410,935,762),(935,410,1254,762),(0,762,320,1254),(320,762,623,1254),(623,762,931,1254),(931,762,1254,1254)],['rice','veg','ice','hot','berry','egg','shrimp','cookie','rabbit','bear','frog','basket'])
rects('logo',[(0,0,1254,1254)],['logo'])
(root/'atlas.json').write_text(json.dumps(data,indent=2))
# Mechanical Android resource resizing from the generated icon.
im=Image.open(p/'store-assets/icon-v2-source.png').convert('RGBA');res=p/'native/engine/android/res'
for folder,size in [('mdpi',48),('hdpi',72),('xhdpi',96),('xxhdpi',144),('xxxhdpi',192)]:
 dest=res/('mipmap-'+folder);dest.mkdir(exist_ok=True,parents=True)
 for name in ['ic_launcher.png','ic_launcher_round.png']:im.resize((size,size),Image.Resampling.LANCZOS).save(dest/name)
im.resize((432,432),Image.Resampling.LANCZOS).save(res/'drawable-nodpi/ic_launcher_foreground.png')
(res/'values/colors.xml').write_text('<resources><color name="ic_launcher_background">#EE6839</color></resources>')
print(json.dumps(data,indent=2))
