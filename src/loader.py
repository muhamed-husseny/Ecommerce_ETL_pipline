from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    from src.models import Product, CategoryAnalytics, ETLLog
except ImportError:
    from models import Product, CategoryAnalytics, ETLLog


class DataLoader:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def load_all(self, clean_products, category_stats, fetched_count, rejected_count):
        session = self.Session()
        try:
            for item in clean_products:
                product_obj = Product(
                    id=item["id"],
                    title=item["title"],
                    category_slug=item["category_slug"],
                    price=item["price"],
                    rating=item["rating"],
                    stock=item["stock"],
                    updated_at=datetime.now(),
                )
                session.merge(product_obj)

            for stat in category_stats:
                stat_obj = CategoryAnalytics(
                    category_slug=stat["category_slug"],
                    total_products=stat["total_products"],
                    avg_price=stat["avg_price"],
                    total_inventory_value=stat["total_inventory_value"],
                    avg_rating=stat["avg_rating"],
                )
                session.merge(stat_obj)

            log_entry = ETLLog(
                records_fetched=fetched_count,
                records_rejected=rejected_count,
                records_loaded=len(clean_products),
                status="SUCCESS",
            )
            session.add(log_entry)

            session.commit()
            print(f"Successfully loaded {len(clean_products)} products and {len(category_stats)} categories into PostgreSQL!")

        except Exception as e:
            session.rollback()
            print(f"Error loading data into database: {e}")

            fail_log = ETLLog(
                records_fetched=fetched_count,
                records_rejected=rejected_count,
                records_loaded=0,
                status="FAILED",
            )
            session.add(fail_log)
            session.commit()
        finally:
            session.close()


if __name__ == "__main__":
    from extractor import APIExtractor, CSVExtractor
    from transformer import DataTransformer
    from analyzer import DataAnalyzer

    DB_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/ecommerce_warehouse"

    raw_data = APIExtractor("https://dummyjson.com/products?limit=100").fetch_products()
    blacklist = CSVExtractor("../data/blacklist.csv").read_blacklist()
    clean_data, rejected = DataTransformer(blacklist_ids=blacklist).transform(raw_data)
    stats = DataAnalyzer().analyze_categories(clean_data)

    loader = DataLoader(DB_URL)
    loader.load_all(
        clean_products=clean_data,
        category_stats=stats,
        fetched_count=len(raw_data),
        rejected_count=rejected,
    )

