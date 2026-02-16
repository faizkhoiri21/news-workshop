# Workshop Project: Online News Scraping

![News Portals Crop](https://github.com/user-attachments/assets/7dc088da-9ac5-4fae-b6ef-c4969d0fb07d)

Web scraping pipeline for online news portals using Medallion Architecture (Bronze → Silver → Gold) to produce analytics-ready datasets.

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

Or using Make:

```bash
make install
```

### Download NLTK Data

Required for stopword removal and tokenization (run once per environment):

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"
```

### Run Pipeline

Execute the complete pipeline:

```bash
make all
```

Or run step-by-step:

```bash
make scrape  # Bronze: raw scraping
make silver  # Silver: cleaning & normalization
make gold    # Gold: analytics-ready tables
```

## Output Structure

```
data/
├── bronze/   # Raw scraped data
├── silver/   # Cleaned & normalized data
└── gold/     # Analytics-ready tables

notebooks/
└── 01_eda.ipynb   # Exploratory data analysis
```

## Key Assumptions

- **Crawling Ethics**: News portals allow light crawling according to robots.txt
- **Timezone**: All `published_at` stored in UTC ISO-8601 format
- **Deduplication**: Articles identified by `url` or `article_id`
- **Scraping Rate**: 1.2s delay per article, max 3 retries

## Limitations

- HTML structure changes may require selector updates
- Some articles may have null `author` or `category` fields
- Limited to 20 index pages per source
- Basic topic analysis (unigram/bigram only)

## Data Sources

**News Portals:**
- https://tempo.co/indeks/
- https://news.detik.com/indeks/

**Architecture Reference:**
- [Medallion Architecture](https://www.databricks.com/glossary/medallion-architecture)

## Analytics

View insights and business recommendations in:
```
reports/analytics_summary.md
```
