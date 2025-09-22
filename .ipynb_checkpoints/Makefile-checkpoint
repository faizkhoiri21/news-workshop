install:
	 pip install -r requirements.txt

scrape:
	 python src/scraping/scrape_portal_tempo.py
	 python src/scraping/scrape_portal_detik.py

silver:
	 python -m src.pipeline.bronze_to_silver

gold:
	 python -m src.pipeline.silver_to_gold

all: scrape silver gold