"""Shared image-rights metadata for ImageObject structured data.

Google Search Console's Image Metadata report looks for creator, creditText,
copyrightNotice, license and acquireLicensePage on every ImageObject.
All illustrations on aibusinessharness.com are original work owned by
AI Business Harness (a Mandile SEO service).
"""
BASE = "https://aibusinessharness.com"
LICENSE_URL = f"{BASE}/image-license/"

RIGHTS = {
    "creator": {"@type": "Organization", "name": "AI Business Harness", "url": f"{BASE}/"},
    "creditText": "AI Business Harness",
    "copyrightHolder": {"@type": "Organization", "name": "AI Business Harness", "url": f"{BASE}/"},
    "copyrightNotice": "© 2026 AI Business Harness. All rights reserved.",
    "copyrightYear": 2026,
    "license": LICENSE_URL,
    "acquireLicensePage": LICENSE_URL,
}


def image_object(url: str, **extra) -> dict:
    """Return a fully attributed ImageObject for an image on this site."""
    return {"@type": "ImageObject", "url": url, "contentUrl": url, **extra, **RIGHTS}
