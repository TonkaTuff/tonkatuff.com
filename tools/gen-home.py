# Builds index.html from the table below: the forty things on the home page, four per library, with
# their one-liners. Edit the table, run `python tools/gen-home.py`, commit both. The <head> is kept
# from the existing index.html; everything from <style> down is written fresh.
import io, os, html
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
SRC = io.open(OUT, encoding='utf-8').read()
head_end = SRC.index('<style>')
HEAD = SRC[:head_end]   # doctype, meta, OG, icon, fonts: unchanged

# name, class, version, count tag, one line, four bodies with one-liners
LIBS = [
 ('Ephemeris', 'orb', '0.12.1', '50 named bodies', 'Things in the sky.', [
   ('gargantua', 'Gargantua', 'A black hole, its disc lensed over the top'),
   ('andromeda', 'Andromeda', 'The nearest big galaxy, tilted, slowly turning'),
   ('orion', 'Orion', 'The nebula, its dust and the Trapezium'),
   ('saturn', 'Saturn', 'Rings edge-lit, the gap, a moon going round')]),
 ('Coriolis', 'wx', '0.8.0', '65 named events', 'Weather, as the satellite sees it.', [
   ('yasi', 'Yasi', 'Cyclone Yasi, spinning the southern way'),
   ('fork-lightning', 'Fork lightning', 'The strike, the branches, the afterglow'),
   ('el-reno', 'El Reno', 'The widest tornado, rope to wedge'),
   ('morning-glory', 'Morning Glory', 'The roll cloud coming in over the Gulf')]),
 ('Swarm', 'swarm', '0.3.0', '23 named swarms', 'Living things, every one a function of time.', [
   ('starlings', 'Starlings', 'A murmuration wheeling and folding'),
   ('gretna', 'Gretna', 'The roost coming in at dusk'),
   ('bait-ball', 'Bait ball', 'Spins, then opens when a predator passes'),
   ('fireflies', 'Fireflies', 'Blinking over a meadow on their own clocks')]),
 ('Ignis', 'fire', '0.2.0', '21 named fires', 'Fire: flames, embers, smoke.', [
   ('bushfire', 'Bushfire', 'A front crossing the canvas, embers on the wind'),
   ('campfire', 'Campfire', 'Logs, flames and smoke carrying on up'),
   ('fireworks', 'Fireworks', 'Shells on a schedule, sparks falling'),
   ('lava-lake', 'Lava lake', 'Lava cracking through its crust')]),
 ('Swell', 'water', '0.1.0', '20 named waters', 'Water: every dot a fixed place on it.', [
   ('nazare', 'Nazaré', 'The big wave standing up and breaking'),
   ('waterfall', 'Waterfall', 'Tearing into mist at the bottom'),
   ('whirlpool', 'Whirlpool', 'Spiralling down to a dark eye'),
   ('fountain', 'Fountain', 'Jets that dance to their own clock')]),
 ('Escapement', 'gear', '0.1.0', '17 named machines', 'Machines: the tick lands on time.', [
   ('clockwork', 'Clockwork', 'Gears meshing at the ratio of their teeth'),
   ('anchor', 'Anchor', 'An escapement letting one tooth slip per swing'),
   ('lissajous', 'Lissajous', 'A harmonograph drawing its figure'),
   ('radar', 'Radar', 'A sweep going round, blips fading')]),
 ('Dendrite', 'micro', '0.1.0', '12 named things', 'The very small.', [
   ('cortex', 'Cortex', 'Neurons wired in a ring, firing'),
   ('snowflake', 'Snowflake', 'Throwing branches as it grows'),
   ('mitosis', 'Mitosis', 'A cell pinching itself in two'),
   ('dna', 'DNA', 'A strand winding past')]),
 ('Chladni', 'sound', '0.1.0', '14 named sounds', 'Sound, made visible.', [
   ('ripple-tank', 'Ripple tank', 'Rings crossing and interfering'),
   ('chladni-plate', 'Chladni plate', 'Sand settling on the still lines of a ringing plate'),
   ('cymatics', 'Cymatics', 'Water on a speaker locking into a lattice'),
   ('speaker', 'Speaker', 'A cone pumping the air in front of it')]),
 ('Tendril', 'plant', '0.1.0', '15 named plants', 'Plants, leaning on one gust field.', [
   ('wheat', 'Wheat', 'A field rippling as the gust runs through'),
   ('sunflower', 'Sunflower', 'Turning with the day'),
   ('oak', 'Oak', 'Bending in the wind, leaves going'),
   ('kelp-forest', 'Kelp forest', 'Swaying in the swell')]),
 ('Lumen', 'light', '0.1.0', '14 named lights', 'Light: caustics, beams, rainbows.', [
   ('lighthouse', 'Lighthouse', 'A beam sweeping the mist'),
   ('pool', 'Pool', 'Sunlight webbing the floor'),
   ('mirror-ball', 'Mirror ball', 'Spots wheeling round the room'),
   ('rainbow', 'Rainbow', 'Over a shower, rain still falling through')]),
]
REPO = {'Ephemeris': 'ephemeris', 'Coriolis': 'coriolis', 'Swarm': 'swarm', 'Ignis': 'ignis', 'Swell': 'swell', 'Escapement': 'escapement', 'Dendrite': 'dendrite', 'Chladni': 'chladni', 'Tendril': 'tendril', 'Lumen': 'lumen'}

