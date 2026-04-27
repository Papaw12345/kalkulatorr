import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AXIOM Calculator",
    page_icon="⬡",
    layout="centered",
)

CALCULATOR_HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;700;800&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

:root{
  --bg0:#0a0b0f;
  --bg1:#111318;
  --bg2:#181b22;
  --bg3:#1f232e;
  --bg4:#272c39;
  --line:rgba(255,255,255,0.07);
  --line2:rgba(255,255,255,0.12);
  --text1:#ecedf2;
  --text2:#8b8fa8;
  --text3:#555870;
  --acc:#c8f54a;       /* lime acid green */
  --acc2:#7b68ee;      /* medium slate purple */
  --acc3:#ff6b6b;      /* coral red for clear */
  --acc-dim:rgba(200,245,74,0.12);
  --acc2-dim:rgba(123,104,238,0.12);
  --mono:'DM Mono',monospace;
  --sans:'Syne',sans-serif;
  --r:14px;
}

body{
  background:var(--bg0);
  min-height:100vh;
  display:flex;
  justify-content:center;
  align-items:flex-start;
  padding:28px 12px 48px;
  font-family:var(--sans);
}

/* ── Shell ── */
.shell{
  width:400px;
  background:var(--bg1);
  border-radius:24px;
  border:1px solid var(--line2);
  overflow:hidden;
  position:relative;
}

/* top ambient glow strip */
.shell::before{
  content:'';
  position:absolute;
  top:0;left:50%;transform:translateX(-50%);
  width:60%;height:1px;
  background:linear-gradient(90deg,transparent,var(--acc),transparent);
  opacity:.6;
}

/* ── Top Bar ── */
.topbar{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:18px 22px 14px;
  border-bottom:1px solid var(--line);
}
.brand{
  display:flex;align-items:center;gap:10px;
}
.brand-hex{
  width:28px;height:28px;
  background:var(--acc);
  clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
  display:flex;align-items:center;justify-content:center;
  flex-shrink:0;
}
.brand-dot{
  width:8px;height:8px;
  background:var(--bg0);
  clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
}
.brand-name{
  font-family:var(--sans);
  font-weight:800;
  font-size:15px;
  letter-spacing:3px;
  color:var(--text1);
}
.chip{
  font-size:9px;
  font-weight:700;
  letter-spacing:2px;
  color:var(--text3);
  border:1px solid var(--line2);
  padding:4px 10px;
  border-radius:20px;
  text-transform:uppercase;
}

/* ── Display ── */
.disp{
  margin:18px 20px 12px;
  background:var(--bg0);
  border-radius:16px;
  border:1px solid var(--line);
  padding:20px 22px 18px;
  position:relative;
  min-height:110px;
  display:flex;
  flex-direction:column;
  justify-content:flex-end;
  align-items:flex-end;
  overflow:hidden;
}
/* corner accent */
.disp::after{
  content:'';
  position:absolute;
  bottom:0;right:0;
  width:80px;height:80px;
  background:radial-gradient(circle at 100% 100%, var(--acc-dim), transparent 70%);
  pointer-events:none;
}
.disp-mode{
  position:absolute;
  top:12px;left:16px;
  font-size:9px;
  letter-spacing:2px;
  color:var(--text3);
  font-family:var(--mono);
}
.disp-hist{
  font-family:var(--mono);
  font-size:12px;
  color:var(--text3);
  min-height:18px;
  word-break:break-all;
  text-align:right;
  margin-bottom:8px;
  transition:color .3s;
}
.disp-num{
  font-family:var(--mono);
  font-size:42px;
  font-weight:300;
  color:var(--text1);
  word-break:break-all;
  text-align:right;
  letter-spacing:-2px;
  line-height:1;
  transition:transform .12s ease, color .2s;
}
.disp-num.flash{
  transform:scale(1.05);
  color:var(--acc);
}

/* ── Secondary info strip ── */
.disp-strip{
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:8px 22px 0;
  margin:0 20px;
}
.strip-angle{
  font-family:var(--mono);
  font-size:10px;
  color:var(--text3);
  letter-spacing:1px;
}
.angle-toggle{
  display:flex;
  border:1px solid var(--line2);
  border-radius:20px;
  overflow:hidden;
}
.angle-btn{
  font-family:var(--mono);
  font-size:9px;
  letter-spacing:1px;
  padding:4px 10px;
  background:transparent;
  border:none;
  color:var(--text3);
  cursor:pointer;
  transition:background .15s,color .15s;
}
.angle-btn.active{
  background:var(--acc-dim);
  color:var(--acc);
}

/* ── Grid ── */
.grid{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:8px;
  padding:14px 20px 22px;
}

/* ── Base Button ── */
.btn{
  font-family:var(--sans);
  font-weight:700;
  font-size:15px;
  height:62px;
  border:1px solid var(--line);
  border-radius:var(--r);
  cursor:pointer;
  outline:none;
  user-select:none;
  position:relative;
  overflow:hidden;
  transition:background .12s, border-color .12s, transform .07s;
  letter-spacing:.5px;
}
.btn::after{
  content:'';
  position:absolute;inset:0;
  background:rgba(255,255,255,0);
  transition:background .08s;
}
.btn:active::after{background:rgba(255,255,255,0.06)}
.btn:active{transform:scale(0.91)}

