# Dattes Medjool Maroc — site one-page FR / EN / ES

Site vitrine d'une seule page, optimisé SEO pour **« dattes medjool maroc »** (FR, langue par défaut),
**« moroccan medjool dates »** (EN) et **« dátiles medjool marruecos »** (ES).
Objectif : faire contacter le vendeur sur **WhatsApp** (`https://wa.me/212661111111`).

- 100 % statique : HTML + CSS + JavaScript, **aucun framework, aucune installation**.
- Trois langues avec un sélecteur **EN / FR / ES** dans l'en-tête (choix mémorisé, et `?lang=en` / `?lang=es` dans l'adresse).
- Le français est écrit directement dans le HTML : Google peut le lire sans JavaScript.
- Bouton WhatsApp flottant + boutons WhatsApp dans chaque section.
- Données structurées : `Organization`, `WebSite`, `FAQPage` (la FAQ change de langue avec le site).
- `robots.txt`, `sitemap.xml` (avec `hreflang`), favicon, image de partage (Open Graph).
- **Aucun outil de suivi installé** (pas de GA4, pas de GTM, pas de pixel). Emplacements prévus pour GTM.

---

## 1. Voir le site sur votre ordinateur (aperçu local)

### Méthode la plus simple (aucun logiciel)
1. Sur la page GitHub du projet, cliquez sur le bouton vert **Code** → **Download ZIP**.
2. Décompressez le fichier ZIP (clic droit → *Extraire tout*).
3. Ouvrez le dossier, puis **double-cliquez sur `index.html`**. Le site s'ouvre dans votre navigateur.
4. Testez le sélecteur **EN / FR / ES** en haut à droite et les boutons WhatsApp.

### Méthode « comme en ligne » (optionnelle, si Node.js est installé)
```bash
cd dattes-medjool-maroc
npx serve .
```
Puis ouvrez l'adresse affichée (en général http://localhost:3000).
Pour tester une langue directement : http://localhost:3000/?lang=en ou http://localhost:3000/?lang=es

---

## 2. Structure du projet

```
index.html               ← la page (contenu français pré-rempli)
css/style.css            ← le design (couleurs or / caramel / ambre)
js/i18n.js               ← TOUS les textes, en FR / EN / ES
js/main.js               ← sélecteur de langue, menu mobile, liens WhatsApp
images/                  ← photos optimisées (WebP) + image de partage og-image.jpg
favicon.svg              ← icône du site
robots.txt, sitemap.xml  ← pour Google
tools/                   ← (optionnel) source des traductions + script de génération
```

Sections de la page : en-tête fixe avec ancres · hero · bandeau de confiance · origine (Errachidia / Tafilalet,
récolte, sélection, conditionnement) · produits & conditionnement · pourquoi nous choisir ·
qualité & certifications · ce que nos clients recherchent · FAQ · appel à l'action final · pied de page.

---

## 3. Comment fonctionnent les traductions

Chaque texte du HTML porte une clé, par exemple :
```html
<h1 data-i18n="hero.title">Dattes Medjool du Maroc, …</h1>
<img alt="…" data-i18n-attr="alt:img.hero.alt">
```
Le fichier `js/i18n.js` contient la même clé dans les trois langues (`fr`, `en`, `es`).
Quand on clique sur EN / FR / ES, `js/main.js` :
- remplace tous les textes, les `alt` des images et les `aria-label` ;
- met à jour `<html lang>`, le `<title>`, la meta description, les balises Open Graph / Twitter et la `canonical` ;
- régénère le JSON-LD `FAQPage` dans la bonne langue ;
- met à jour tous les liens WhatsApp (message pré-rempli dans la langue choisie) ;
- mémorise le choix (localStorage) et met l'adresse à jour (`?lang=en`, `?lang=es`, rien pour le français).

**Modifier un texte :** le plus simple est d'éditer `tools/translations.json` puis de lancer
`python3 tools/build.py` (régénère `index.html` et `js/i18n.js`).
Sans Python : modifiez le texte dans `js/i18n.js` (les 3 langues) **et** le texte français dans `index.html`.

---

## 4. WhatsApp

Tous les liens utilisent exactement `https://wa.me/212661111111` (+212 661 111 111), avec un message
pré-rempli (`?text=…`) dans la langue courante. Chaque lien porte :
```html
data-cta="whatsapp" data-cta-location="hero | hero-quote | header | product-premium | product-wholesale |
                                       product-boxes | why | quality | final | final-quote | footer | floating"
```
Pour changer le numéro : remplacez `212661111111` dans `js/main.js`, `tools/build.py` et `index.html`.

## 5. Ajouter Google Tag Manager plus tard

Deux emplacements commentés sont prévus dans `index.html` :
1. tout en haut de `<head>` → bloc « GOOGLE TAG MANAGER (HEAD) » : collez le 1er extrait `<script>` GTM ;
2. juste après `<body>` → bloc « GOOGLE TAG MANAGER (BODY / noscript) » : collez l'extrait `<noscript>`.

Dans GTM, un déclencheur « Clic – Liens uniquement » avec la condition *Click Element correspond au
sélecteur CSS* `a[data-cta="whatsapp"]` suffit pour suivre les clics WhatsApp
(la variable `data-cta-location` indique quel bouton a été cliqué).
Pensez à ajouter une bannière de consentement cookies avant d'activer un suivi.

---

## 6. À savoir / à compléter

- **Domaine provisoire** : `https://dattesmedjoolmaroc.vercel.app` (canonical, hreflang, sitemap, robots, Open Graph,
  JSON-LD). À remplacer partout si l'adresse finale est différente.
- **Pas de témoignages inventés** : la section « Ce que nos clients recherchent » décrit des attentes générales.
  Un modèle de témoignage est prêt en commentaire dans `index.html` (TODO) — à n'utiliser qu'avec de vrais avis.
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

Le site **n'est pas encore publié**. La mise en ligne sur Vercel se fera uniquement après validation de l'aperçu.
(Le projet est statique : aucun réglage de build n'est nécessaire.)
