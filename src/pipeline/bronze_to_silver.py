# src/pipeline/bronze_to_silver.py
import pandas as pd, glob, re, math
from slugify import slugify
from datetime import datetime, timezone
from collections import Counter
from nltk.corpus import stopwords

from src.scraping.utils import silver_path

def load_bronze(pattern="data/bronze/*/source=*/part-*.jsonl"):
    """Load semua file bronze jsonl ke DataFrame"""
    frames = [pd.read_json(p, lines=True) for p in glob.glob(pattern)]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

def normalize_published_at(row):
    """Gunakan published_at jika ada, kalau tidak fallback ke scraped_at"""
    pub = row.get("published_at")
    if pd.isna(pub) or not pub:
        pub = row.get("scraped_at")
    try:
        return pd.to_datetime(pub, errors="coerce", utc=True).isoformat()
    except Exception:
        return None

def clean_content(text: str) -> str:
    """Bersihkan konten: hapus script/share text, trim whitespace"""
    if not isinstance(text, str):
        return None
    # buang teks 'pilihan editor', 'baca juga', dll
    text = re.sub(r"(pilihan editor.*|baca juga.*)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Cleaning & standardization sesuai kriteria Silver"""
    # drop baris tanpa title/content
    df = df.dropna(subset=["title", "content"])

    # normalisasi published_at
    df["published_at"] = df.apply(normalize_published_at, axis=1)

    # source_normalized
    df["source_normalized"] = df["source"].astype(str).map(slugify)

    # deduplicate by url or article_id (keep terbaru by scraped_at)
    if "scraped_at" in df.columns:
        df["scraped_at_dt"] = pd.to_datetime(df["scraped_at"], errors="coerce", utc=True)
        df = df.sort_values("scraped_at_dt", ascending=False)
    df = df.drop_duplicates(subset=["url", "article_id"], keep="first")

    # bersihkan text
    df["title"] = df["title"].astype(str).str.strip()
    df["content"] = df["content"].astype(str).map(clean_content)

    # tambah word_count & read_time_min
    df["word_count"] = df["content"].str.split().str.len()
    df["read_time_min"] = (df["word_count"] / 200).apply(lambda x: math.ceil(x) if pd.notna(x) else None)

    return df

if __name__ == "__main__":
    df = load_bronze()
    df = clean(df)

    outpath = silver_path("news.parquet")
    df.to_parquet(outpath, index=False)

    print("✅ Bronze to Silver selesai")
    print("Jumlah artikel:", len(df))
    print("Output:", outpath)