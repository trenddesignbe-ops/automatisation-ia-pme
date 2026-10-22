#!/usr/bin/env python3
"""Build the static site into ../public: python3 src/build.py

Articles: add src/articles/<slug>.html (body only, h2 with id) and an entry in src/articles.json.
Share images: python3 src/og.py (creates missing src/assets/og-<slug>.jpg)."""
import json, os, re, shutil, sys, html

SRC = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(SRC, 'assets')
REPO = os.path.abspath(os.path.join(SRC, '..'))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'public')
FONTS = sys.argv[2] if len(sys.argv) > 2 else 'self'
SITE = "https://www.automatisation-ia-pme.fr"
LEGAL_DATE = '2026-10-18'
INDEXNOW_KEY = '05797ebba808f37ca89c168a6782eaf3'
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

def fr_date(iso):
    y, m, d = iso.split('-')
    return f'{int(d)} {MOIS[int(m) - 1]} {y}'
CAL = 'https://calendly.com/alexandre-cottret/audit-automatisation-ia-20-min'
WA = 'https://wa.me/33767463870?text=Bonjour%20Alexandre%2C%20j%27aimerais%20automatiser%20une%20t%C3%A2che.'
LINKEDIN = 'https://www.linkedin.com/in/alexandre-cottret-designer-web/'
MALT = 'https://www.malt.fr/profile/alexandrecottret-zapier'
MALT1 = 'https://www.malt.fr/profile/alexcottret-webdesigner'

GOOGLE_FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
                '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400&display=swap">')

def fonts(p):
    if FONTS == 'google':
        return GOOGLE_FONTS
    css = open(os.path.join(ASSETS, 'fonts.css')).read().replace('url(fonts/', f'url({p}assets/fonts/')
    css = re.sub(r'\s+', ' ', css)
    pre = ''.join(f'<link rel="preload" href="{p}assets/fonts/{f}" as="font" type="font/woff2" crossorigin>\n' for f in ('Geist-400-latin.woff2', 'EBGaramond-400-latin.woff2', 'GeistMono-400-latin.woff2'))
    return pre + '<style>' + css + '</style>'

def esc(t):
    return html.escape(t, quote=True)

def head(title, desc, path, p, og_img, og_type='website', extra=''):
    url = SITE + '/' + path
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Alexandre Cottret">
<meta name="theme-color" content="#f7f5ee">
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Automatisation IA PME">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{fonts(p)}
<link rel="stylesheet" href="{p}assets/site.css">
{extra}</head>
<body>
'''

sys.path.insert(0, SRC)
from tools_data import TOOLS
CHEV = '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 4.5l3 3 3-3"/></svg>'
FORMATION = 'formation-automatisation-ia.html'

def header(p, home=False):
    h = '' if home else (p or './')
    logo = '#' if home else h
    form = p + FORMATION
    need = [('Agent IA 24/7', 'Chaque demande lue, classée et préparée', h + '#solutions-demandes'),
            ('Devis automatisés', 'Un brouillon prêt en quelques minutes', h + '#solutions-devis'),
            ('Relances et avis Google', 'Plus aucune relance oubliée', h + '#solutions-relances'),
            ('Factures et documents', "Lus, classés et saisis par l'IA", h + '#solutions-documents')]
    tools = [(x['menu'][0], x['menu'][1], p + x['slug'] + '.html') for x in TOOLS[:4]] + [(f'Tous les outils ({len(TOOLS)})', 'Notion, HubSpot, Excel, WhatsApp, Gmail…', p + 'integrations.html')]
    jobs = [('Artisans et BTP', 'Devis, relances, avis Google', h + '#cas-artisans'),
            ('Coachs, salles et instituts', 'Rendez-vous et rappels sur WhatsApp', h + '#cas-coachs'),
            ('Cabinets et PME de services', 'Factures, documents, reporting', h + '#cas-cabinets'),
            ('E-commerce', 'Commandes, factures et stock', p + 'integrateur-make.html#cas-pratiques')]
    col = lambda items: ''.join(f'<li><a href="{u}"><b>{t}</b><span>{d}</span></a></li>' for t, d, u in items)
    mega = f'''<div class="mega" id="mega" hidden><div class="mega__in">
    <div class="mega__col"><p class="mega__h">Par besoin</p><ul>{col(need)}</ul></div>
    <div class="mega__col"><p class="mega__h">Par outil</p><ul>{col(tools)}</ul></div>
    <a class="mega__feat" href="{form}"><span class="mega__tag">Nouveau</span><p class="mega__h">Se former</p><b>Formation automatisation IA</b><span>En visio, sur vos propres outils : vous repartez avec votre première automatisation.</span><span class="mega__more">Voir le programme et les tarifs →</span></a>
  </div></div>
  <div class="mega" id="mega-cas" hidden><div class="mega__in">
    <div class="mega__col mega__col--wide"><p class="mega__h">Par métier</p><ul class="mega__2col">{col(jobs)}</ul></div>
    <a class="mega__feat" href="{CAL}" rel="noopener"><p class="mega__h">Votre métier n'est pas listé ?</p><b>Audit offert de 20 minutes</b><span>On regarde ensemble la tâche qui vous coûte le plus de temps, et si elle s'automatise.</span><span class="mega__more">Réserver un créneau →</span></a>
  </div></div>'''
    rest = [('Formation', form), ('Blog', p + 'blog.html')]
    li = ''.join(f'<li><a href="{u}">{t}</a></li>' for t, u in rest)
    sub = ('<li class="mnav__lab">Par besoin</li>' + ''.join(f'<li><a href="{u}">{t}</a></li>' for t, d, u in need)
           + '<li class="mnav__lab">Par outil</li>' + ''.join(f'<li><a href="{u}">{t}</a></li>' for t, d, u in tools)
           + f'<li class="mnav__lab">Se former</li><li><a class="mnav__feat" href="{form}">Formation automatisation IA</a></li>')
    subcas = ''.join(f'<li><a href="{u}">{t}</a></li>' for t, d, u in jobs)
    trig = lambda label, target: f'<li class="nav__dd"><button class="nav__trigger" type="button" aria-expanded="false" aria-controls="{target}">{label}{CHEV}</button></li>'
    return f'''<header class="nav">
  <div class="nav__inner">
    <a class="logo" href="{logo}">automatisation <span class="logo__tag">IA PME</span></a>
    <div class="nav__right">
      <ul class="nav__links">{trig('Solutions', 'mega')}{trig("Cas d'usage", 'mega-cas')}{li}</ul>
      <a class="btn btn--ghost" href="{h}#contact">Contact</a>
    </div>
    <button class="nav__menu" type="button" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="mnav"><svg viewBox="0 0 20 20" aria-hidden="true"><path class="l1" d="M3 7h14"/><path class="l2" d="M3 13h14"/></svg></button>
  </div>
  {mega}
  <nav class="mnav" id="mnav" aria-label="Menu mobile" hidden><ul><li><details class="mnav__dd"><summary>Solutions{CHEV}</summary><ul class="mnav__sub">{sub}</ul></details></li><li><details class="mnav__dd"><summary>Cas d'usage{CHEV}</summary><ul class="mnav__sub"><li class="mnav__lab">Par métier</li>{subcas}</ul></details></li>{li}<li><a href="{h}#contact">Contact</a></li></ul><a class="btn btn--primary" href="{CAL}" rel="noopener">Réserver un audit</a></nav>
