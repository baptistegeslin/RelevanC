import os
from pathlib import Path

BATCH_SIZE = 20_000_000
ENCODING = "utf-8"
RANDOMIZED_TRANSACTIONS_FILE_NAME = "randomized-transactions-202009.psv"
DELIMITER = "|"
TOP_50_STORES_CSV_NAME = "top-50-stores.csv"
TOP_100_PRODUCTS_STORE_CSV_NAME = "top-100-products-store-{}.csv"
TOP_100_PRODUCTS_STORE_FOLDER_NAME = "top-products-by-store"
RESULTS_FOLDER_NAME = "results"
CURRENT_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
