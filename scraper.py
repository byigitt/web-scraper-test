import requests
from bs4 import BeautifulSoup
import re

def get_sitemap_url_from_robots(robots_txt_url):
    try:
        response = requests.get(robots_txt_url)
        response.raise_for_status()
        
        lines = response.text.splitlines()
        sitemap_urls = [line.split(': ')[1].strip() for line in lines if line.startswith('Sitemap:')]
        
        if not sitemap_urls:
            raise ValueError("Sitemap robots.txt içinde bulunamadı.")

        print(f"Sitemap bulundu: {sitemap_urls[0]}")
        return sitemap_urls[0]
    except Exception as e:
        print(f"Sitemap robots.txt dosyasından alınırken bir hata oluştu: {e}")
        return None

def get_sitemap_urls(sitemap_url):
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'xml')
        sitemap_links = [loc_tag.get_text() for loc_tag in soup.find_all('loc')]

        if not sitemap_links:
            raise ValueError("Sitemap linki sitemap sayfasında bulunamadı.")

        print(f"{len(sitemap_links)} URL bulundu.")
        return sitemap_links
    except Exception as e:
        print(f"Sitemap URL'lerini alırken bir hata oluştu: {e}")
        return []

def clean_price(price_text):
    price_text = price_text.replace('SEPETE EKLE', '').replace('ÜRÜNÜ İNCELE', '').strip()
    prices = re.findall(r'\d+ TL', price_text)

    if len(prices) > 1:
        price_text = prices[1]
    elif prices:
        price_text = prices[0]

    clean_price = re.sub(r' TL', '', price_text).strip()

    try:
        clean_price = float(clean_price.replace('.', '').replace(',', '.'))
        return f"{clean_price:.2f} TL"
    except ValueError:
        return "Fiyat Bilgisi Yok"

def extract_product_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        print(f"{url} sayfası işleniyor.")

        product_data = []
        products = soup.find_all('div', class_='product')

        for product in products:
            name_tag = product.find('a', class_='product-name')
            name = name_tag.get_text(strip=True) if name_tag else 'Ürün İsmi Bulunamadı'
            
            price_div = product.find('div', class_='product-price-productbox')
            price = "Fiyat Bilgisi Yok"
            if price_div:
                price = clean_price(price_div.get_text(strip=True))

            rating_div = product.find('div', class_='absolute-grad')
            rating = None
            if rating_div and 'style' in rating_div.attrs:
                style_value = rating_div['style']
                width_percentage = float(style_value.split('width:')[1].replace('%', '').strip())
                rating = round((width_percentage / 100) * 10, 1)

            image_tag = product.find('div', class_='product-image-productcard').find('img')
            image_url = image_tag['data-original'] if image_tag and 'data-original' in image_tag.attrs else (image_tag['src'] if image_tag else 'Resim Yok')

            product_data.append({
                "Ürün İsmi": name,
                "Fiyat": price,
                "Puan": rating if rating else "Puan Yok",
                "Ürün Resmi": image_url
            })

        return product_data
    except Exception as e:
        print(f"{url} sayfası işlenirken hata oluştu: {e}")
        return []