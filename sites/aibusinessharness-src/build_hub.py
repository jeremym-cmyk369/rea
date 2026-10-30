#!/usr/bin/env python3
"""Build the /ai-business-harness/ pillar page.

Reads hub/ai-business-harness.md and writes ../aibusinessharness/ai-business-harness/index.html,
reusing the site header and footer from an existing article so the chrome stays identical.
Also renders the social JPEG from the hero SVG (needs cairosvg + ImageMagick `convert`).
Run: python3 build_hub.py
"""
import html
import json
import pathlib
import re
import subprocess

import markdown

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent / "aibusinessharness"
BASE = "https://aibusinessharness.com"
URL = f"{BASE}/ai-business-harness/"
OUT = SITE / "ai-business-harness" / "index.html"
IMG = "/blog/images"
PUBLISHED = "2026-10-30"
MODIFIED = "2026-10-30"
ASSET_V = "20261030i"

SEO_TITLE = "AI Business Harness: Controlled AI Workflows for Business"
META_DESC = ("Learn what an AI business harness is, how it differs from an AI agent, and how controlled AI "
             "workflows connect tools, permissions, approvals, and monitoring.")
H1 = "What Is an AI Business Harness?"
SUBHEAD = "The operating system for useful business AI"
DEK = ("A complete guide to the operating layer around AI: the nine components, how it differs from an agent, "
       "illustrative use cases, and how to run a controlled 30-day pilot.")
HERO = "ai-business-harness-operating-layer"
HERO_ALT = "Diagram showing an AI model and agent connected to business tools through a controlled AI business harness"
HERO_CAP = "The model provides reasoning. The harness connects it to approved tools, permissions, review, and monitoring."

FAQ = [
    ("Is an AI business harness the same as an AI agent?",
     "No. An agent chooses steps and uses tools toward a goal. A harness coordinates that work within business "
     "permissions, approvals, operating procedures, and monitoring. Those responsibilities may be built into the same system."),
    ("Does every business need multiple AI agents?",
     "No. A defined workflow with one model call, rules, and human review may be enough. Use additional agents only "
     "when there is a clear reason to separate responsibilities, context, or permissions."),
    ("Can an AI business harness replace employees?",
     "That should not be the default assumption. A well-designed harness can prepare information, draft work, route "
     "tasks, and surface exceptions while leaving decisions and accountability with the appropriate people."),
    ("Should AI send customer messages automatically?",
     "The answer depends on the workflow's risk, permissions, testing, and approval design. A common starting point "
     "is to prepare customer-facing messages for human review rather than sending them automatically."),
    ("What happens when an AI integration fails?",
     "The workflow should verify the external state, retry safely where supported, queue the work, or escalate to a "
     "person. It should not assume an uncertain action succeeded."),
    ("How do I know whether an AI workflow is worth building?",
     "Start with one repeated task. Define the finish line, measure the baseline, limit the permissions, test with "
     "controlled work, and compare the result with the original process."),
]

RELATED = ["what-is-an-ai-business-harness", "human-approval-in-ai-workflows", "30-day-ai-workflow-pilot"]


def figure(m):
    name, alt, cap = m.group(1).split("|")
    return (f'<figure class="post-figure"><img src="{IMG}/{name}.svg" alt="{html.escape(alt)}" width="1200" '
            f'height="630" loading="lazy" decoding="async" /><figcaption>{html.escape(cap)}</figcaption></figure>')


def body_html():
    src = (HERE / "hub" / "ai-business-harness.md").read_text()
    out = markdown.markdown(src, extensions=["tables", "attr_list"])
    out = re.sub(r"<p>\[\[FIGURE:(.+?)\]\]</p>", figure, out)
    faq = "\n".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q, a in FAQ)
    out = out.replace("<p>[[FAQ]]</p>", faq)
    out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    return out


def toc(body):
    items = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    lis = "".join(f'<li><a href="#{i}">{re.sub("<.*?>", "", t)}</a></li>' for i, t in items)
    return f'<nav class="hub-toc" aria-label="On this page"><p class="eyebrow">On this page</p><ol>{lis}</ol></nav>'


