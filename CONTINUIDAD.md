# Continuidad del pitch — Ruta Segura

Para que otra IA (o una persona del equipo) retome **la presentación viva** sin reconstruir contexto. El research y el encuadre del curso siguen en `Agents.md`. Este archivo cubre el deck, las decisiones de diseño y los trampas técnicas.

Fecha de este corte: 26 agosto 2026. HEAD del repo de presentación: `2debfff`.

---

## 1. Dónde está el trabajo

| Qué | Dónde |
| --- | --- |
| Repo | https://github.com/Viborasnake/examen-diplomado.git |
| Rama | `main` (no hay otra rama de trabajo) |
| Pitch | https://viborasnake.github.io/examen-diplomado/ |
| Guion | https://viborasnake.github.io/examen-diplomado/speaker.html |
| Código local reciente | `/tmp/examen-diplomado-fresh` (clone; no es el workspace de research) |
| Research / insumos | este workspace: `Evaluación Del insight al caso de negocio` |

El deck es estático: `index.html` + `speaker.html` + `assets/`. GitHub Pages se publica con `.github/workflows/pages.yml` (`deploy-pages`, `build_type` workflow). **Un push a `main` despliega.** `concurrency.group: ruta-segura-pages` con `cancel-in-progress: true`: no dispares un `workflow_dispatch` mientras un push aún corre, o se cancelan entre sí.

Tras cada deploy, pedir recarga forzada. El CDN de Pages cachea `index.html` y PNGs.

No inventar entrevistas, cifras, integraciones ni apoyo de bancos. El prototipo es Wizard of Oz / hipótesis, no evidencia de campo.

---

## 2. Qué es el caso (no mover sin decisión explícita)

**Producto:** Ruta Segura. Coordina una rectificación de antecedente para que una **operación hipotecaria** siga viva. No es un dashboard de privacidad, ni una billetera de datos, ni “borrar todo con un clic”.

**Persona:** Carolina (en archivos a veces aparece como Catalina / Caro). Encontró vivienda, el banco evalúa, un dato incorrecto (deuda pagada que sigue apareciendo) detiene la evaluación. El job no es “corregir un dato”: es **ser evaluada con información correcta antes de que caduque la operación**.

**Pagador:** el banco (B2B2C). Carolina usa; Crédito Hipotecario es la hipótesis de comprador. Se cobra por caso **gestionado**, no corregido.

**Diferencia local:** Soyio = identidad/consentimiento/firma. AlayaTrust = infraestructura B2B de derechos. Ruta Segura = hilo de evidencia entre origen, registro y reingreso hipotecario.

**Promesa acotada:** no promete acceso a todas las bases, ni eliminación en terceros, ni cumplimiento legal automático.

La evaluación original habla de Ley 21.719 como desafío común. El recorte del equipo es hipotecarios bloqueados por inconsistencia, no “control de datos para todos los chilenos”.

---

## 3. Cómo está armado el deck

### Intro (overlay, 4 clicks, no es lámina 1)

Orden: `dream` → `evaluation` → `problem` → `risk`.

1. Tu sueño de la casa propia  
2. Evaluando tu crédito  
3. Antecedentes comerciales  
4. OPERACIÓN EN RIESGO (nombres del equipo + diploma)

`finishIntro()` **esconde el overlay y no re-renderiza** la lámina 1. Volver a renderizar colgaba el hilo (MutationObservers). No reintroducir `render()` al terminar la intro.

### Numeración

Hay más `idx` que números lógicos. El cierre (pausado → interviene → banco → evaluación retomada → ambos ganan) cuenta como **15**. Gracias es **16**.

```
logicalSlideTotal = 16
logicalSlideNumber: último idx → 16; idx >= 14 → 15; si no → idx+1
```

Hashes: `#1` portada … `#19` Gracias. El usuario ve `#16` como EL BANCO REINCORPORA (idx interno).

### Quién presenta

