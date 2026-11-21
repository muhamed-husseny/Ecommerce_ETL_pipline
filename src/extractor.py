import csv
import requests

class APIExtractor:
    def __init__(self,api_url):
        self.api_url = api_url


    def fetch_products(self):
        try:
            response = requests.get(self.api_url,timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("products", [])
        except requests.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return []



class CSVExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_blacklist(self):
        blacklisted_ids = set()
        try:
            with open(self.file_path, mode="r",encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    blacklisted_ids.add(int(row["product_id"]))
        except FileExistsError:
            print(f"Warning: Blacklist file not found at {self.file_path}")
        return blacklisted_ids

if __name__ == "__main__":
    api = APIExtractor("https://dummyjson.com/products?limit=100")
    products = api.fetch_products()
    print(f"Fetched {len(products)} products.")
    if products:
        print("Sample product:", products[0])

    csv_ext = CSVExtractor("../data/blacklist.csv")
    blacklist = csv_ext.read_blacklist()
    print("Blacklisted IDs:", blacklist)


