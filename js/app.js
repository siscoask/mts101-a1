(()=>{
const $=s=>document.querySelector(s),R=MatMath.render,KEY='mts101a1.v1';
const TOPICS=["Set Theory and Venn Diagram","Number System","Quadratic Equation","Sequence and Series","Mathematical Induction","Binomial Theorem","Complex Number","Circular Measure","Trigonometry Function of Angle"];
const raw=window.MAT_QUESTIONS||[];
const ok=q=>q&&q.id&&q.topic&&q.question&&Array.isArray(q.options)&&q.options.length>1&&q.options.some(o=>o.id===q.correctAnswer)&&q.explanation&&Array.isArray(q.explanation.steps);
const all=raw.filter(ok),skipped=raw.length-all.length,byId=Object.fromEntries(all.map(q=>[q.id,q]));
let st={log:[],flags:[],mocks:[]};
const OLDT={"Set Theory and Venn Diagrams":TOPICS[0],"Number Systems":TOPICS[1],"Quadratic Equations":TOPICS[2],"Complex Numbers":TOPICS[6],"Trigonometric Functions of Angles":TOPICS[8]};
const adopt=r=>({log:r.log.map(e=>({...e,topic:OLDT[e.topic]||e.topic})),flags:Array.isArray(r.flags)?r.flags:[],mocks:Array.isArray(r.mocks)?r.mocks:[]});
try{const r=JSON.parse(localStorage.getItem(KEY)||localStorage.getItem('mts105a1.v1')||localStorage.getItem('mat101a1.v1'));if(r&&Array.isArray(r.log))st=adopt(r)}catch(e){}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}};
const E=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.random()*(i+1)|0;[a[i],a[j]]=[a[j],a[i]]}return a};
const logs=()=>st.log.filter(e=>byId[e.id]);
const latest=()=>{const m={};logs().forEach(e=>m[e.id]=e.ok);return m};
const wrongIds=()=>{const m=latest();return Object.keys(m).filter(k=>!m[k])};
const rec=(q,ok_)=>{st.log.push({id:q.id,ok:ok_,t:Date.now(),topic:q.topic});if(st.log.length>20000)st.log=st.log.slice(-20000)};
const tickSVG='<svg class="tick" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 13l6 6L21 5"/></svg>';
const penSVG='<svg class="pen" viewBox="0 0 200 60" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" vector-effect="non-scaling-stroke" d="M14 30C16 9 60 4 110 5s86 8 86 26-48 23-94 23S9 52 11 30c1-13 28-21 68-24"/></svg>';
const topicSel=(id,val)=>`<select id="${id}" aria-label="Topic"><option value="all">All topics</option>${TOPICS.map(t=>`<option value="${E(t)}"${val===t?' selected':''}>${t}</option>`).join('')}</select>`;
const optHTML=(o,extra='')=>`<button class="opt" data-id="${o.id}"${extra}><b>${o.id}</b><span>${R(o.text)}</span></button>`;
/* ---------- Practise ---------- */
const P={mode:'practice',topic:'all',len:10,queue:[],idx:0,done:false,right:0,answered:false,fresh:true};
function buildP(){
  const pool=all.filter(q=>P.topic==='all'||q.topic===P.topic);
  if(P.mode==='review'){const w=new Set(wrongIds());P.queue=shuffle(pool.filter(q=>w.has(q.id)))}
  else{const c={};logs().forEach(e=>c[e.id]=(c[e.id]||0)+1);P.queue=shuffle(pool.slice()).sort((a,b)=>(c[a.id]||0)-(c[b.id]||0))}
  if(P.len)P.queue=P.queue.slice(0,P.len);P.idx=0;P.done=false;P.right=0;P.answered=false;P.fresh=false;
}
function vPractise(){
  if(P.fresh)buildP();const w=wrongIds().length;
  $('#view').innerHTML=`<div class="chips">${topicSel('t',P.topic)}<select id="n" aria-label="Number of questions">${[5,10,20,0].map(n=>`<option value="${n}"${P.len===n?' selected':''}>${n?n+' questions':'Until I stop'}</option>`).join('')}</select><button class="chip" id="rv" aria-pressed="${P.mode==='review'}">Mistakes${w?' ('+w+')':''}</button></div><div class="prog"><span id="cnt"></span><i><b id="bar"></b></i></div><article id="q"></article>`;
  $('#t').onchange=e=>{P.topic=e.target.value;buildP();vPractise()};
  $('#n').onchange=e=>{P.len=+e.target.value;buildP();vPractise()};
  $('#rv').onclick=()=>{P.mode=P.mode==='review'?'practice':'review';buildP();vPractise()};
  drawQ();
}
function drawQ(){
  const box=$('#q'),n=P.queue.length;$('#bar').style.width=(n?(P.idx+(P.answered?1:0))/n*100:0)+'%';
  $('#cnt').textContent=n&&!P.done?(P.len?`Question ${P.idx+1} of ${n}`:`Question ${P.idx+1}`):'';
  if(!all.length){box.innerHTML='<p class="empty">The question bank could not be loaded. Keep data/questions.js next to index.html.</p>';return}
  if(!n){box.innerHTML=`<p class="empty">${P.mode==='review'?'No mistakes to review. Questions you get wrong will show up here.':'No questions for this choice.'}</p>`;return}
  if(P.done){box.innerHTML=`<p class="meta">Finished</p><div class="big">${P.right} of ${n}</div><p class="empty">${P.mode==='review'?'Questions you got right have left your mistakes list.':'Go again for a new order. Questions you have seen least come first.'}</p><div class="row"><button class="primary" id="again">Go again</button></div>`;$('#again').onclick=()=>{buildP();vPractise()};return}
  const q=P.queue[P.idx];
  box.innerHTML=`<p class="meta">${q.topic} · ${q.difficulty||''}</p><div class="qtext">${R(q.question)}</div><div class="opts">${q.options.map(o=>optHTML(o)).join('')}</div><div id="fb" aria-live="polite"></div>`;
  box.querySelectorAll('.opt').forEach(b=>b.onclick=()=>answer(q,b.dataset.id));
  if(P.answered)show(q,P.pick);
}
function answer(q,pick){
  if(P.answered)return;P.answered=true;P.pick=pick;const right=pick===q.correctAnswer;if(right)P.right++;rec(q,right);save();show(q,pick);
}
function show(q,pick){
  const right=pick===q.correctAnswer;
  document.querySelectorAll('.opt').forEach(b=>{b.disabled=true;if(b.dataset.id===q.correctAnswer){b.classList.add('right');b.insertAdjacentHTML('beforeend',tickSVG)}else if(b.dataset.id===pick){b.classList.add('wrong');b.insertAdjacentHTML('beforeend',penSVG)}});
  const e=q.explanation,last=P.idx>=P.queue.length-1,fl=st.flags.includes(q.id);
  $('#fb').innerHTML=`<div class="verdict ${right?'good':'bad'}">${right?'Right. Here is why it works.':'Not quite. The answer is '+q.correctAnswer+'.'}</div>${q.concept?`<p class="meta">${E(q.concept)}</p>`:''}
  <div class="work"><ol>${e.steps.map(s=>`<li>${R(s)}</li>`).join('')}</ol></div>${!right&&e.commonMistake?`<p class="note"><b>Common slip:</b> ${R(e.commonMistake)}</p>`:''}
  <div class="row"><button class="btn" id="fl" aria-pressed="${fl}">${fl?'Flagged':'Flag question'}</button><button class="primary" id="next">${last?'Finish':'Next question'}</button></div>`;
  $('#bar').style.width=(P.idx+1)/P.queue.length*100+'%';
  $('#fl').onclick=ev=>{const i=st.flags.indexOf(q.id);if(i<0)st.flags.push(q.id);else st.flags.splice(i,1);save();ev.target.textContent=i<0?'Flagged':'Flag question'};
  $('#next').onclick=()=>{P.answered=false;P.pick=null;if(last)P.done=true;else P.idx++;drawQ();window.scrollTo(0,0)};$('#next').focus({preventScroll:true});
}
/* ---------- Topics ---------- */
function readiness(t){
  const a=logs().filter(e=>e.topic===t);if(a.length<5)return a.length?['Just started','']:['Not started',''];
  const r=a.slice(-10),p=r.filter(e=>e.ok).length/r.length;return p>=.8?['Solid','s']:p>=.5?['Getting there','']:['Needs work',''];
}
function vTopics(){
  $('#view').innerHTML=`<h2>Topics</h2><ul class="list">${TOPICS.map(t=>{const a=logs().filter(e=>e.topic===t),n=all.filter(q=>q.topic===t).length,seen=new Set(a.map(e=>e.id)).size,r=readiness(t);return `<li><a href="#/practise" data-t="${E(t)}"><span>${t}<br><small>${seen} of ${n} seen</small></span><span class="tag ${r[1]}">${r[0]}</span></a></li>`}).join('')}</ul>`;
  document.querySelectorAll('[data-t]').forEach(a=>a.onclick=()=>{P.topic=a.dataset.t;P.mode='practice';P.fresh=true});
}
/* ---------- Mock ---------- */
const MK='mts101a1.mock';
const M={phase:'setup',kind:'standard',topic:TOPICS[0],qs:[],ans:{},i:0,end:0,mins:20,secs:0,timeUp:false,tm:null};
const saveM=()=>{try{if(M.phase==='run')localStorage.setItem(MK,JSON.stringify({kind:M.kind,topic:M.topic,ids:M.qs.map(q=>q.id),ans:M.ans,i:M.i,end:M.end,mins:M.mins}));else localStorage.removeItem(MK)}catch(e){}};
function pickBalanced(n){
  const base=Math.floor(n/TOPICS.length),per={};TOPICS.forEach(t=>per[t]=base);
  shuffle(TOPICS.slice()).slice(0,n-base*TOPICS.length).forEach(t=>per[t]++);
  const out=[];TOPICS.forEach(t=>out.push(...shuffle(all.filter(q=>q.topic===t)).slice(0,per[t])));
  if(out.length<n){const u=new Set(out.map(q=>q.id));out.push(...shuffle(all.filter(q=>!u.has(q.id))).slice(0,n-out.length))}
  return shuffle(out);
}
function vMock(){
  const v=$('#view'),std=M.kind==='standard';
  if(M.phase==='setup'){
    v.innerHTML=`<h2>Mock test</h2><div class="chips"><button class="chip" id="k1" aria-pressed="${std}">Standard</button><button class="chip" id="k2" aria-pressed="${!std}">Single topic</button></div><p class="meta">${std?'30 questions from all nine topics in 20 minutes.':'10 questions from one topic in 7 minutes.'} No answers are shown until you submit, and you can submit at any time.</p>${std?'':`<div class="chips"><select id="mt" aria-label="Topic">${TOPICS.map(t=>`<option value="${E(t)}"${M.topic===t?' selected':''}>${t}</option>`).join('')}</select></div>`}<div class="row"><button class="primary" id="go">Start</button></div>`;
    $('#k1').onclick=()=>{M.kind='standard';vMock()};$('#k2').onclick=()=>{M.kind='topic';vMock()};
    const mt=$('#mt');if(mt)mt.onchange=e=>M.topic=e.target.value;
    $('#go').onclick=()=>{const qs=std?pickBalanced(30):shuffle(all.filter(q=>q.topic===M.topic)).slice(0,10);if(!qs.length)return;
      M.qs=qs;M.ans={};M.i=0;M.mins=std?20:Math.max(1,Math.round(qs.length*.7));M.end=Date.now()+M.mins*60000;M.timeUp=false;M.phase='run';saveM();clearInterval(M.tm);M.tm=setInterval(tick,1000);vMock()};
    return}
  const n=M.qs.length;
  if(M.phase==='run'){const q=M.qs[M.i],got=Object.keys(M.ans).length,last=M.i===n-1;
    v.innerHTML=`<div class="prog"><span>Question ${M.i+1} of ${n} · ${got} answered · <span id="tm"></span></span></div><div class="grid" role="group" aria-label="Jump to question">${M.qs.map((x,i)=>`<button data-j="${i}" class="${M.ans[x.id]?'a':''}"${i===M.i?' aria-current="true"':''}>${i+1}</button>`).join('')}</div><p class="meta">${q.topic}</p><div class="qtext">${R(q.question)}</div><div class="opts">${q.options.map(o=>optHTML(o,` aria-pressed="${M.ans[q.id]===o.id}"`)).join('')}</div><div class="row"><button class="btn" id="bk"${M.i?'':' disabled'}>Back</button><button class="btn" id="nx"${last?' disabled':''}>Next</button><button class="primary" id="sb">Submit test</button></div>`;
    v.querySelectorAll('[data-j]').forEach(b=>b.onclick=()=>{M.i=+b.dataset.j;saveM();vMock()});
    v.querySelectorAll('.opt').forEach(b=>b.onclick=()=>{M.ans[q.id]=b.dataset.id;saveM();vMock()});
    $('#bk').onclick=()=>{M.i--;saveM();vMock()};$('#nx').onclick=()=>{M.i++;saveM();vMock()};
    $('#sb').onclick=()=>{const un=n-got;if(confirm(un?`${un} question${un>1?'s':''} unanswered. Submit now?`:'Submit your test?'))finish(false)};tick();return}
  const sc=M.qs.filter(q=>M.ans[q.id]===q.correctAnswer).length,un=M.qs.filter(q=>!M.ans[q.id]).length;
  v.innerHTML=`<p class="meta">${M.timeUp?"Time's up. ":''}Mock test finished${M.secs?' in '+Math.floor(M.secs/60)+' min '+M.secs%60+' s':''}</p><div class="big">${sc} of ${n}</div><p class="empty">${un?un+' unanswered. ':''}Open any question to see the working.</p>${M.qs.map((q,i)=>{const a=M.ans[q.id],g=a===q.correctAnswer;return `<details><summary>${i+1}. ${g?'Right':a?'Wrong':'Unanswered'} · ${q.topic}</summary><div class="qtext">${R(q.question)}</div><p class="meta">You chose ${a||'nothing'}. Correct: ${q.correctAnswer}.</p><div class="work"><ol>${q.explanation.steps.map(s=>`<li>${R(s)}</li>`).join('')}</ol></div></details>`}).join('')}<div class="row"><button class="primary" id="new">New test</button></div>`;
  $('#new').onclick=()=>{M.phase='setup';vMock()};
}
function tick(){const s=Math.max(0,Math.round((M.end-Date.now())/1000));const el=$('#tm');if(el)el.textContent=Math.floor(s/60)+':'+String(s%60).padStart(2,'0')+' left';if(s<=0&&M.phase==='run')finish(true)}
function finish(auto){
  clearInterval(M.tm);M.timeUp=!!auto;M.secs=Math.min(M.mins*60,Math.max(1,Math.round((Date.now()-(M.end-M.mins*60000))/1000)));
  M.qs.forEach(q=>{if(M.ans[q.id])rec(q,M.ans[q.id]===q.correctAnswer)});
  st.mocks.push({t:Date.now(),score:M.qs.filter(q=>M.ans[q.id]===q.correctAnswer).length,n:M.qs.length,secs:M.secs,topic:M.kind==='topic'?M.topic:'All topics'});if(st.mocks.length>200)st.mocks=st.mocks.slice(-200);
  save();M.phase='result';saveM();if(location.hash==='#/mock')vMock();
}
(function resume(){try{const r=JSON.parse(localStorage.getItem(MK));if(!r||!Array.isArray(r.ids))return;const qs=r.ids.map(id=>byId[id]).filter(Boolean);if(!qs.length)return;
  Object.assign(M,{kind:r.kind==='topic'?'topic':'standard',topic:TOPICS.includes(r.topic)?r.topic:TOPICS[0],qs,ans:r.ans||{},i:Math.min(r.i||0,qs.length-1),end:r.end,mins:r.mins||20,phase:'run'});
  if(Date.now()>=M.end)finish(true);else M.tm=setInterval(tick,1000)}catch(e){}})();