| Quién | Láminas lógicas | Enfoque |
| --- | --- | --- |
| Cris | 00–03 (intro + 1–3) | Hipótesis · Encuadre |
| Vale | 04–07 | Evidencia · Oportunidad |
| Erick | 08–11 | Prototipo · Modelo |
| Tami | 12–16 | Negocio · Cierre + Gracias |

### Timer

- 10:00 (`TIMER_SECONDS = 600`), reloj de pared (`Date.now`), no `setInterval` que se acelera.  
- Visible desde la intro. **Empieza a correr cuando `introStep > 0`** (después del primer beat).  
- Pulso/tilt de pantalla con restante **7:30 / 5:00 / 2:30 / 0:00** (marcas 450, 300, 150, 0). Suave (~0.55deg).  
- En cierre (`idx >= 13`) se esconde relator y timer.

---

## 4. Decisiones de diseño vigentes

Tomarlas como default. Si se cambian, actualizar este archivo.

### Portada (`#1`)

- **No mostrar el prototipo/celular** en la primera lámina. El artefacto aparece en la 08 (Erick).  
- A la derecha: personaje **Caro confundida** (encogida de hombros, palmas arriba). Recorte con fondo transparente y borde nítido.  
- **Sin texto sobre o bajo la figura** (se quitó la etiqueta “CAROLINA”).  
- El titular y el párrafo van **centrados en el alto**; la figura se apoya abajo a la derecha.  
- Archivo: `assets/carolina-confundida.png`. Fuente: `insumos/Caro-confundida` (PNG 1024×1536, a veces sin extensión). No volver a aplastar a JPG: pierde el alpha y reaparece un halo gris.  
- No usar máscara CSS (`mask-image` radial) sobre el personaje: eso era el “degradado” en los bordes.

### Prototipo (lámina 08 y hero antiguo)

- Cinco teléfonos HTML (`.rs-app`), no fotos. El 5.º (cierre verificable / banco) es **verde**.  
- En el teléfono 1, el teclado **ocupa todo el ancho**, escribe la consulta de Carolina y luego envía. Tipeo lento (no 16 ms/carácter).  
- El teclado se monta en `.screen` / `.hero-app-screen`. Las teclas van `flex: 1` **sin** `max-width` chico (si no, quedan un racimo al centro).

### Láminas de contenido

- Una palabra en celeste (`--blue #3F8CD5`) por título.  
- Títulos arriba; cuerpo centrado en el resto.  
- Tipografía: **Plus Jakarta Sans** en títulos; Inter en cuerpo.  
- Fondo de láminas normales: blanco con **gradiente azul muy suave** (no en el cierre a sangre).  
- En “siguen separados”, el recuadro de valor es **Reingreso** (pastilla “Donde está el valor”), columna compacta, no título flotando.  
- En “Menos fricción”, se marcan **Cierre** y **Evidencia para reingresar**.  
- En piloto, las **cuatro puertas de éxito** van grandes y legibles (número + título + párrafo).

### Cierre a sangre (`idx >= 13`)

Secuencia click a click, microanimación sola:

1. CRÉDITO PAUSADO — rojo `#C62828`, ícono blanco  
2. RUTA SEGURA INTERVIENE  
3. EL BANCO REINCORPORA — contenido **centrado en el viewport**  
4. EVALUACIÓN RETOMADA — verde  
5. Ambos ganan  
6. **Gracias.** — blanco, centrado, **solo** título + 4 cards del equipo (Cris, Vale, Erick, Tami) con avatar saliendo del círculo. **Sin links, sin diploma, sin “¿Preguntas?”.**

`.slide` usa `grid-template-rows: auto 1fr auto`. Si `.top` y `.footer` están en `display:none`, el `.main` cae en la pista `auto` y el contenido se pega arriba. En cierre hay que forzar `grid-template-rows: 1fr` en `.slide.closing-sequence`.

`enhanceClosingVisuals` compara el `h1` recortado. El título es `Gracias.` (con punto). Normalizar puntuación o el observer **saca** `closing-sequence` y reaparecen header/footer. Hay un fallback `idx >= 13`.

