#!/usr/bin/env python3
"""
fetch_article.py — Fetches and extracts clean article content from any URL.

Primary:  trafilatura   (pip install trafilatura)
Fallback: newspaper4k  (pip install newspaper4k)
Last resort: requests + BeautifulSoup (pip install requests beautifulsoup4)

Usage:
    python3 fetch_article.py --url "https://example.com/article"

Output (stdout, JSON):
    {
        "url":          "https://example.com/article",
        "title":        "Article Title",
        "author":       "Author Name or null",
        "date":         "YYYY-MM-DD or null",
        "site_name":    "Site Name",
        "description":  "Short meta description or null",
    "word_count":   1234,
    "read_minutes": 5,
    "content":      "Full clean article text...",
    "media": {
        "images": [
            {"src": "https://example.com/image.jpg", "alt": "Image description"}
        ],
        "videos": [
            {"src": "https://youtube.com/embed/xxx", "platform": "youtube"}
        ],
        "links": [
            {"href": "https://example.com/related", "text": "Related article"}
        ]
    },
    "status":       "ok"
}

    On failure:
    {
        "url":    "...",
        "status": "error",
        "reason": "Human-readable explanation"
    }
"""

import argparse
import json
import sys
import re
from datetime import datetime
from urllib.parse import urlparse


# ─── helpers ──────────────────────────────────────────────────────────────────

def estimate_read_time(text: str) -> int:
    """Average adult reading speed: ~238 words/min."""
    words = len(text.split())
    return max(1, round(words / 238))


def clean_text(text: str) -> str:
    """Remove excessive blank lines and leading/trailing whitespace."""
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def site_name_from_url(url: str) -> str:
    hostname = urlparse(url).hostname or url
    hostname = hostname.replace("www.", "")
    return hostname


def error(url: str, reason: str) -> dict:
    return {"url": url, "status": "error", "reason": reason}


# ─── media extraction ──────────────────────────────────────────────────────────

def resolve_url(src: str | None, base_parsed) -> str | None:
    if not src:
        return None
    src = src.strip()
    if src.startswith("data:") or src.startswith("blob:"):
        return None
    if src.startswith("//"):
        src = "https:" + src
    elif src.startswith("/"):
        src = f"{base_parsed.scheme}://{base_parsed.netloc}{src}"
    elif not src.startswith("http"):
        return None
    return src


