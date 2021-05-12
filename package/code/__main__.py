import logging
import re
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from package.code.config import (BATCH_SIZE, CURRENT_PATH,
                                 RANDOMIZED_TRANSACTIONS_FILE_NAME,
                                 RESULTS_FOLDER_NAME, TOP_50_STORES_CSV_NAME,
                                 TOP_100_PRODUCTS_STORE_CSV_NAME,
                                 TOP_100_PRODUCTS_STORE_FOLDER_NAME)
from package.code.utils import (create_folder, get_csv_filenames,
                                get_csv_reader,
                                get_highest_values_from_all_records, read_csv,
                                update_intermediate_csv_file_with_batch,
                                write_csv, write_final_results)

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()


def process_batch(sales_by_store_batch: dict, product_by_store_batch: dict):
    update_intermediate_csv_file_with_batch(
        csv_path= CURRENT_PATH.parents[1] / RESULTS_FOLDER_NAME / TOP_50_STORES_CSV_NAME,
        batch_content= sales_by_store_batch,
    )
    for store, products in product_by_store_batch.items():
        update_intermediate_csv_file_with_batch(
            csv_path= CURRENT_PATH.parents[1]
            / RESULTS_FOLDER_NAME
            / TOP_100_PRODUCTS_STORE_FOLDER_NAME
            / TOP_100_PRODUCTS_STORE_CSV_NAME.format(store),
            batch_content= products,
            store= store,
        )


def process_randomized_transations_csv(
    csv_path: str, batch_size: int
):
    sales_by_store_batch = {}
    product_by_store_batch = defaultdict(dict)

    reader = get_csv_reader(csv_path)
    next(reader, None)  # skip header

    for count, row in enumerate(reader, 1):
        sales_by_store_batch[row[3]] = Decimal( sales_by_store_batch.get(row[3], 0)) + Decimal(row[5])  
        # eg. {25001: 55.25, 87666: 10.2}
        
        product_by_store_batch[row[3]][row[2]] = (product_by_store_batch.get(row[3], {}).get(row[2], 0) + 1)  
        # eg. {25001: {8C7008317E: 25, B75F7C0E1C: 18}, 87666: {B75F7C0E1C: 10}}

        if count % batch_size == 0:
            
            process_batch(sales_by_store_batch, product_by_store_batch)
            sales_by_store_batch.clear()
            product_by_store_batch.clear()

            logger.info(f"{count:_} rows processed")

    # Process last incomplete batch
    process_batch(sales_by_store_batch, product_by_store_batch)

    # Get top50 stores and top100 products by store
    write_final_results(
        file_path= CURRENT_PATH.parents[1] / RESULTS_FOLDER_NAME / TOP_50_STORES_CSV_NAME,
        number_of_record= 50,
    )

    for csv_file in get_csv_filenames(
        path= CURRENT_PATH.parents[1]
        / RESULTS_FOLDER_NAME
        / TOP_100_PRODUCTS_STORE_FOLDER_NAME
    ):
        write_final_results(
            file_path= CURRENT_PATH.parents[1]
            / RESULTS_FOLDER_NAME
            / TOP_100_PRODUCTS_STORE_FOLDER_NAME
            / csv_file,
            number_of_record= 100,
            store= re.search(TOP_100_PRODUCTS_STORE_CSV_NAME.format("(.*)"), csv_file).group(1),
        )


if __name__ == "__main__":

    create_folder(
        path= CURRENT_PATH.parents[1]
        / RESULTS_FOLDER_NAME
        / TOP_100_PRODUCTS_STORE_FOLDER_NAME
    )

    process_randomized_transations_csv(
        csv_path= CURRENT_PATH.parents[1] / RANDOMIZED_TRANSACTIONS_FILE_NAME,
        batch_size= BATCH_SIZE,
    )
