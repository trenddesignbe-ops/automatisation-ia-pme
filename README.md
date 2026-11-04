# automatisation-ia-pme.fr

Site statique de l'offre Automatisation IA PME d'Alexandre Cottret. Domaine principal : https://www.automatisation-ia-pme.fr

## Structure
- `src/` : sources (à modifier)
  - `index.html` : page d'accueil (le bloc des 3 derniers articles est régénéré automatiquement)
  - `articles/<slug>.html` : corps de chaque article (h2 avec un id, sans titre h1)
  - `articles.json` : métadonnées des articles (title_tag, meta, h1, short, cat, eyebrow, lead, summary, faq, sources, related, date)
  - `site.css`, `consent.html` (bandeau cookies et GA4), `assets/` (images, polices)
  - `build.py` : génère `public/`, `netlify.toml`, le sitemap et le fichier robots
  - `og.py` : génère les images de partage manquantes (`assets/og-<slug>.jpg`)
  - `editorial.md` : plan éditorial et statut des articles
- `public/` : site généré, publié par Netlify (ne pas modifier à la main)

## Ajouter un article
1. Écrire `src/articles/<slug>.html` et ajouter son entrée dans `src/articles.json`
2. `python3 src/og.py` puis `python3 src/build.py`
3. Vérifier : aucun tiret cadratin ou demi-cadratin, pas de « min de lecture », liens internes valides

## Adresses des pages
Une seule adresse par page : la version sans .html (https://www.automatisation-ia-pme.fr/tarifs). Les fichiers restent en `.html` dans `public/`, mais `build.py` écrit sans .html la canonique, og:url, le JSON-LD, le sitemap et tous les liens internes (`clean_urls`). Dans `src/`, on peut continuer à écrire les liens avec .html : ils sont nettoyés au build. Les redirections 301 de `/page.html` vers `/page` sont générées dans `netlify.toml` (une règle par fichier). Les mentions légales sont en noindex et hors du sitemap.

## Règles de rédaction
Vouvoiement, phrases simples, aucun chiffre inventé, sources officielles vérifiées, jamais de tiret cadratin (—) ni demi-cadratin (–).

## Hébergement
Netlify (projet automatisation-ia-pme, dossier publié : `public`). Domaines : www.automatisation-ia-pme.fr (principal), automatisation-ia-pme.fr et automatisation-ia-pme.cloud redirigent vers lui.
