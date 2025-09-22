# src/scraping/scrape_portal_tempo.py
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
    """Parse halaman indeks tempo.co → daftar URL artikel."""
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.select("figcaption p a[href]"):
        href = a["href"]
        if href.startswith("/"):
            href = "https://www.tempo.co" + href
        links.append(href)
    return links

def parse_article(html):
    """Ambil konten utama dari halaman artikel tempo.co."""
    soup = BeautifulSoup(html, "lxml")

    title = soup.select_one("h1").get_text(strip=True) if soup.select_one("h1") else None

    content_parts = []
    for p in soup.select("div#content-wrapper p"):
        text = p.get_text(" ", strip=True)
        if "pilihan editor" in text.lower():
            continue
        content_parts.append(text)
    content = " ".join(content_parts).strip()

    date_tag = soup.select_one("p.text-neutral-900.text-sm")
    date_raw = date_tag.get_text(strip=True) if date_tag else None
    published = parse_dt(date_raw, settings={"RETURN_AS_TIMEZONE_AWARE": True}) if date_raw else None

    author_tag = soup.select_one("a[href*='/penulis/'] p.text-neutral-1200.font-bold")
    author = author_tag.get_text(strip=True) if author_tag else None

    category_tag = soup.select_one("span.text-sm.font-medium.text-primary-main")
    category = category_tag.get_text(strip=True) if category_tag else None

    return {
        "title": title,
        "content": content,
        "published_at": published.astimezone(timezone.utc).isoformat() if published else None,
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
                    "source": "tempo",
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
    urls = ["https://www.tempo.co/indeks"] + [
        f"https://www.tempo.co/indeks?page={i}" for i in range(2, pages + 1)
    ]
    data = run(urls)

    today = datetime.now().strftime("%Y%m%d")
    outpath = bronze_path(today, "source=tempo", "part-000.jsonl") 
    os.makedirs(os.path.dirname(outpath), exist_ok=True)

    with open(outpath, "w", encoding="utf-8") as f:
        for row in data:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    logging.info(f"✅ Scraped {len(data)} articles → {outpath}")