</header>
'''

WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>'

MENU_JS = '''<script>
(function(){
var b=document.querySelector('.nav__menu'),m=document.getElementById('mnav');
if(b&&m){var set=function(o){m.hidden=!o;b.setAttribute('aria-expanded',o);b.setAttribute('aria-label',o?'Fermer le menu':'Ouvrir le menu');document.documentElement.classList.toggle('mnav-open',o);};
b.addEventListener('click',function(){set(m.hidden)});m.addEventListener('click',function(e){if(e.target.closest('a'))set(false)});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!m.hidden){set(false);b.focus()}});}
var ts=[].slice.call(document.querySelectorAll('.nav__trigger')),fine=window.matchMedia('(hover: hover) and (pointer: fine)'),tm,hov=false;
var pan=function(t){return document.getElementById(t.getAttribute('aria-controls'))};
var op=function(t,o){clearTimeout(tm);ts.forEach(function(x){var g=pan(x),on=o&&x===t;if(g){g.hidden=!on}x.setAttribute('aria-expanded',on)});if(!o)hov=false;};
var cur=function(){for(var k=0;k<ts.length;k++){if(ts[k].getAttribute('aria-expanded')==='true')return ts[k]}return null};
ts.forEach(function(t){var g=pan(t);if(!g)return;
t.addEventListener('click',function(){var open=t.getAttribute('aria-expanded')==='true';if(hov&&open){hov=false;return}op(t,!open)});
[t.parentNode,g].forEach(function(el){el.addEventListener('mouseenter',function(){if(fine.matches){if(t.getAttribute('aria-expanded')!=='true')hov=true;op(t,true)}});el.addEventListener('mouseleave',function(){if(fine.matches){tm=setTimeout(function(){op(t,false)},200)}})});
g.addEventListener('click',function(e){if(e.target.closest('a'))op(t,false)});});
document.addEventListener('click',function(e){var c=cur();if(c&&!pan(c).contains(e.target)&&!c.contains(e.target))op(c,false)});
document.addEventListener('keydown',function(e){var c=cur();if(e.key==='Escape'&&c){op(c,false);c.focus()}});
var hs=function(){var r=location.hash.match(/^#solutions-([a-z]+)$/);if(!r)return;var tb=document.getElementById('tab-'+r[1]),sc=document.getElementById('solutions');if(tb)tb.click();if(sc)sc.scrollIntoView();};
window.addEventListener('hashchange',hs);hs();
})();
</script>'''

def footer(p, band=True, band_title='Et si vos demandes se traitaient toutes seules ?', band_cta='Réserver un audit offert'):
    h = p or './'
    b = ''
    if band:
        b = f'''<section class="band"><h2>{band_title}</h2><div class="band__btns"><a class="btn btn--ghost" href="{WA}" rel="noopener">Écrire sur WhatsApp</a><a class="btn btn--primary" href="{CAL}" rel="noopener">{band_cta}</a></div></section>
'''
    return f'''{b}<footer>
  <div class="foot">
    <div class="foot__brand"><p>L'intelligence artificielle qui traite vos demandes de A à Z</p></div>
    <nav class="foot__cols" aria-label="Pied de page">
      <div><h2 class="foot__h">Offre</h2><ul><li><a href="{h}#solutions">Solutions</a></li><li><a href="{h}#methode">Méthode</a></li><li><a href="{p}agence-automatisation-n8n.html">Automatisation n8n</a></li><li><a href="{p}integrateur-make.html">Intégrateur Make</a></li><li><a href="{p}integrateur-zapier.html">Intégrateur Zapier</a></li><li><a href="{p}integrations.html">Toutes les intégrations</a></li><li><a href="{p}formation-automatisation-ia.html">Formation IA</a></li><li><a href="{p}blog.html">Blog</a></li></ul></div>
      <div><h2 class="foot__h">Trend Design</h2><ul><li><a href="https://www.trend-design.fr/">Création de sites</a></li><li><a href="https://www.trend-design.fr/">Référencement SEO</a></li><li><a href="{h}#contact">Contact</a></li></ul></div>
      <div><h2 class="foot__h">Réseaux</h2><ul><li><a href="{MALT}" rel="noopener">Malt</a></li><li><a href="{LINKEDIN}" rel="noopener">LinkedIn</a></li></ul></div>
      <div><h2 class="foot__h">Légal</h2><ul><li><a href="{p}mentions-legales.html">Mentions légales</a></li><li><a href="{p}mentions-legales.html#confidentialite">Confidentialité</a></li><li><a href="{p}mentions-legales.html#cookies">Cookies</a></li><li><a href="#" data-cc-open>Gérer les cookies</a></li></ul></div>
    </nav>
  </div>
  <svg class="wordmark" viewBox="0 0 1280 186" role="img" aria-label="Automatisation IA PME"><text x="0" y="141" font-size="136">automatisation ia pme</text></svg>
  <div class="foot__bar"><span>© 2026 Automatisation IA PME · Alexandre Cottret</span><span>Automatisation IA pour PME et TPE, partout en France</span></div>
</footer>
<div class="fab"><a class="wa" href="{WA}" rel="noopener" aria-label="Me contacter sur WhatsApp">{WA_SVG}</a><div class="fab__menu"><div class="fab__card"><p>Une question ?</p><a class="fab__wa" href="{WA}" rel="noopener">Écrire sur WhatsApp</a><a class="fab__cal" href="{CAL}" rel="noopener">Réserver un appel de 20 min</a></div></div></div>
{MENU_JS}
{open(os.path.join(SRC, 'consent.html')).read().replace('{P}', p)}</body>
</html>
'''

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>\n'

PERSON = {"@type": "Person", "@id": SITE + "/#alexandre", "name": "Alexandre Cottret",
          "jobTitle": "Intégrateur en automatisation IA et webdesigner", "url": SITE + "/",
          "image": SITE + "/assets/alexandre.webp", "sameAs": [LINKEDIN, MALT, MALT1, "https://www.trend-design.fr/"]}
ORG = {"@type": "Organization", "@id": SITE + "/#entreprise", "name": "Automatisation IA PME", "url": SITE + "/",
       "logo": {"@type": "ImageObject", "url": SITE + "/assets/logo-512.png", "width": 512, "height": 512}}

def crumbs_html(items):
    out = []
    for i, (name, url) in enumerate(items):
        out.append(f'<li><a href="{url}">{esc(name)}</a></li>' if url and i < len(items) - 1 else f'<li aria-current="page">{esc(name)}</li>')
    return '<ol class="crumbs">' + ''.join(out) + '</ol>'

def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + "/" + u} for i, (n, u) in enumerate(items)]}

# ---------------------------------------------------------------- articles
ARTICLES = sorted(json.load(open(os.path.join(SRC, 'articles.json'))), key=lambda a: a['date'], reverse=True)
BY = {a['slug']: a for a in ARTICLES}

def words(t):
    return len(re.sub(r'<[^>]+>', ' ', t).split())

def article_page(a):
    p = '../'
    body = open(os.path.join(SRC, 'articles', a['slug'] + '.html')).read()
    toc = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    n = words(body) + words(' '.join(q + r for q, r in a['faq'])) + words(a['lead'])
    DATE, DATE_FR = a['date'], fr_date(a['date'])
    # inline CTA after the 3rd h2
    parts = re.split(r'(?=<h2 id=)', body)
    cta = f'<div class="cta-inline"><p>Vous voulez savoir si une de vos tâches s\'automatise avec l\'IA ? 20 minutes suffisent.</p><a class="btn btn--primary" href="{CAL}" rel="noopener">Réserver l\'audit offert</a></div>\n'
    if len(parts) > 4:
        parts.insert(4, cta)
    body = ''.join(parts)
    path = f'blog/{a["slug"]}.html'
    items = [('Accueil', ''), ('Blog', 'blog.html'), (a['short'], path)]
    crumb_links = [('Accueil', '../'), ('Blog', '../blog.html'), (a['short'], None)]
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "@id": SITE + "/" + path + "#article", "headline": a['h1'], "description": a['meta'],
         "image": SITE + f"/assets/og-{a['slug']}.jpg", "datePublished": DATE, "dateModified": DATE, "inLanguage": "fr-FR",
         "wordCount": n, "author": PERSON, "publisher": ORG, "mainEntityOfPage": SITE + "/" + path,
         "articleSection": a['cat']},
        crumbs_ld(items),
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in a['faq']]}]}
    out = head(a['title_tag'], a['meta'], path, p, f"og-{a['slug']}.jpg", 'article',
               f'<meta property="article:published_time" content="{DATE}">\n<meta property="article:modified_time" content="{DATE}">\n<meta property="article:author" content="Alexandre Cottret">\n' + ld(graph))
    out += header(p)
    summary = ''.join(f'<li>{esc(x)}</li>' for x in a['summary'])
    tocl = ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in toc) + '<li><a href="#faq">Questions fréquentes</a></li>'
    faq = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(r)}</p></details>' for q, r in a['faq'])
    src = ''.join(f'<li><a href="{u}" rel="noopener">{esc(t)}</a></li>' for t, u in a['sources'])
    rel = ''.join(f'<a href="{r}.html"><span>{BY[r]["cat"]}</span>{esc(BY[r]["short"])}</a>' for r in a['related'])
    out += f'''<main>
