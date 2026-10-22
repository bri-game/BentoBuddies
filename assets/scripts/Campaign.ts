export const CHAPTERS=[
 {title:'First Picnics',theme:'Getting started, Rice with Veggie, Ice Cream away from Soup'},
 {title:'Small Requests',theme:'Berry on the rim, and tastes that mix'},
 {title:'Saved Seats',theme:'Cover every marked cell with the right food'},
 {title:'A Little Ribbon',theme:'Locked items can move, but never rotate'},
 {title:'The Sheltered Cookie',theme:'Every Cookie cell stays inside the box'},
 {title:'Two Halves, One Meal',theme:'Pick a side, squeeze past corners, split the space'},
 {title:'Promises Together',theme:'Combine everything your friends love'},
 {title:'A Clever Gift Box',theme:'Fixed angles and awkward gaps'},
 {title:'Master Picnics',theme:'Everything combined, challenges, and calm breaks'}
];
export const RULE_SHORT:Record<string,string>={rice:'Rice touches Veggie',cold:'Ice Cream far from Soup',edge:'Berry on the rim',target:'Cover marked cells',fixed:'Locked = no rotating',center:'Cookie off the rim'};
export const RULE_HELP:Record<string,string>={
 rice:'Rice must touch a Veggie edge to edge.\nDiagonal corners do not count.',
 cold:'Ice Cream must never touch Soup edge to edge.',
 edge:'At least one Berry cell must touch\nthe outer rim of the box.',
 target:'A cell with a food picture and a star\nis a saved seat. Cover it with that food.\nTap a marked cell to see what it needs.',
 fixed:'A locked item keeps the angle it has\non the tray. You can still move it,\ntake it out and undo. Rotate the rest.',
 center:'The whole Cookie must sit inside the box.\nNo Cookie cell may touch the outer rim.\nOther foods can still rest on the rim.'
};
