# Dattes Medjool Maroc — site one-page EN / FR / ES

Site vitrine d'une seule page, en trois langues, chacune à sa propre adresse :

| Langue | Adresse | Mot-clé SEO principal |
|---|---|---|
| Anglais (**par défaut**) | `https://medjooldateswholesale.vercel.app/` | « medjool dates wholesale » (marché US : wholesale / bulk medjool dates, medjool dates supplier) |
| Français | `https://medjooldateswholesale.vercel.app/fr/` | « dattes medjool maroc » |
| Espagnol | `https://medjooldateswholesale.vercel.app/es/` | « dátiles medjool marruecos » |

Objectif : faire contacter le vendeur sur **WhatsApp** (`https://wa.me/212664738219`).

- 100 % statique : HTML + CSS + un petit JavaScript (menu mobile), **aucun framework, aucune installation**.
- Chaque langue est une **vraie page HTML complète** (titre, description, Open Graph, `canonical`, `hreflang`,
  FAQ JSON-LD, textes alternatifs des images, message WhatsApp pré-rempli dans la bonne langue) :
  Google lit chaque version sans JavaScript.
- Sélecteur **EN / FR / ES** dans l'en-tête = simples liens vers `/`, `/fr/`, `/es/`.
  Pas de redirection automatique selon la langue du navigateur (pour que Google puisse tout explorer).
- Anciennes adresses : `/?lang=fr` → `/fr/` et `/?lang=es` → `/es/` (redirection permanente 308, dans `vercel.json`).
  `/?lang=en` affiche simplement la page anglaise (sa `canonical` pointe vers `/`).
- Bouton WhatsApp flottant + boutons WhatsApp dans chaque section (12 liens par page).
- Données structurées : `Organization`, `WebSite`, `FAQPage` (une par langue).
- `robots.txt`, `sitemap.xml` (les 3 adresses avec leurs `hreflang`), favicon, image de partage (Open Graph).
- **Aucun outil de suivi installé** (pas de GA4, pas de GTM, pas de pixel). Emplacements prévus pour GTM.

---

## 1. Voir le site sur votre ordinateur (aperçu local)