<article>
<div class="content"><div class="content__frame">
<header class="page-head"><div class="page-head__in">
<nav aria-label="Fil d'Ariane">{crumbs_html(crumb_links)}</nav>
<p class="eyebrow">{esc(a['eyebrow'])}</p>
<h1 class="page-title">{esc(a['h1'])}</h1>
<p class="lead">{esc(a['lead'])}</p>
<div class="byline"><img src="{p}assets/alexandre-160.webp" alt="" width="44" height="44"><div><b>Alexandre Cottret</b>Publié le <time datetime="{DATE}">{DATE_FR}</time></div></div>
</div></header>
<div class="art-wrap"><div class="art">
<div class="box summary"><p class="box__t">En bref</p><ul>{summary}</ul></div>
<nav class="box toc" aria-label="Sommaire"><p class="box__t">Sommaire</p><ol>{tocl}</ol></nav>
{body}
<h2 id="faq">Questions fréquentes</h2>
<div class="faq">{faq}</div>
<h2 id="auteur">À propos de l'auteur</h2>
<div class="box author"><img src="{p}assets/alexandre-160.webp" alt="Alexandre Cottret" width="96" height="96" loading="lazy">
<div><p class="author__name">Alexandre Cottret</p>
<p>Intégrateur en automatisation IA (Make, Zapier, n8n) et webdesigner indépendant depuis 2021. J'ai créé plus de 165 sites pour des TPE et PME, avec une note de 4,97/5 sur 91 avis Malt. Aujourd'hui, j'automatise avec l'IA ce qui se passe après le formulaire de contact : demandes, devis, relances et documents.</p>
<p><a href="{LINKEDIN}" rel="noopener">LinkedIn</a> · <a href="{MALT1}" rel="noopener">Avis Malt</a> · <a href="../">Mon offre d'automatisation IA</a></p></div></div>
<h2 id="sources">Sources</h2>
<ul class="sources">{src}</ul>
<p class="small">Article publié le {DATE_FR}. Les informations sur les outils et la réglementation sont vérifiées à cette date ; les tarifs des éditeurs évoluent régulièrement.</p>
<h2 id="a-lire">À lire aussi</h2>
<div class="related">{rel}</div>
</div></div>
</div></div>
</article>
</main>
<div class="content"><div class="content__frame">
'''
    out += footer(p)
    # close frame wrappers before body end: wrap band+footer inside frame
    out = out.replace('<div class="fab">', '</div></div>\n<div class="fab">', 1)
    return out

def blog_page():
    p = ''
    path = 'blog.html'
    items = [('Accueil', ''), ('Blog', path)]
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "@id": SITE + "/blog.html#blog", "name": "Blog Automatisation IA PME", "url": SITE + "/blog.html", "inLanguage": "fr-FR",
         "publisher": ORG, "blogPost": [{"@type": "BlogPosting", "headline": a['h1'], "url": SITE + f"/blog/{a['slug']}.html", "datePublished": a['date'], "author": {"@id": SITE + "/#alexandre"}} for a in ARTICLES]},
        crumbs_ld(items)]}
    out = head("Blog automatisation IA pour PME : guides et comparatifs", "Guides pratiques sur l'automatisation IA en TPE et PME : agents IA 24/7, Zapier, Make, n8n, CRM. Des conseils concrets, sans jargon, par Alexandre Cottret.", path, p, 'og-blog.jpg', 'website', ld(graph))
    out += header(p)
    cards = ''.join(f'<a class="card" href="blog/{a["slug"]}.html"><p class="eyebrow">{a["cat"]} · {fr_date(a["date"])}</p><h2>{esc(a["h1"])}</h2><p>{esc(a["meta"])}</p></a>' for a in ARTICLES)
    out += f'''<div class="content"><div class="content__frame"><main>
<header class="page-head"><div class="page-head__in">
<nav aria-label="Fil d'Ariane">{crumbs_html([('Accueil', './'), ('Blog', None)])}</nav>
<p class="eyebrow">Ressources</p>
<h1 class="page-title">Guides sur l'automatisation IA en PME</h1>
<p class="lead">Des conseils concrets pour automatiser vos demandes, devis, relances et documents avec l'intelligence artificielle, sans jargon et sans perdre la main.</p>
</div></header>
<div class="art-wrap"><div class="cards">{cards}</div></div>
'''
    out += '</main>\n' + footer(p).replace('<div class="fab">', '</div></div>\n<div class="fab">', 1)
    return out

def legal_page():
    p = ''
    path = 'mentions-legales.html'
    T = '<span class="todo">[À COMPLÉTER]</span>'
    out = head("Mentions légales et confidentialité · Automatisation IA PME", "Mentions légales, politique de confidentialité et cookies du site automatisation-ia-pme.fr, édité par Alexandre Cottret.", path, p, 'og-home.jpg')
    out += header(p)
    out += f'''<div class="content"><div class="content__frame"><main>