CSS = """<style>
:root{
  --ground:#0a0c11; --panel:#12151c; --panel-2:#171b23; --well:#0d1017; --ink:#e9ecf1; --ink-2:#a3aab6; --ink-3:#6e7583;
  --line:#232833; --line-2:#2f3542; --amber:#fac800; --amber-ink:#141000; --amber-soft:#fac8001f;
}
*{box-sizing:border-box}
html{color-scheme:dark;scroll-behavior:smooth}
body{margin:0;background:var(--ground);color:var(--ink);font-family:Manrope,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:inherit}
.mono{font-family:"IBM Plex Mono",ui-monospace,monospace}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}

nav{position:sticky;top:0;z-index:5;background:#0a0c11cc;backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
nav .wrap{display:flex;align-items:center;gap:22px;height:56px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:-.02em;text-decoration:none;font-size:16px}
.brand canvas{display:block}
nav .links{display:flex;gap:18px;margin-left:8px;font-size:13.5px;color:var(--ink-2);white-space:nowrap}
@media (max-width:720px){nav .links{display:none}nav .wrap{gap:12px}}
nav .links a{text-decoration:none}
nav .links a:hover{color:var(--ink)}
nav .spacer{flex:1}
.btn{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:999px;font-weight:700;font-size:13.5px;text-decoration:none;border:1px solid var(--line-2);color:var(--ink);background:var(--panel);transition:transform .15s ease,background .15s ease;cursor:pointer;font-family:inherit;line-height:1.3}
.btn:hover{transform:translateY(-1px);background:var(--panel-2)}
.btn.amber{background:var(--amber);color:var(--amber-ink);border-color:var(--amber)}
.btn.amber:hover{background:#ffd52e}
.btn.light{background:var(--ink);color:var(--ground);border-color:var(--ink)}
.btn.light:hover{background:#fff}
.btn.small{padding:6px 12px;font-size:12.5px}
.btn:focus-visible,a:focus-visible,button:focus-visible{outline:2px solid var(--amber);outline-offset:3px}

.hero{position:relative;padding:88px 0 40px;overflow:hidden;min-height:520px;display:flex;align-items:center}
.hero .wrap{position:relative;text-align:center;display:flex;flex-direction:column;align-items:center;gap:16px}
.hero h1{margin:0;font-size:clamp(38px,6vw,62px);font-weight:800;letter-spacing:-.035em;line-height:1.02;text-wrap:balance;max-width:14ch}
.hero p{margin:0;max-width:50ch;color:var(--ink-2);font-size:17px;text-wrap:pretty}
.hero p b{color:var(--ink);font-weight:700}
.cta{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:6px}
.pill{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);border:1px solid var(--line);border-radius:999px;padding:5px 12px}
.pill b{color:var(--amber);font-weight:700;letter-spacing:0;text-transform:none;font-size:12.5px}
.hero .pill{position:relative;z-index:1}
.hero-text{position:relative;isolation:isolate;display:flex;flex-direction:column;align-items:center;gap:16px}
.hero-text h1{position:relative}
.hero-bh{display:block;position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:-1;pointer-events:none;opacity:.75}
.hero-text h1,.hero-text p{text-shadow:0 0 4px var(--ground),0 0 14px var(--ground),0 0 28px var(--ground)}
.hero-bh canvas{display:block;width:min(1120px,180vw)!important;height:auto!important}
@media (max-width:980px){.hero{min-height:0;padding-top:60px}}

/* the gallery: filter row, then the grid of things */
#things{padding:8px 0 56px}
.filters{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:0 0 18px}
.chip{border:1px solid var(--line-2);background:var(--panel);color:var(--ink-2);border-radius:999px;padding:6px 13px;font:600 13px/1.3 Manrope,sans-serif;cursor:pointer;transition:background .15s ease,color .15s ease}
.chip:hover{color:var(--ink);background:var(--panel-2)}
.chip[aria-pressed="true"]{background:var(--ink);color:var(--ground);border-color:var(--ink)}
.filters .count{margin-left:auto;color:var(--ink-3);font-size:13px}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(280px,1fr))}
.thing{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:10px;display:flex;flex-direction:column;gap:10px;min-width:0}
.thing[hidden]{display:none}
.thing .demo{position:relative;height:190px;border-radius:12px;background:var(--well);border:1px solid var(--line);display:flex;align-items:center;justify-content:center;overflow:hidden}
.thing .demo canvas{display:block;max-width:100%;max-height:100%}
.thing .demo .from{position:absolute;left:10px;top:9px;font:500 11px/1 "IBM Plex Mono",monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.thing .meta{display:flex;align-items:flex-start;gap:10px;padding:2px 6px 4px}
.thing .meta div{min-width:0;flex:1}
.thing h3{margin:0;font-size:14.5px;font-weight:800;letter-spacing:-.01em}
.thing p{margin:2px 0 0;color:var(--ink-2);font-size:13px;line-height:1.35;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.copy{flex:none;width:34px;height:34px;border-radius:10px;border:1px solid var(--line-2);background:var(--panel-2);color:var(--ink-2);display:inline-flex;align-items:center;justify-content:center;cursor:pointer;transition:background .15s ease,color .15s ease}
.copy:hover{color:var(--ink);background:#1d222c}
.copy.done{color:var(--amber);border-color:var(--amber)}
.copy svg{width:15px;height:15px}
.more{margin:18px 0 0;color:var(--ink-3);font-size:13.5px}
.more a{color:var(--ink-2)}

section{padding:56px 0}
section h2{margin:0 0 6px;font-size:26px;font-weight:800;letter-spacing:-.025em}
section .sub{margin:0 0 24px;color:var(--ink-2);max-width:62ch}
.libs{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(210px,1fr))}
.lib{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 16px;display:flex;flex-direction:column;gap:6px;min-width:0}
.lib h3{margin:0;font-size:15.5px;font-weight:800;letter-spacing:-.01em;display:flex;align-items:baseline;gap:8px}
.lib h3 .ver{font-size:11.5px;color:var(--ink-3);font-weight:500}
.lib p{margin:0;color:var(--ink-2);font-size:13px}
.lib .tag{align-self:flex-start;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);border:1px solid var(--line-2);border-radius:4px;padding:2px 7px}
.lib .row{display:flex;gap:6px;margin-top:6px}
.lib .row a{font-size:12.5px;color:var(--ink-2);text-decoration:none}
.lib .row a:hover{color:var(--ink)}
.lib .row a+a::before{content:"·";color:var(--ink-3);margin-right:6px}

.steps{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.step{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:20px;display:flex;flex-direction:column;gap:10px}
.step .n{width:26px;height:26px;border-radius:50%;background:var(--amber-soft);color:var(--amber);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12.5px}
.step h3{margin:0;font-size:16px;font-weight:800;letter-spacing:-.01em}
.step p{margin:0;color:var(--ink-2);font-size:14px}
pre{margin:0;padding:12px 14px;background:var(--well);border:1px solid var(--line);border-radius:10px;overflow-x:auto;font-size:12px;line-height:1.6;color:var(--ink)}
code{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.92em;background:var(--well);border:1px solid var(--line);padding:1px 5px;border-radius:4px}
pre code{border:0;padding:0;background:none}

.beer{background:linear-gradient(180deg,#12151c,#0f1218);border:1px solid var(--line);border-radius:20px;padding:32px 28px;display:grid;gap:22px;grid-template-columns:1fr auto;align-items:center}
@media (max-width:760px){.beer{grid-template-columns:1fr}}
.beer h2{margin:0 0 8px}
.beer p{margin:0;color:var(--ink-2);max-width:56ch}
.beer p.via{margin-top:10px;font-size:13px}
.beer .pay{display:flex;flex-direction:column;gap:10px}
@media (max-width:760px){.beer .pay{flex-direction:row;flex-wrap:wrap}}

details{border-top:1px solid var(--line);padding:14px 0}
details:last-of-type{border-bottom:1px solid var(--line)}
summary{cursor:pointer;font-weight:700;font-size:15px;list-style:none;display:flex;justify-content:space-between;align-items:center}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";color:var(--ink-3);font-weight:500;font-size:20px}
details[open] summary::after{content:"–"}
details p{margin:10px 0 0;color:var(--ink-2);max-width:66ch}

footer{border-top:1px solid var(--line);padding:28px 0 44px;color:var(--ink-3);font-size:13.5px}
footer .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
footer a{color:var(--ink-2);text-decoration:none}
footer a:hover{color:var(--ink)}
@media (prefers-reduced-motion:reduce){.btn,.chip,.copy{transition:none}html{scroll-behavior:auto}}
</style>
</head>
<body>
"""

