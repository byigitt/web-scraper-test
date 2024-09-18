import json
from scraper import extract_product_data, get_sitemap_url_from_robots, get_sitemap_urls
from file_writer import write_to_csv, write_to_json, append_to_master_files
import os
from urllib.parse import urlparse

def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)

def get_dynamic_file_names(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    category_name = path_parts[2]
    return f"{category_name}.csv", f"{category_name}.json"

def main():
    config = load_config()
    base_url = config['base_url']
    
    robots_txt_url = f"{base_url}/robots.txt"
    sitemap_url = get_sitemap_url_from_robots(robots_txt_url)

    if not sitemap_url:
        print("Sitemap bulunamadı.")
        return

    sitemap_urls = get_sitemap_urls(sitemap_url)

    if not sitemap_urls:
        print("Sitemap URL'leri bulunamadı.")
        return

    category_files = {}

    for sitemap_url in sitemap_urls:
        print(f"Sayfa inceleniyor: {sitemap_url}")
        try:
            products = extract_product_data(sitemap_url)
            if products:
                csv_filename, json_filename = get_dynamic_file_names(sitemap_url)
                if csv_filename not in category_files:
                    category_files[csv_filename] = []

                parsed_url = urlparse(sitemap_url)
                folder_name = os.path.join("data", parsed_url.path.strip('/'))

                csv_file = f"{parsed_url.path.strip('/')}.csv".replace('/', '_')
                json_file = f"{parsed_url.path.strip('/')}.json".replace('/', '_')
                
                write_to_csv(products, folder_name, csv_file)
                write_to_json(products, folder_name, json_file)
                
                category_files[csv_filename].extend(products)
        except Exception as e:
            print(f"Hata oluştu: {e}")

    for csv_filename, product_data in category_files.items():
        json_filename = csv_filename.replace('.csv', '.json')
        append_to_master_files(product_data, csv_filename, json_filename)
        
        print(f"Tüm ürünler {csv_filename} ve {json_filename} dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