<header class="page-head"><div class="page-head__in">
<nav aria-label="Fil d'Ariane">{crumbs_html([('Accueil', './'), ('Mentions légales', None)])}</nav>
<h1 class="page-title">Mentions légales et confidentialité</h1>
<p class="lead">Dernière mise à jour : {fr_date(LEGAL_DATE)}.</p>
</div></header>
<div class="art-wrap"><div class="art legal">
<h2 id="editeur">Éditeur du site</h2>
<p>Le site automatisation-ia-pme.fr est édité par <strong>Alexandre Cottret</strong>, entrepreneur individuel (micro-entreprise), exerçant sous les noms commerciaux « Automatisation IA PME » et « Trend Design ».</p>
<ul>
<li>Adresse : 15 boulevard Cordier, 02100 Saint-Quentin</li>
<li>SIREN : 905 374 237 · SIRET : 905 374 237 00014 (inscrit au Registre national des entreprises)</li>
<li>TVA intracommunautaire : FR18905374237</li>
<li>Code APE : 6201Z</li>
<li>Téléphone : 07 67 46 38 70</li>
<li>E-mail : trend.design.be@gmail.com</li>
<li>Directeur de la publication : Alexandre Cottret</li>
</ul>
<h2 id="hebergeur">Hébergeur</h2>
<p>Netlify, Inc., 512 2nd Street, Suite 200, San Francisco, CA 94107, États-Unis. Site : netlify.com.</p>
<h2 id="propriete">Propriété intellectuelle</h2>
<p>Les textes, illustrations et éléments graphiques de ce site sont la propriété d'Alexandre Cottret, sauf mention contraire. Les noms et logos des outils cités (Zapier, Make, n8n, Claude, ChatGPT, HubSpot, etc.) appartiennent à leurs propriétaires respectifs et sont utilisés uniquement pour désigner les outils avec lesquels je travaille. Les avis clients présentés proviennent de mon profil Malt.</p>
<h2 id="confidentialite">Politique de confidentialité</h2>
<p>Ce site ne comporte aucun formulaire. En dehors de la mesure d'audience décrite plus bas, soumise à votre accord, il ne collecte aucune donnée personnelle par lui-même. Vous pouvez me contacter de trois façons, chacune soumise à la politique de confidentialité de son service :</p>
<ul>
<li><strong>Prise de rendez-vous</strong> via Calendly (Calendly LLC) : nom, adresse e-mail et informations que vous choisissez de renseigner.</li>
<li><strong>WhatsApp</strong> (WhatsApp Ireland Ltd) : numéro de téléphone et contenu de vos messages.</li>
<li><strong>Téléphone ou e-mail</strong>.</li>
</ul>
<p><strong>Finalité :</strong> répondre à votre demande, préparer un audit ou un devis, puis assurer le suivi de la relation commerciale. <strong>Base légale :</strong> mesures précontractuelles prises à votre demande, puis exécution du contrat. <strong>Durée de conservation :</strong> trois ans après le dernier contact pour un prospect, et pendant la durée légale de conservation des documents comptables pour un client.</p>
<p>Vos données ne sont ni vendues ni cédées. Vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation, d'opposition et de portabilité : il suffit de m'écrire par e-mail ou par WhatsApp. Si vous estimez que vos droits ne sont pas respectés, vous pouvez adresser une réclamation à la CNIL (cnil.fr).</p>
<h2 id="cookies">Cookies</h2>
<p>Avec votre accord uniquement, ce site utilise <strong>Google Analytics 4</strong> (Google Ireland Ltd) pour mesurer son audience : pages consultées, durée de visite, provenance des visiteurs et clics sur les boutons de contact. Ces statistiques servent seulement à améliorer le site.</p>
<ul>
<li><strong>Cookies déposés :</strong> _ga et _ga_* (identifiant de mesure aléatoire), pour une durée maximale de 13 mois.</li>
<li><strong>Consentement :</strong> rien n'est déposé tant que vous n'avez pas cliqué sur « Accepter ». Votre choix, accepté ou refusé, est conservé 6 mois dans votre navigateur.</li>
<li><strong>Changer d'avis :</strong> à tout moment via le lien « Gérer les cookies » en bas de chaque page. En cas de refus, les cookies de mesure sont supprimés.</li>
<li><strong>Transfert de données :</strong> Google peut traiter certaines données aux États-Unis, dans le cadre du Data Privacy Framework UE / États-Unis.</li>
</ul>
<p>Les polices de caractères sont hébergées sur le site lui-même, sans appel à un service tiers. Les liens vers Calendly, WhatsApp, Malt ou LinkedIn vous mènent vers des sites qui appliquent leur propre politique de cookies.</p>
</div></div>
'''
    out += '</main>\n' + footer(p, band=False).replace('<div class="fab">', '</div></div>\n<div class="fab">', 1)
    return out

sys.path.insert(0, SRC)
from tools_data import TOOLS
TICONS = json.load(open(os.path.join(SRC, 'tool_icons.json')))

def tool_page(t):
    p = ''
    path = t['slug'] + '.html'
    url = SITE + '/' + path
    items = [('Accueil', ''), (t['menu'][0], path)]
    strip = lambda s: re.sub(r'<[^>]+>', '', s)
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "@id": url + "#service", "name": t['h1'], "url": url, "serviceType": "Automatisation " + t['tool'],
         "description": t['desc'], "provider": {"@id": SITE + "/#entreprise"}, "areaServed": {"@type": "Country", "name": "France"},
         "offers": {"@type": "Offer", "price": "590", "priceCurrency": "EUR", "description": "Automatisation simple, prix fixe à partir de 590 €"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in t['faq']]},
        crumbs_ld(items)]}
    out = head(t['title'], t['desc'], path, p, 'og-' + t['slug'] + '.jpg', 'website', ld(graph))
    out += header(p)
    sec = lambda id_, eb, h2, lead, body: f'<section class="fsec" id="{id_}"><div class="fsec__head"><p class="eyebrow">{eb}</p><h2 class="fh2">{h2}</h2>' + (f'<p class="fsec__lead">{lead}</p>' if lead else '') + f'</div>{body}</section>\n'
    icon = TICONS.get(t['tool'], '').replace('<svg', '<svg class="pcard__logo"', 1)
    flow = ''.join(f'<li class="fl" style="--d:{0.4 + i * 0.7:.1f}s"><span>{a}</span>{b}</li>' for i, (a, b) in enumerate(t['flow']))
    out += f'''<div class="content"><div class="content__frame"><main>
