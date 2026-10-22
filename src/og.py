import asyncio, base64, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(HERE, 'assets'))
ALL = '--all' in sys.argv
from playwright.async_api import async_playwright
bg=base64.b64encode(open('hero-1200.webp','rb').read()).decode()
F='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400&family=Geist:wght@500;600&family=Geist+Mono&display=swap">'
def og(title, eyebrow):
    return F+f'''<style>body{{margin:0}}.c{{width:1200px;height:630px;position:relative;overflow:hidden;background:#f7f5ee;font-family:Geist,sans-serif;color:#1f3a2e}}
.bg{{position:absolute;right:-120px;top:0;width:820px;height:630px;background:#cfe2d2 url(data:image/webp;base64,{bg}) center/cover;background-blend-mode:multiply;opacity:.9;-webkit-mask:linear-gradient(90deg,transparent,#000 45%)}}
.in{{position:absolute;inset:0;padding:64px 72px 80px;display:flex;flex-direction:column;justify-content:space-between}}
.logo{{display:flex;align-items:center;gap:10px;font-weight:600;font-size:34px;letter-spacing:-.04em}}.tag{{padding:6px 10px;border-radius:8px;background:#cfe2d2;font-size:20px;letter-spacing:.02em}}
.e{{font:400 30px/1.2 "Geist Mono",monospace;text-transform:uppercase;color:#a8402a;margin-bottom:26px;letter-spacing:.01em}}
h1{{margin:0;font:400 84px/1 "EB Garamond",serif;letter-spacing:-.04em;max-width:960px}}
.f{{font-size:22px;color:#56635b;font-weight:500}}</style>
<div class="c"><div class="bg"></div><div class="in"><div class="logo">automatisation<span class="tag">IA PME</span></div><div><div class="e">{eyebrow}</div><h1>{title}</h1></div></div></div>'''
ARTS = json.load(open(os.path.join(HERE, 'articles.json')))
items=[('og-home',"L'automatisation IA qui gère vos demandes de A à Z","Agents IA · n8n, Make, Zapier"),('og-blog',"Guides sur l'automatisation IA en PME","Blog"),('og-formation',"Formation automatisation IA sur mesure","Formation · IA et automatisation")]
items+=[('og-'+a['slug'], a['short'], a['cat']) for a in ARTS]
import sys as _s; _s.path.insert(0, HERE); from tools_data import TOOLS
items+=[('og-'+t['slug'], t['menu'][0], t['eyebrow']) for t in TOOLS]
from solutions_data import SOLUTIONS, METIERS
items+=[('og-'+t['slug'], t['menu'][0], t['eyebrow'].split(' · ')[-1]) for t in SOLUTIONS+METIERS]
items+=[('og-tarifs','Des prix fixes, annoncés avant de commencer','Tarifs'),('og-a-propos','Alexandre Cottret, intégrateur automatisation IA','À propos')]
items=[it for it in items if ALL or not os.path.exists(it[0]+'.jpg')]
icon=F+'''<style>body{margin:0}.i{width:512px;height:512px;border-radius:0;background:#1f3a2e;display:grid;place-items:center;font:600 230px/1 Geist,sans-serif;letter-spacing:-.05em;color:#cfe2d2}</style><div class="i">IA</div>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        pg=await b.new_page(viewport={'width':1200,'height':630})
        for name,t,e in items:
            await pg.set_content(og(t,e)); await pg.wait_for_timeout(1500)
            await pg.screenshot(path=name+'.png')
        await b.close()
asyncio.run(main())
from PIL import Image
for name,_,_ in items:
    Image.open(name+'.png').convert('RGB').save(name+'.jpg',quality=86,optimize=True,progressive=True); os.remove(name+'.png')
print('og generated:', [n for n,_,_ in items])
