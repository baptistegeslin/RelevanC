from csv import reader, writer
from decimal import Decimal
from pathlib import Path

import pytest

from package.code.config import CURRENT_PATH
from package.code.utils import (get_csv_reader, get_csv_writer,
                                get_highest_values_from_all_records, read_csv,
                                update_intermediate_csv_file_with_batch)

sales_by_store_path = CURRENT_PATH.parents[0] / "test" / "sales-by-store.csv"
product_by_store_path = CURRENT_PATH.parents[0] / "test" / "product-by-store.csv"
sample = {
    "76094": Decimal("2638.74"),
    "38185": Decimal("27110.11"),
    "38963": Decimal("68307.54"),
    "06638": Decimal("61985.31"),
    "74339": Decimal("581644.11"),
    "85094": Decimal("12638.74"),
    "37585": Decimal("7110.11"),
    "38985": Decimal("8307.54"),
    "98538": Decimal("1985.31"),
    "74139": Decimal("5644.11"),
}


def test_get_csv_writer():
    # Given

    # When
    writer1 = get_csv_writer(sales_by_store_path, "a")
    writer2 = get_csv_writer(product_by_store_path, "a")

    # Then
    assert type(writer1).__name__ == writer.__name__
    assert type(writer2).__name__ == writer.__name__


def test_get_csv_reader():
    # Given

    # When
    reader1 = get_csv_reader(sales_by_store_path)
    reader2 = get_csv_reader(product_by_store_path)

    # Then
    assert type(reader1).__name__ == reader.__name__
    assert type(reader2).__name__ == reader.__name__


def test_read_csv():
    # Given
    sales_by_store = {}
    sales_by_store_result = {
        "76094": Decimal("2638.74"),
        "38185": Decimal("27110.11"),
        "38963": Decimal("68307.54"),
        "06638": Decimal("61985.31"),
        "74339": Decimal("581644.11"),
    }

    # When
    sales_by_store = read_csv(sales_by_store_path)

    # Then
    assert sales_by_store == sales_by_store_result


@pytest.mark.parametrize(
    "content,number_of_records,expected_results",
    [(sample, 2, {"74339": Decimal("581644.11"), "38963": Decimal("68307.54")}),
    (sample, 3, {"74339": Decimal("581644.11"), "38963": Decimal("68307.54"), "06638": Decimal("61985.31")})],
)
def test_get_highest_values_from_all_records(content, number_of_records, expected_results):
    # Given

    # When 
    result = get_highest_values_from_all_records(content= content, number_of_records= number_of_records)

    # Then 
    assert result == expected_results


def test_update_intermediate_csv_file_with_batch():
    #Given
    path = Path("not/existing/path")

    #When
    with pytest.raises(FileNotFoundError):
        update_intermediate_csv_file_with_batch(csv_path= path, batch_content= {})