<header class="fhero">
<div class="fhero__txt">
<nav aria-label="Fil d'Ariane">{crumbs_html([('Accueil', './'), (t['menu'][0], None)])}</nav>
<p class="eyebrow">{t['eyebrow']}</p>
<h1 class="page-title">{t['h1']}</h1>
<p class="lead">{t['lead']}</p>
<div class="fhero__btns"><a class="btn btn--primary" href="{CAL}" rel="noopener">Réserver un audit offert</a><a class="btn btn--ghost" href="#cas-pratiques">Voir les cas pratiques</a></div>
<ul class="trust"><li><b>★ 4,97/5</b> · 91 avis Malt</li><li><b>Dès 590 €</b> · prix fixe</li><li><b>Comptes à votre nom</b></li></ul>
</div>
<div class="fhero__art" aria-hidden="true"><div class="pcard"><p class="pcard__h">{icon}Exemple de scénario {t['tool']}</p><ol class="pcard__flow">{flow}</ol><div class="pcard__ok fl-ok" style="--d:{0.4 + len(t['flow']) * 0.7:.1f}s">✓ {t['flow_ok']}</div></div></div>
</header>
'''
    out += sec('usages', 'Cas d\'usage', t['uses_h2'], t['uses_lead'],
               '<div class="grid3">' + ''.join(f'<div class="fcard"><h3>{a}</h3><p>{b}</p></div>' for a, b in t['uses']) + '</div>')
    cases = ''.join(f'''<article class="case"><h3>{ti}</h3><p class="case__ctx">{ctx}</p><ul class="timeline">{''.join(f"<li><b>{s}</b>{d}</li>" for s, d in steps)}</ul><p class="case__res">✓ {res}</p></article>''' for ti, ctx, steps, res in t['cases'])
    out += sec('cas-pratiques', 'Cas pratiques', t.get('cases_h2', 'Trois cas pratiques, étape par étape'), "Des scénarios types, construits sur des besoins réels de TPE et PME. Les vôtres seront adaptés à vos outils.",
               f'<div class="cases">{cases}</div>')
    out += sec('pourquoi', 'Pourquoi ' + t['tool'], t['why_h2'], None,
               '<div class="grid3">' + ''.join(f'<div class="fcard"><h3>{a}</h3><p>{b}</p></div>' for a, b in t['why']) + f'</div><p class="fnote">{t["limit"]}</p>')
    rows = t['table']
    tbl = '<div class="tbl"><table><thead><tr>' + ''.join(f'<th scope="col">{c}</th>' for c in rows[0]) + '</tr></thead><tbody>' + ''.join('<tr><th scope="row">' + r[0] + '</th>' + ''.join(f'<td>{c}</td>' for c in r[1:]) + '</tr>' for r in rows[1:]) + '</tbody></table></div>'
    out += sec('comparatif', 'Comparatif', t['table_h2'], None, tbl + '<p class="fnote">Le détail des différences est dans le guide <a href="blog/zapier-make-n8n-choisir.html">Zapier, Make ou n8n : lequel choisir</a>.</p>')
    steps = [("01", "Audit offert", "20 minutes pour repérer la tâche qui vous coûte le plus de temps et vérifier qu'elle s'automatise."),
             ("02", "Prix fixe", "Dès 590 € pour une automatisation simple. Périmètre, outils et délai annoncés par écrit."),
             ("03", "Mise en production", f"Construction sur {t['tool']}, tests sur vos vrais cas, documentation simple."),
             ("04", "Suivi", "Surveillance et ajustements chaque mois si vous le souhaitez. Vous restez propriétaire de tout.")]
    out += sec('methode', 'Méthode', 'Comment on travaille ensemble', None,
               '<ol class="steps">' + ''.join(f'<li><b>{n}</b><h3>{a}</h3><p>{b}</p></li>' for n, a, b in steps) + '</ol>')
    out += sec('faq', 'Questions fréquentes', f"Vos questions sur l'automatisation {t['tool']}", None,
               '<div class="faq">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in t['faq']) + '</div>')
    same = [x for x in TOOLS if x['slug'] != t['slug'] and x['group'] == t['group']]
    others = (same + [x for x in TOOLS[:3] if x['slug'] != t['slug'] and x not in same])[:5]
    rel = ''.join(f'<a href="{x["slug"]}.html"><span>{x["group"]}</span>{x["menu"][0]}</a>' for x in others) + '<a href="integrations.html"><span>Tous les outils</span>Toutes les intégrations</a>'
    out += sec('voir-aussi', 'Voir aussi', 'Les autres outils', None, f'<div class="related">{rel}</div>')
    out += '</main>\n' + footer(p, band_title=f"Un scénario {t['tool']} en tête ?").replace('<div class="fab">', '</div></div>\n<div class="fab">', 1)
    return out

def integrations_page():
    p = ''
    path = 'integrations.html'
    items = [('Accueil', ''), ('Intégrations', path)]
    groups = []
    for t in TOOLS:
        if t['group'] not in groups: groups.append(t['group'])
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "ItemList", "name": "Outils automatisés par Automatisation IA PME", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t['menu'][0], "url": SITE + '/' + t['slug'] + '.html'} for i, t in enumerate(TOOLS)]},
        crumbs_ld(items)]}
    out = head("Intégrations : n8n, Make, Zapier, Claude, Notion, HubSpot, Excel", "Toutes les intégrations d'Automatisation IA PME : n8n, Make, Zapier, Claude, ChatGPT, HubSpot, Airtable, Notion, Google Sheets, Excel, WhatsApp, Gmail, Wix.", path, p, 'og-home.jpg', 'website', ld(graph))
    out += header(p)
    blocks = ''
    for g in groups:
        cards = ''.join(f'<a class="tcard" href="{t["slug"]}.html">{TICONS.get(t["tool"], "").replace("<svg", "<svg class=\"tcard__logo\"", 1)}<b>{t["menu"][0]}</b><span>{t["menu"][1]}</span></a>' for t in TOOLS if t['group'] == g)
        blocks += f'<div class="tgroup"><p class="eyebrow">{g}</p><div class="tcards">{cards}</div></div>'
    out += f'''<div class="content"><div class="content__frame"><main>
