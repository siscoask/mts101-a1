/* Tiny LaTeX-subset -> MathML renderer (frac, sqrt, ^, _, Greek, sets, trig names). No dependencies. */
(function(root){
const G={pi:'π',theta:'θ',alpha:'α',beta:'β',gamma:'γ',cup:'∪',cap:'∩',in:'∈',cdot:'·',times:'×',le:'≤',ge:'≥',infty:'∞',sum:'∑',ne:'≠',pm:'±',circ:'°',div:'÷',dots:'…',setminus:'∖'};
const esc=t=>t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
function tex(s){
  let i=0;
  const seq=end=>{let o='';while(i<s.length&&s[i]!==end)o+=item();return o};
  const group=()=>{if(s[i]==='{'){i++;const r=seq('}');i++;return `<mrow>${r}</mrow>`}return atom()};
  function atom(){
    const c=s[i];
    if(c==='\\'){
      let j=i+1;while(j<s.length&&/[a-zA-Z]/.test(s[j]))j++;
      if(j===i+1){const ch=s[j]||'';i=j+1;return ch===','||ch===' '?'<mspace width="0.17em"></mspace>':`<mo>${esc(ch)}</mo>`}
      const cmd=s.slice(i+1,j);i=j;
      if(cmd==='frac'){const a=group(),b=group();return `<mfrac>${a}${b}</mfrac>`}
      if(cmd==='sqrt')return `<msqrt>${group()}</msqrt>`;
      if(cmd==='mathcal'){const g=group();return `<mi>${g.replace(/<[^>]+>/g,'')==='U'?'𝒰':'U'}</mi>`}
      if(['sin','cos','tan'].includes(cmd))return `<mi mathvariant="normal">${cmd}</mi><mo>&#8289;</mo>`;
      if(cmd==='left'||cmd==='right'){const ch=s[i++];return `<mo>${esc(ch==='.'?'':ch)}</mo>`}
      if(cmd==='binom'){const a=group(),b=group();return `<mo>(</mo><mfrac linethickness="0">${a}${b}</mfrac><mo>)</mo>`}
      const g=G[cmd]||cmd;
      return '∑∪∩∈·×≤≥≠±÷∖'.includes(g)?`<mo>${g}</mo>`:`<mi>${g}</mi>`;
    }
    if(/\d/.test(c)){let j=i;while(j<s.length&&/[\d.]/.test(s[j]))j++;const t=s.slice(i,j);i=j;return `<mn>${t}</mn>`}
    if(/[a-zA-Z]/.test(c)){i++;return `<mi>${c}</mi>`}
    if(c===' '){i++;return ''}
    i++;return `<mo>${esc(c==='-'?'−':c)}</mo>`;
  }
  function item(){
    const b=group();let sub='',sup='';
    while(s[i]==='_'||s[i]==='^'){const t=s[i++],g=group();if(t==='_')sub=g;else sup=g}
    return sub&&sup?`<msubsup>${b}${sub}${sup}</msubsup>`:sub?`<msub>${b}${sub}</msub>`:sup?`<msup>${b}${sup}</msup>`:b;
  }
  return `<math>${seq('\0')}</math>`;
}
function render(str){return String(str).split(/(\$[^$]+\$)/).map(p=>p[0]==='$'&&p.length>2?tex(p.slice(1,-1)):esc(p)).join('')}
root.MatMath={render,tex};
if(typeof module!=='undefined')module.exports=root.MatMath;
})(typeof window!=='undefined'?window:globalThis);