/* Number */
.n{background:var(--bg3);color:var(--text1);}
.n:hover{background:var(--bg4);border-color:var(--line2);}

/* Operator */
.op{background:var(--bg2);color:var(--acc2);font-size:18px;}
.op:hover{background:var(--acc2-dim);border-color:rgba(123,104,238,.25);}

/* Scientific */
.sci{background:var(--bg2);color:var(--text2);font-size:12px;font-family:var(--mono);font-weight:400;}
.sci:hover{background:var(--bg3);}

/* Equals */
.eq{
  background:var(--acc);
  color:var(--bg0);
  font-size:22px;
  border-color:transparent;
}
.eq:hover{filter:brightness(1.08);}

/* Clear */
.cl{background:rgba(255,107,107,.12);color:var(--acc3);border-color:rgba(255,107,107,.2);}
.cl:hover{background:rgba(255,107,107,.2);}

/* Wide */
.w2{grid-column:span 2;}

/* ── Separator ── */
.sep{grid-column:1/-1;height:1px;background:var(--line);margin:2px 0;}

/* ── Ripple ── */
@keyframes ripple{
  from{transform:scale(0);opacity:.3}
  to{transform:scale(3);opacity:0}
}
.ripple-el{
  position:absolute;
  border-radius:50%;
  background:rgba(255,255,255,.3);
  width:60px;height:60px;
  pointer-events:none;
  animation:ripple .4s ease-out forwards;
  transform:scale(0);
}
</style>
</head>
<body>

<div class="shell">

  <!-- Top Bar -->
  <div class="topbar">
    <div class="brand">
      <div class="brand-hex"><div class="brand-dot"></div></div>
      <span class="brand-name">AXIOM</span>
    </div>
    <span class="chip">Scientific</span>
  </div>

  <!-- Display -->
  <div class="disp">
    <span class="disp-mode">RAD</span>
    <div class="disp-hist" id="hist"></div>
    <div class="disp-num" id="num">0</div>
  </div>

  <!-- Angle mode toggle -->
  <div class="disp-strip">
    <span class="strip-angle">angle mode</span>
    <div class="angle-toggle">
      <button class="angle-btn active" id="btn-rad" onclick="setAngle('rad')">RAD</button>
      <button class="angle-btn"        id="btn-deg" onclick="setAngle('deg')">DEG</button>
    </div>
  </div>

  <!-- Button Grid -->
  <div class="grid">

    <!-- Row 1: Scientific -->
    <button class="btn sci" onclick="ins('Math.sin(','sin(')">sin</button>
    <button class="btn sci" onclick="ins('Math.cos(','cos(')">cos</button>
    <button class="btn sci" onclick="ins('Math.tan(','tan(')">tan</button>
    <button class="btn sci" onclick="ins('Math.log10(','log(')">log</button>

    <!-- Row 2: More sci -->
    <button class="btn sci" onclick="ins('Math.sqrt(','√(')">√x</button>
    <button class="btn sci" onclick="ins('Math.pow(','pow(')">xⁿ</button>
    <button class="btn sci" onclick="ins('Math.PI','π')">π</button>
    <button class="btn sci" onclick="ins('Math.E','e')">e</button>

    <div class="sep"></div>

    <!-- Row 3: AC ( ) ÷ -->
    <button class="btn cl"  onclick="ac()">AC</button>
    <button class="btn op"  onclick="ch('(',  '('  )">(</button>
    <button class="btn op"  onclick="ch(')',  ')'  )">)</button>
    <button class="btn op"  onclick="ch('/',  '÷'  )">÷</button>

    <!-- Row 4: 7 8 9 × -->
    <button class="btn n"   onclick="ch('7','7')">7</button>
    <button class="btn n"   onclick="ch('8','8')">8</button>
    <button class="btn n"   onclick="ch('9','9')">9</button>
    <button class="btn op"  onclick="ch('*',  '×'  )">×</button>

    <!-- Row 5: 4 5 6 − -->
    <button class="btn n"   onclick="ch('4','4')">4</button>
    <button class="btn n"   onclick="ch('5','5')">5</button>
    <button class="btn n"   onclick="ch('6','6')">6</button>
    <button class="btn op"  onclick="ch('-',  '−'  )">−</button>

    <!-- Row 6: 1 2 3 + -->
    <button class="btn n"   onclick="ch('1','1')">1</button>
    <button class="btn n"   onclick="ch('2','2')">2</button>
    <button class="btn n"   onclick="ch('3','3')">3</button>
    <button class="btn op"  onclick="ch('+',  '+'  )">+</button>

    <!-- Row 7: 0 . = -->
    <button class="btn n w2" onclick="ch('0','0')">0</button>
    <button class="btn n"    onclick="ch('.','.')">.</button>
    <button class="btn eq"   onclick="calc()">=</button>

  </div>
</div>

