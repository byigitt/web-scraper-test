import csv
import json
import os

def write_to_csv(data, folder_path, filename):
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)
    
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=['Ürün İsmi', 'Fiyat', 'Puan', 'Ürün Resmi'])
        writer.writeheader()
        writer.writerows(data)

def write_to_json(data, folder_path, filename):
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)
    
    with open(file_path, 'w', encoding='utf-8-sig') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def append_to_master_files(data, csv_filename, json_filename):
    file_exists = os.path.isfile(csv_filename)
    
    with open(csv_filename, 'a', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=['Ürün İsmi', 'Fiyat', 'Puan', 'Ürün Resmi'])
        if not file_exists:
            writer.writeheader()
        
        writer.writerows(data)
    
    if os.path.exists(json_filename):
        with open(json_filename, 'r', encoding='utf-8-sig') as file:
            existing_data = json.load(file)
            data = existing_data + data

    with open(json_filename, 'w', encoding='utf-8-sig') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