COPY_SVG = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="5.5" y="5.5" width="8" height="8" rx="1.5"/><path d="M10.5 5.5v-2a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2"/></svg>'

def thing(lib, cls, ver, slug, title, line):
    tag = f'<canvas class="{cls}" width="300" height="170" data-{cls}-body="{slug}"></canvas>'
    snippet = f'<script src="https://cdn.jsdelivr.net/gh/TonkaTuff/{REPO[lib]}@v{ver}/dist/{REPO[lib]}.min.js"></script>\n<canvas class="{cls}" width="120" height="88" data-{cls}-body="{slug}"></canvas>'
    return (f'      <article class="thing" data-lib="{REPO[lib]}">\n'
            f'        <div class="demo"><span class="from">{lib}</span>{tag}</div>\n'
            f'        <div class="meta"><div><h3>{html.escape(title)}</h3><p>{html.escape(line)}</p></div>'
            f'<button class="copy" type="button" title="Copy the two lines that put {html.escape(title)} on a page" aria-label="Copy the embed for {html.escape(title)}" data-snippet="{html.escape(snippet, quote=True)}">{COPY_SVG}</button></div>\n'
            f'      </article>\n')

things = ''.join(thing(lib, cls, ver, s, t, l) for lib, cls, ver, cnt, tl, bodies in LIBS for s, t, l in bodies)
chips = '      <button class="chip" type="button" aria-pressed="true" data-filter="">All</button>\n' + ''.join(
    f'      <button class="chip" type="button" aria-pressed="false" data-filter="{REPO[lib]}">{lib}</button>\n' for lib, *_ in LIBS)
