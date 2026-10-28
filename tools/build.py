#!/usr/bin/env python3
"""Generates the 3 static, fully pre-rendered pages from tools/translations.json
+ tools/index.template.html:
    index.html     -> English (default)  https://medjooldateswholesale.vercel.app/
    fr/index.html  -> French             https://medjooldateswholesale.vercel.app/fr/
    es/index.html  -> Spanish            https://medjooldateswholesale.vercel.app/es/
and sitemap.xml. No JavaScript translation at runtime.
Usage (from the project folder):  python3 tools/build.py
"""
import json, html, re, urllib.parse, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://medjooldateswholesale.vercel.app"  # production domain (no trailing slash)
LANGS = ["en", "fr", "es"]          # first = default language, served at /
PATHS = {"en": "/", "fr": "/fr/", "es": "/es/"}
LASTMOD = "2026-10-28"
WA_NUMBER = "212661111111"
FAQ_COUNT = 7

T = json.loads((ROOT / "tools/translations.json").read_text(encoding="utf-8"))

def wa(lang):
    return f"https://wa.me/{WA_NUMBER}?text=" + urllib.parse.quote(T[lang]["wa.text"])

def faq_ld(lang):
    d = T[lang]
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": lang,
        "mainEntity": [
            {"@type": "Question", "name": d[f"faq.q{i}"],
             "acceptedAnswer": {"@type": "Answer", "text": d[f"faq.a{i}"]}}
            for i in range(1, FAQ_COUNT + 1)
        ],
    }

ORG = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Organization",
            "@id": SITE + "/#organization",
            "name": "Dattes Medjool Maroc",
            "url": SITE + "/",
            "logo": SITE + "/images/apple-touch-icon.png",
            "image": SITE + "/images/og-image.jpg",
            "telephone": "+212661111111",
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+212661111111",
                "contactType": "sales",
                "url": "https://wa.me/" + WA_NUMBER,
                "availableLanguage": ["English", "French", "Spanish"],
            },
        },
        {
            "@type": "WebSite",
            "@id": SITE + "/#website",
            "url": SITE + "/",
            "name": "Dattes Medjool Maroc",
            "inLanguage": ["en", "fr", "es"],
            "publisher": {"@id": SITE + "/#organization"},
        },
    ],
}

ICONS = {
    "ICON_WA": '<svg class="i-wa" viewBox="0 0 32 32" width="20" height="20" aria-hidden="true" focusable="false"><path fill="currentColor" d="M16.04 3C9.4 3 4 8.33 4 14.9c0 2.1.56 4.15 1.62 5.95L4 29l8.4-1.6a12.2 12.2 0 0 0 3.64.55C22.66 27.95 28 22.62 28 16.05 28 9.48 22.66 3 16.04 3zm0 22.8c-1.13 0-2.24-.18-3.3-.53l-.6-.2-4.98.95.97-4.83-.22-.6a9.6 9.6 0 0 1-1.44-5.1c0-5.3 4.3-9.6 9.57-9.6s9.57 4.3 9.57 9.6-4.3 10.31-9.57 10.31zm5.27-7.07c-.29-.14-1.7-.83-1.96-.92-.27-.1-.46-.14-.65.14-.2.29-.75.92-.92 1.1-.17.2-.34.22-.63.08-.29-.15-1.22-.45-2.32-1.43-.86-.76-1.44-1.7-1.6-1.99-.17-.29-.02-.44.12-.58.13-.13.29-.34.43-.5.15-.18.2-.3.29-.49.1-.19.05-.36-.02-.5-.07-.15-.65-1.56-.89-2.13-.23-.56-.47-.48-.65-.49h-.55c-.19 0-.5.07-.77.36-.26.29-1 .98-1 2.4 0 1.4 1.03 2.77 1.17 2.96.15.19 2.03 3.1 4.92 4.34.69.3 1.22.47 1.64.6.69.22 1.32.19 1.81.12.55-.08 1.7-.69 1.94-1.36.24-.67.24-1.25.17-1.37-.07-.12-.26-.19-.55-.33z"/></svg>',
    "ICON_PALM": '<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" d="M12 22c0-5 .5-9 1-12M13 10c-2-3-6-4-9-2M13 10c1-3 5-5 8-3M13 10c-3-1-6 1-7 4M13 10c3-1 6 1 6 5M13 10c0-3-1-5-3-7"/></svg>',
    "ICON_STAR": '<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" d="M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4 6.7 19.4l1.2-6L3.4 9.3l6-.7z"/></svg>',
    "ICON_SCALE": '<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" d="M12 4v16M7 20h10M5 7h14M5 7l-3 6a3 3 0 0 0 6 0zM19 7l-3 6a3 3 0 0 0 6 0z"/></svg>',
    "ICON_CHAT": '<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" d="M4 5h16v11H9l-5 4z"/></svg>',
}

