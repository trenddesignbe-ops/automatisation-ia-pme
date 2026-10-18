# automatisation-ia-pme.fr

Site statique (HTML/CSS, sans build) de l'offre Automatisation IA PME d'Alexandre Cottret.

## Contenu
- `index.html` : page d'accueil (landing)
- `blog.html` et `blog/*.html` : articles
- `mentions-legales.html` : mentions légales, confidentialité, cookies
- `assets/` : styles, polices auto-hébergées, images, images de partage
- `netlify.toml` : en-têtes de cache et de sécurité, redirections www et .cloud vers le .fr
- `sitemap.xml`, `robots.txt`, `404.html`

## Hébergement
Netlify, déploiement automatique à chaque push sur `main` (dossier publié : racine).

Domaine principal : `automatisation-ia-pme.fr`. Le domaine `automatisation-ia-pme.cloud` est ajouté en alias sur Netlify et redirigé en 301 vers le .fr.
