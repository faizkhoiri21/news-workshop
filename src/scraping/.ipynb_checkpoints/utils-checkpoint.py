# src/scraping/utils.py
from pathlib import Path

# Tentukan root project = dua tingkat di atas folder utils.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]

def bronze_path(*parts):
    return str(PROJECT_ROOT.joinpath("data/bronze", *parts))

def silver_path(*parts):
    return str(PROJECT_ROOT.joinpath("data/silver", *parts))

def gold_path(*parts):
    return str(PROJECT_ROOT.joinpath("data/gold", *parts))