from src.utils import embedding
from src.mysql import clean_html

def process_product_record(record):
    description = clean_html(record['description'])
    text = f"""
Product Name: {record['product_name']}

Product Code: {record['model']}
Category: {record['category_name']}
Price: {record['price']}
Keywords: {record['meta_keyword']}
Stock Status: {record['stock_status']}
Manufacturer: {record['manufacturer_name']}

Attribute:
{record['combined_attribute_text']}


Description:
{description}
"""
    if not record['product_image']:
        record['product_image'] = ""
    if not record['manufacturer_image']:
        record['manufacturer_image'] = ""
    if not record['category_image']:
        record['category_image'] = ""
    if not record['download_ids']:
        record['download_ids'] = ""
    metadata = {
        'image': record['product_image'],
        'manufacturer_image': record['manufacturer_image'],
        'category_image': record['category_image'],
        'download_ids': record['download_ids'],
        'text': text
    }
    return {
        'metadata': metadata,
        'embedding': embedding(text)
    }
