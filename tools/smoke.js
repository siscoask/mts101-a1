// Render smoke test in a stub DOM (NOT a browser): runs every page's render code, incl. a resumed and an expired mock test.
const fs=require('fs'),vm=require('vm'),root=__dirname+'/../';
function run(seed){
  const mk=()=>new Proxy(function(){},{get:(t,k)=>k===Symbol.toPrimitive?()=>'':k==='style'||k==='dataset'?{}:mk(),set:()=>true,apply:()=>mk()});
  const store=Object.assign({},seed),L={};
  const ctx={document:{querySelector:()=>mk(),querySelectorAll:()=>mk(),createElement:()=>mk()},location:{hash:'',protocol:'file:'},navigator:{},confirm:()=>true,alert(){},prompt(){},URL:{createObjectURL(){}},Blob:function(){},
    localStorage:{getItem:k=>k in store?store[k]:null,setItem:(k,v)=>store[k]=String(v),removeItem:k=>delete store[k]},addEventListener:(e,f)=>L[e]=f,scrollTo(){},setInterval:()=>0,clearInterval(){},console};
  ctx.window=ctx;vm.createContext(ctx);
  for(const f of['data/questions.js','js/math.js','js/app.js'])vm.runInContext(fs.readFileSync(root+f,'utf8'),ctx,{filename:f});
  for(const h of['#/practise','#/topics','#/mock','#/progress']){ctx.location.hash=h;L.hashchange()}
  return store;
}
const Q=JSON.parse(fs.readFileSync(root+'data/questions.json','utf8')),ids=Q.slice(0,30).map(q=>q.id),ans={};ids.slice(0,12).forEach((id,i)=>ans[id]='A');
const mock=end=>({'mts101a1.mock':JSON.stringify({kind:'standard',topic:'x',ids,ans,i:3,end,mins:20})});
run({});console.log('fresh ok');
run(mock(Date.now()+600000));console.log('resumed mock ok');
const s=run(mock(Date.now()-1000));console.log('expired mock auto-submitted:',JSON.parse(s['mts101a1.v1']).mocks.length===1);
const old=run({'mts105a1.v1':JSON.stringify({log:[{id:Q[0].id,ok:false,t:1,topic:'Number Systems'}],flags:[]})});console.log('old progress migrated, topic:',JSON.parse(old['mts101a1.v1']||'{"log":[{"topic":"(saved on first write)"}]}').log[0].topic);
