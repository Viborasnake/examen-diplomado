from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

css = """
.intro-cover-label{font-size:clamp(12px,1vw,16px);font-weight:900;letter-spacing:.18em;text-transform:uppercase;color:#FFD9D9;margin-bottom:24px}
.intro-cover-meta{margin:44px auto 0;display:grid;gap:8px;justify-items:center;max-width:980px;color:#fff}
.intro-cover-names{font-size:clamp(17px,1.55vw,25px);font-weight:800;letter-spacing:.015em}
.intro-cover-program{font-size:clamp(12px,1.05vw,17px);font-weight:600;opacity:.9;line-height:1.45}
"""
if '.intro-cover-meta{' not in s:
    s = s.replace('</style>', css + '</style>')

old_cover = """<section class=\"intro-state intro-risk\" data-intro=\"risk\">\n    <div class=\"intro-inner\">\n      <div class=\"intro-kicker\">El tiempo importa</div>\n      <h1 class=\"intro-title\">OPERACIÓN EN RIESGO</h1>\n      <p class=\"intro-sub\">Corregir el dato no sirve si la actualización no llega al banco a tiempo.</p>\n    </div>\n  </section>"""
new_cover = """<section class=\"intro-state intro-risk\" data-intro=\"risk\">\n    <div class=\"intro-inner\">\n      <div class=\"intro-kicker\">Ruta Segura</div>\n      <div class=\"intro-cover-label\">El tiempo importa</div>\n      <h1 class=\"intro-title\">OPERACIÓN EN RIESGO</h1>\n      <p class=\"intro-sub\">Corregir el dato no sirve si la actualización no llega al banco a tiempo.</p>\n      <div class=\"intro-cover-meta\">\n        <div class=\"intro-cover-names\">Cristian · Valeria · Erick · Tamara</div>\n        <div class=\"intro-cover-program\">Diplomado Product &amp; Digital Experience Management · Unegocios FEN Universidad de Chile · Agosto 2026</div>\n      </div>\n    </div>\n  </section>"""
if old_cover not in s:
    raise SystemExit('Cover block not found')
s = s.replace(old_cover, new_cover, 1)

pat = re.compile(r"\{stage:0,time:'0:00–0:25',k:'RUTA SEGURA · EL PROBLEMA'.*?\},(?=\{stage:0,time:'0:25–0:50',k:'RUTA SEGURA · PITCH v0\.5')", re.S)
s, n = pat.subn('', s, count=1)
if n != 1:
    raise SystemExit(f'Redundant first slide not removed; replacements={n}')

s = s.replace("time:'0:25–0:50'", "time:'0:00–0:30'", 1)
s = s.replace("time:'0:50–1:30'", "time:'0:30–1:15'", 1)
s = s.replace("time:'1:30–2:10'", "time:'1:15–2:05'", 1)
s = s.replace("time:'2:10–3:15'", "time:'2:05–3:15'", 1)

p.write_text(s, encoding='utf-8')