def schema():
    images = [{"@type": "ImageObject", "url": f"{BASE}{IMG}/{HERO}.jpg", "width": 1200, "height": 630},
              {"@type": "ImageObject", "url": f"{BASE}{IMG}/{HERO}.svg", "width": 1200, "height": 630,
               "caption": HERO_CAP}]
    graph = [
        {"@type": "TechArticle", "@id": f"{URL}#article", "mainEntityOfPage": {"@type": "WebPage", "@id": URL},
         "headline": "What Is an AI Business Harness? The Operating System for Useful Business AI",
         "description": META_DESC, "image": images,
         "author": {"@type": "Person", "name": "Jeremy Mandile", "url": f"{BASE}/"},
         "publisher": {"@type": "Organization", "name": "AI Business Harness", "url": f"{BASE}/",
                       "logo": {"@type": "ImageObject", "url": f"{BASE}/assets/mark.svg"},
                       "parentOrganization": {"@type": "Organization", "name": "Mandile SEO",
                                              "url": "https://mandileseo.com"}},
         "datePublished": PUBLISHED, "dateModified": MODIFIED, "inLanguage": "en-US",
         "about": [{"@type": "Thing", "name": n} for n in
                   ["AI business harness", "AI workflow automation", "Enterprise AI governance"]],
         "keywords": ["AI business harness", "what is an AI business harness", "AI agent vs AI business harness",
                      "AI workflow automation", "AI automation for business", "enterprise AI governance",
                      "human approval AI workflows", "controlled AI workflows", "AI agent governance",
                      "AI automation for small business"],
         "isAccessibleForFree": True},
        {"@type": "FAQPage", "@id": f"{URL}#faq",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                        for q, a in FAQ]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "AI Business Harness Guide", "item": URL}]},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def related(_template=None):
    pages = [p.read_text() for p in sorted((SITE / "blog").glob("*/index.html"))] + [(SITE / "index.html").read_text()]
    cards = []
    for slug in RELATED:
        for t in pages:
            m = re.search(rf'<article class="post-card"><a href="/blog/{slug}/".*?</article>', t)
            if m:
                cards.append(m.group(0))
                break
    return ('<section class="related container" aria-labelledby="related-title"><h2 id="related-title">'
            f'Keep reading</h2><div class="post-grid">{"".join(cards)}</div></section>')


def main():
    tpl = (SITE / "blog" / "ai-model-vs-agent-vs-harness" / "index.html").read_text()
    header = re.search(r'<body class="blog-page">.*?</header>', tpl, re.S).group(0)
    footer = re.search(r'<footer class="site-footer">.*?</footer>', tpl, re.S).group(0)
    tpl_related = (SITE / "blog" / "what-is-an-ai-business-harness" / "index.html").read_text()
    body = body_html()
    e = html.escape
    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#080a0e" />
  <title>{e(SEO_TITLE)}</title>
  <meta name="description" content="{e(META_DESC)}" />
  <link rel="canonical" href="{URL}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="author" content="Jeremy Mandile" />
  <meta property="og:site_name" content="AI Business Harness" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{e(SEO_TITLE)}" />
  <meta property="og:description" content="{e(META_DESC)}" />
  <meta property="og:url" content="{URL}" />
  <meta property="og:image" content="{BASE}{IMG}/{HERO}.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{e(HERO_ALT)}" />
  <meta property="article:published_time" content="{PUBLISHED}" />
  <meta property="article:modified_time" content="{MODIFIED}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{e(SEO_TITLE)}" />
  <meta name="twitter:description" content="{e(META_DESC)}" />
  <meta name="twitter:image" content="{BASE}{IMG}/{HERO}.jpg" />
  <meta name="twitter:image:alt" content="{e(HERO_ALT)}" />
  <link rel="icon" href="/assets/mark.svg" type="image/svg+xml" />
  <link rel="alternate" type="application/rss+xml" title="AI Business Harness Insights" href="/blog/feed.xml" />
  <link rel="stylesheet" href="/styles.css?v={ASSET_V}" />
  <script defer src="/main.js?v={ASSET_V}"></script>
  <script type="application/ld+json">{schema()}</script>
</head>
{header}
  <main id="main">
    <article class="post hub-page">
      <header class="post-head container">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span aria-current="page">AI Business Harness Guide</span></nav>
        <p class="eyebrow">The complete guide · {e(SUBHEAD)}</p>
        <h1>{e(H1)}</h1>
        <p class="post-dek">{e(DEK)}</p>
        <p class="post-meta">By Jeremy Mandile · Published <time datetime="{PUBLISHED}">October 30, 2026</time> · 18 min read</p>
      </header>
      <figure class="post-hero container"><img src="{IMG}/{HERO}.svg" alt="{e(HERO_ALT)}" width="1200" height="630" fetchpriority="high" decoding="async" /><figcaption>{e(HERO_CAP)}</figcaption></figure>
      <div class="post-body container">
{toc(body)}
{body}
      </div>
      <aside class="post-cta container" aria-label="Start with one workflow">
        <div><p class="eyebrow eyebrow-light">ONE WORKFLOW · THIRTY DAYS</p><h2>Start with one business workflow.</h2><p>Tell us about a task that keeps repeating. We'll help you frame it, identify the systems and controls it needs, and decide what stays under human review before anything touches live customer communication.</p></div>
        <a class="button button-light" href="/#contact">Start with one business workflow <span aria-hidden="true">↗</span></a>
      </aside>
    </article>
    {related(tpl_related)}
  </main>
  {footer}
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page)
    print("wrote", OUT)

    import cairosvg
    svg = SITE / "blog" / "images" / f"{HERO}.svg"
    png = HERE / f"{HERO}.tmp.png"
    cairosvg.svg2png(url=str(svg), write_to=str(png), output_width=1200, output_height=630)
    jpg = SITE / "blog" / "images" / f"{HERO}.jpg"
    subprocess.run(["convert", str(png), "-quality", "86", "-strip", str(jpg)], check=True)
    png.unlink()
    print("wrote", jpg)


if __name__ == "__main__":
    main()