<script>
// ── State ──────────────────────────────────────────────
let expr     = "";      // evaluatable expression
let disp     = "";      // display string
let angleMode= "rad";   // "rad" | "deg"
let freshCalc= false;   // just finished calc?

// ── DOM ────────────────────────────────────────────────
const elNum  = document.getElementById("num");
const elHist = document.getElementById("hist");
const elMode = document.querySelector(".disp-mode");

// ── Render ─────────────────────────────────────────────
function render(){
  elNum.textContent  = disp || "0";
  elHist.textContent = "";
}

// ── Flash animation ────────────────────────────────────
function flash(){
  elNum.classList.remove("flash");
  void elNum.offsetWidth;
  elNum.classList.add("flash");
  setTimeout(()=>elNum.classList.remove("flash"),250);
}

// ── Ripple on button ───────────────────────────────────
function ripple(btn, e){
  const r = document.createElement("span");
  r.className = "ripple-el";
  const rect = btn.getBoundingClientRect();
  r.style.left = (e.clientX - rect.left - 30)+"px";
  r.style.top  = (e.clientY - rect.top  - 30)+"px";
  btn.appendChild(r);
  setTimeout(()=>r.remove(), 450);
}

// ── Append plain char ──────────────────────────────────
function ch(evalChar, dispChar){
  if(freshCalc){
    if(/^[0-9.]$/.test(evalChar)){ expr=""; disp=""; }
    freshCalc = false;
  }
  expr += evalChar;
  disp += dispChar;
  render();
}

// ── Insert scientific function ─────────────────────────
function ins(evalStr, dispStr){
  freshCalc = false;
  expr += evalStr;
  disp += dispStr;
  render();
}

// ── All clear ─────────────────────────────────────────
function ac(){
  expr=""; disp=""; freshCalc=false;
  elHist.textContent="";
  elNum.textContent="0";
}

// ── Angle mode ────────────────────────────────────────
function setAngle(mode){
  angleMode = mode;
  elMode.textContent = mode.toUpperCase();
  document.getElementById("btn-rad").classList.toggle("active", mode==="rad");
  document.getElementById("btn-deg").classList.toggle("active", mode==="deg");
}

// ── Normalize for prank check ─────────────────────────
function norm(e){ return e.replace(/\s+/g,"").toLowerCase(); }

// ── Prank logic (hidden hardcode) ─────────────────────
function prank(raw){
  const n = norm(raw);
  if(n==="306000+316000"||n==="316000+306000") return "1.000.000";
  if(n==="306+316"       ||n==="316+306"      ) return "1.000";
  return null;
}

// ── Wrap trig for DEG mode ────────────────────────────
function buildEvalExpr(rawExpr){
  if(angleMode === "rad") return rawExpr;
  // Replace Math.sin/cos/tan with degree-converted versions
  return rawExpr
    .replace(/Math\.sin\(/g, "Math.sin((Math.PI/180)*")
    .replace(/Math\.cos\(/g, "Math.cos((Math.PI/180)*")
    .replace(/Math\.tan\(/g, "Math.tan((Math.PI/180)*");
}

// ── Calculate ─────────────────────────────────────────
function calc(){
  if(!expr) return;

  // 1. Prank check first
  const pranked = prank(expr);
  if(pranked !== null){
    elHist.textContent = disp + " =";
    elNum.textContent  = pranked;
    flash();
    freshCalc = true;
    expr      = pranked.replace(/\./g,"");
    disp      = pranked;
    return;
  }

  // 2. Normal evaluation
  try{
    const safeExpr  = buildEvalExpr(expr);
    // eslint-disable-next-line no-new-func
    const raw       = new Function("return "+safeExpr)();
    if(!isFinite(raw)) throw new Error("Non-finite");

    const formatted = parseFloat(raw.toPrecision(12)).toString();

    elHist.textContent = disp + " =";
    elNum.textContent  = formatted;
    flash();

    freshCalc = true;
    expr      = formatted;
    disp      = formatted;
  }catch{
    elHist.textContent = disp;
    elNum.textContent  = "Error";
    setTimeout(ac, 1200);
  }
}

// ── Keyboard support ──────────────────────────────────
document.addEventListener("keydown", e => {
  if(/^[0-9]$/.test(e.key))          ch(e.key, e.key);
  else if(e.key==="+")               ch("+","+");
  else if(e.key==="-")               ch("-","−");
  else if(e.key==="*")               ch("*","×");
  else if(e.key==="/"){e.preventDefault(); ch("/","÷");}
  else if(e.key===".")               ch(".",".");
  else if(e.key==="(")               ch("(","(");
  else if(e.key===")")               ch(")",")" );
  else if(e.key==="Enter"||e.key==="=") calc();
  else if(e.key==="Escape")          ac();
  else if(e.key==="Backspace"){
    expr=expr.slice(0,-1);
    disp=disp.slice(0,-1);
    render();
  }
});

// Ripple event on all buttons
document.querySelectorAll(".btn").forEach(btn=>{
  btn.addEventListener("pointerdown", e => ripple(btn, e));
});
</script>

</body>
</html>
"""

components.html(CALCULATOR_HTML, height=820, scrolling=False)
