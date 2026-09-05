import {cells,canPlace,evaluate,touching} from '../assets/scripts/Rules.ts';
export function search(l,{cap=100000,accept=()=>true}={}){
 const opts=l.pieces.map(p=>{const out=[],seen=new Set();for(let r=0;r<(p.fixed?1:4);r++)for(let y=0;y<l.h;y++)for(let x=0;x<l.w;x++){
  const pos={x,y,r};if(!canPlace(l,{},p.id,pos))continue;const cs=cells(p,pos),key=cs.map(c=>c.join(',')).sort().join(';');if(seen.has(key))continue;seen.add(key);
  if(l.rules.includes('center')&&p.kind==='cookie'&&cs.some(([a,b])=>!a||!b||a===l.w-1||b===l.h-1))continue;
  if((l.targets||[]).some(t=>t.kind!==p.kind&&cs.some(c=>c[0]===t.cell[0]&&c[1]===t.cell[1])))continue;
  let mask=0;for(const [a,b]of cs)mask|=1<<(a+b*l.w);out.push({pos,cs,mask});
 }return out;});
 let nodes=0,result=null;const board={},chosen=[];
 function dfs(used,mask){if(++nodes>cap)return false;if(used===(1<<l.pieces.length)-1){if(evaluate(l,board).ok&&accept(board)){result=structuredClone(board);return true;}return false;}
  let best=-1,choices=[];
  for(let i=0;i<opts.length;i++)if(!(used&(1<<i))){let fits=opts[i].filter(o=>!(o.mask&mask)&&chosen.every(q=>{
   const a=l.pieces[i].kind,b=l.pieces[q.i].kind;if(l.rules.includes('cold')&&((a==='ice'&&b==='hot')||(a==='hot'&&b==='ice'))&&touching(o.cs,q.o.cs))return false;
   return true;
  }));if(!fits.length)return false;if(best<0||fits.length<choices.length){best=i;choices=fits;}}
  for(const o of choices){board[l.pieces[best].id]=o.pos;chosen.push({i:best,o});if(dfs(used|(1<<best),mask|o.mask))return true;chosen.pop();delete board[l.pieces[best].id];if(nodes>cap)return false;}return false;
 }
 dfs(0,0);return {solution:result,nodes,capped:nodes>cap,placementOptions:opts.map(o=>o.length)};
}