/* ---------- Progress ---------- */
function vProgress(){
  const L=logs(),n=L.length,c=L.filter(e=>e.ok).length,w=wrongIds().length,fl=st.flags.filter(id=>byId[id]);
  $('#view').innerHTML=`<h2>Progress</h2><p><b>${n}</b> attempted · <b>${c}</b> correct · <b>${n-c}</b> incorrect · accuracy <b>${n?Math.round(c/n*100)+'%':'–'}</b> · <b>${w}</b> to retry</p>
  <table><thead><tr><th>Topic</th><th>Tried</th><th>Accuracy</th></tr></thead><tbody>${TOPICS.map(t=>{const a=L.filter(e=>e.topic===t),k=a.filter(e=>e.ok).length;return `<tr><td>${t}</td><td>${a.length}</td><td>${a.length?Math.round(k/a.length*100)+'%':'–'}</td></tr>`}).join('')}</tbody></table>
  <h3>Recent</h3><ul class="list">${L.slice(-6).reverse().map(e=>`<li><span class="it"><span>${E(e.topic)}<br><small>${new Date(e.t).toLocaleDateString()}</small></span><span class="tag">${e.ok?'Correct':'Incorrect'}</span></span></li>`).join('')||'<li class="empty">Nothing yet.</li>'}</ul>
  <h3>Mock tests</h3><ul class="list">${st.mocks.slice(-5).reverse().map(m=>`<li><span class="it"><span>${E(m.topic||'All topics')}<br><small>${new Date(m.t).toLocaleDateString()} · ${Math.floor(m.secs/60)} min ${m.secs%60} s</small></span><span class="tag">${m.score} / ${m.n}</span></span></li>`).join('')||'<li class="empty">No mock tests yet.</li>'}</ul><h3>Flagged questions</h3>${fl.length?`<ul class="list">${fl.map(id=>`<li><span class="it"><span>${id}<br><small>${E(byId[id].question.replace(/\$/g,'').slice(0,70))}</small></span><button class="btn" data-u="${id}">Unflag</button></span></li>`).join('')}</ul><div class="row"><button class="btn" id="cp">Copy flagged list</button></div>`:'<p class="empty">Flag a question after answering it, and it will be listed here.</p>'}
  <h3>Your data</h3><p class="meta">Everything is saved on this device only.</p><div class="row"><button class="btn" id="bu">Back up to file</button><button class="btn" id="rs">Restore</button><input type="file" id="fi" accept=".json" hidden></div><div class="row"><button class="btn danger" id="rz">Reset progress</button></div>
  <p class="meta" style="margin-top:1.4rem">Original practice questions, not past examination papers.${skipped?' '+skipped+' malformed question(s) skipped.':''}</p>`;
  document.querySelectorAll('[data-u]').forEach(b=>b.onclick=()=>{st.flags=st.flags.filter(x=>x!==b.dataset.u);save();vProgress()});
  const cp=$('#cp');if(cp)cp.onclick=()=>{const t=fl.map(id=>id+': '+byId[id].question.replace(/\$/g,'')).join('\n');(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>cp.textContent='Copied',()=>prompt('Copy this list:',t))};
  $('#bu').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify({app:'mts101a1',...st})],{type:'application/json'}));a.download='mts101-progress.json';a.click()};
  $('#rs').onclick=()=>$('#fi').click();
  $('#fi').onchange=e=>{const f=e.target.files[0];if(!f)return;f.text().then(t=>{const r=JSON.parse(t);if(!Array.isArray(r.log))throw 0;if(confirm('Replace the progress on this device with this file?')){st=adopt(r);save();P.fresh=true;vProgress()}}).catch(()=>alert('That file is not a valid progress backup.'))};
  $('#rz').onclick=()=>{if(confirm('Delete all progress on this device? This cannot be undone.')){st={log:[],flags:[],mocks:[]};save();P.fresh=true;vProgress()}};
}
/* ---------- Router ---------- */
const V={practise:vPractise,topics:vTopics,mock:vMock,progress:vProgress};
function route(){const k=(location.hash.match(/^#\/(\w+)/)||[])[1];const name=V[k]?k:'practise';
  document.querySelectorAll('#nav a').forEach(a=>a.setAttribute('aria-current',a.getAttribute('href')==='#/'+name?'page':'false'));V[name]();window.scrollTo(0,0)}
addEventListener('hashchange',route);route();
if('serviceWorker'in navigator&&/^https?:/.test(location.protocol))navigator.serviceWorker.register('sw.js').catch(()=>{});
})();