Les pages utilisent des chemins qui commencent par `/` (ex. `/css/style.css`) pour fonctionner depuis `/fr/` et `/es/`.
Il faut donc un petit serveur local (un double-clic sur `index.html` n'affiche pas le design).

```bash
cd dattes-medjool-maroc
python3 -m http.server 8000      # ou : npx serve .
```
Puis ouvrez http://localhost:8000/ (anglais), http://localhost:8000/fr/ et http://localhost:8000/es/.

---

## 2. Structure du projet

```
index.html               ← page anglaise (générée)
fr/index.html            ← page française (générée)
es/index.html            ← page espagnole (générée)
css/style.css            ← le design (couleurs or / caramel / ambre)
js/main.js               ← menu mobile, ombre de l'en-tête (pas de traduction)
images/                  ← photos optimisées (WebP) + image de partage og-image.jpg
favicon.svg              ← icône du site
robots.txt, sitemap.xml  ← pour Google (sitemap généré)
vercel.json              ← adresses propres (/fr/, /es/) + redirections ?lang=
tools/translations.json  ← TOUS les textes, en EN / FR / ES
tools/index.template.html← le modèle HTML commun aux 3 pages
tools/build.py           ← génère les 3 pages + sitemap.xml
```

Sections de la page : en-tête fixe avec ancres · hero · bandeau de confiance · origine (Errachidia / Tafilalet,
récolte, sélection, conditionnement) · produits & conditionnement · pourquoi nous choisir ·
qualité & certifications · ce que nos clients recherchent · FAQ · appel à l'action final · pied de page.

---

## 3. Modifier un texte

1. Modifiez le texte dans `tools/translations.json` (clés `en`, `fr`, `es`).
2. Lancez `python3 tools/build.py` : il régénère `index.html`, `fr/index.html`, `es/index.html` et `sitemap.xml`.

Pour la structure de la page (sections, boutons), modifiez `tools/index.template.html` puis relancez le script.
Ne modifiez pas directement les fichiers `index.html` générés (ils seraient écrasés au prochain build).

---

## 4. WhatsApp

Tous les liens utilisent exactement `https://wa.me/212664738219` (+212 664 738 219), avec un message
pré-rempli (`?text=…`) dans la langue de la page. Chaque lien porte :
```html
data-cta="whatsapp" data-cta-location="hero | hero-quote | header | product-premium | product-wholesale |
                                       product-boxes | why | quality | final | final-quote | footer | floating"
```
Pour changer le numéro : remplacez `212664738219` dans `tools/build.py` (et le texte affiché dans `tools/translations.json` si besoin), puis relancez `python3 tools/build.py`.

## 5. Ajouter Google Tag Manager plus tard

Deux emplacements commentés sont prévus dans `tools/index.template.html` (donc dans les 3 pages) :
1. tout en haut de `<head>` → bloc « GOOGLE TAG MANAGER (HEAD) » : collez le 1er extrait `<script>` GTM ;
2. juste après `<body>` → bloc « GOOGLE TAG MANAGER (BODY / noscript) » : collez l'extrait `<noscript>`.

Dans GTM, un déclencheur « Clic – Liens uniquement » avec la condition *Click Element correspond au
sélecteur CSS* `a[data-cta="whatsapp"]` suffit pour suivre les clics WhatsApp
(la variable `data-cta-location` indique quel bouton a été cliqué).
Pensez à ajouter une bannière de consentement cookies avant d'activer un suivi.

---

## 6. À savoir / à compléter

- **Domaine** : `https://medjooldateswholesale.vercel.app` (variable `SITE` dans `tools/build.py`, plus `robots.txt`).
  Utilisé pour canonical, hreflang, sitemap, Open Graph et JSON-LD.
- **Pas de témoignages inventés** : la section « Ce que nos clients recherchent » décrit des attentes générales.
  Un modèle de témoignage est prêt en commentaire dans `tools/index.template.html` (TODO) — à n'utiliser qu'avec de vrais avis.
- **Certifications** : aucune certification n'est affichée. Le texte invite les professionnels à vérifier
  ensemble les documents nécessaires. Un commentaire TODO indique où ajouter de vraies certifications.
- **Aucun prix, volume, année ou nom d'entreprise** n'est indiqué. Nom du site neutre : « Dattes Medjool Maroc ».
- **Photos** : photos d'illustration libres de droits (voir ci-dessous). Idéalement, remplacez-les par vos propres
  photos de produits (mêmes noms de fichiers, format WebP, 800 px de large).

## 7. Crédits photos (licences gratuites)

| Fichier | Photo | Auteur | Licence |
|---|---|---|---|
| `images/dattes-medjool-maroc-*.webp`, `images/og-image.jpg` | [Delicious Medjool Dates on Rustic Background](https://www.pexels.com/photo/delicious-medjool-dates-on-rustic-background-37417610/) | Husien Bisky (Pexels) | [Pexels License](https://www.pexels.com/license/) |
| `images/palmeraie-tafilalet-*.webp` | [Desert village nestled among palm trees and greenery](https://unsplash.com/photos/desert-village-nestled-among-palm-trees-and-greenery-Zq7i1xAGtO8) | Falco Negenman (Unsplash) | [Unsplash License](https://unsplash.com/license) |
| `images/dattes-mejhoul-*.webp` | [Four dates sitting on top of a white towel](https://unsplash.com/photos/four-dates-sitting-on-top-of-a-white-towel-jbzsJUoqTpg) | beyza yurtkuran (Unsplash) | [Unsplash License](https://unsplash.com/license) |
| `images/dattes-medjool-en-gros-*.webp` | [A pile of dried dates](https://unsplash.com/photos/a-pile-of-dried-dates-1VZi7-YH_DY) | Mustafa akın (Unsplash) | [Unsplash License](https://unsplash.com/license) |

Images recadrées, redimensionnées et compressées en WebP. Le favicon et l'image de partage sont créés pour ce projet.

## 8. Mise en ligne

Hébergé sur Vercel (projet `medjooldateswholesale`), site statique : aucun réglage de build.
`vercel.json` active les adresses propres avec barre finale (`/fr/`, `/es/`) et les redirections `?lang=`.
Chaque mise en production est validée par Jose sur un aperçu (preview) avant d'être publiée.
