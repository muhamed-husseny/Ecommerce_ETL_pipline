class DataTransformer:
    def __init__(self,blacklist_ids, min_price=0.0):
        self.blacklist_ids = blacklist_ids
        self.min_price = min_price


    def _clean_category(self,raw_category):
        if not raw_category:
            return "uncategorized"
        return raw_category.strip().lower().replace(" ","-")



    def transform(self, raw_products):
            clean_products = []
            seen_ids = set()
            rejected_count = 0

            for item in raw_products:
                product_id = item.get("id")
                price = item.get("price", 0.0)

                if (
                        product_id is None
                        or product_id in self.blacklist_ids
                        or product_id in seen_ids
                        or price <= self.min_price
                ):
                    rejected_count += 1
                    continue

                seen_ids.add(product_id)


                cleaned_item = {
                    "id": product_id,
                    "title": item.get("title", "Unknown").strip(),
                    "category_slug": self._clean_category(item.get("category")),
                    "price": float(price),
                    "rating": float(item.get("rating", 0.0)),
                    "stock": int(item.get("stock", 0)),
                }
                clean_products.append(cleaned_item)

            clean_products.sort(key=lambda x: x["rating"], reverse=True)

            return clean_products, rejected_count

if __name__ == "__main__":
    from extractor import APIExtractor, CSVExtractor

    raw_data = APIExtractor("https://dummyjson.com/products?limit=100").fetch_products()
    blacklist = CSVExtractor("../data/blacklist.csv").read_blacklist()

    transformer = DataTransformer(blacklist_ids=blacklist, min_price=0.0)
    clean_data, rejected = transformer.transform(raw_data)

    print(f"Total fetched: {len(raw_data)}")
    print(f"Rejected: {rejected}")
    print(f"Clean ready for DB: {len(clean_data)}")
    if clean_data:
        print("Top rated product:", clean_data[0])