def url(lang):
    return SITE + PATHS[lang]

def faq_items(d):
    out = []
    for i in range(1, FAQ_COUNT + 1):
        q, a = html.escape(d[f"faq.q{i}"], quote=False), html.escape(d[f"faq.a{i}"], quote=False)
        out.append(
            f'          <details class="faq__item"{" open" if i == 1 else ""}>\n'
            f'            <summary><h3>{q}</h3></summary>\n'
            f'            <p>{a}</p>\n'
            f'          </details>')
    return "\n".join(out)

HREFLANG = "\n".join(
    [f'  <link rel="alternate" hreflang="{l}" href="{url(l)}">' for l in LANGS]
    + [f'  <link rel="alternate" hreflang="x-default" href="{url(LANGS[0])}">'])

def lang_links(cur):
    out = []
    for l in LANGS:
        attrs = ' aria-current="page"' if l == cur else ''
        out.append(f'          <a href="{PATHS[l]}" hreflang="{l}" lang="{l}"{attrs}>{l.upper()}</a>')
    return "\n".join(out)

TPL = (ROOT / "tools/index.template.html").read_text(encoding="utf-8")

def render(lang):
    d = T[lang]
    s = TPL
    s = s.replace("{{LD_ORG}}", json.dumps(ORG, ensure_ascii=False, indent=2))
    s = s.replace("{{LD_FAQ}}", json.dumps(faq_ld(lang), ensure_ascii=False, indent=2))
    s = s.replace("{{FAQ_ITEMS}}", faq_items(d))
    s = s.replace("{{WA}}", html.escape(wa(lang)))
    s = s.replace("{{LANG}}", lang)
    s = s.replace("{{CANONICAL}}", url(lang))
    s = s.replace("{{HREFLANG}}", HREFLANG)
    s = s.replace("{{LANG_LINKS}}", lang_links(lang))
    s = s.replace("{{OG_ALT}}", "\n".join(
        f'  <meta property="og:locale:alternate" content="{T[l]["meta.ogLocale"]}">' for l in LANGS if l != lang))
    for k, v in ICONS.items():
        s = s.replace("{{" + k + "}}", v)
    s = re.sub(r"\{\{([a-zA-Z0-9_.]+)\}\}", lambda m: html.escape(d[m.group(1)]), s)
    assert "{{" not in s, lang
    return s

for lang in LANGS:
    out = ROOT / PATHS[lang].strip("/") / "index.html" if PATHS[lang] != "/" else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(lang), encoding="utf-8")
    print("generated", out.relative_to(ROOT))

alts = "\n".join(
    [f'    <xhtml:link rel="alternate" hreflang="{l}" href="{url(l)}"/>' for l in LANGS]
    + [f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url(LANGS[0])}"/>'])
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<!-- Generated by tools/build.py -->',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for l in LANGS:
    sm += ["  <url>", f"    <loc>{url(l)}</loc>", f"    <lastmod>{LASTMOD}</lastmod>", alts, "  </url>"]
sm.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
print("generated sitemap.xml")
