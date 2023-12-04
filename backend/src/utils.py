import os
import pinecone
import openai
import uuid
import json
from itertools import islice
from openai import OpenAI
client = OpenAI()
# from openai.embeddings_utils import get_embedding


# openai.api_key = os.getenv("OPENAI_API_KEY")
embedding_model = "text-embedding-ada-002"
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV"))

def embedding(sentences):
    # if isinstance(sentences, str):
    #     return client.embeddings.create(input=sentences, model=embedding_model)["data"][0]["embedding"] #get_embedding(sentences, engine=embedding_model)
    # elif isinstance(sentences, list):
    #     result = []
    #     for sentence in sentences:
    #         result.append(client.embedding.create(input=sentence, model=embedding_model)["data"][0]["embedding"])
    #     return result
    return client.embeddings.create(input=sentences, model=embedding_model).data[0].embedding
    
def upsert_pinecone(index, data, batch_size=10):
    item_ids = []
    embeddings = []
    metadata = []

    size = 0
    for record in data:
        embeddings.append(record["embedding"])
        item_ids.append(str(uuid.uuid4()))
        metadata.append(record["metadata"])
        
        if size >= batch_size:
            upsert_results = index.upsert(vectors=zip(item_ids, embeddings, metadata))
            item_ids = []
            embeddings = []
            metadata = []
            size = 0
        size += 1

    records = zip(item_ids, embeddings, metadata)
    upsert_results = index.upsert(vectors=records)
    return upsert_results



# def chunked_iterable(iterable, size):
#     """Helper function that yields chunks of the iterable."""
#     it = iter(iterable)
#     for first in it:
#         yield [first] + list(islice(it, size - 1))

# def upsert_pinecone(index, data, batch_size=10):
#     def upsert_batch(batch_data):
#         item_ids = [str(uuid.uuid4()) for _ in batch_data]
#         embeddings = [record["embedding"] for record in batch_data]
#         metadata = [record["metadata"] for record in batch_data]

#         records = zip(item_ids, embeddings, metadata)
#         upsert_results = index.upsert(vectors=list(records))
#         return upsert_results

#     all_results = []
#     for batch in chunked_iterable(data, size=batch_size):
#         upsert_results = upsert_batch(batch)
#         all_results.append(upsert_results)

#     return all_results

# Usage example:
# upsert_pinecone(index, data)

def read_data(fpath):
    with open(fpath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    keys = list(data.keys())
    values = list(data.values())
    
    new_data = []
    for i in range(len(data)):
        new_data.append({
            'metadata': {'question': keys[i], 'answer': values[i]},
            'text': keys[i] + values[i],
            'embedding': embedding(keys[i] + '\n' + values[i])
        })
    
    return new_data

