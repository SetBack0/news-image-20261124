# -*- coding: utf-8 -*-
"""Render the 24 Nov 2026 front page (v7)."""
import html
from build_map import STORIES, REGIONS

RC = dict(REGIONS)
LAT_TOP, LAT_BOT = 84, -58


def esc(s):
    return html.escape(s, quote=True)


def pill(status):
    cls = {'REPORTED': 'ok', 'CLAIM': 'claim', 'ONGOING': 'live'}.get(status, 'ok')
    return f'<span class="pill {cls}">{status}</span>'


def pin(s):
    lon, lat = s[8], s[9]
    if lon is None:
        return ''
    x = (lon + 180.0) / 360.0 * 100
    y = (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * 100
    return (f'<span class="pin" style="left:{x:.2f}%;top:{y:.2f}%;--c:{RC[s[2]]}">'
            f'<b>{s[0]}</b></span>')


STRAIT = '''<svg class="strait" viewBox="0 0 300 210" preserveAspectRatio="none">
  <rect width="300" height="210" fill="#E7EDF1"/>
  <path d="M0 0 H300 V58 C262 70 236 54 208 62 C180 70 162 92 146 112 C132 130 104 138 74 132 C46 126 22 134 0 128 Z"
        fill="#DDD6C6" stroke="#C3BBA8"/>
  <path d="M0 210 H300 V160 C266 148 244 162 220 146 C202 134 200 116 188 100 C176 84 148 80 120 92 C86 106 52 130 0 140 Z"
        fill="#DDD6C6" stroke="#C3BBA8"/>
  <path d="M0 142 C46 132 92 124 130 116 C168 108 190 94 214 84 C240 72 268 74 300 68"
        stroke="#1F7FA8" stroke-width="1.8" stroke-dasharray="7 6" opacity=".55" fill="none"/>
  <path d="M262 62 C278 96 278 148 256 182" fill="none" stroke="#B3202C" stroke-width="2.6"/>
  <text x="10" y="26" fill="#3A3F4A" font-family="Barlow" font-size="13" font-weight="700" letter-spacing="3">IRAN</text>
  <text x="196" y="200" fill="#3A3F4A" font-family="Barlow" font-size="13" font-weight="700" letter-spacing="3">OMAN</text>
  <text x="16" y="150" fill="#1F7FA8" font-family="Barlow" font-size="10" font-weight="700" letter-spacing="1.6">PERSIAN GULF</text>
  <text x="176" y="96" fill="#B3202C" font-family="Barlow" font-size="10" font-weight="700" letter-spacing="1.4">BLOCKADE</text>
  <text x="96" y="118" fill="#1F7FA8" font-family="Barlow" font-size="9.5" font-weight="700" letter-spacing="1.2">HORMUZ</text>
  <g transform="translate(150,112) rotate(-8)"><path d="M-13 -4 H13 L8 6 H-8 Z" fill="#5C6674"/><rect x="-6" y="-10" width="12" height="6" fill="#8B95A3"/></g>
  <circle cx="157" cy="102" r="10" fill="#E5484D" opacity=".30"/><circle cx="157" cy="102" r="3.2" fill="#E5484D"/>
  <g transform="translate(206,84) rotate(4)"><path d="M-13 -4 H13 L8 6 H-8 Z" fill="#5C6674"/><rect x="-6" y="-10" width="12" height="6" fill="#8B95A3"/></g>
  <circle cx="213" cy="74" r="11" fill="#E5484D" opacity=".30"/><circle cx="213" cy="74" r="3.4" fill="#E5484D"/>
  <g transform="translate(240,74) rotate(10)"><path d="M-12 -4 H12 L7 6 H-7 Z" fill="#5C6674"/><rect x="-5" y="-10" width="11" height="6" fill="#8B95A3"/></g>
  <circle cx="246" cy="64" r="9" fill="#E5484D" opacity=".30"/><circle cx="246" cy="64" r="3" fill="#E5484D"/>
</svg>'''


def hero(s):
    col = RC[s[2]]
    return f'''<article class="hero" style="--c:{col}">
  <div class="krow"><span class="num">{s[0]:02d}</span><span class="place">{esc(s[1])}</span>{pill(s[4])}
    <span class="sec">{esc(s[2])} · {esc(s[3])}</span></div>
  <div class="hbody">
    <div>
      <h2>{esc(s[5])}</h2>
      <p>{esc(s[6])} <b>{esc(s[7])}</b></p>
      <div class="chips"><span><b>3</b> tankers ablaze</span><span><b>$88.97</b> Brent</span></div>
    </div>
    <div class="hmap">{STRAIT}</div>
  </div>
</article>'''


def side(s):
    col = RC[s[2]]
    return f'''<article class="side" style="--c:{col}">
  <div class="krow"><span class="num">{s[0]:02d}</span><span class="place">{esc(s[1])}</span></div>
  <div class="sec">{esc(s[2])} · {esc(s[3])}</div>
  <h3>{esc(s[5])}</h3>
  <p>{esc(s[6])}</p>
</article>'''


def std_card(s):
    col = RC[s[2]]
    return f'''<article class="card" style="--c:{col}">
  <div class="krow"><span class="num">{s[0]:02d}</span><span class="place">{esc(s[1])}</span>{pill(s[4])}</div>
  <h3>{esc(s[5])}</h3>
  <p>{esc(s[6])}</p>
</article>'''


def brief(s):
    col = RC[s[2]]
    return f'''<li style="--c:{col}"><span class="bnum">{s[0]:02d}</span>
  <span class="btxt"><b>{esc(s[5])}</b><i>{esc(s[1])} · {esc(s[7])}</i></span></li>'''


def build():
    leads, cards, rest = STORIES[0:3], STORIES[3:11], STORIES[11:29]
    counts = {}
    for s in STORIES:
        counts[s[2]] = counts.get(s[2], 0) + 1
    tabs = ''.join(f'<span class="tab" style="--c:{c}">{n.upper()}<b>{counts[n]}</b></span>'
                   for n, c in REGIONS if counts.get(n))
    nums = [("12,000", "fled Co-op Live arena"), ("$88.97", "Brent crude, a three-month low"),
            ("548", "commutations Trump wants reversed"), ("+31%", "Nvidia's jump on Huang's return"),
            ("26", "body bags pulled from the Banten fire"), ("+6.1%", "Singapore's GDP growth in Q3")]
    numhtml = ''.join(f'<div class="nb"><span class="v">{v}</span><span class="k">{k}</span></div>' for v, k in nums)
    cols = [rest[:len(rest)//2], rest[len(rest)//2:]]
    briefcols = ''.join('<ul>' + ''.join(brief(s) for s in c) + '</ul>' for c in cols)
    pins = ''.join(pin(s) for s in STORIES[:11])

    page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Playfair;src:url(fonts/PlayfairDisplay-900.ttf);font-weight:900}}
@font-face{{font-family:Playfair;src:url(fonts/PlayfairDisplay-700.ttf);font-weight:700}}
@font-face{{font-family:InterTight;src:url(fonts/InterTight-400.ttf);font-weight:400}}
@font-face{{font-family:InterTight;src:url(fonts/InterTight-600.ttf);font-weight:600}}
@font-face{{font-family:InterTight;src:url(fonts/InterTight-800.ttf);font-weight:800}}
@font-face{{font-family:Barlow;src:url(fonts/BarlowCondensed-500.ttf);font-weight:500}}
@font-face{{font-family:Barlow;src:url(fonts/BarlowCondensed-600.ttf);font-weight:600}}
@font-face{{font-family:Barlow;src:url(fonts/BarlowCondensed-700.ttf);font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1024px;height:1024px;overflow:hidden}}
body{{font-family:InterTight,Arial,sans-serif;color:#15171C;-webkit-font-smoothing:antialiased;
 background:linear-gradient(#F8F5ED,#EFEBE0)}}
.page{{position:relative;width:1024px;height:1024px;padding:12px 18px 0}}
.page:after{{content:"";position:absolute;inset:0;pointer-events:none;opacity:.30;
 background-image:repeating-linear-gradient(0deg,rgba(20,23,28,.05) 0 1px,transparent 1px 4px)}}
.rail{{display:flex;justify-content:space-between;font-family:Barlow;font-size:11px;font-weight:700;
 letter-spacing:.20em;text-transform:uppercase;color:#5C6270;border-bottom:1.5px solid #15171C;padding-bottom:4px}}
.kick{{font-family:Barlow;font-size:11.5px;font-weight:700;letter-spacing:.34em;color:#B3202C;text-transform:uppercase;margin-top:6px}}
h1{{font-family:Playfair;font-size:84px;line-height:.94;letter-spacing:-.014em}}
.deck{{font-size:14px;font-weight:600;color:#3A3F4A;margin-top:1px}}
.deck b{{color:#B3202C}}
.tabs{{display:flex;gap:5px;margin-top:6px;justify-content:space-between}}
.tab{{font-family:Barlow;font-size:11px;font-weight:700;letter-spacing:.12em;color:#fff;background:var(--c);
 padding:2px 7px 1px;border-radius:2px}}
.tab b{{font-weight:700;opacity:.72;margin-left:4px}}
.band{{display:grid;grid-template-columns:644px 328px;gap:10px;margin-top:8px;height:234px}}
.hero{{grid-row:span 1;background:#fff;border:1px solid #D6D1C4;border-top:5px solid var(--c);padding:10px 12px 0;display:flex;flex-direction:column;overflow:hidden}}
.krow{{display:flex;align-items:center;gap:6px}}
.num{{font-family:Barlow;font-size:13px;font-weight:700;color:#fff;background:var(--c);padding:0 4px;line-height:16px}}
.place{{font-family:Barlow;font-size:11.5px;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:#3A3F4A}}
.sec{{font-family:Barlow;font-size:10.5px;font-weight:600;letter-spacing:.15em;text-transform:uppercase;color:var(--c)}}
.krow .sec{{margin-left:auto}}
.pill{{font-family:Barlow;font-size:9px;font-weight:700;letter-spacing:.10em;padding:1px 4px;border:1px solid}}
.pill.ok{{color:#1E7A4B;border-color:#1E7A4B}}
.pill.claim{{color:#B26A00;border-color:#B26A00}}
.pill.live{{color:#1F4E9C;border-color:#1F4E9C}}
.hero h2{{font-family:Playfair;font-weight:900;font-size:33px;line-height:.96;letter-spacing:-.018em;margin-top:6px}}
.hero p{{font-size:11.5px;line-height:1.34;color:#454B57;margin-top:6px}}
.hero p b{{font-family:Barlow;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:#8A909C;font-weight:600}}
.chips{{display:flex;gap:6px;margin-top:8px}}
.chips span{{font-family:Barlow;font-size:10px;font-weight:600;letter-spacing:.04em;background:#F1EDE2;border:1px solid #DCD6C8;padding:2px 6px}}
.chips b{{font-weight:700;color:#B3202C}}
.hbody{{display:grid;grid-template-columns:1fr 246px;gap:12px;margin-top:4px;flex:1;min-height:0}}
.hmap{{position:relative}}
.strait{{width:100%;height:100%;display:block;border:1px solid #D6D1C4}}
.stack{{display:grid;grid-template-rows:1fr 1fr;gap:10px;height:234px}}
.side{{background:#fff;border:1px solid #D6D1C4;border-left:4px solid var(--c);padding:8px 10px;display:flex;flex-direction:column}}
.side h3{{font-family:Playfair;font-weight:900;font-size:22px;line-height:.99;letter-spacing:-.01em;margin-top:3px}}
.side p{{font-size:10.5px;line-height:1.28;color:#545B67;margin-top:3px}}
.side .sec{{margin-top:4px}}
.numbers{{background:#FFFDF7;color:#15171C;padding:0;margin-top:7px;height:56px;display:grid;grid-template-columns:repeat(6,1fr);border-top:2px solid #15171C;border-bottom:2px solid #15171C}}
.numbers .t{{display:none}}
.nb{{padding:6px 9px;display:flex;align-items:baseline;gap:6px;border-left:1px solid #DDD7C9}}
.nb .v{{font-family:Playfair;font-weight:900;font-size:25px;line-height:.9;white-space:nowrap}}
.nb .k{{font-size:8.6px;line-height:1.14;color:#5C6270}}
.cards{{display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:92px 92px;gap:8px;margin-top:9px}}
.card{{background:#fff;border:1px solid #D9D4C7;border-left:3px solid var(--c);padding:6px 8px;overflow:hidden}}
.card .num{{font-size:11px;line-height:14px}}
.card .place{{font-size:10px}}
.card .pill{{margin-left:auto}}
.card h3{{font-size:15.5px;font-weight:800;line-height:1.05;letter-spacing:-.012em;margin-top:4px}}
.card p{{font-size:9.6px;line-height:1.26;color:#5B616D;margin-top:3px}}
.bottom{{display:grid;grid-template-columns:1fr 322px;gap:10px;margin-top:9px;height:284px}}
.briefs{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}}
.briefs ul{{list-style:none;display:flex;flex-direction:column}}
.briefs li{{display:flex;gap:5px;padding:2.4px 0;border-bottom:1px dotted #C7C2B4}}
.bnum{{font-family:Barlow;font-size:9.5px;font-weight:700;color:var(--c);padding-top:1px}}
.btxt b{{display:block;font-size:11.6px;line-height:1.15;font-weight:600}}
.btxt i{{display:block;font-style:normal;font-family:Barlow;font-size:9.4px;color:#8A909C;letter-spacing:.04em;margin-top:1px}}
.mapbox{{background:#fff;border:1px solid #D9D4C7;padding:7px 8px;display:flex;flex-direction:column}}
.mapbox .mt{{font-family:Barlow;font-size:9.8px;font-weight:700;letter-spacing:.20em;color:#3A3F4A}}
.mapbox .ms{{font-size:8.4px;color:#8A909C;margin-top:1px}}
.mapwrap{{position:relative;width:304px;margin:3px auto 0}}
.mapwrap img{{width:100%;display:block;opacity:1}}
.pin{{position:absolute;transform:translate(-50%,-50%);width:13px;height:13px;border-radius:50%;
 background:#fff;border:1.8px solid var(--c);display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 1px #fff}}
.pin b{{font-family:Barlow;font-size:7px;font-weight:700;color:var(--c);line-height:1}}
.datecheck{{margin-top:auto;border-top:1.5px solid #15171C;padding-top:4px;display:flex;gap:6px;align-items:baseline}}
.datecheck .dc{{font-family:Barlow;font-size:9px;font-weight:700;letter-spacing:.14em;color:#fff;background:#B3202C;padding:1px 4px}}
.datecheck .dt{{font-size:9px;line-height:1.2;color:#3A3F4A}}
.foot{{display:flex;justify-content:space-between;gap:10px;margin-top:4px;font-family:Barlow;font-size:8.4px;color:#6B7180}}
.foot b{{color:#15171C;font-weight:700}}
</style></head><body><div class="page">
<div class="rail"><span>The world in one day · front page</span><span>29 stories · 6 regions · 24 Nov 2026</span></div>
<div class="kick">World news · Tuesday edition</div>
<h1>24 November 2026</h1>
<div class="deck"><b>Hormuz ablaze</b> as a US blockade meets Iran · COP31 collapses without a pact · Nvidia takes Huang back</div>
<div class="tabs">{tabs}</div>

<div class="numbers"><div class="t">The day in numbers</div>{numhtml}</div>
<div class="band">
{hero(leads[0])}
<div class="stack">{side(leads[1])}{side(leads[2])}</div>
</div>

<div class="cards">{''.join(std_card(s) for s in cards)}</div>

<div class="bottom">
  <div class="briefs">{briefcols}</div>
  <div class="mapbox">
    <div class="mt">WHERE IT HAPPENED</div>
    <div class="ms">pins = story numbers 1–11</div>
    <div class="mapwrap"><img src="map.png">{pins}</div>
    <div class="datecheck"><span class="dc">DATE CHECK</span>
      <span class="dt">Every story here happened, or was first reported, on <b>Tuesday 24 November 2026</b> — any time zone.</span></div>
  </div>
</div>

<div class="foot">
  <span><b>HOW SURE</b> · REPORTED = carried by the day's wires or officials · CLAIM = one side's account, labelled · ONGOING = still unfolding · graphics are drawn, not photographed</span>
  <span>Reuters · AP · Al Jazeera · Xinhua · Yonhap · Antara · UN News · Nikkei</span>
</div>
</div></body></html>'''
    open('poster.html', 'w').write(page)
    print('wrote', len(page))


if __name__ == '__main__':
    build()
