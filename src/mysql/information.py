from src.utils import embedding
from src.mysql import clean_html

def process_information_record(record):
    description = clean_html(record['description'])
    text = f"""
{record['title']}:
{description}
"""
    metadata = {
        'text': text
    }
    return {
        'metadata': metadata,
        'embedding': embedding(text)
    }
