"""Reconstroi o slide 3 (harness) de dist/apresentacao-pcc.html.

A cena 3D em canvas orbitava e reposicionava rotulos a cada quadro, o que
causava flicker e sobreposicao. Substitui por um diagrama SVG 2D com posicoes
fixas e remove as citacoes desse slide (pedido do autor, 2026-09-14).

Uso: python tools/slides_h3_2026-09-14.py
"""
from pathlib import Path

DECK = Path(__file__).resolve().parent.parent / "dist" / "apresentacao-pcc.html"

SECTION = r'''<!-- 3 HARNESS -->
<section class="slide" id="s-h3d" data-title="O que é um harness">
  <h2>O que é um <em>harness</em><small>clique no módulo ou tecle 0–5 para destacar</small></h2>
  <div class="row">
    <div class="col" id="h3d">
      <svg id="h3svg" viewBox="0 0 1020 760" role="img" aria-label="Diagrama: modelo de linguagem no centro, quatro módulos do harness em órbita e o proxy externo abaixo">
        <defs>
          <radialGradient id="h3core" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#fff6dd"/><stop offset=".4" stop-color="#ffd97a"/><stop offset=".72" stop-color="#f5b638"/><stop offset="1" stop-color="#9a6a18"/></radialGradient>
          <radialGradient id="h3halo"><stop offset="0" stop-color="#f5b638" stop-opacity=".45"/><stop offset=".55" stop-color="#f5b638" stop-opacity=".12"/><stop offset="1" stop-color="#f5b638" stop-opacity="0"/></radialGradient>
          <radialGradient id="h3vig" cx="50%" cy="50%" r="72%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
          <linearGradient id="h3card" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2a40"/><stop offset="1" stop-color="#0f1826"/></linearGradient>
          <linearGradient id="h3cardOn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe6a8"/><stop offset="1" stop-color="#f5b638"/></linearGradient>
          <pattern id="h3grid" width="46" height="46" patternUnits="userSpaceOnUse"><path d="M46 0H0V46" fill="none" stroke="rgba(148,170,200,.07)" stroke-width="1"/></pattern>
          <filter id="h3glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
        <rect width="1020" height="760" fill="url(#h3grid)"/>
        <g id="h3dust" class="h3dust" aria-hidden="true"></g>
        <circle cx="510" cy="360" r="330" fill="url(#h3halo)" opacity=".6"/>
        <g id="h3links" fill="none" stroke-linecap="round"></g>
        <g fill="none">
          <circle cx="510" cy="360" r="200" stroke="rgba(139,152,168,.18)" stroke-width="1.5"/>
          <circle cx="510" cy="360" r="250" stroke="rgba(245,182,56,.12)" stroke-width="12"/>
          <circle class="h3dash" cx="510" cy="360" r="250" stroke="rgba(245,182,56,.8)" stroke-width="3" stroke-dasharray="18 13"/>
        </g>
        <text x="510" y="84" text-anchor="middle" class="h3ringlab">◆  harness · andaime do agente</text>
        <g id="h3nodes"></g>
        <rect width="1020" height="760" fill="url(#h3vig)" pointer-events="none"/>
      </svg>
    </div>
    <div id="h3dpanel" class="card hi">
      <div class="h3-eyebrow"><span id="h3badge">0</span><span id="h3kicker">Núcleo · fixo em todos os braços</span></div>
      <h3 id="h3title">Modelo de linguagem</h3>
      <p id="h3text">Sem estado. Fixo em todos os braços. Tudo ao redor é o <em>harness</em>: componentes externos ao modelo e editáveis.</p>
      <div class="h3-div" aria-hidden="true"></div>
      <div class="chips" id="h3chips"></div>
      <div class="h3-meta"><span class="h3-hint">clique no módulo, no chip ou tecle 0–5</span><span class="h3-hint" id="h3count">1 / 6</span></div>
    </div>
  </div>
</section>

'''

