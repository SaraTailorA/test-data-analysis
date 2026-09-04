import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd 
import numpy as np 
from sqlalchemy import URL, create_engine, text
from sqlalchemy.exc import OperationalError
load_dotenv(Path(__file__).resolve().parent.parent / "data" / ".env", override=True)

df = pd.read_csv("data/e-commerceSales.csv")

print(df.columns)

df.info()

print("Duplicados:", df.duplicated().sum())

print(df.isnull().sum())

#I've verified null values in all columns of the dataset. Didn't found values missing, so that, was not neccesary to apply treatment of imputation or remove any register.

#print(df.dtypes)

df["order_date"] = pd.to_datetime(df["order_date"])

print(df.dtypes)

#The column names were reviewed and found to be already normalized in snake_case format, so no modifications were necessary.

df["order_year"] = df["order_date"].dt.year

df["order_month"] = df["order_date"].dt.month

print(df[["order_date", "order_year", "order_month"]].head())

#validation
print(df[[
    "quantity",
    "unit_price",
    "discount",
    "delivery_days",
    "customer_rating",
    "revenue"
]].describe())

print((df["quantity"] <= 0).sum())

print((df["unit_price"] <= 0).sum())

print(((df["discount"] < 0) | (df["discount"] > 1)).sum())

print((df["delivery_days"] <= 0).sum())

print(((df["customer_rating"] < 1) | (df["customer_rating"] > 5)).sum())

print((df["revenue"] <= 0).sum())

#star

#dim_date
dim_date = df[["order_date", "order_year", "order_month"]].copy()
print(dim_date.head())

dim_date = dim_date.drop_duplicates()

print(dim_date.shape)

dim_date = dim_date.reset_index(drop=True)

dim_date["date_id"] = dim_date.index + 1

dim_date = dim_date[[
    "date_id",
    "order_date",
    "order_year",
    "order_month"
]]

print(dim_date.head())

#dim_product
dim_product = df[["product_category"]].copy()

print(dim_product.head())
print(dim_product.shape)

dim_product = dim_product.drop_duplicates()

print(dim_product)
print(dim_product.shape)

dim_product = dim_product.reset_index(drop=True)
dim_product["product_category_id"] = dim_product.index + 1
dim_product = dim_product[["product_category_id", "product_category"]]
print(dim_product)


#dim_region
dim_region = df[["region"]].copy()

dim_region = dim_region.drop_duplicates()
print(dim_region)
print(dim_region.shape)

#region_id
dim_region = dim_region.reset_index(drop=True)
dim_region["region_id"] = dim_region.index + 1
dim_region = dim_region[["region_id", "region"]]
print(dim_region)

#dim_payment_method
dim_payment_method = df[["payment_method"]].copy()

dim_payment_method = dim_payment_method.drop_duplicates()

print(dim_payment_method)
print(dim_payment_method.shape)

#payment_id
dim_payment_method = dim_payment_method.reset_index(drop=True)

dim_payment_method["payment_method_id"] = dim_payment_method.index + 1

dim_payment_method = dim_payment_method[["payment_method_id", "payment_method"]]

print(dim_payment_method)

#fact_sales
fact_sales = df.copy()

print(fact_sales.head())
print(fact_sales.shape)

fact_sales = fact_sales.merge(
    dim_date[["date_id", "order_date"]],
    on="order_date",
    how="left"
)

print(fact_sales.head())
print(fact_sales.shape)

fact_sales = fact_sales.merge(
    dim_product[["product_category_id", "product_category"]],
    on="product_category",
    how="left"
)

print(fact_sales.head())
print(fact_sales.shape)

fact_sales = fact_sales.merge(
    dim_region[["region_id", "region"]],
    on="region",
    how="left"
)

print(fact_sales.head())
print(fact_sales.shape)

fact_sales = fact_sales.merge(
    dim_payment_method[["payment_method_id", "payment_method"]],
    on="payment_method",
    how="left"
)

print(fact_sales.head())
print(fact_sales.shape)

fact_sales = fact_sales[
    [
        "order_id",
        "customer_id",
        "date_id",
        "product_category_id",
        "region_id",
        "payment_method_id",
        "quantity",
        "unit_price",
        "discount",
        "delivery_days",
        "customer_rating",
        "revenue"
    ]
]

print(fact_sales.head())
print(fact_sales.shape)

print("Null in fact_sales:")
print(fact_sales.isnull().sum())

print("Row in fact_sales:", len(fact_sales))
print("Duplicate:", fact_sales.duplicated().sum())


# connect Python with PostgreSQL
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

missing_settings = [
    name for name, value in {
        "DB_USER": USER,
        "DB_PASSWORD": PASSWORD,
        "DB_NAME": DB_NAME,
    }.items() if not value
]

try:
    if missing_settings:
        print(f"Error: faltan variables de entorno: {', '.join(missing_settings)}")
    else:
        try:
            port_number = int(PORT)
        except ValueError:
            print(f"Error: DB_PORT debe ser un número válido, recibido: {PORT}\n")
        else:
            DATABASE_URL = URL.create(
                drivername="postgresql+psycopg2",
                username=USER,
                password=PASSWORD,
                host=HOST,
                port=port_number,
                database=DB_NAME,
            )
            engine = create_engine(DATABASE_URL)
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print(f"Conexión exitosa a '{DB_NAME}' en {HOST}:{PORT}\n")
except OperationalError as e:
    print(f"Error de credenciales o conexión a PostgreSQL: {e}\n")
except UnicodeDecodeError:
    print("Error de conexión: PostgreSQL devolvió una respuesta con codificación inválida. "
          "Verifica el servidor y las credenciales.\n")
except Exception as e:
    print(f"Error inesperado: {e}\n")


# export table to sql
dim_date.to_sql(
    "dim_date",
    engine,
    if_exists="replace",
    index=False
)

print("dim_date loaded correctly")

dim_product.to_sql(
    "dim_product",
    engine,
    if_exists="replace",
    index=False
)

print("dim_product loaded correctly")

dim_region.to_sql(
    "dim_region",
    engine,
    if_exists="replace",
    index=False
)

print("dim_region loaded correctly")


dim_payment_method.to_sql(
    "dim_payment_method",
    engine,
    if_exists="replace",
    index=False
)

print("dim_payment_method loaded correctly")


fact_sales.to_sql(
    "fact_sales",
    engine,
    if_exists="replace",
    index=False
)

print("fact_sales loaded correctly")