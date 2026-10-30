# AI Business Harness blog source

Posts live in `blog/NN-slug.md` (front matter + Markdown). Illustrations are drawn in `images.py`.

Build: `python3 build_blog.py` (needs `markdown` and `playwright` with Chromium).
It writes `../aibusinessharness/blog/`, the homepage "Insights" teaser and `sitemap.xml`.
Only `sites/aibusinessharness/` is deployed.