<header class="page-head"><div class="page-head__in">
<nav aria-label="Fil d'Ariane">{crumbs_html([('Accueil', './'), ('Intégrations', None)])}</nav>
<p class="eyebrow">Intégrations</p>
<h1 class="page-title">Les outils que j'automatise pour votre PME</h1>
<p class="lead">Je relie l'intelligence artificielle aux outils que vous utilisez déjà. Choisissez un outil pour voir des cas d'usage concrets, étape par étape.</p>
</div></header>
<section class="fsec"><div class="tgroups">{blocks}</div></section>
'''
    out += '</main>\n' + footer(p).replace('<div class="fab">', '</div></div>\n<div class="fab">', 1)
    return out

FORMATION_DATE = '2026-10-22'

def formation_page():
    p = ''
    path = FORMATION
    url = SITE + '/' + path
    items = [('Accueil', ''), ('Formation automatisation IA', path)]
    title = "Formation automatisation IA sur mesure : n8n, Make, Zapier"
    desc = "Formation automatisation IA en visio pour TPE et PME : Claude, ChatGPT, Zapier, Make et n8n, sur vos propres outils. Dès 150 €, prix fixe."
    cmp_url = 'blog/zapier-make-n8n-choisir.html'
    faqs = [
        ("La formation est-elle éligible au CPF ?",
         "Non. Pour être finançable par le CPF, une formation doit préparer à une certification enregistrée et être dispensée par un organisme certifié Qualiopi. J'ai fait un autre choix : des séances courtes et sur mesure, à prix fixe, nettement moins chères qu'une formation certifiante. Si le financement CPF est indispensable pour vous, une formation certifiante sera plus adaptée."),
        ("Faut-il des connaissances techniques ?",
         "Non. Savoir utiliser un navigateur et une messagerie suffit. On part de votre niveau, et le module sur les agents IA avec n8n n'arrive qu'une fois les bases acquises."),
        ("Par quel outil commencer : Zapier, Make ou n8n ?",
         f"Zapier est le plus simple pour une première automatisation, Make le plus lisible pour des scénarios avec conditions, n8n le plus complet pour les agents IA et l'hébergement des données en Europe. En formation, on commence presque toujours par Zapier ou Make, puis on passe à n8n si votre besoin le justifie. Le détail est dans mon <a href=\"{cmp_url}\">comparatif Zapier, Make et n8n</a>."),
        ("Existe-t-il une formation automatisation IA gratuite ?",
         "Oui pour découvrir : Zapier, Make et n8n proposent chacun des tutoriels gratuits (surtout en anglais), et l'édition communautaire de n8n est gratuite si vous l'hébergez vous-même. Ces ressources suffisent pour comprendre les principes. Une formation accompagnée vous fait surtout gagner du temps sur votre cas réel. L'appel de cadrage de 20 minutes est offert, et mes guides sont en accès libre sur le <a href=\"blog.html\">blog</a>."),
        ("Combien de temps faut-il pour être autonome ?",
         "Pour une automatisation simple, 5 heures suffisent en général : vous repartez avec un scénario qui tourne et la méthode pour en créer d'autres. Pour construire des agents IA sur n8n, comptez plutôt 10 heures."),
        ("Peut-on suivre la formation en équipe ?",
         "Oui, jusqu'à 4 personnes avec la formule Équipe, en visio. Chacun travaille sur ses propres tâches, pour que la formation serve dès le lendemain."),
        ("Quelle différence avec une automatisation clé en main ?",
         "En formation, vous apprenez à construire vous-même. Si vous préférez déléguer, je mets aussi l'automatisation en place pour vous, à prix fixe : voyez l'<a href=\"./\">offre d'automatisation IA</a>. Beaucoup de clients combinent les deux : je construis l'automatisation principale, puis je forme l'équipe à la faire évoluer."),
        ("Où se déroulent les séances ?",
         "En visio sur Google Meet, avec partage d'écran, partout en France. Vous pratiquez sur vos propres comptes, ce qui évite de tout refaire après la formation."),
    ]
    strip = lambda t: re.sub(r'<[^>]+>', '', t)
    offers = [("Prise en main", 150, "PT2H"), ("Première automatisation", 350, "PT5H"), ("Équipe", 700, "PT10H")]
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "Course", "@id": url + "#formation", "name": "Formation automatisation IA", "url": url,
         "description": "Formation sur mesure, en visio, pour apprendre à utiliser Claude et ChatGPT puis à créer des automatisations avec Zapier, Make et n8n, sur ses propres outils.",
         "inLanguage": "fr", "educationalLevel": "Débutant", "provider": ORG, "author": PERSON,
         "teaches": ["IA générative au quotidien avec Claude et ChatGPT", "Automatisation avec Zapier et Make", "Agents IA avec n8n", "Automatisation des tâches administratives", "RGPD et validation humaine"],
         "hasCourseInstance": [{"@type": "CourseInstance", "name": n, "courseMode": "Online", "courseWorkload": w, "instructor": {"@id": SITE + "/#alexandre"}} for n, _, w in offers],
         "offers": [{"@type": "Offer", "name": n, "price": str(pr), "priceCurrency": "EUR", "category": "Paid", "url": url + "#formules", "availability": "https://schema.org/InStock"} for n, pr, _ in offers]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]},
        crumbs_ld(items)]}
    out = head(title, desc, path, p, 'og-formation.jpg', 'website', ld(graph))
    out += header(p)
    sec = lambda id_, eb, h2, lead, body: f'<section class="fsec" id="{id_}"><div class="fsec__head"><p class="eyebrow">{eb}</p><h2 class="fh2">{h2}</h2>' + (f'<p class="fsec__lead">{lead}</p>' if lead else '') + f'</div>{body}</section>\n'
    who = [("Dirigeants de TPE et PME", "Comprendre ce que l'IA peut vraiment faire dans votre entreprise, et automatiser vous-même vos premières tâches."),
           ("Assistants et fonctions administratives", "Automatiser les tâches administratives qui reviennent chaque semaine : saisie, relances, classement, comptes rendus."),
           ("Indépendants, alternants, marketing", "Gagner du temps sur la rédaction, la prospection et le suivi client, avec des outils simples et peu coûteux.")]
    goals = ["Utiliser Claude et ChatGPT avec des consignes précises, adaptées à votre métier",
             "Repérer les tâches répétitives qui valent vraiment la peine d'être automatisées",
             "Créer un scénario Zapier ou Make : déclencheur, actions, filtres",
             "Ajouter l'IA dans une automatisation pour lire, classer, résumer ou rédiger",
             "Comprendre ce qu'est un agent IA, et savoir quand passer à n8n",
             "Garder la main : validation humaine, RGPD, données sensibles"]
    mods = [("01", "Débutant", "IA générative : les bases utiles", "Ce que Claude, ChatGPT et Mistral savent faire, leurs limites, et comment écrire une consigne qui donne un bon résultat du premier coup."),
            ("02", "Débutant", "Claude et ChatGPT au quotidien", "Rédiger un e-mail, résumer une réunion, préparer un devis ou une fiche produit, avec vos propres modèles de consignes."),
            ("03", "Débutant", "Votre première automatisation", "Zapier ou Make, pas à pas : un formulaire qui crée la fiche client, ajoute une ligne dans Google Sheets et vous prévient."),
            ("04", "Intermédiaire", "L'IA dans vos scénarios", "Faire lire, classer et résumer les demandes ou les factures par l'IA, puis préparer une réponse que vous validez."),
            ("05", "Avancé", "Agents IA avec n8n", "Un agent qui cherche dans votre CRM, consulte l'agenda et prépare un brouillon. Hébergement des données en Europe possible."),
            ("06", "Tous niveaux", "Garder la main", "Validation humaine, RGPD, règlement européen sur l'IA, documentation : les bons réflexes pour automatiser sans risque.")]
    admin = [("Tâche", "Outils", "Ce que vous construisez"),
             ("Saisie des demandes", "Zapier ou Make, Google Sheets, HubSpot", "Chaque formulaire crée la fiche client, sans ressaisie"),
             ("Relances de devis", "Zapier, Gmail", "Une relance personnalisée après 3 jours sans réponse"),
             ("Factures fournisseurs", "Make, Google Drive, IA", "La facture est lue, renommée, rangée, et ses montants saisis"),
             ("Comptes rendus de réunion", "Claude ou ChatGPT", "Un résumé en 5 lignes avec décisions et prochaines étapes"),
             ("Rappels de rendez-vous", "Make ou n8n, Google Agenda", "Un rappel envoyé la veille à chaque client")]
    prices = [("Prise en main", "150 €", "2 h", "Pour découvrir l'IA générative et l'utiliser dès le lendemain.",
               ["Claude et ChatGPT sur vos tâches réelles", "Vos modèles de consignes, prêts à réutiliser", "Un récapitulatif écrit après la séance"], False),
              ("Première automatisation", "350 €", "5 h", "Pour repartir avec une automatisation qui tourne sur vos outils.",
               ["Modules 1 à 4, en 2 ou 3 séances", "Une automatisation Zapier ou Make construite ensemble", "Un récapitulatif écrit après chaque séance"], True),
              ("Équipe", "700 €", "10 h", "Pour rendre une équipe autonome, jusqu'à 4 personnes.",
               ["Programme complet, agents IA n8n inclus", "Exercices sur les tâches de chaque participant", "La documentation des automatisations créées"], False)]
    steps = [("01", "Appel de cadrage offert", "20 minutes pour faire le point sur votre niveau, vos outils et la tâche à automatiser."),
             ("02", "Programme sur mesure", "Je vous envoie par écrit le contenu des séances, leur nombre et le prix, sans surprise."),
             ("03", "Séances en visio", "Sur Google Meet, avec partage d'écran. Vous pratiquez directement sur vos comptes."),
             ("04", "Récapitulatif écrit", "Après chaque séance : les étapes, vos consignes et les liens utiles, pour refaire seul.")]
    cmp_rows = [("", "Formation certifiante", "Inter-entreprises", "Sur mesure (cette formation)"),
                ("Format", "30 à 50 h, en groupe, souvent à distance", "2 à 3 jours, en salle ou à distance", "2 à 10 h, en individuel ou jusqu'à 4 personnes"),
                ("Prix observés", "1 300 à 1 900 €", "Environ 1 600 € HT par participant, 2 660 € en intra", "150 à 700 €"),
                ("Financement", "CPF, France Travail, OPCO", "OPCO, si l'organisme est certifié Qualiopi", "Non finançable, prix fixe"),
                ("Sur vos outils", "En partie", "Rarement", "Oui, sur vos propres comptes"),
                ("Idéal si", "Vous visez une certification", "Vous formez plusieurs salariés à la fois", "Vous voulez un résultat concret, vite")]
    tbl = lambda rows: '<div class="tbl"><table><thead><tr>' + ''.join(f'<th scope="col">{c}</th>' for c in rows[0]) + '</tr></thead><tbody>' + ''.join('<tr><th scope="row">' + r[0] + '</th>' + ''.join(f'<td>{c}</td>' for c in r[1:]) + '</tr>' for r in rows[1:]) + '</tbody></table></div>'
    out += f'''<div class="content"><div class="content__frame"><main>
