#!/usr/bin/env python3
"""Optional helper: regenerates index.html (French pre-rendered) and js/i18n.js
from tools/translations.json + tools/index.template.html.
Usage (from the project folder):  python3 tools/build.py
"""
import json, html, re, urllib.parse, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://dattesmedjoolmaroc.vercel.app"  # provisional domain
WA_NUMBER = "212661111111"
FAQ_COUNT = 7

T = json.loads((ROOT / "tools/translations.json").read_text(encoding="utf-8"))
fr = T["fr"]

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
                "availableLanguage": ["French", "English", "Spanish"],
            },
        },
        {
            "@type": "WebSite",
            "@id": SITE + "/#website",
            "url": SITE + "/",
            "name": "Dattes Medjool Maroc",
            "inLanguage": ["fr", "en", "es"],
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

def faq_items():
    out = []
    for i in range(1, FAQ_COUNT + 1):
        q, a = html.escape(fr[f"faq.q{i}"], quote=False), html.escape(fr[f"faq.a{i}"], quote=False)
        out.append(
            f'          <details class="faq__item"{" open" if i == 1 else ""}>\n'
            f'            <summary><h3 data-i18n="faq.q{i}">{q}</h3></summary>\n'
            f'            <p data-i18n="faq.a{i}">{a}</p>\n'
            f'          </details>')
    return "\n".join(out)

tpl = (ROOT / "tools/index.template.html").read_text(encoding="utf-8")
tpl = tpl.replace("{{LD_ORG}}", json.dumps(ORG, ensure_ascii=False, indent=2))
tpl = tpl.replace("{{LD_FAQ}}", json.dumps(faq_ld("fr"), ensure_ascii=False, indent=2))
tpl = tpl.replace("{{FAQ_ITEMS}}", faq_items())
tpl = tpl.replace("{{WA}}", html.escape(wa("fr")))
for k, v in ICONS.items():
    tpl = tpl.replace("{{" + k + "}}", v)

def sub(m):
    key = m.group(1)
    return html.escape(fr[key])
tpl = re.sub(r"\{\{([a-zA-Z0-9_.]+)\}\}", sub, tpl)
assert "{{" not in tpl
(ROOT / "index.html").write_text(tpl, encoding="utf-8")

js = ("/* Generated by tools/build.py from tools/translations.json — edit there, or edit here directly.\n"
      "   One object per language: fr (default), en, es. */\n"
      "window.I18N = " + json.dumps(T, ensure_ascii=False, indent=1) + ";\n"
      "window.I18N_FAQ_COUNT = " + str(FAQ_COUNT) + ";\n")
(ROOT / "js/i18n.js").write_text(js, encoding="utf-8")
print("index.html + js/i18n.js generated")
