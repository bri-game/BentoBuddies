export type Cell = [number, number];
export type Kind = 'rice'|'veg'|'ice'|'hot'|'berry'|'egg'|'shrimp'|'cookie';
export type Piece = {id:string;kind:Kind;shape:Cell[];fixed?:boolean};
export type Placement = {x:number;y:number;r:number};
export type Level = {id:number;title:string;friend:number;w:number;h:number;blocked:Cell[];pieces:Piece[];rules:string[];solution:Record<string,Placement>;stage:string;targets?:{cell:Cell;kind:Kind}[];topology?:string;difficulty?:string;seed?:number};
export type Board = Record<string,Placement>;
export const FOOD:Record<Kind,{name:string;mark:string;color:string}>={rice:{name:'Cơm',mark:'C',color:'#F5E9C9'},veg:{name:'Rau',mark:'R',color:'#91AE72'},ice:{name:'Kem',mark:'K',color:'#ABD3CF'},hot:{name:'Súp',mark:'S',color:'#E8896B'},berry:{name:'Dâu',mark:'D',color:'#DE7B81'},egg:{name:'Trứng',mark:'T',color:'#F3C66C'},shrimp:{name:'Tôm',mark:'Ô',color:'#EDA183'},cookie:{name:'Bánh',mark:'B',color:'#CBA275'}};
export function rotate(shape:Cell[],r:number):Cell[]{let a=shape.map(c=>[...c] as Cell);for(let i=0;i<((r%4)+4)%4;i++)a=a.map(([x,y])=>[-y,x]);let mx=Math.min(...a.map(c=>c[0])),my=Math.min(...a.map(c=>c[1]));return a.map(([x,y])=>[x-mx,y-my]);}
export function cells(piece:Piece,p:Placement):Cell[]{return rotate(piece.shape,p.r).map(([x,y])=>[x+p.x,y+p.y]);}
export function canPlace(l:Level,b:Board,id:string,p:Placement):boolean{const piece=l.pieces.find(q=>q.id===id);if(!piece||!p||![p.x,p.y,p.r].every(Number.isInteger)||(piece.fixed&&p.r!==0))return false;const occupied=new Set(l.blocked.map(c=>c.join(',')));for(const q of l.pieces)if(q.id!==id&&b[q.id])cells(q,b[q.id]).forEach(c=>occupied.add(c.join(',')));return cells(piece,p).every(([x,y])=>x>=0&&x<l.w&&y>=0&&y<l.h&&!occupied.has(`${x},${y}`));}
export function place(l:Level,b:Board,id:string,p:Placement):Board|null{return canPlace(l,b,id,p)?{...b,[id]:{...p}}:null;}
export function touching(a:Cell[],b:Cell[]):boolean{return a.some(([x,y])=>b.some(([u,v])=>Math.abs(x-u)+Math.abs(y-v)===1));}
export function evaluate(l:Level,b:Board):{ok:boolean;issues:string[];bad:string[]}{const issues:string[]=[],bad:string[]=[];if(l.pieces.some(p=>!b[p.id]))issues.push('Xếp hết các món vào hộp nhé.');for(const p of l.pieces)if(b[p.id]&&!canPlace(l,b,p.id,b[p.id])){issues.push('Có món nằm ngoài hộp hoặc chồng nhau.');bad.push(p.id);}const by=(kind:Kind)=>l.pieces.filter(p=>p.kind===kind&&b[p.id]);const cs=(p:Piece)=>cells(p,b[p.id]);if(l.rules.includes('rice'))for(const p of by('rice'))if(!by('veg').some(v=>touching(cs(p),cs(v)))){issues.push('Cơm cần chạm cạnh rau.');bad.push(p.id);}if(l.rules.includes('cold'))for(const p of by('ice'))for(const h of by('hot'))if(touching(cs(p),cs(h))){issues.push('Kem cần cách súp ít nhất một ô.');bad.push(p.id,h.id);}if(l.rules.includes('edge'))for(const p of by('berry'))if(!cs(p).some(([x,y])=>x===0||y===0||x===l.w-1||y===l.h-1)){issues.push('Dâu cần chạm viền ngoài hộp.');bad.push(p.id);}if(l.rules.includes('center'))for(const p of by('cookie'))if(cs(p).some(([x,y])=>x===0||y===0||x===l.w-1||y===l.h-1)){issues.push('Toàn bộ Bánh phải nằm bên trong, không chạm viền ngoài.');bad.push(p.id);}
for(const t of l.targets||[]){const occupant=l.pieces.find(p=>b[p.id]&&cs(p).some(c=>c[0]===t.cell[0]&&c[1]===t.cell[1]));if(!occupant||occupant.kind!==t.kind){issues.push('Ô đánh dấu cần được phủ bằng '+FOOD[t.kind].name+'.');if(occupant)bad.push(occupant.id);}}
return {ok:issues.length===0,issues:[...new Set(issues)],bad:[...new Set(bad)]};}
export function fingerprint(l:Level):string{
 const variants:string[]=[];
 const shapeKey=(shape:Cell[])=>[0,1,2,3].map(r=>rotate(shape,r).map(c=>c.join(',')).sort().join(';')).sort()[0];
 for(let mirror=0;mirror<2;mirror++)for(let r=0;r<4;r++){
  const transform=([x,y]:Cell):Cell=>{if(mirror)x=-x;for(let i=0;i<r;i++){const t=x;x=-y;y=t;}return [x,y];};
  const all:Cell[]=[];for(let y=0;y<l.h;y++)for(let x=0;x<l.w;x++)all.push(transform([x,y]));
  const minX=Math.min(...all.map(c=>c[0])),minY=Math.min(...all.map(c=>c[1]));
  const blocks=l.blocked.map(c=>{const [x,y]=transform(c);return `${x-minX},${y-minY}`;}).sort().join(';');
  const groups=l.pieces.map(p=>{
   const relevant=(l.rules.includes('rice')&&['rice','veg'].includes(p.kind))||(l.rules.includes('cold')&&['ice','hot'].includes(p.kind))||(l.rules.includes('edge')&&p.kind==='berry')||(l.rules.includes('center')&&p.kind==='cookie')||(l.targets||[]).some(t=>t.kind===p.kind);
   return (relevant?p.kind:'neutral')+':'+(p.fixed?'fixed:'+rotate(p.shape.map(transform),0).map(c=>c.join(',')).sort().join(';'):shapeKey(p.shape.map(transform)));
  }).sort().join('|');
  const targets=(l.targets||[]).map(t=>{const [x,y]=transform(t.cell);return `${x-minX},${y-minY}:${t.kind}`;}).sort().join(';');
  variants.push([Math.max(...all.map(c=>c[0]))-minX+1,Math.max(...all.map(c=>c[1]))-minY+1,blocks,groups,targets,[...l.rules].sort().join(',')].join('/'));
 }
 return variants.sort()[0];
}
