import os
import dotenv
import pandas as pd
import mysql.connector

dotenv.load_dotenv()
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
    FROM
        new_category nc
    JOIN
        new_category_description ncd
    ON
        nc.category_id = ncd.category_id;
"""

# Fetch all rows using the fetchall() method
df_dictionary['category'] = pd.read_sql(category_sql_query, conn)

information_sql_query = """
    SELECT
        *
    FROM
        new_information ni
    JOIN
        new_information_description nid
    ON
        ni.information_id = nid.information_id;
"""
df_dictionary['information'] = pd.read_sql(information_sql_query, conn)


manufacturer_sql_query = """
    SELECT
        *
    FROM
        new_manufacturer nm
    JOIN
        new_manufacturer_description nmd
    ON
        nm.manufacturer_id = nmd.manufacturer_id;
"""
df_dictionary['manufacturer'] = pd.read_sql(manufacturer_sql_query, conn)

attribute_sql_query = """
    SELECT
        attribute_id,
        t1.name as attribute_name,
        new_attribute_group_description.name as attribute_group_name,
        sort_order
    FROM
        (
            SELECT
                new_attribute.attribute_id as attribute_id,
                attribute_group_id,
                sort_order,
                new_attribute_description.name as name
            from new_attribute
                left outer join new_attribute_description
                    on new_attribute.attribute_id = new_attribute_description.attribute_id
        ) t1 left outer join new_attribute_group_description
            on t1.attribute_group_id = new_attribute_group_description.attribute_group_id
"""

df_dictionary['attribute'] = pd.read_sql(attribute_sql_query, conn)
product_sql_query = """
    select
        new_product.product_id as product_id,
        model,
        mpn,
        location,
        new_product.image as product_image
        price,
        date_available,
        viewed,
        date_added,
        new_product_description.name as product_name,
        new_product_description.description as description,
        new_product_description.meta_title as meta_title,
        new_product_description.meta_description as meta_description,
        new_product_description.meta_keyword as meta_keyword,
        new_product_description.meta_h1 as meta_h1,
        new_stock_status.name as stock_status,
        new_manufacturer.name as manufacturer_name,
        new_manufacturer.image as manufacturer_image
    from new_product
    left outer join new_product_description
        on new_product.product_id = new_product_description.product_id
    left outer join new_stock_status
        on new_product.stock_status_id = new_stock_status.stock_status_id
    left outer join new_manufacturer
        on new_product.manufacturer_id = new_manufacturer.manufacturer_id;
"""
df_dictionary['product'] = pd.read_sql(product_sql_query, conn)

