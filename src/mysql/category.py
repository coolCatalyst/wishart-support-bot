from src.utils import embedding

def process_category_record(record):
    text = f"""
Category Name: {record['name']}
Title: {record['meta_title']}
Keywords: {record['meta_keyword']}

Description:
{record['meta_description']}
"""
    metadata = {
        'image': record['image'],
        'text': text
    }
    return {
        'metadata': metadata,
        'embedding': embedding(text)
    }
