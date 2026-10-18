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

def header(p):
    h = p or './'
    links = [('Solutions', h + '#solutions'), ('Méthode', h + '#methode'), ('Intégrations', h + '#integrations'),
             ("Cas d'usage", h + '#cas'), ('Blog', p + 'blog.html')]
    li = ''.join(f'<li><a href="{u}">{t}</a></li>' for t, u in links)
    return f'''<header class="nav">
  <div class="nav__inner">
    <a class="logo" href="{h}">automatisation <span class="logo__tag">IA PME</span></a>
    <div class="nav__right">
      <ul class="nav__links">{li}</ul>
      <a class="btn btn--ghost" href="{h}#contact">Contact</a>
    </div>
    <button class="nav__menu" type="button" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="mnav"><svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><circle cx="3" cy="10" r="1.6"/><circle cx="10" cy="10" r="1.6"/><circle cx="17" cy="10" r="1.6"/></svg></button>
  </div>
  <nav class="mnav" id="mnav" aria-label="Menu mobile" hidden><ul>{li}</ul><a class="btn btn--primary" href="{CAL}" rel="noopener">Réserver un audit</a></nav>
</header>
'''

WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>'

MENU_JS = '''<script>
(function(){var b=document.querySelector('.nav__menu'),m=document.getElementById('mnav');if(!b||!m)return;
function set(o){m.hidden=!o;b.setAttribute('aria-expanded',o);b.setAttribute('aria-label',o?'Fermer le menu':'Ouvrir le menu');}
b.addEventListener('click',function(){set(m.hidden)});m.addEventListener('click',function(e){if(e.target.closest('a'))set(false)});
document.addEventListener('keydown',function(e){if(e.key==='Escape')set(false)});})();
</script>'''

def footer(p, band=True):
    h = p or './'
    b = ''
    if band:
        b = f'''<section class="band"><h2>Et si vos demandes se traitaient toutes seules ?</h2><div class="band__btns"><a class="btn btn--ghost" href="{WA}" rel="noopener">Écrire sur WhatsApp</a><a class="btn btn--primary" href="{CAL}" rel="noopener">Réserver un audit offert</a></div></section>
'''
    return f'''{b}<footer>
  <div class="foot">
    <div class="foot__brand"><p>L'intelligence artificielle qui traite vos demandes de A à Z</p></div>
    <nav class="foot__cols" aria-label="Pied de page">
      <div><h2 class="foot__h">Offre</h2><ul><li><a href="{h}#solutions">Solutions</a></li><li><a href="{h}#methode">Méthode</a></li><li><a href="{h}#cas">Cas d'usage</a></li><li><a href="{p}blog.html">Blog</a></li></ul></div>
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
    shutil.copy(os.path.join(SRC, 'site.css'), os.path.join(OUT, 'assets', 'site.css'))
    for a in ARTICLES:
        open(os.path.join(OUT, 'blog', a['slug'] + '.html'), 'w').write(article_page(a))
    open(os.path.join(OUT, 'blog.html'), 'w').write(blog_page())
    open(os.path.join(OUT, 'mentions-legales.html'), 'w').write(legal_page())
    open(os.path.join(OUT, 'index.html'), 'w').write(build_index())
    if FONTS == 'self':
        open(os.path.join(OUT, '404.html'), 'w').write(notfound_page())
        open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
        last = max(a['date'] for a in ARTICLES)
        urls = [('', '1.0', last), ('blog.html', '0.7', last), ('mentions-legales.html', '0.2', LEGAL_DATE)] + [(f'blog/{a["slug"]}.html', '0.8', a['date']) for a in ARTICLES]
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