Avatares del equipo: `assets/team-{cris,vale,erick,tami}.png` desde `insumos/*.png` **con alpha**. No convertir a JPG.

### Copy sensible

- “operación hipotecaria”, no “colocación”.  
- Diploma en pantalla de intro: *Diploma en Estrategia y Experiencia de Productos en la Era de la IA · Unegocios FEN Universidad de Chile · Agosto 2026*. El material del curso en este workspace habla de UDD; no mezclar sin preguntar.  
- La persona del caso se llama **Carolina** en el relato.

---

## 5. Archivos que importan

### Repo de presentación

| Ruta | Uso |
| --- | --- |
| `index.html` | Deck completo (CSS + `slides[]` + intro + timer). Es la fuente de verdad visual. |
| `speaker.html` | Guion sincronizado, s0–s16. |
| `assets/carolina-confundida.png` | Portada. |
| `assets/team-*.png` | Lámina Gracias. |
| `assets/proto-0*.jpg` | Renders viejos del proto; el deck ya no los usa como UI. |
| `.github/workflows/pages.yml` | Único workflow. No reactivar patchers. |

### Este workspace (research)

| Ruta | Uso |
| --- | --- |
| `Agents.md` | Encuadre, ley, desk research, reglas de evidencia. |
| `insumos/Caro-confundida` | Fuente del personaje de portada (PNG). |
| `insumos/caro-1.png` … `caro-4.png` | Otras poses (salto, sorpresa, duda recortada, festejo). |
| `insumos/{Cris,Vale,Erick,Tami}.png` | Avatares del equipo, con transparencia. |
| `insumos/desk research/articulos_analizados.txt` | 24 lecturas; no duplicar research. |
| `Pitch_Ruta_Segura_v0.5.md` | Guion narrativo v0.5; puede estar un paso atrás del HTML. |

---

## 6. Trampas ya pagadas (no repetir)

1. **Intro pegada en OPERACIÓN EN RIESGO:** `finishIntro` → `render` + observers en `document` trababan el main thread. Ocultar overlay primero; observers solo en `#slide`.  
2. **Timer rápido:** no ticks de `setInterval`. Usar `Date.now`.  
3. **Deploys que no publican:** workflows basura + Pages en “branch” vs “workflow”. Quedó solo `pages.yml`.  
4. **Cierre no a sangre / Gracias con header:** ver sección 4 (grid `auto` + `Gracias.`).  
5. **Personaje con halo:** recorte JPG o `mask-image`. Usar PNG con alpha y recorte duro.  
6. **Teclado diminuto:** `max-width` en `.rs-key` + `cqi` sobre un teléfono de ~190 px. Flex a todo el ancho.  
7. **Celular de portada:** decisión explícita de no mostrarlo al partir.

---

## 7. Qué no está cerrado

- No hay entrevistas reales ni piloto corrido. Las cifras tipo ≥60%, +30%, +25% son **hipótesis de diseño**, no resultados.  
- `speaker.html` a veces se desfasa si solo se edita `index.html`.  
- El material de research todavía habla de una fase previa al pitch; el caso ya se recortó a hipotecarios.  
- Soyio sigue siendo el competidor a diferenciar, no a clonar.  
- Hay poses extra de Carolina (`caro-1` a `caro-4`) si se quiere otra emoción más adelante.

---

## 8. Cómo trabajar el próximo cambio

1. Clonar o actualizar `Viborasnake/examen-diplomado` en `main`.  
2. Editar `index.html` / `speaker.html` / `assets`.  
3. Commit + push. Esperar el run de **Deploy GitHub Pages** (`success`) antes de decir que está en vivo.  
4. Verificar la URL pública con recarga forzada.  
5. Actualizar **este archivo** si cambia segmento, promesa, numeración, portada, cierre o el pagador.

No reescribir el caso como “app de privacidad para Chile”. No mostrar el prototipo en la lámina 1 salvo que el equipo lo pida otra vez.
