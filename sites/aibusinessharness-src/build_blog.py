#!/usr/bin/env python3
"""Build the AI Business Harness blog into sites/aibusinessharness/blog/.

Usage: python3 build_blog.py
Reads blog/*.md (front matter + Markdown), renders each post to
/blog/<slug>/index.html, the index to /blog/index.html, writes original SVG
hero images plus 1200x630 PNG share images, and refreshes sitemap.xml.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import math
import pathlib
import re

import markdown

from images import INLINE, svg_for

ROOT = pathlib.Path(__file__).resolve().parent
SITE = ROOT.parent / "aibusinessharness"
OUT = SITE / "blog"
IMG = OUT / "images"
BASE = "https://aibusinessharness.com"
ASSET_V = "20261030i"
PUBLISHED = "2026-10-29"
AUTHOR = "Jeremy Mandile"

NAV = [("/#solutions", "Solutions"), ("/#approach", "How it works"), ("/blog/", "Blog"), ("/#pricing", "Pricing")]


def parse(path: pathlib.Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    meta = {}
    for ln in m.group(1).splitlines():
        k, _, v = ln.partition(":")
        meta[k.strip()] = v.strip()
    body = m.group(2).strip()
    words = len(re.findall(r"\w+", body))
    meta.update(body=body, minutes=max(3, math.ceil(words / 230)), order=int(path.name[:2]))
    meta["url"] = f"/blog/{meta['slug']}/"
    meta.setdefault("date", PUBLISHED)
    meta["faq"] = faq_items(body)
    return meta


def faq_items(body: str) -> list[tuple[str, str]]:
    """Question/answer pairs under a '## Frequently asked questions' heading."""
    m = re.search(r"^## Frequently asked questions\n(.*?)(?=^## |^Sources:|\Z)", body, re.S | re.M)
    if not m:
        return []
    pairs = re.findall(r"^### (.+?)\n+(.+?)(?=\n### |\Z)", m.group(1).strip() + "\n", re.S | re.M)
    return [(q.strip(), re.sub(r"\s+", " ", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", a)).strip()) for q, a in pairs]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def render_body(md: str) -> str:
    out = markdown.markdown(md, extensions=["tables", "sane_lists"], output_format="html5")
    # External links open in a new tab; internal links stay put.
    out = re.sub(r'<a href="(https?://(?!aibusinessharness\.com)[^"]+)">',
                 r'<a href="\1" target="_blank" rel="noopener">', out)
    out = re.sub(r'<p><img alt="([^"]*)" src="([^"]+)" ?/?></p>',
                 r'<figure class="post-figure"><img src="\2" alt="\1" width="1200" height="630" loading="lazy" decoding="async" /></figure>', out)
    out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    return out


def header() -> str:
    links = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    return f'''<header class="site-header" id="top">
    <a class="brand" href="/" aria-label="AI Business Harness homepage"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span class="brand-text">AI BUSINESS <strong>HARNESS</strong></span></a>
    <nav class="desktop-nav" aria-label="Main navigation">{links}</nav>
    <a class="nav-cta" href="/#contact">Let's talk <span aria-hidden="true">↗</span></a>
    <button class="menu-toggle" type="button" aria-label="Open navigation menu" aria-expanded="false" aria-controls="mobile-nav"><span></span><span></span></button>
    <nav class="mobile-nav" id="mobile-nav" aria-label="Mobile navigation" hidden>{links}<a href="/#contact">Start a conversation</a></nav>
  </header>'''


FOOTER = '''<footer class="site-footer"><div class="container footer-top"><a class="brand brand-dark" href="/" aria-label="AI Business Harness homepage"><span class="brand-mark"><i></i><i></i><i></i></span><span class="brand-text">AI BUSINESS <strong>HARNESS</strong></span></a><p>Make room for better work.</p><a href="mailto:jeremy@aibusinessharness.com">Get in touch ↗</a></div><div class="container footer-bottom"><span>© <span id="year">2026</span> AI Business Harness · A Mandile SEO service</span><div><a href="/ai-business-harness/">AI Harness Guide</a><a href="/blog/">Blog</a><a href="/privacy.html">Privacy</a><a href="https://mandileseo.com" target="_blank" rel="noopener noreferrer">Mandile SEO ↗</a></div></div></footer>'''


def head(title, desc, canonical, image, og_type, jsonld) -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#080a0e" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <link rel="canonical" href="{canonical}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta property="og:site_name" content="AI Business Harness" />
  <meta property="og:type" content="{og_type}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{image}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <meta name="twitter:image" content="{image}" />
  <link rel="icon" href="/assets/mark.svg" type="image/svg+xml" />
  <link rel="alternate" type="application/rss+xml" title="AI Business Harness Insights" href="/blog/feed.xml" />
  <link rel="stylesheet" href="/styles.css?v={ASSET_V}" />
  <script defer src="/main.js?v={ASSET_V}"></script>
  <script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>'''


def card(p: dict, heading="h3") -> str:
    return (f'<article class="post-card"><a href="{p["url"]}" class="post-card-link">'
            f'<img src="/blog/images/{p["slug"]}.svg" alt="" width="1200" height="630" loading="lazy" decoding="async" />'
            f'<div class="post-card-body"><span class="post-card-cat">{esc(p["category"])} · {p["minutes"]} min read</span>'
            f'<{heading}>{esc(p["title"])}</{heading}><p>{esc(p["excerpt"])}</p><span class="post-card-more">Read article <span aria-hidden="true">→</span></span></div></a></article>')


def nice_date(d: str) -> str:
    return dt.date.fromisoformat(d).strftime("%B %-d, %Y")


def post_page(p: dict, all_posts: list[dict]) -> str:
    canonical = BASE + p["url"]
    image = f"{BASE}/blog/images/{p['slug']}.jpg"
    related = sorted((q for q in all_posts if q["slug"] != p["slug"]),
                     key=lambda q: (q["category"] != p["category"], abs(q["order"] - p["order"])))[:3]
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "BlogPosting", "headline": p["title"], "description": p["description"],
             "image": [image], "datePublished": p["date"], "dateModified": p["date"],
             "author": {"@type": "Person", "name": AUTHOR, "url": BASE + "/"},
             "publisher": {"@type": "Organization", "name": "AI Business Harness", "url": BASE + "/",
                           "parentOrganization": {"@type": "Organization", "name": "Mandile SEO", "url": "https://mandileseo.com"}},
             "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
             "keywords": p["keyword"], "articleSection": p["category"], "inLanguage": "en-US"},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE + "/blog/"},
                {"@type": "ListItem", "position": 3, "name": p["title"], "item": canonical}]},
        ],
    }
    if p["faq"]:
        jsonld["@graph"].append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]})
    rel = "".join(card(q) for q in related)
    return f'''{head(p["meta_title"] + " | AI Business Harness", p["description"], canonical, image, "article", jsonld)}
<body class="blog-page">
  <a class="skip-link" href="#main">Skip to content</a>
  {header()}
  <main id="main">
    <article class="post">
      <header class="post-head container">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/blog/">Blog</a><span aria-hidden="true">/</span><span aria-current="page">{esc(p["category"])}</span></nav>
        <p class="eyebrow">{esc(p["category"])}</p>
        <h1>{esc(p["title"])}</h1>
        <p class="post-dek">{esc(p["excerpt"])}</p>
        <p class="post-meta">By {AUTHOR} · <time datetime="{p["date"]}">{nice_date(p["date"])}</time> · {p["minutes"]} min read</p>
      </header>
      <figure class="post-hero container"><img src="/blog/images/{p["slug"]}.svg" alt="{esc(p["image_alt"])}" width="1200" height="630" fetchpriority="high" /></figure>
      <div class="post-body container">
{render_body(p["body"])}
      </div>
      <aside class="post-cta container" aria-label="Start a pilot">
        <div><p class="eyebrow eyebrow-light">ONE WORKFLOW · THIRTY DAYS</p><h2>Have a task that keeps repeating?</h2><p>Tell us about it. We'll help you decide whether a controlled AI workflow is worth it, before anything touches your live systems.</p></div>
        <a class="button button-light" href="/#contact">Find your first workflow <span aria-hidden="true">↗</span></a>
      </aside>
    </article>
    <section class="related container" aria-labelledby="related-title"><h2 id="related-title">Keep reading</h2><div class="post-grid">{rel}</div></section>
  </main>
  {FOOTER}
</body>
</html>
'''


def index_page(posts: list[dict]) -> str:
    canonical = BASE + "/blog/"
    image = f"{BASE}/blog/images/{posts[0]['slug']}.jpg"
    desc = "Practical, plain-English guides to using AI in a small business: choosing workflows, human approval, integrations, audit trails and 30-day pilots."
    jsonld = {"@context": "https://schema.org", "@type": "Blog", "name": "AI Business Harness Insights", "url": canonical,
              "description": desc, "publisher": {"@type": "Organization", "name": "AI Business Harness", "url": BASE + "/"},
              "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": BASE + p["url"], "datePublished": p["date"]} for p in posts]}
    feature, rest = posts[0], posts[1:]
    grid = "".join(card(p, "h2") for p in rest)
    return f'''{head("AI for Small Business: Practical Guides | AI Business Harness", desc, canonical, image, "website", jsonld)}
<body class="blog-page">
  <a class="skip-link" href="#main">Skip to content</a>
  {header()}
  <main id="main">
    <section class="blog-hero container">
      <p class="eyebrow">INSIGHTS</p>
      <h1>Practical AI for<br /><span>real business work.</span></h1>
      <p>Plain-English guides for owners and operators: what to automate first, where people stay in control, and how to tell whether it's working.</p>
    </section>
    <section class="container" aria-label="Complete guide"><div class="hub-callout"><p>New: the complete guide to AI business harnesses — components, use cases and a 30-day pilot.</p><a class="text-link" href="/ai-business-harness/">Read the guide <span aria-hidden="true">→</span></a></div></section>
    <section class="container featured" aria-label="Featured article">{card(feature, "h2").replace('class="post-card"', 'class="post-card post-card-featured"', 1)}</section>
    <section class="container" aria-label="All articles"><div class="post-grid">{grid}</div></section>
  </main>
  {FOOTER}
</body>
</html>
'''


def feed(posts: list[dict]) -> str:
    def pub(d: str) -> str:
        return dt.datetime.fromisoformat(d + "T09:00:00-07:00").strftime("%a, %d %b %Y %H:%M:%S %z")
    items = "".join(
        f"<item><title>{esc(p['title'])}</title><link>{BASE}{p['url']}</link><guid>{BASE}{p['url']}</guid>"
        f"<pubDate>{pub(p['date'])}</pubDate><description>{esc(p['description'])}</description></item>" for p in posts)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>AI Business Harness Insights</title>'
            f"<link>{BASE}/blog/</link><description>Practical AI guides for small businesses.</description>{items}</channel></rss>\n")


def sitemap(posts: list[dict]) -> str:
    latest = max(p["date"] for p in posts)
    urls = ([("/", "1.0", latest), ("/ai-business-harness/", "0.9", PUBLISHED), ("/blog/", "0.8", latest)]
            + [(p["url"], "0.7", p["date"]) for p in posts] + [("/privacy.html", "0.3", PUBLISHED)])
    body = "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority></url>" for u, pr, lm in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>\n'


def render_pngs(slugs: list[str]) -> None:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        for s in slugs:
            pg.set_content(f'<html><body style="margin:0">{svg_for(s)}</body></html>')
            pg.screenshot(path=str(IMG / f"{s}.jpg"), type="jpeg", quality=86)
        b.close()


def main() -> None:
    posts = sorted((parse(f) for f in (ROOT / "blog").glob("*.md")), key=lambda p: p["order"])
    IMG.mkdir(parents=True, exist_ok=True)
    for p in posts:
        (IMG / f"{p['slug']}.svg").write_text(svg_for(p["slug"]), encoding="utf-8")
        d = OUT / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(post_page(p, posts), encoding="utf-8")
    for name in INLINE:
        (IMG / f"{name}.svg").write_text(svg_for(name), encoding="utf-8")
    render_pngs([p["slug"] for p in posts])
    newest = sorted(posts, key=lambda p: (p["date"], p["order"]), reverse=True)
    newest = [newest[0]] + sorted(newest[1:], key=lambda p: p["order"])
    (OUT / "index.html").write_text(index_page(newest), encoding="utf-8")
    (OUT / "feed.xml").write_text(feed(newest), encoding="utf-8")
    (SITE / "sitemap.xml").write_text(sitemap(posts), encoding="utf-8")
    home = SITE / "index.html"
    picks = [p for p in posts if p["order"] in (12, 11, 1)]
    picks.sort(key=lambda p: -p["order"])
    teaser = ('<!-- blog-teaser:start --><section class="blog-teaser section-pad" aria-labelledby="teaser-title"><div class="container">'
              '<div class="section-heading"><div><p class="eyebrow">INSIGHTS</p><h2 id="teaser-title">Practical AI,<br />explained plainly.</h2></div>'
              '<p>Guides for owners and operators on choosing workflows, keeping people in control, and measuring what works.</p></div>'
              f'<div class="post-grid">{"".join(card(p) for p in picks)}</div>'
              '<div class="blog-teaser-foot"><a class="text-link" href="/ai-business-harness/">Read the complete AI business harness guide <span aria-hidden="true">→</span></a> <a class="text-link" href="/blog/">See all articles <span aria-hidden="true">→</span></a></div>'
              '</div></section><!-- blog-teaser:end -->')
    h = home.read_text(encoding="utf-8")
    h = re.sub(r"<!-- blog-teaser:start -->.*?<!-- blog-teaser:end -->", lambda _: teaser, h, flags=re.S)
    home.write_text(h, encoding="utf-8")
    print(f"built {len(posts)} posts")


if __name__ == "__main__":
    main()
