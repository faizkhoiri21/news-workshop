# src/pipeline/silver_to_gold.py
import pandas as pd
from collections import Counter
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from src.scraping.utils import silver_path, gold_path

# Stopwords: Indonesian + English
STOPWORDS = set(stopwords.words("indonesian")) | set(stopwords.words("english"))

# Custom Stopwords
CUSTOM_STOPWORDS = {"video", "januari", "februari", "maret",
                    "april", "mei", "juni", "juli",
                    "agustus", "september", "oktober",
                    "november", "desember"}

STOPWORDS |= CUSTOM_STOPWORDS

def tokenize_and_filter(text: str):
    """Tokenisasi + filter stopwords & non-alfabetik"""
    if not isinstance(text, str):
        return []
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalpha()]  # hanya huruf
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    return tokens

def top_terms(texts: pd.Series, n=20):
    """Hitung top terms (unigram + bigram) dari kumpulan teks"""
    toks = []
    for t in texts.dropna().astype(str):
        toks.extend(tokenize_and_filter(t))

    # Unigram
    unigram_counts = Counter(toks)

    # Bigram
    bigrams = ["_".join(pair) for pair in zip(toks, toks[1:])]
    bigram_counts = Counter(bigrams)

    # Gabungkan unigram + bigram
    combined = unigram_counts + bigram_counts
    return combined.most_common(n)

def daily_articles(df: pd.DataFrame) -> pd.DataFrame:
    """Agregasi jumlah artikel per sumber per hari"""
    return (
        df.assign(date=pd.to_datetime(df["published_at"], errors="coerce").dt.date)
          .groupby(["source_normalized", "date"])
          .size()
          .reset_index(name="articles_per_day")
    )

def quality_check(df: pd.DataFrame) -> pd.DataFrame:
    """Hitung null rate & duplicate rate per kolom utama"""
    rows = []
    for col in ["title", "content", "url", "published_at"]:
        null_rate = df[col].isna().mean()
        dup_rate = 1 - df[col].nunique() / len(df)
        rows.append({
            "column": col,
            "null_rate": round(null_rate, 4),
            "dup_rate": round(dup_rate, 4)
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    # Load silver
    df = pd.read_parquet(silver_path("news.parquet"))

    # Daily aggregation
    daily = daily_articles(df)
    daily.to_parquet(gold_path("daily_articles.parquet"), index=False)

    # Quality table
    quality = quality_check(df)
    quality.to_parquet(gold_path("quality.parquet"), index=False)

    # Top terms per source + kategori
    rows = []
    for (src, cat), g in df.groupby(["source_normalized", "category"]):
        for term, cnt in top_terms(g["content"], n=30):
            rows.append({
                "source_normalized": src,
                "category": cat,
                "term": term,
                "count": cnt
            })

    pd.DataFrame(rows).to_parquet(gold_path("top_terms.parquet"), index=False)

    # Simpan full artikel (untuk EDA analitik)
    df.to_parquet(gold_path("news.parquet"), index=False)

    print("✅ Silver → Gold selesai")
    print("Daily:", daily.shape, gold_path("daily_articles.parquet"))
    print("Quality:", quality.shape, gold_path("quality.parquet"))
    print("Top terms:", len(rows), gold_path("top_terms.parquet"))
    print("News:", df.shape, gold_path("news.parquet"))