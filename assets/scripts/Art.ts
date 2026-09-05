import {Node,Layers,UITransform,Sprite,SpriteFrame,Texture2D,JsonAsset,resources,Rect,Size} from 'cc';
export class Art {
 private frames:Record<string,SpriteFrame>={};
 async load(){
  const get=<T>(path:string,type:any)=>new Promise<T>((resolve,reject)=>resources.load(path,type,(e,a)=>e?reject(e):resolve(a as T)));
  const atlas=await get<JsonAsset>('art/v2/atlas',JsonAsset);
  await Promise.all(['background','ui','icons','food','logo'].map(async group=>{
   const texture=await get<Texture2D>(`art/v2/${group}/texture`,Texture2D);
   const entries=group==='background'?{background:[0,0,texture.width,texture.height]}:(atlas.json as any)[group];
   for(const name of Object.keys(entries)){const [x,y,w,h]=entries[name];const f=new SpriteFrame();f.texture=texture;f.rect=new Rect(x,y,w,h);f.originalSize=new Size(w,h);
    if(group==='ui'){const edge=name==='primary'||name==='secondary'?.24:.14;f.insetLeft=w*edge;f.insetRight=w*edge;f.insetTop=h*edge;f.insetBottom=h*edge;}
    this.frames[`${group}/${name}`]=f;
   }
  }));
 }
 draw(parent:Node,key:string,x:number,y:number,w:number,h:number,sliced=false){
  const frame=this.frames[key];const outer=new Node(key);outer.layer=Layers.Enum.UI_2D;outer.addComponent(UITransform).setContentSize(w,h);outer.setPosition(x-360,640-y);parent.addChild(outer);if(!frame)return outer;
  const node=new Node('Artwork');node.layer=Layers.Enum.UI_2D;const transform=node.addComponent(UITransform);outer.addChild(node);const sprite=node.addComponent(Sprite);sprite.spriteFrame=frame;sprite.sizeMode=Sprite.SizeMode.CUSTOM;
  const scale=Math.min(w/frame.rect.width,h/frame.rect.height);
  if(sliced){sprite.type=Sprite.Type.SLICED;transform.setContentSize(w/scale,h/scale);node.setScale(scale,scale,1);}else transform.setContentSize(frame.rect.width*scale,frame.rect.height*scale);
  return outer;
 }
}
