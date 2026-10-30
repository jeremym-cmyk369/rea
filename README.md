# AI Business Harness — launch-ready static marketing site

An original, responsive website for **https://aibusinessharness.com**. Design direction: clean full-bleed product storytelling, striking scale, generous whitespace and refined interactions inspired by contemporary premium technology websites. No Tesla/Apple trademarks, code, fonts or imagery were copied.

## Pages / files
- `index.html` — complete home page and illustrative estimate review demo
- `privacy.html` — privacy and contact details
- `styles.css` — responsive styles, reduced-motion support, focus indicators
- `main.js` — client-side demo interaction, mobile navigation and inquiry composer
- `assets/mark.svg` — original mark
- `assets/share.png` — original 1200 × 630 Open Graph social image
- `robots.txt` / `sitemap.xml` — crawl directives

## Running locally
From this directory run `python3 -m http.server 8080`, then visit `http://localhost:8080`.

## Hostinger deployment
This is a zero-dependency static website. Upload the **contents of this directory** to the document root for `aibusinessharness.com` or configure a Git deployment with this directory as the publish root. If the Git host only deploys from the repository root, copy this website into a dedicated deployment repository rather than publishing the entire REA monorepo.

The site is intentionally isolated from REA's own `website/` directory and from mandileseo.com. Connecting the domain and deploying to production are separate tasks and are not completed by a GitHub pull request.

## Contact form
The inquiry form opens the visitor's email program using a prefilled `mailto:` link addressed to `jeremy@mandileseo.com`. This does **not** deliver messages from the server. For reliable inbound submissions, connect a tested backend service and update the privacy disclosure before launch.

## Demonstration integrity
The estimate-follow-up demo is entirely client-side and uses fictional records. Its approval buttons simulate a review decision only; no CRM, agent, email, or back-office integration is connected. Never describe it as production AI automation.

## Acceptance checks
- Responsive layout at desktop and mobile widths, accessible header/menu and controls
- Demo counters update on approval/flag, reset restores defaults
- All internal anchor destinations exist
- HTML meta title, canonical, OG image, JSON-LD and sitemap align with domain
- No external network dependencies, analytics pixels, third-party images, or installed packages

## Relationship to REA
[REA](https://github.com/morluto/rea) is a separate reverse-engineering analysis toolkit. This project may live in the user's REA fork under `sites/aibusinessharness/` during development without modifying or replacing REA's existing product code. It does not claim that REA was executed against Tesla or Apple; public visual references were used to build an original design.