<header class="fhero">
<div class="fhero__txt">
<nav aria-label="Fil d'Ariane">{crumbs_html([('Accueil', './'), ('Formation automatisation IA', None)])}</nav>
<p class="eyebrow">Formation · IA et automatisation</p>
<h1 class="page-title">Formation automatisation IA pour TPE et PME</h1>
<p class="lead">En visio, sur vos propres outils : apprenez à utiliser Claude et ChatGPT, puis à créer vos automatisations avec Zapier, Make ou n8n. Vous repartez avec une automatisation qui tourne.</p>
<div class="fhero__btns"><a class="btn btn--primary" href="{CAL}" rel="noopener">Réserver l'appel de cadrage</a><a class="btn btn--ghost" href="#formules">Voir les formules</a></div>
<ul class="trust"><li><b>★ 4,97/5</b> · 91 avis Malt</li><li><b>Ambassadeur Superprof</b> · 5/5</li><li><b>Dès 150 €</b> · prix fixe</li></ul>
</div>
<div class="fhero__art" aria-hidden="true"><div class="pcard"><p class="pcard__h">Formule Première automatisation</p><ol>
<li><span>Séance 1</span>Claude et ChatGPT au quotidien</li>
<li><span>Séance 2</span>Votre première automatisation Zapier ou Make</li>
<li><span>Séance 3</span>L'IA dans votre scénario, testée sur vos vrais cas</li>
</ol><div class="pcard__ok">✓ Automatisation en production</div></div></div>
</header>
'''
    out += sec('pour-qui', 'Pour qui', 'Une formation IA et automatisation pensée pour les petites structures',
               "Pas besoin d'être technicien. La formation part de vos tâches réelles, pas d'exercices génériques.",
               '<div class="grid3">' + ''.join(f'<div class="fcard"><h3>{t}</h3><p>{d}</p></div>' for t, d in who) + '</div>')
    out += sec('objectifs', 'Objectifs', 'Ce que vous saurez faire à la fin',
               "Une formation à l'automatisation avec l'IA doit vous rendre autonome sur des cas concrets. Voici les compétences visées.",
               '<ul class="checks">' + ''.join(f'<li>{g}</li>' for g in goals) + '</ul>')
    out += sec('programme', 'Programme', 'Programme de la formation automatisation IA',
               "Six modules, adaptés à votre niveau et à vos outils après l'appel de cadrage. Les formules courtes en reprennent une partie.",
               '<div class="mods">' + ''.join(f'<div class="mod"><div class="mod__top"><span class="mod__n">{n}</span><span class="mod__tag">{tg}</span></div><h3>{t}</h3><p>{d}</p></div>' for n, tg, t, d in mods) + '</div>')
    out += sec('taches-administratives', 'Cas pratiques', 'Automatiser vos tâches administratives : les exemples travaillés',
               "On choisit ensemble une ou deux de ces tâches, ou la vôtre si elle n'est pas dans la liste.",
               tbl(admin))
    out += sec('formules', 'Formules et tarifs', 'Trois formules, un prix fixe',
               "Séances en visio, à votre rythme. Le prix est annoncé avant de commencer.",
               '<div class="prices">' + ''.join(
                   f'<div class="price{" price--hl" if hl else ""}">' + ('<span class="price__badge">Recommandée</span>' if hl else '') +
                   f'<p class="price__name">{n}</p><p class="price__amt">{a}<small>{d}</small></p><p>{tx}</p><ul>' + ''.join(f'<li>{x}</li>' for x in li) +
                   f'</ul><a class="btn {"btn--primary" if hl else "btn--ghost"}" href="{CAL}" rel="noopener">Réserver l\'appel de cadrage</a></div>'
                   for n, a, d, tx, li, hl in prices) + '</div>'
               + '<p class="fnote">Formation non éligible au CPF (voir la question plus bas). Les abonnements aux outils restent à votre charge, mais les versions gratuites de Zapier, Make, ChatGPT et Claude suffisent pour débuter.</p>')
    out += sec('deroule', 'Déroulé', 'Comment se passe la formation', None,
               '<ol class="steps">' + ''.join(f'<li><b>{n}</b><h3>{t}</h3><p>{d}</p></li>' for n, t, d in steps) + '</ol>')
    out += sec('choisir', 'Comparatif', 'Comment choisir la meilleure formation automatisation IA ?',
               "Trois formats coexistent. Aucun n'est meilleur dans l'absolu : tout dépend de votre objectif, de votre budget et du temps dont vous disposez.",
               tbl(cmp_rows) + '<p class="fnote">Prix relevés en octobre 2026 sur des formations publiées en ligne, à titre indicatif. Quel que soit le format, vérifiez trois choses : que vous pratiquez sur vos propres outils, que le programme va jusqu\'à l\'IA dans les scénarios (pas seulement ChatGPT), et, si vous cherchez la meilleure formation n8n, qu\'elle couvre les agents IA et l\'hébergement des données.</p>')
    out += sec('formateur', 'Qui vous forme', 'Votre formateur automatisation IA', None,
               f'''<div class="trainer"><img src="assets/alexandre.webp" alt="Alexandre Cottret, formateur en automatisation IA" width="768" height="865" loading="lazy">