libcards = ''.join(
    f'      <div class="lib"><h3>{lib} <span class="ver mono">{ver}</span></h3><p>{tl}</p><span class="tag">{cnt}</span>'
    f'<div class="row"><a href="https://tonkatuff.github.io/{REPO[lib]}/">Playground</a><a href="https://github.com/TonkaTuff/{REPO[lib]}">GitHub</a></div></div>\n'
    for lib, cls, ver, cnt, tl, bodies in LIBS)
scripts = ''.join(f'<script src="https://cdn.jsdelivr.net/gh/TonkaTuff/{REPO[lib]}@v{ver}/dist/{REPO[lib]}.min.js"></script>\n' for lib, cls, ver, *_ in LIBS)

BODY = f"""
<nav>
  <div class="wrap">
    <a class="brand" href="#"><canvas class="orb" width="26" height="26" data-orb-mode="blackhole" data-orb-lite="1"></canvas>TonkaTuff</a>
    <div class="links"><a href="#things">Things</a><a href="#libraries">Libraries</a><a href="export/">Export</a><a href="#how">How to use</a><a href="#faq">FAQ</a></div>
    <div class="spacer"></div>
    <a class="btn small" href="https://github.com/TonkaTuff">GitHub</a>
    <a class="btn small amber" href="#thanks">Say thanks 🍺</a>
  </div>
</nav>

<header class="hero">
  <div class="wrap">
    <div class="hero-text">
      <h1><span class="hero-bh" aria-hidden="true"><canvas class="orb" width="1120" height="400" data-orb-body="gargantua" data-orb-reach="9"></canvas></span>Stipple in Motion!</h1>
      <p>Two hundred and fifty-one things drawn in dots, from a black hole to a kelp forest, each one a single script and a canvas tag. Free, MIT, nothing behind a paywall. <b>If one saved you an afternoon, shout me a beer.</b></p>
    </div>
    <div class="cta">
      <a class="btn light" href="#things">Browse</a>
      <a class="btn amber" href="https://github.com/sponsors/TonkaTuff">🍺 Shout me a beer</a>
    </div>
  </div>
</header>

<section id="things">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filter by library">
{chips}      <span class="count" aria-live="polite">40 of 251</span>
    </div>
    <div class="grid">
{things}    </div>
    <p class="more">Four from each library. All two hundred and fifty-one are on the <a href="export/">export page</a>, as a PNG, GIF or WebM at any size. Want one that isn't here? <a href="https://github.com/TonkaTuff/ephemeris/issues">Open an issue</a> with a photo of the thing.</p>
  </div>
</section>

<section id="libraries">
  <div class="wrap">
    <h2>Ten libraries</h2>
    <p class="sub">Each one is a single script with the same shape: a class on the canvas and data attributes for every option. The dots match, so they all sit together on a page.</p>
    <div class="libs">
{libcards}    </div>
  </div>
</section>

<section id="how">
  <div class="wrap">
    <h2>How to use</h2>
    <p class="sub">Paste two lines. The copy button on any card above gives you both. Your coding agent can do it from the README if you'd rather not.</p>
    <div class="steps">
      <div class="step"><div class="n">1</div><h3>Add the script</h3><p>From the repo or a CDN. One file, nothing to install.</p>
<pre><code>&lt;script src="https://cdn.jsdelivr.net/gh/TonkaTuff/ephemeris@v0.12.1/dist/ephemeris.min.js"&gt;&lt;/script&gt;</code></pre></div>
      <div class="step"><div class="n">2</div><h3>Drop in a canvas</h3><p>Height is the preset. Width lets wide ones stretch. Every option is a data attribute.</p>
<pre><code>&lt;canvas class="orb" width="64" height="64"
        data-orb-body="andromeda"&gt;&lt;/canvas&gt;</code></pre></div>
      <div class="step"><div class="n">3</div><h3>Make it yours</h3><p>Six CSS variables, read every frame, so a theme switch applies live.</p>
<pre><code>canvas.orb {{
  --orb-cold: #0a7a5a;
  --orb-hot:  #e8fff6;
}}</code></pre></div>
    </div>
  </div>
</section>

<section id="thanks">
  <div class="wrap">
    <div class="beer">
      <div>
        <h2>Say thanks</h2>
        <p>I'm not going to charge a monthly fee for a loading spinner. Everything here stays free and MIT,
          commercial use included. If something saved you time and you feel like it, shout me a beer or a
          coffee. If not, no hard feelings.</p>
        <p class="via">Beer goes through GitHub Sponsors. Coffee goes through Ko-fi, which doesn't need an account.</p>
      </div>
      <div class="pay">
        <a class="btn amber" href="https://github.com/sponsors/TonkaTuff">🍺 Shout me a beer</a>
        <a class="btn amber" href="https://ko-fi.com/tonkatuff">☕ Shout me a coffee</a>
      </div>
    </div>
  </div>
</section>

<section id="faq">
  <div class="wrap">
    <h2>FAQ</h2>
    <p class="sub">The things people ask.</p>
    <details open><summary>Is it really free?</summary><p>Yes. MIT licence, use it in anything, commercial included. Nothing here will move behind a paywall later.</p></details>
    <details><summary>What's the catch?</summary><p>There isn't one. People saying thanks with a beer or a coffee is the whole business model.</p></details>
    <details><summary>What do I need?</summary><p>A browser with Canvas 2D, which is all of them. No framework, no bundler, no npm install. It works inside React, Vue, Svelte or plain HTML the same way: put a canvas on the page.</p></details>
    <details><summary>Does it work with coding agents?</summary><p>Yes. Point Claude Code, Cursor or Codex at the README and it'll wire the script and a canvas in. Every option is a data attribute or a CSS variable, so there's nothing to configure in JavaScript unless you want to.</p></details>
    <details><summary>Can I ask for something?</summary><p>Open an issue on the repo. The roadmap's in the README and I pick from it in whatever order looks fun.</p></details>
  </div>
</section>

<footer>
  <div class="wrap">
    <span>TonkaTuff</span>
    <span><a href="https://github.com/TonkaTuff">GitHub</a> · <a href="https://github.com/sponsors/TonkaTuff">Sponsors</a> · <a href="https://ko-fi.com/tonkatuff">Ko-fi</a> · <a href="https://github.com/TonkaTuff/tonkatuff.com">This site</a></span>
  </div>
</footer>

{scripts}<script>
(() => {{
  // Filter chips: one library at a time, or all. The count line says how many are showing.
  const chips = [...document.querySelectorAll('.chip')], things = [...document.querySelectorAll('.thing')], count = document.querySelector('.count');
  for (const c of chips) c.addEventListener('click', () => {{
    const f = c.dataset.filter;
    for (const o of chips) o.setAttribute('aria-pressed', String(o === c));
    let n = 0; for (const t of things) {{ const show = !f || t.dataset.lib === f; t.hidden = !show; n += show; }}
    count.textContent = f ? `${{n}} of ${{c.textContent}}` : '40 of 251';
  }});
  // Copy: the script tag and the canvas, two lines, then a tick for a moment.
  for (const b of document.querySelectorAll('.copy')) b.addEventListener('click', async () => {{
    try {{ await navigator.clipboard.writeText(b.dataset.snippet); }}
    catch (e) {{   // no async clipboard (older browser, or a sandboxed frame): the old way still works
      const ta = document.createElement('textarea'); ta.value = b.dataset.snippet; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select(); let ok = false; try {{ ok = document.execCommand('copy'); }} catch (e2) {{}} ta.remove(); if (!ok) return;
    }}
    b.classList.add('done'); b.innerHTML = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 8.5l3 3 7-7"/></svg>';
    setTimeout(() => {{ b.classList.remove('done'); b.innerHTML = {COPY_SVG!r}; }}, 1400);
  }});
}})();
</script>
</body>
</html>
"""
io.open(OUT, 'w', encoding='utf-8', newline='\n').write(HEAD + CSS + BODY)
print('written', len(HEAD + CSS + BODY), 'bytes;', things.count('<article'), 'things')
