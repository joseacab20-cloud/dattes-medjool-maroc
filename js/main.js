/* Dattes Medjool Maroc — language switcher + small UI helpers. No framework, no tracking. */
(function () {
  'use strict';
  var T = window.I18N || {};
  var LANGS = ['fr', 'en', 'es'];
  var DEFAULT = 'fr';
  var SITE = 'https://medjooldateswholesale.vercel.app/'; // provisional domain
  var WA_BASE = 'https://wa.me/212661111111';
  var STORE_KEY = 'dmm_lang';

  function pickLang() {
    var p = new URLSearchParams(location.search).get('lang');
    if (p && LANGS.indexOf(p) > -1) return p;
    try { var s = localStorage.getItem(STORE_KEY); if (s && LANGS.indexOf(s) > -1) return s; } catch (e) {}
    return DEFAULT;
  }

  function faqSchema(lang) {
    var d = T[lang], items = [];
    for (var i = 1; i <= (window.I18N_FAQ_COUNT || 0); i++) {
      items.push({ '@type': 'Question', name: d['faq.q' + i],
        acceptedAnswer: { '@type': 'Answer', text: d['faq.a' + i] } });
    }
    return { '@context': 'https://schema.org', '@type': 'FAQPage', inLanguage: lang, mainEntity: items };
  }

  function apply(lang, updateUrl) {
    var d = T[lang]; if (!d) return;
    document.documentElement.lang = lang;

    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var v = d[el.getAttribute('data-i18n')]; if (v != null) el.textContent = v;
    });
    document.querySelectorAll('[data-i18n-attr]').forEach(function (el) {
      el.getAttribute('data-i18n-attr').split(';').forEach(function (pair) {
        var parts = pair.split(':'); var v = d[parts[1]];
        if (parts[0] && v != null) el.setAttribute(parts[0].trim(), v);
      });
    });

    // WhatsApp links: always https://wa.me/212661111111 + prefilled message in the current language
    var href = WA_BASE + '?text=' + encodeURIComponent(d['wa.text']);
    document.querySelectorAll('a[data-cta="whatsapp"]').forEach(function (a) { a.href = href; });

    // FAQ structured data
    var ld = document.getElementById('ld-faq');
    if (ld) ld.textContent = JSON.stringify(faqSchema(lang));

    // canonical + og:url follow the language version
    var url = lang === DEFAULT ? SITE : SITE + '?lang=' + lang;
    var c = document.getElementById('canonical'); if (c) c.href = url;
    var og = document.getElementById('og-url'); if (og) og.content = url;

    document.querySelectorAll('.lang button').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-lang') === lang ? 'true' : 'false');
    });

    try { localStorage.setItem(STORE_KEY, lang); } catch (e) {}
    if (updateUrl && history.replaceState) {
      var u = new URL(location.href);
      if (lang === DEFAULT) u.searchParams.delete('lang'); else u.searchParams.set('lang', lang);
      history.replaceState(null, '', u.pathname + u.search + u.hash);
    }
  }

  var initial = pickLang();
  if (initial !== DEFAULT) apply(initial, false); else apply(DEFAULT, false);

  document.querySelectorAll('.lang button').forEach(function (b) {
    b.addEventListener('click', function () { apply(b.getAttribute('data-lang'), true); });
  });

  // Mobile menu
  var burger = document.querySelector('.burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', open ? 'false' : 'true');
      document.body.classList.toggle('nav-open', !open);
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        burger.setAttribute('aria-expanded', 'false');
        document.body.classList.remove('nav-open');
      });
    });
  }

  // Header shadow on scroll
  var header = document.querySelector('.header');
  var onScroll = function () { header && header.classList.toggle('is-scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
})();