<div class="trainer__txt"><p class="trainer__name">Alexandre Cottret</p><p class="trainer__role">Intégrateur en automatisation IA (n8n, Make, Zapier) et webdesigner</p>
<p>Je crée des sites internet depuis 2021 et j'automatise aujourd'hui les demandes, devis et relances des TPE et PME avec n8n, Make, Zapier, Claude et ChatGPT. Ce que j'enseigne, je l'utilise chaque semaine chez mes clients : vous apprenez des méthodes testées sur de vrais projets, pas des démonstrations.</p>
<p>Je donne aussi des cours en visio depuis 2023, avec une règle simple : pas de théorie inutile. On construit ensemble, sur vos outils, et vous repartez avec quelque chose qui fonctionne.</p>
<ul class="trainer__stats"><li><b>165+</b><span>sites livrés depuis 2021</span></li><li><b>4,97/5</b><span>sur 91 avis Malt</span></li><li><b>5/5</b><span>Professeur Ambassadeur Superprof</span></li></ul>
</div></div>''')
    out += sec('faq', 'Questions fréquentes', 'Vos questions sur la formation', None,
               '<div class="faq">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs) + '</div>')
    rel = [BY[s] for s in ('agent-ia-24-7-pme', 'zapier-make-n8n-choisir', 'agence-n8n-pme') if s in BY]
    out += sec('guides', 'Pour aller plus loin', 'Guides gratuits', None,
               '<div class="related">' + ''.join(f'<a href="blog/{a["slug"]}.html"><span>{a["cat"]}</span>{esc(a["short"])}</a>' for a in rel) + '</div>')
    out += '</main>\n' + footer(p, band_title='Prêt à automatiser votre première tâche ?', band_cta="Réserver l'appel de cadrage").replace('<div class="fab">', '</div></div>\n<div class="fab">', 1)
    return out

def notfound_page():
    p = '/'
    out = head("Page introuvable · Automatisation IA PME", "Cette page n'existe pas ou a été déplacée.", '404.html', p, 'og-home.jpg')
    out = out.replace('content="index, follow, max-image-preview:large"', 'content="noindex"', 1)
    out += header(p).replace('href="/#', 'href="/#')
    out += f'''<div class="content"><div class="content__frame"><main>
<header class="page-head"><div class="page-head__in">
<p class="eyebrow">Erreur 404</p>
<h1 class="page-title">Cette page n'existe pas, ou plus.</h1>
<p class="lead">Elle a peut-être été déplacée. Revenez à l'accueil ou parcourez les guides.</p>
<p><a class="btn btn--primary" href="/">Retour à l'accueil</a> <a class="btn btn--ghost" href="/blog.html">Voir le blog</a></p>
</div></header>
'''
    out += '</main>\n' + footer(p, band=False).replace('<div class="fab">', '</div></div>\n<div class="fab">', 1)
    return out

def build_index():
    s = open(os.path.join(SRC, 'index.html')).read()
    s = re.sub(r'<!--FONTS-->.*?<!--/FONTS-->', lambda m: fonts(''), s, flags=re.S)
    if FONTS == 'self':
        s = s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
        s = '<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + s
        i = s.find('</style>')
        s = s[:i + 8] + '\n</head>\n<body>' + s[i + 8:]
        s = s.rstrip() + '\n</body>\n</html>\n'
    # shared header (mega menu), menu script and CSS
    s, n1 = re.subn(r'<header class="nav">.*?</header>', lambda m: header('', home=True).rstrip(), s, count=1, flags=re.S)
    s, n2 = re.subn(r"<script>\n\(function\(\)\{var b=document\.querySelector\('\.nav__menu'\).*?</script>", lambda m: MENU_JS, s, count=1, flags=re.S)
    mega_css = open(os.path.join(SRC, 'mega.css')).read().replace('url(hero-800.webp)', 'url(assets/hero-800.webp)')
    k = s.index('/* ---------- Mobile < 810 ---------- */')
    s = s[:k] + mega_css + s[k:]
    assert n1 == 1 and n2 == 1, (n1, n2)
    # regenerate the 3 latest articles block
    i = s.find('<div class="posts reveal"')
    j = s.find('</article></div>', i) + len('</article></div>')
    block = s[i:j]
    arts = re.findall(r'<div class="post__img[^"]*">.*?</svg></div>', block, flags=re.S)
    open_tag = re.match(r'<div class="posts reveal"[^>]*>', block).group(0)
    cards = ''.join(f'<article class="post"><a href="blog/{a["slug"]}.html">{arts[k % len(arts)]}<h3>{esc(a["short"])}</h3><p class="post__meta"><b>{a["cat"]}</b><span>{fr_date(a["date"])}</span></p></a></article>' for k, a in enumerate(ARTICLES[:3]))
    s = s[:i] + open_tag + cards + '</div>' + s[j:]
    return s

NETLIFY = """[build]
  publish = "public"

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    X-Frame-Options = "SAMEORIGIN"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/assets/site.css"
  [headers.values]
    Cache-Control = "public, max-age=3600"


[[redirects]]
  from = "https://automatisation-ia-pme.cloud/*"
  to = "https://www.automatisation-ia-pme.fr/:splat"
  status = 301
  force = true

[[redirects]]
  from = "https://www.automatisation-ia-pme.cloud/*"
  to = "https://www.automatisation-ia-pme.fr/:splat"
  status = 301
  force = true
"""

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, 'blog'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
    for f in os.listdir(ASSETS):
        fp = os.path.join(ASSETS, f)
        if os.path.isdir(fp):
            shutil.copytree(fp, os.path.join(OUT, 'assets', f), dirs_exist_ok=True)
        else:
            shutil.copy(fp, os.path.join(OUT, 'assets', f))
    open(os.path.join(OUT, 'assets', 'site.css'), 'w').write(open(os.path.join(SRC, 'site.css')).read() + '\n' + open(os.path.join(SRC, 'mega.css')).read())
    for a in ARTICLES:
        open(os.path.join(OUT, 'blog', a['slug'] + '.html'), 'w').write(article_page(a))
    open(os.path.join(OUT, 'blog.html'), 'w').write(blog_page())
    open(os.path.join(OUT, 'mentions-legales.html'), 'w').write(legal_page())
    open(os.path.join(OUT, FORMATION), 'w').write(formation_page())
    for t in TOOLS:
        open(os.path.join(OUT, t['slug'] + '.html'), 'w').write(tool_page(t))
    open(os.path.join(OUT, 'integrations.html'), 'w').write(integrations_page())
    open(os.path.join(OUT, 'index.html'), 'w').write(build_index())
    if FONTS == 'self':
        open(os.path.join(OUT, '404.html'), 'w').write(notfound_page())
        open(os.path.join(OUT, INDEXNOW_KEY + '.txt'), 'w').write(INDEXNOW_KEY)
        open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
        last = max(a['date'] for a in ARTICLES)
        urls = [('', '1.0', last), ('blog.html', '0.7', last), ('mentions-legales.html', '0.2', LEGAL_DATE), (FORMATION, '0.9', FORMATION_DATE)] + [(t['slug'] + '.html', '0.9', t['date']) for t in TOOLS] + [('integrations.html', '0.7', FORMATION_DATE)] + [(f'blog/{a["slug"]}.html', '0.8', a['date']) for a in ARTICLES]
        sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
            f'  <url><loc>{SITE}/{u}</loc><lastmod>{d}</lastmod><priority>{pr}</priority></url>\n' for u, pr, d in urls) + '</urlset>\n'
        open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sm)
        open(os.path.join(REPO, 'netlify.toml'), 'w').write(NETLIFY)
    else:
        os.remove(os.path.join(OUT, 'assets', 'fonts.css'))
        shutil.rmtree(os.path.join(OUT, 'assets', 'fonts'))
    # guard: no em or en dashes in visible text
    for root, _, files in os.walk(OUT):
        for f in files:
            if f.endswith('.html'):
                t = open(os.path.join(root, f)).read()
                assert '—' not in t and '–' not in t, f
    print('built', OUT, FONTS, [a['slug'] for a in ARTICLES])

main()
