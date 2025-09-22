# Workshop Project: Scraping Online News

Proyek ini bertujuan untuk melakukan web scraping pada portal berita online dan mengolah data yang diperoleh melalui pipeline *Medallion Architecture* untuk mendapatkan dataset yang siap digunakan untuk analitik.

## Table of Contents

- [Cara Menjalankan Proyek](#cara-menjalankan-proyek)
  - [Persiapan Lingkungan](#persiapan-lingkungan)
  - [Jalankan Pipeline End-to-End](#jalankan-pipeline-end-to-end)
- [Asumsi](#asumsi)
- [Keterbatasan](#keterbatasan)
- [Sumber](#sumber)
- [Tip](#tip)

## Cara Menjalankan Proyek

### Persiapan Lingkungan

#### Install dependencies

```bash
pip install -r requirements.txt
```

#### atau

```bash
make install
```

#### Unduh data NLTK

Beberapa tahap pipeline (misal pembuangan stopwords dan tokenisasi) membutuhkan dataset tambahan dari NLTK.
Setelah meng-install dependencies, jalankan sekali per environment:

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"
```

### Jalankan Pipeline End-to-End

Proyek ini menggunakan pipeline Medallion Architecture (Bronze → Silver → Gold). Jalankan seluruh pipeline:

```bash
make all
```

Atau step-by-step:

```bash
make scrape  # hanya scraping
make silver  # transform bronze → silver
make gold    # transform silver → gold
```

#### Output utama:

- `data/`
  - `bronze/` – hasil raw scraping
  - `silver/` – data sudah dibersihkan & dinormalisasi
  - `gold/` – tabel analytics-ready

#### Notebook analitik:

```bash
notebooks/01_eda.ipynb
```

---

## Asumsi

- **Akses & Etika**: Portal berita yang di-scrape mengizinkan crawling ringan sesuai robots.txt.
- **Zona Waktu**: Semua `published_at` disimpan dalam format UTC ISO-8601 (`YYYY-MM-DDTHH:MM:SS+00:00`).
- **Dedup**: Duplikat artikel diidentifikasi via `url` atau `article_id`.
- **Performa Scraping**: Delay 1,2 detik per artikel; retry maks 3x.

---

## Keterbatasan

- Struktur HTML situs dapat berubah → selector di scraper mungkin perlu disesuaikan ulang.
- Tidak semua artikel memiliki `author` atau `category`, sehingga kolom ini bisa `null`.
- Hanya meng-crawl 20 halaman index; dataset bukan representasi penuh seluruh portal.
- Analisis topik bersifat ringan (hanya unigram/bigram), belum menggunakan NLP lanjutan.

---

## Sumber

- **Portal Berita**:
  - https://tempo.co/indeks/
  - https://news.detik.com/indeks/

- **Library Python**:
  - [requests](https://docs.python-requests.org/)
  - [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
  - [pandas](https://pandas.pydata.org/docs/)
  - [numpy](https://numpy.org/doc/stable/)
  - [pyarrow](https://arrow.apache.org/docs/python/)
  - [matplotlib](https://matplotlib.org/stable/contents.html)
  - [tqdm](https://tqdm.github.io/)
  - [python-slugify](https://github.com/un33k/python-slugify)
  - [dateparser](https://dateparser.readthedocs.io/en/latest/)
  - [lxml](https://lxml.de/)
  - [fastparquet](https://fastparquet.readthedocs.io/en/latest/)
  - [nltk](https://www.nltk.org/)
  - [seaborn](https://seaborn.pydata.org/)

- **Referensi Arsitektur**:
  - [Medallion Architecture](https://www.databricks.com/glossary/medallion-architecture)

---

## Tip

📄 Lihat `reports/analytics_summary.md` untuk ringkasan insight dan rekomendasi bisnis dari data Gold.