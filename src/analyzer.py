import pandas as pd

class DataAnalyzer:
    def analyze_categories(self,clean_products):
        if not clean_products:
            return []


        df = pd.DataFrame(clean_products)

        df["inventory_value"] = df["price"] * df["stock"]


        summary = (
            df.groupby("category_slug")
            .agg(
                total_products = ("id","count"),
                avg_price = ("price","mean"),
                total_inventory_value = ("inventory_value","sum"),
                avg_rating = ("rating","mean")
            )
            .reset_index()
        )

        summary = summary.round(2)
        return summary.to_dict(orient="records")



if __name__ == "__main__":
    from extractor import APIExtractor, CSVExtractor
    from transformer import DataTransformer

    raw_data = APIExtractor("https://dummyjson.com/products?limit=100").fetch_products()
    blacklist = CSVExtractor("../data/blacklist.csv").read_blacklist()
    clean_data, _ = DataTransformer(blacklist_ids=blacklist).transform(raw_data)

    analyzer = DataAnalyzer()
    category_stats = analyzer.analyze_categories(clean_data)


    print(f"Total categories analyzed: {len(category_stats)}")
    for stat in category_stats[:3]:
        print(stat)

