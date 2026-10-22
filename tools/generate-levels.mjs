import fs from 'node:fs';
import {search} from './campaign-solver.mjs';
import {rotate,evaluate,fingerprint,touching,canPlace,cells} from '../assets/scripts/Rules.ts';
const base=JSON.parse(fs.readFileSync(new URL('./base-levels-24.json',import.meta.url))).levels;
const levels=structuredClone(base),seen=new Set(levels.map(fingerprint));
const geometry=l=>fingerprint({...l,rules:[],targets:[],pieces:l.pieces.map(p=>({...p,fixed:false,kind:'egg'}))});
const shapesSeen=new Set(levels.map(geometry));
let seed=310825;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};
const pick=a=>a[Math.floor(rand()*a.length)];
const shuffle=a=>{a=[...a];for(let i=a.length-1;i>0;i--){let j=Math.floor(rand()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
const stages=['introduce','vary','vary','combine','pressure','mastery','recovery','vary','combine','pressure','mastery','recovery'];
const titles=[
 ['The First Saved Seat','Seats Saved Ahead','A Little Meeting Corner','A Note on the Box','Two Small Seats','Right Food, Right Spot','A Walk Through Flowers','Choose the Cell First','Rice Meets Veggie','A Pair of Cards','Three Little Notes','An Easy Picnic'],
 ['Keep That Angle','A Little Ribbon','Straight Across','A Snug Corner','Two Locked Items','A Clever Knot','Rest by the Stream','One Long Direction','Ribbon and Promise','Turn What Is Left','A Neat Square Gift','A Breeze in the Garden'],
 ['The Cookie Stays In','A Cozy Middle','The Sheltered Cookie','Cool Cream, Soft Cookie','Room for the Cookie','Outer Ring, Inner Ring','Tea Under the Leaves','A Quiet Space','Cookie and Note','Snug in the Core','Rim Left for Berry','A Slow Afternoon Tea'],
 ['Two Picnic Halves','A Small Step','Around the Stones','Pick a Corner','Just Enough Gap','Two Meals, One Box','Rest Between Banks','An Unexpected Notch','A Long Piece Through','A Nook by the Lake','A Clever Divide','The Wooden Bridge'],
 ['A Shared Promise','Rice and Veggie in Place','A Box Full of Notes','Keep the Cream Cool','Every Little Care','A Lunch in Harmony','Just One Request','Ribbon and Cookie','A Lunch of Every Flavor','Who Is This Seat For','Three Small Promises','A Peaceful Picnic'],
 ['A Gift Box of Corners','A Knot in the Middle','Through the Narrow Gap','Two Ways, One Promise','Around the Core','Sunshine, Neatly Packed','A Gentle Meal','Turn Your Thinking Around','Who Gets the Last Corner','Choose the First Piece','A Delicate Box','A Rest With Friends'],
 ['A Careful Journey','The Last Promise','Three Friends, One Box','Choose the Empty Space','Cool Through the Sun','A Master Picnic','Under the Old Tree','A Garden Feast','Foods in Harmony','The Final Knot','A Gift Complete','Picnic Again Tomorrow']
];
function rulePlan(ch,i){
 if(ch===0)return i<3||i===6?['target']:i<6?['target','rice']:i===8||i===10?['target','rice','edge']:['target','cold'];
 if(ch===1)return i<3||i===6?['fixed']:i<6?['fixed','edge']:i===8||i===10?['fixed','target']:['fixed','cold'];
 if(ch===2)return i<3||i===6?['center']:i<6?['center','cold']:i===8||i===10?['center','target','edge']:['center','rice'];
 if(ch===3)return i===6||i===11?['target']:pick([['rice','cold'],['fixed','target'],['center','edge'],['rice','target']]);
 const pool=[['target','rice','cold'],['fixed','center','edge'],['target','fixed','rice'],['center','cold','edge'],['target','center','fixed'],['rice','cold','edge','fixed'],['target','rice','cold','center']];
 return i===6||i===11?pick([['target'],['fixed','edge'],['center']]):pool[(i+ch)%pool.length];
}
function layout(w,h,type){
 if(type==='corners')return [[0,0],[w-1,h-1]];
 if(type==='notch')return [[w-1,0],[w-1,1],[w-2,0]];
 if(type==='well')return [[Math.floor(w/2),Math.floor(h/2)]];
 if(type==='stairs')return [[0,0],[0,1],[1,0],[w-1,h-1]];
 if(type==='split')return Array.from({length:h},(_,y)=>[Math.floor(w/2),y]);
 return [];
}
for(let n=25;n<=108;n++){
 const ch=Math.floor((n-25)/12),i=(n-25)%12,stage=stages[i],rules=rulePlan(ch,i),intro=ch<3&&i===0,recovery=stage==='recovery';let built;
 for(let attempt=0;attempt<60000&&!built;attempt++){
  let w=intro?(ch===2?4:4):recovery?pick([4,5]):ch>=4?pick([5,6]):pick([4,5]),h=intro?(ch===2?4:3):recovery?4:ch>=4?pick([4,5]):4;
  const topology=intro?'rectangle':ch===3&&[0,5,8,10].includes(i)?'split':pick(['rectangle','corners','notch','well','stairs',...(ch>=3?['split']:[])]);
  // A split box with center cookies needs a wide-enough inner compartment.
  if(topology==='split'&&rules.includes('center'))w=6;
  const blocked=layout(w,h,topology),area=w*h-blocked.length;
  const count=intro?4:recovery?5:Math.min(8,Math.max(6,Math.ceil(area/4)+(stage==='mastery'?1:0)));
  if(area>count*5)continue;
  let available=[];for(let y=0;y<h;y++)for(let x=0;x<w;x++)if(!blocked.some(c=>c[0]===x&&c[1]===y))available.push([x,y]);
  const groups=[];
  while(available.length&&groups.length<count){const left=count-groups.length,size=left===1?available.length:Math.max(1,Math.min(5,Math.round(available.length/left)+(rand()<.2?-1:0)));let g=[available.splice(Math.floor(rand()*available.length),1)[0]];
   while(g.length<size){const candidates=available.filter(c=>touching([c],g));if(!candidates.length)break;const c=pick(candidates);available.splice(available.indexOf(c),1);g.push(c);}groups.push(g);
  }
  if(available.length||groups.length!==count||groups.some(g=>g.length>5)||groups.filter(g=>g.length===1).length>2)continue;
  const kinds=Array(count).fill(null);
  if(rules.includes('center')){const opts=groups.map((g,j)=>g.every(([x,y])=>x>0&&y>0&&x<w-1&&y<h-1)?j:-1).filter(j=>j>=0);if(!opts.length)continue;kinds[pick(opts)]='cookie';}
  if(rules.includes('cold')){const opts=[];for(let a=0;a<count;a++)for(let b=a+1;b<count;b++)if(!kinds[a]&&!kinds[b]&&!touching(groups[a],groups[b]))opts.push([a,b]);if(!opts.length)continue;const [a,b]=pick(opts);kinds[a]='ice';kinds[b]='hot';}
  if(rules.includes('rice')){const opts=[];for(let a=0;a<count;a++)for(let b=a+1;b<count;b++)if(!kinds[a]&&!kinds[b]&&touching(groups[a],groups[b]))opts.push([a,b]);if(!opts.length)continue;const [a,b]=pick(opts);kinds[a]='rice';kinds[b]='veg';}
  if(rules.includes('edge')){const opts=groups.map((g,j)=>!kinds[j]&&g.some(([x,y])=>!x||!y||x===w-1||y===h-1)?j:-1).filter(j=>j>=0);if(!opts.length)continue;kinds[pick(opts)]='berry';}
  let extras=shuffle(['egg','shrimp','cookie','rice','veg','berry','ice','hot'].filter(k=>!kinds.includes(k)&&!(rules.includes('center')&&k==='cookie')));kinds.forEach((k,j)=>{if(!k)kinds[j]=extras.shift()||'egg';});
  const solution={};const pieces=groups.map((g,j)=>{const x=Math.min(...g.map(c=>c[0])),y=Math.min(...g.map(c=>c[1])),r=Math.floor(rand()*4),shape=rotate(g.map(([a,b])=>[a-x,b-y]),r);solution[String(j)]={x,y,r:(4-r)%4};return {id:String(j),kind:kinds[j],shape};});
  if(rules.includes('fixed')){const opts=shuffle(pieces.filter(p=>new Set([0,1,2,3].map(r=>rotate(p.shape,r).map(c=>c.join(',')).sort().join(';'))).size>1));if(!opts.length)continue;for(const p of opts.slice(0,intro?1:stage==='mastery'?3:2)){p.shape=rotate(p.shape,solution[p.id].r);solution[p.id].r=0;p.fixed=true;}}
  const targets=rules.includes('target')?shuffle(groups.map((g,j)=>({cell:pick(g),kind:kinds[j]}))).slice(0,intro?1:stage==='mastery'?3:2):[];
  const l={id:n,title:titles[ch][i],friend:ch%3,w,h,blocked,pieces,rules,solution,stage:ch>=3&&stage==='introduce'?'vary':stage,topology,targets,difficulty:intro?'Gentle':recovery?'Relax':stage==='mastery'?'Mastery':stage==='pressure'?'Hard':'Steady',seed};
  if(!evaluate(l,solution).ok||seen.has(fingerprint(l))||shapesSeen.has(geometry(l)))continue;
  // Target and interior rules must exclude at least one geometrically legal placement.
  if(rules.includes('center')){const p=pieces.find(p=>p.kind==='cookie');if(!p||!Array.from({length:w*h},(_,a)=>({x:a%w,y:Math.floor(a/w),r:0})).some(pos=>canPlace(l,{},p.id,pos)&&cells(p,pos).some(([x,y])=>!x||!y||x===w-1||y===h-1)))continue;}
  const measured=search(l,{cap:30000});if(!measured.solution)continue;
  const minimum=stage==='mastery'?(ch<3?80:300):stage==='pressure'?(ch<3?30:100):0;
  if(measured.nodes<minimum||((intro||recovery)&&measured.nodes>45))continue;
  // New restrictions should create a real decision, not merely restate geometry.
  let redundant=false;for(const kind of ['target','fixed','center'].filter(k=>rules.includes(k))){
   const relaxed={...l,rules:l.rules.filter(r=>r!==kind),targets:kind==='target'?[]:l.targets,pieces:l.pieces.map(p=>({...p,fixed:kind==='fixed'?false:p.fixed}))};
   if(!search(relaxed,{cap:12000,accept:b=>!evaluate(l,b).ok}).solution){redundant=true;break;}
  }
  if(redundant)continue;
  built=l;seen.add(fingerprint(l));shapesSeen.add(geometry(l));
 }
 if(!built)throw Error('Could not generate '+n);levels.push(built);
}
fs.writeFileSync(new URL('../assets/resources/data/levels.json',import.meta.url),JSON.stringify({version:2,seed:310825,levels},null,2));console.log(`Generated ${levels.length} levels; first 24 preserved, 84 geometrically distinct additions.`);
