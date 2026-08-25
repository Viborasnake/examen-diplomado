from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

css = r'''
.intro-evaluation{background:#F4F9FE;color:var(--navy)}
.intro-evaluation .intro-kicker{color:#5F7B8F}.intro-evaluation .intro-title{color:var(--blue)}.intro-evaluation .intro-sub{color:#60798A}
.intro-paperwork{background:#fff;color:var(--navy)}.intro-paperwork .intro-kicker{color:#60798A}.intro-paperwork .intro-title span{color:var(--blue)}.intro-paperwork .intro-sub{color:#60798A}
.intro-offers{background:#F3FBF5;color:#167C38}.intro-offers .intro-kicker{color:#368553}.intro-offers .intro-sub{color:#4F7560}
.intro-problem{background:#FFF8F2;color:#9A5A13}.intro-problem .intro-kicker{color:#A77740}.intro-problem .intro-sub{color:#7F6A51}
.intro-paused{background:#FFF3F3;color:#B42323}.intro-paused .intro-kicker{color:#B75A5A}.intro-paused .intro-sub{color:#8E5A5A}.intro-paused .intro-title{font-size:clamp(68px,9.4vw,154px)}
.intro-risk{background:#C62828;color:#fff}.intro-risk .intro-kicker{color:#FFD9D9}.intro-risk .intro-title{font-size:clamp(68px,9.4vw,154px)}.intro-risk .intro-sub{color:#fff;opacity:.94}
.intro-clock{display:flex;align-items:center;justify-content:center;gap:12px;margin:34px auto 0;font-weight:800;font-size:clamp(18px,1.6vw,26px)}.intro-clock i{width:13px;height:13px;border-radius:50%;background:currentColor;animation:introPulse 1.05s ease-in-out infinite}
'''

if '.intro-evaluation{' not in s:
    s = s.replace('</style>', css + '</style>')

new_intro = r'''<div id="introSequence" class="intro-sequence" aria-hidden="false">
  <section class="intro-state intro-dream active" data-intro="dream">
    <div class="intro-inner">
      <div class="intro-kicker">Ruta Segura</div>
      <h1 class="intro-title">Tu sueño de la<br><span>casa propia.</span></h1>
    </div>
  </section>
  <section class="intro-state intro-evaluation" data-intro="evaluation">
    <div class="intro-inner">
      <div class="intro-kicker">Evaluación hipotecaria</div>
      <h1 class="intro-title">Evaluando tu crédito</h1>
      <p class="intro-sub">Comienza la revisión de antecedentes.</p>
    </div>
  </section>
  <section class="intro-state intro-paperwork" data-intro="paperwork">
    <div class="intro-inner">
      <div class="intro-kicker">Proceso hipotecario</div>
      <h1 class="intro-title">Realizando<br><span>trámites</span></h1>
      <p class="intro-sub">Reúnes documentos y avanzas en el proceso.</p>
    </div>
  </section>
  <section class="intro-state intro-offers" data-intro="offers">
    <div class="intro-inner">
      <div class="intro-kicker">Proceso hipotecario</div>
      <h1 class="intro-title">Recibiendo ofertas</h1>
      <p class="intro-sub">La operación parece avanzar con normalidad.</p>
    </div>
  </section>
  <section class="intro-state intro-problem" data-intro="problem">
    <div class="intro-inner">
      <div class="intro-kicker">Pero aparece un problema</div>
      <h1 class="intro-title">Antecedentes comerciales</h1>
      <p class="intro-sub">Hay información que la persona no puede destrabar de inmediato.</p>
    </div>
  </section>
  <section class="intro-state intro-paused" data-intro="paused">
    <div class="intro-inner">
      <div class="intro-kicker">La evaluación se detiene</div>
      <h1 class="intro-title">CRÉDITO PAUSADO</h1>
      <p class="intro-sub">Mientras intenta resolverlo, empieza a correr el tiempo.</p>
      <div class="intro-clock"><i></i><span>La operación sigue perdiendo vigencia.</span></div>
    </div>
  </section>
  <section class="intro-state intro-risk" data-intro="risk">
    <div class="intro-inner">
      <div class="intro-kicker">El tiempo importa</div>
      <h1 class="intro-title">OPERACIÓN EN RIESGO</h1>
      <p class="intro-sub">Corregir el dato no sirve si la actualización no llega al banco a tiempo.</p>
    </div>
  </section>
</div>'''

pattern = re.compile(r'<div id="introSequence" class="intro-sequence".*?</div><main class="deck">', re.S)
s, n = pattern.subn(new_intro + '<main class="deck">', s, count=1)
if n != 1:
    raise SystemExit(f'Intro HTML block not found; replacements={n}')

old_state = "function setIntroStep(step){introStep=Math.max(0,Math.min(2,step));introState(['dream','processing','rejected'][introStep])}"
new_state = "function setIntroStep(step){introStep=Math.max(0,Math.min(6,step));introState(['dream','evaluation','paperwork','offers','problem','paused','risk'][introStep])}"
if old_state in s:
    s = s.replace(old_state, new_state, 1)
elif new_state not in s:
    raise SystemExit('Intro state function not found')

old_forward = "if(introStep<2)setIntroStep(introStep+1);else finishIntro()"
new_forward = "if(introStep<6)setIntroStep(introStep+1);else finishIntro()"
if old_forward in s:
    s = s.replace(old_forward, new_forward, 1)
elif new_forward not in s:
    raise SystemExit('Intro forward keyboard handler not found')

p.write_text(s, encoding='utf-8')