CSS = r'''/* slide 3 — palco do harness (SVG 2D, sem órbita: posições fixas, sem flicker) */
#s-h3d{background:
  radial-gradient(900px 480px at 32% 62%,rgba(245,182,56,.08),transparent 60%),
  radial-gradient(700px 420px at 85% 20%,rgba(59,123,214,.10),transparent 60%)}
#h3d{position:relative;border-radius:20px;overflow:hidden;background:
  radial-gradient(ellipse at 50% 40%,#162032 0%,#0b0f14 72%);
  background-color:#0d131c;border:1px solid rgba(60,78,102,.6);box-shadow:inset 0 0 120px rgba(0,0,0,.55),0 24px 70px rgba(0,0,0,.4)}
#h3svg{position:absolute;inset:0;width:100%;height:100%;display:block}
#h3svg text{font-family:"Archivo","Segoe UI",sans-serif}
.h3ringlab{fill:rgba(245,182,56,.92);font-size:20px;font-weight:700;letter-spacing:.02em}
@keyframes h3dash{to{stroke-dashoffset:-310}}
@keyframes h3flow{to{stroke-dashoffset:-34}}
@keyframes h3twinkle{0%,100%{opacity:.12}50%{opacity:.5}}
@keyframes h3pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.04)}}
.h3dash{animation:h3dash 12s linear infinite}
.h3link{stroke:rgba(139,152,168,.32);stroke-width:2;stroke-dasharray:9 8;animation:h3flow 1.4s linear infinite;transition:stroke .25s,stroke-width .25s}
.h3link.proxy{stroke:rgba(123,216,143,.5)}
.h3link.on{stroke:#ffe19a;stroke-width:4;filter:url(#h3glow)}
.h3node{cursor:pointer;outline:none}
.h3node .box{fill:url(#h3card);stroke:rgba(90,110,135,.6);stroke-width:1.5;transition:stroke .2s}
.h3node:hover .box,.h3node:focus-visible .box{stroke:rgba(245,182,56,.8)}
.h3node .num{fill:#3b7bd6}.h3node .num.proxy{fill:#7bd88f}
.h3node .numt{fill:#0b0f14;font-family:Consolas,monospace;font-size:19px;font-weight:700}
.h3node .abbr{fill:#8b98a8;font-family:Consolas,monospace;font-size:16px;letter-spacing:.06em}
.h3node .name{fill:#e8edf2;font-size:22px;font-weight:600}
.h3node.on .box{fill:url(#h3cardOn);stroke:#fff;stroke-width:2.5;filter:url(#h3glow)}
.h3node.on .num{fill:#241a05}.h3node.on .numt{fill:#ffe19a}
.h3node.on .abbr{fill:rgba(36,26,5,.75)}.h3node.on .name{fill:#241a05;font-weight:700}
#h3core{cursor:pointer;outline:none;transform-origin:510px 360px;transform-box:view-box}
#h3core .halo{opacity:0;transition:opacity .3s}
#h3core.on .halo{opacity:1}
#h3core.on{animation:h3pulse 2.4s ease-in-out infinite}
#h3core:focus-visible .rim{stroke:#fff}
#h3core .lab{fill:#241a05;font-size:34px;font-weight:700}
#h3core .sub{fill:rgba(36,26,5,.82);font-size:17px;font-weight:600}
.h3dust circle{animation:h3twinkle 3s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){.h3dash,.h3link,#h3core.on,.h3dust circle{animation:none}}
#h3dpanel{width:600px;flex:none;overflow:hidden}
#h3dpanel h3{margin:10px 0 12px;font-size:40px;line-height:1.1;color:var(--fg);letter-spacing:-.01em}
#h3dpanel h3 em{color:var(--acc)}
#h3dpanel p{margin:0 0 14px;font-size:27px;line-height:1.42}
'''

