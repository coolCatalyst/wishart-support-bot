import pickle
import dotenv
dotenv.load_dotenv()

import os
import pandas as pd
import pinecone
import mysql.connector
from tqdm import tqdm

from src.mysql.information import process_information_record
from src.mysql.category import process_category_record
from src.mysql.product import process_product_record
from src.utils import upsert_pinecone


pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV"),
)
index_name = os.getenv("PINECONE_INDEX_NAME")
index = pinecone.Index(index_name)
# if index_name not in pinecone.list_indexes():
pinecone.delete_index(index_name)
pinecone.create_index(index_name, dimension=1536, metric="cosine")
    
# Replace the following variables with your own details
host = os.getenv("MYSQL_HOST")  # or the IP/hostname if the database is on a remote server
database = "ocdb_308"
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")

# Establish a connection to the database
conn = mysql.connector.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

df_dictionary = dict()

# Execute SQL query
category_sql_query = """
SELECT
    *
FROM new_category nc
JOIN new_category_description ncd
    ON nc.category_id = ncd.category_id;
"""

# Fetch all rows using the fetchall() method
df_dictionary['category'] = pd.read_sql(category_sql_query, conn)

information_sql_query = """
SELECT
    *
FROM new_information ni
JOIN new_information_description nid
    ON ni.information_id = nid.information_id;
"""
df_dictionary['information'] = pd.read_sql(information_sql_query, conn)

product_sql_query = """
SELECT
    new_product.product_id AS product_id,
    model,
    mpn,
    location,
    new_product.image AS product_image, -- Added comma here
    price,
    date_available,
    viewed,
    new_product.date_added AS data_added,
    new_product_description.name AS product_name,
    new_product_description.description AS description,
    new_product_description.meta_title AS meta_title,
    new_product_description.meta_description AS meta_description,
    new_product_description.meta_keyword AS meta_keyword,
    new_product_description.meta_h1 AS meta_h1,
    new_stock_status.name AS stock_status,
    new_manufacturer.name AS manufacturer_name,
    new_manufacturer.image AS manufacturer_image,
    new_category.image AS category_image,
    new_category_description.name AS category_name,
    GROUP_CONCAT(DISTINCT new_product_to_download.download_id) AS download_ids,
    GROUP_CONCAT(CONCAT(new_attribute_description.name, ':  ', new_product_attribute.text) SEPARATOR '\n') as combined_attribute_text,
    GROUP_CONCAT(DISTINCT new_attribute_group_description.name) AS attribute_group_names
FROM new_product
LEFT OUTER JOIN new_product_description
    ON new_product.product_id = new_product_description.product_id
LEFT OUTER JOIN new_stock_status
    ON new_product.stock_status_id = new_stock_status.stock_status_id
LEFT OUTER JOIN new_manufacturer
    ON new_product.manufacturer_id = new_manufacturer.manufacturer_id
LEFT OUTER JOIN new_product_to_category
    ON new_product.product_id = new_product_to_category.product_id
LEFT OUTER JOIN new_category
    ON new_product_to_category.category_id = new_category.category_id
LEFT OUTER JOIN new_category_description
    ON new_category.category_id = new_category_description.category_id
LEFT OUTER JOIN new_product_to_download
    ON new_product.product_id = new_product_to_download.product_id
LEFT OUTER JOIN new_product_attribute
    ON new_product.product_id = new_product_attribute.product_id
LEFT OUTER JOIN new_attribute
    ON new_product_attribute.attribute_id = new_attribute.attribute_id
LEFT OUTER JOIN new_attribute_description
    ON new_attribute.attribute_id = new_attribute_description.attribute_id
LEFT OUTER JOIN new_attribute_group_description
    ON new_attribute.attribute_group_id = new_attribute_group_description.attribute_group_id
GROUP BY new_product.product_id
"""
df_dictionary['product'] = pd.read_sql(product_sql_query, conn)

infos = []
for record in tqdm(df_dictionary['information'].iloc):
    infos.append(process_information_record(record))
upsert_pinecone(index, infos)

categories = []
for record in tqdm(df_dictionary['category'].iloc):
    categories.append(process_category_record(record))
upsert_pinecone(index, categories)

products = []
for record in tqdm(df_dictionary['product'].iloc):
    products.append(process_product_record(record))
    
pickle.dump(products, open('products.pkl', 'wb'))
print("Done!")

# with open('products.pkl', 'rb') as f:
#     products = pickle.load(f)

upsert_pinecone(index, products, batch_size=10)
