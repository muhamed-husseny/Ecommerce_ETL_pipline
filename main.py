import os
from dotenv import load_dotenv
from src.models import init_db
from src.extractor import APIExtractor, CSVExtractor
from src.transformer import DataTransformer
from src.analyzer import DataAnalyzer
from src.loader import DataLoader


def run_pipeline():
    load_dotenv()
    DB_URL = os.getenv("DB_URL")
    API_URL = os.getenv("API_URL")
    BLACKLIST_PATH = os.getenv("BLACKLIST_PATH")

    print("--- Starting E-Commerce ETL Pipeline ---")

    init_db(DB_URL)

    print("[1/4] Extracting data from API and CSV...")
    raw_products = APIExtractor(API_URL).fetch_products()
    blacklisted_ids = CSVExtractor(BLACKLIST_PATH).read_blacklist()

    if not raw_products:
        print("No products fetched. Stopping pipeline.")
        return

    print("[2/4] Cleaning and filtering products...")
    transformer = DataTransformer(blacklist_ids=blacklisted_ids, min_price=0.0)
    clean_products, rejected_count = transformer.transform(raw_products)

    print("[3/4] Analyzing category metrics with Pandas...")
    category_stats = DataAnalyzer().analyze_categories(clean_products)

    print("[4/4] Loading data into PostgreSQL...")
    loader = DataLoader(DB_URL)
    loader.load_all(
        clean_products=clean_products,
        category_stats=category_stats,
        fetched_count=len(raw_products),
        rejected_count=rejected_count,
    )

    print("--- Pipeline Finished Successfully ---")


if __name__ == "__main__":
    run_pipeline()