def extract_media_from_html(html: str, base_url: str) -> dict:
    """Extract images, videos, and meaningful links from raw HTML."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return {"images": [], "videos": [], "links": []}

    soup = BeautifulSoup(html, "html.parser")
    base_parsed = urlparse(base_url)
    base_domain = base_parsed.netloc

    # ── images ──
    images = []
    seen_srcs: set = set()
    for img in soup.find_all("img"):
        src = resolve_url(img.get("src"), base_parsed)
        if not src or src in seen_srcs:
            continue
        # skip tiny icons (<100px wide)
        w = img.get("width")
        if w and w.isdigit() and int(w) < 100:
            continue
        # skip common ad / tracking patterns
        sl = src.lower()
        if any(p in sl for p in ("advertisement", "banner", "sponsor", "pixel", "analytics")):
            continue
        # skip svg/data placeholders
        if any(p in sl for p in ("1x1", "placeholder", "transparent")):
            continue
        seen_srcs.add(src)
        images.append({"src": src, "alt": (img.get("alt") or "")[:300]})

    # ── videos (iframes + <video> tags) ──
    videos = []
    seen_vsrcs: set = set()
    for iframe in soup.find_all("iframe"):
        src = resolve_url(iframe.get("src", ""), base_parsed)
        if not src or src in seen_vsrcs:
            continue
        platform = "other"
        if "youtube.com" in src or "youtu.be" in src:
            platform = "youtube"
        elif "vimeo.com" in src:
            platform = "vimeo"
        seen_vsrcs.add(src)
        videos.append({"src": src, "platform": platform})

    for video in soup.find_all("video"):
        src = resolve_url(video.get("src"), base_parsed)
        if src and src not in seen_vsrcs:
            seen_vsrcs.add(src)
            videos.append({"src": src, "platform": "html5"})
        for source in video.find_all("source"):
            src = resolve_url(source.get("src"), base_parsed)
            if src and src not in seen_vsrcs:
                seen_vsrcs.add(src)
                videos.append({"src": src, "platform": "html5"})

    # ── links (meaningful external / deep links) ──
    links = []
    seen_hrefs: set = set()
    for a in soup.find_all("a", href=True):
        href = resolve_url(a["href"], base_parsed)
        text = a.get_text(strip=True)
        if not href or not text or href in seen_hrefs:
            continue
        # skip social sharing
        ph = urlparse(href).netloc
        if any(d in ph for d in ("twitter.com/share", "facebook.com/sharer", "linkedin.com/share", "pinterest.com/pin")):
            continue
        # skip same-domain nav links with very short text
        if ph == base_domain and len(text) < 5:
            continue
        # skip comment / category / tag anchors
        if any(p in href.lower() for p in ("#comment", "#reply", "#respond", "/tag/", "/category/")):
            continue
        seen_hrefs.add(href)
        links.append({"href": href, "text": text[:200]})

    return {
        "images": images[:10],
        "videos": videos[:5],
        "links":  links[:20],
    }


# ─── extraction methods ────────────────────────────────────────────────────────

def try_trafilatura(url: str) -> dict | None:
    try:
        import trafilatura
        from trafilatura.settings import use_config

        config = use_config()
        config.set("DEFAULT", "EXTRACTION_TIMEOUT", "30")

        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return None

        result = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=True,
            output_format="json",
            with_metadata=True,
        )
        if not result:
            return None

        data = json.loads(result)
        content = clean_text(data.get("text") or "")
        if len(content) < 100:
            return None

        title = data.get("title") or ""
        author = data.get("author") or None
        date = data.get("date") or None
        description = data.get("description") or None
        hostname = data.get("hostname") or site_name_from_url(url)

        media = extract_media_from_html(downloaded, url)

        return {
            "url": url,
            "title": title,
            "author": author,
            "date": date,
            "site_name": hostname,
            "description": description,
            "word_count": len(content.split()),
            "read_minutes": estimate_read_time(content),
            "content": content,
            "media": media,
            "status": "ok",
        }
    except ImportError:
        return None
    except Exception:
        return None


def try_newspaper(url: str) -> dict | None:
    try:
        from newspaper import Article
        article = Article(url)
        article.download()
        article.parse()

        content = clean_text(article.text)
        if len(content) < 100:
            return None

        author = ", ".join(article.authors) if article.authors else None
        date = article.publish_date.strftime("%Y-%m-%d") if article.publish_date else None
        hostname = site_name_from_url(url)

        html = getattr(article, "html", "")
        media = extract_media_from_html(html, url) if html else {"images": [], "videos": [], "links": []}

        return {
            "url": url,
            "title": article.title or "",
            "author": author,
            "date": date,
            "site_name": hostname,
            "description": article.meta_description or None,
            "word_count": len(content.split()),
            "read_minutes": estimate_read_time(content),
            "content": content,
            "media": media,
            "status": "ok",
        }
    except ImportError:
        return None
    except Exception:
        return None


def try_bs4(url: str) -> dict | None:
    try:
        import requests
        from bs4 import BeautifulSoup

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove noise
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        # Title
        title = ""
        if soup.find("h1"):
            title = soup.find("h1").get_text(strip=True)
        elif soup.title:
            title = soup.title.get_text(strip=True)

        # Meta description
        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = desc_tag["content"] if desc_tag and desc_tag.get("content") else None

        # Main content — prefer <article> or <main>
        body = soup.find("article") or soup.find("main") or soup.find("body")
        content = clean_text(body.get_text(separator="\n") if body else "")

        if len(content) < 100:
            return None

        media = extract_media_from_html(resp.text, url)

        return {
            "url": url,
            "title": title,
            "author": None,
            "date": None,
            "site_name": site_name_from_url(url),
            "description": description,
            "word_count": len(content.split()),
            "read_minutes": estimate_read_time(content),
            "content": content,
            "media": media,
            "status": "ok",
        }
    except ImportError:
        return None
    except Exception:
        return None


# ─── auto-install helper ───────────────────────────────────────────────────────

def pip_install(*packages):
    import subprocess
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", *packages]
    )


# ─── main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fetch article content from a URL.")
    parser.add_argument("--url", required=True, help="Article URL to fetch")
    parser.add_argument("--no-install", action="store_true", help="Skip auto-install")
    args = parser.parse_args()

    url = args.url.strip()

    # Validate URL
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        print(json.dumps(error(url, "Invalid URL — must start with http:// or https://")))
        sys.exit(1)

    # Try trafilatura first (best quality)
    result = try_trafilatura(url)

    # Fallback: newspaper4k
    if result is None:
        result = try_newspaper(url)

    # Last resort: requests + BeautifulSoup
    if result is None:
        result = try_bs4(url)

    # All failed — try installing trafilatura and retry once
    if result is None and not args.no_install:
        try:
            pip_install("trafilatura")
            result = try_trafilatura(url)
        except Exception:
            pass

    if result is None:
        print(json.dumps(error(
            url,
            "Could not extract article content. The page may require JavaScript, "
            "be behind a paywall, or block automated access. "
            "Try installing: pip install trafilatura newspaper4k"
        )))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