JS = r'''// ---------- slide 3: diagrama do harness (SVG 2D, posições fixas; sem citações no slide) ----------
const H3=[
 {id:0,key:'core',abbr:'LLM',kick:'Núcleo · fixo em todos os braços',name:'Modelo de linguagem',text:'Sem estado. Fixo em todos os braços. Tudo ao redor é o <em>harness</em>: componentes externos ao modelo e editáveis.',x:510,y:360},
 {id:1,key:'sys',abbr:'SYS',kick:'Andaime · conduta do agente',name:'Prompt de sistema',text:'Molda o estilo de trabalho. Na Camada 1, pi envia 2.499 bytes; OpenCode, 9.738 (3,9×).',x:333,y:183},
 {id:2,key:'tool',abbr:'TOOL',kick:'Andaime · corpo do agente',name:'Ferramentas',text:'Expõem sistema de arquivos e shell ao modelo. Esquemas viajam a cada requisição: 4 no pi, 9 no OpenCode.',x:687,y:183},
 {id:3,key:'ctx',abbr:'CTX',kick:'Andaime · memória e limite',name:'Middleware de contexto',text:'Controla contexto, execução e recuperação: compactação, memória, permissões, verificação.',x:333,y:537},
 {id:4,key:'loop',abbr:'LOOP',kick:'Andaime · o motor',name:'Laço de execução',text:'Monta prompts, gerencia estado, invoca ferramentas, coordena o laço. Do ReAct mínimo ao planejamento com subagentes.',x:687,y:537},
 {id:5,key:'proxy',abbr:'PROXY',kick:'Instrumento · fora do harness',name:'Proxy externo',text:'Fora do <em>harness</em>: instrumento do projeto. Conta requisições, tokens e latência igual para os dois braços.',x:510,y:690,proxy:true}
];
let h3sel=0;
function h3select(i){
  h3sel=i;const c=H3[i];
  document.getElementById('h3title').innerHTML=c.name;
  document.getElementById('h3text').innerHTML=c.text;
  document.getElementById('h3badge').textContent=i;
  document.getElementById('h3kicker').textContent=c.kick;
  document.getElementById('h3count').textContent=(i+1)+' / '+H3.length;
  document.querySelectorAll('#h3chips .chip').forEach((ch,j)=>ch.classList.toggle('on',j===i));
  document.querySelectorAll('#h3svg [data-i]').forEach(el=>el.classList.toggle('on',+el.dataset.i===i));
}
(function(){
  const NS='http://www.w3.org/2000/svg';
  const el=(tag,attrs,parent)=>{const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);if(parent)parent.appendChild(e);return e;};
  const chips=document.getElementById('h3chips');
  H3.forEach((c,i)=>{const b=document.createElement('button');b.className='chip'+(i===0?' on':'');b.dataset.k=c.key;b.setAttribute('aria-label','Destacar '+c.name);b.innerHTML='<span class="dot" aria-hidden="true"></span><span><span class="n">'+i+' · '+c.abbr+'</span><br>'+c.name+'</span>';b.onclick=()=>h3select(i);chips.appendChild(b);});
  // poeira: posições fixas por semente, sem reposicionar por quadro
  const dust=document.getElementById('h3dust');
  let seed=7;const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647;};
  for(let k=0;k<60;k++){const d=el('circle',{cx:(rnd()*1020).toFixed(1),cy:(rnd()*760).toFixed(1),r:(0.8+rnd()*1.6).toFixed(2),fill:'#dce8f5'},dust);d.style.animationDelay=(-rnd()*3).toFixed(2)+'s';}
  const core=H3[0],links=document.getElementById('h3links'),nodes=document.getElementById('h3nodes');
  // conexões núcleo → módulo, atrás dos cartões
  H3.forEach(c=>{if(!c.id)return;el('line',{x1:core.x,y1:core.y,x2:c.x,y2:c.y,class:'h3link'+(c.proxy?' proxy':''),'data-i':c.id},links);});
  // núcleo
  const g=el('g',{id:'h3core','data-i':0,tabindex:0,role:'button','aria-label':'Destacar Modelo de linguagem'},nodes);
  el('circle',{class:'halo',cx:core.x,cy:core.y,r:150,fill:'url(#h3halo)'},g);
  el('circle',{class:'rim',cx:core.x,cy:core.y,r:104,fill:'#101825',stroke:'rgba(255,225,154,.6)','stroke-width':2.5},g);
  el('circle',{cx:core.x,cy:core.y,r:88,fill:'url(#h3core)'},g);
  el('text',{x:core.x,y:core.y+2,'text-anchor':'middle',class:'lab'},g).textContent='LLM';
  el('text',{x:core.x,y:core.y+30,'text-anchor':'middle',class:'sub'},g).textContent='modelo';
  // módulos e proxy
  H3.forEach(c=>{if(!c.id)return;const w=c.proxy?420:322,h=c.proxy?80:92;const x=c.x-w/2,y=c.y-h/2;
    const n=el('g',{class:'h3node','data-i':c.id,tabindex:0,role:'button','aria-label':'Destacar '+c.name},nodes);
    el('rect',{class:'box',x,y,width:w,height:h,rx:16},n);
    el('circle',{class:'num'+(c.proxy?' proxy':''),cx:x+34,cy:c.y,r:16},n);
    el('text',{class:'numt',x:x+34,y:c.y+7,'text-anchor':'middle'},n).textContent=c.id;
    el('text',{class:'abbr',x:x+64,y:c.y-11},n).textContent=c.abbr;
    el('text',{class:'name',x:x+64,y:c.y+17},n).textContent=c.name;
    if(c.proxy)el('text',{class:'abbr',x:x+w-22,y:c.y+6,'text-anchor':'end'},n).textContent='req · tok · ms';
    else ['#7bd88f','#f5b638','#5b9ae6'].forEach((col,k)=>el('circle',{cx:x+w-22-k*14,cy:y+16,r:4,fill:col},n));
  });
  const go=e=>{const t=e.target.closest('[data-i]');if(t)h3select(+t.dataset.i);};
  nodes.addEventListener('click',go);
  nodes.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();go(e);}});
  h3select(0);
  window.h3fallback=()=>{}; // SVG já é o caminho único: nada a rebaixar
})();

'''


def main() -> None:
    s = DECK.read_text(encoding="utf-8")
    a, b = s.index("<!-- 3 HARNESS"), s.index("<!-- 4 TEMA")
    s = s[:a] + SECTION + s[b:]
    a, b = s.index("/* 3d — palco do harness */"), s.index(".h3-eyebrow{")
    s = s[:a] + CSS + s[b:]
    s = s.replace("#h3src{border-left:3px solid rgba(245,182,56,.5);padding-left:14px}\n", "")
    s = s.replace("#fallback2d{display:none}\n", "")
    a, b = s.index("// ---------- slide 3: cena 3D"), s.index("// ---------- slide 5:")
    s = s[:a] + JS + s[b:]
    DECK.write_text(s, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
