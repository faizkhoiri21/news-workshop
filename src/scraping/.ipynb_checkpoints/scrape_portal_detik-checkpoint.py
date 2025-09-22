# src/scraping/scrape_portal_detik.py
import os, time, json, uuid, logging, requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from dateparser import parse as parse_dt
from utils import bronze_path  

HEADERS = {"User-Agent": "TLab-DA-Workshop/1.0 (+contact@example.com)"}

def fetch(url):
    """Ambil HTML dengan retry sederhana."""
    for i in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            logging.warning(f"Retry {i+1} {url}: {e}")
        time.sleep(2 * (i+1))
    raise RuntimeError(f"Failed: {url}")

def parse_list(html):
    """Parse halaman indeks detik.com → daftar URL artikel."""
    soup = BeautifulSoup(html, "lxml")
    urls = []
    for art in soup.select("article.list-content__item"):
        a = art.find("a")
        if not a:
            continue
        href = a.get("href")
        if href and href.startswith("https://news.detik.com/"):
            urls.append(href)
    return list(dict.fromkeys(urls))  # hapus duplikat

def parse_article(html):
    """Ambil konten utama dari halaman artikel detik.com."""
    soup = BeautifulSoup(html, "lxml")

    # Judul
    title_tag = soup.select_one("h1.detail__title")
    title = title_tag.get_text(strip=True) if title_tag else None

    # Konten
    banned = ["scroll to continue with content"]
    content_parts = []
    for p in soup.select("div.detail__body-text p"):
        text = p.get_text(" ", strip=True)
        if not any(bad in text.lower() for bad in banned):
            content_parts.append(text)
    content = " ".join(content_parts).strip() if content_parts else None

    # Tanggal publish
    date_raw = soup.select_one("div.detail__date")
    date_raw = date_raw.get_text(strip=True) if date_raw else None
    published = parse_dt(date_raw, settings={"RETURN_AS_TIMEZONE_AWARE": True}) if date_raw else None
    published = published.astimezone(timezone.utc).isoformat() if published else None

    # Penulis
    author_tag = soup.select_one("div.detail__author")
    author = None
    if author_tag:
        author_texts = [t for t in author_tag.contents if t.name is None]
        if author_texts:
            author = author_texts[0].strip().rstrip("-").strip()

    # Kategori → ambil dari breadcrumb
    category_tag = soup.select_one('a[dtr-evt="breadcrumb"]')
    category = category_tag.get_text(strip=True) if category_tag else None

    return {
        "title": title,
        "content": content,
        "published_at": published,
        "author": author,
        "category": category
    }

def run(start_urls):
    """Scraping loop: dari daftar halaman indeks → artikel."""
    seen, out = set(), []
    for list_url in start_urls:
        listing = fetch(list_url)
        for url in parse_list(listing):
            if url in seen:
                continue
            seen.add(url)
            try:
                html = fetch(url)
                art = parse_article(html)
                art.update({
                    "article_id": str(uuid.uuid5(uuid.NAMESPACE_URL, url)),
                    "source": "detik",
                    "url": url,
                    "scraped_at": datetime.now(timezone.utc).isoformat()
                })
                out.append(art)
                time.sleep(1.2)
            except Exception as e:
                logging.exception(f"Error {url}: {e}")
    return out

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    pages = 20
    urls = ["https://news.detik.com/indeks"] + [
        f"https://news.detik.com/indeks?page={i}" for i in range(2, pages + 1)
    ]
    data = run(urls)

    today = datetime.now().strftime("%Y%m%d")
    outpath = bronze_path(today, "source=detik", "part-000.jsonl")
    os.makedirs(os.path.dirname(outpath), exist_ok=True)

    with open(outpath, "w", encoding="utf-8") as f:
        for row in data:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    logging.info(f"✅ Scraped {len(data)} articles → {outpath}")
