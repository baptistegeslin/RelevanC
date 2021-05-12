import logging
import operator
from csv import reader, writer
from decimal import Decimal
from os import listdir
from pathlib import Path

from package.code.config import DELIMITER, ENCODING

logger = logging.getLogger()


def get_csv_reader(path_csv_file: Path) -> reader:
    try:
        return reader(
            open(path_csv_file, "r", newline="", encoding=ENCODING),
            delimiter=DELIMITER,
        )

    except FileNotFoundError as e:
        raise e

    except IOError as e:
        logger.exception(f"I/O error when reading {path_csv_file} file")
        raise e


def get_csv_writer(path_csv_file: Path, mode: str = "w") -> writer:
    try:
        return writer(
            open(path_csv_file, mode, newline="", encoding=ENCODING),
            delimiter=DELIMITER,
        )

    except IOError as e:
        logger.exception(f"I/O error when writing {path_csv_file} file")
        raise e


def create_folder(path: Path):
    try:
        path.mkdir(exist_ok=True, parents=True)
    except Exception as e:
        logger.exception(e)
        raise e


def read_csv(
    path_csv_file: Path, store: str = None
) -> dict:

    csv_content = {}
    reader = get_csv_reader(path_csv_file)
    for line in reader:
        if store:
            csv_content[line[1]] = Decimal(line[2])
        else:
            csv_content[line[0]] = Decimal(line[1])
    return csv_content


def write_csv(
    path_csv_file: Path, content: dict, store: str
):
    writer = get_csv_writer(path_csv_file)

    for key, value in content.items():
        if store:
            writer.writerow([store, key, value])
        else:
            writer.writerow([key, value])


def get_highest_values_from_all_records(content: dict, number_of_records: int):
    return dict(
        sorted(content.items(), key=operator.itemgetter(1), reverse=True)[
            :number_of_records
        ]
    )


def update_intermediate_csv_file_with_batch(
    csv_path: Path,
    batch_content: dict,
    store: str = None,
):
    try:
        content_from_existing_csv = read_csv(csv_path, store)
    except FileNotFoundError as e:
        content_from_existing_csv = {}

    for key, value in batch_content.items():
        content_from_existing_csv[key] = content_from_existing_csv.get(key, 0) + value

    write_csv(csv_path, content_from_existing_csv, store)


def write_final_results(
    file_path: Path,
    number_of_record: int,
    store: str = None,
):
    content = read_csv(file_path, store)

    final_result = get_highest_values_from_all_records(content, number_of_record)

    write_csv(file_path, final_result, store)


def get_csv_filenames(path: Path(), suffix=".csv"):
    return [filename for filename in listdir(path) if filename.endswith(suffix)]
