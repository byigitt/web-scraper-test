# Web Scraper Test Projesi

Bu proje, supplementler.com sitesinden ürün bilgilerini çekmek için oluşturulmuş bir web scraper'dır. Ürün isimlerini, fiyatlarını, puanlarını ve resim URL'lerini çekerek CSV ve JSON dosyalarına kaydeder.

## Kurulum

1. Depoyu klonlayın:
```bash
git clone github.com/byigitt/web-scraper-test.git
```

2. Gereksinimleri yükleyin:
```bash
pip install -r requirements.txt
```

3. `config.json` dosyasını inceleyin ve gerekirse yapılandırma ayarlarını düzenleyin:
```json
{
  "base_url": "https://www.supplementler.com"
}
```

## Kullanım

Ana dosyayı çalıştırarak scraping işlemini başlatabilirsiniz:
```bash
python main.py
```

## Çıktı

Ürün bilgileri, site URL'lerine göre `data` klasöründe CSV ve JSON dosyalarına kaydedilecektir.
Dinamik olarak kategoriye göre oluşturulmuş dosyalar bulunacaktır.

## Lisans

Bu proje MIT lisansı ile lisanslanmıştır. Daha fazla bilgi için `license` dosyasına bakın.