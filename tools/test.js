// Node checks: every question's math converts to well-formed MathML; data sanity.
const fs=require('fs');const M=require('../js/math.js');const Q=JSON.parse(fs.readFileSync(__dirname+'/../data/questions.json','utf8'));
let bad=0;const chk=(id,s)=>{const h=M.render(s);const st=[];for(const t of h.matchAll(/<(\/?)([a-z]+)[^>]*?(\/?)>/g)){if(t[3])continue;if(!t[1])st.push(t[2]);else if(st.pop()!==t[2]){bad++;console.log('mismatch',id,s);return}}if(st.length||/\\[a-z]/.test(h.replace(/<[^>]+>/g,''))||/\$/.test(h)){bad++;console.log('bad',id,s)}};
for(const q of Q){chk(q.id,q.question);q.options.forEach(o=>chk(q.id,o.text));q.explanation.steps.forEach(s=>chk(q.id,s));chk(q.id,q.explanation.commonMistake)}
console.log('questions',Q.length,'math problems',bad);process.exit(bad?1:0);
