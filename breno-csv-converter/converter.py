import logging
import click
from pathlib import Path

logging.basicConfig(
    level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
)

logger = logging.getLogger(__name__)
input_path = Path("input/")
output_path = Path("output/")


@click.command()
@click.option(
    "--delimiter",
    "-d",
    default=",",
    help="Char used to separate fields.",
    type=str
)
def converter(delimiter):
    logger.info("Input Path: %s", input_path)
    logger.info("Output Path: %s", output_path)

    convert_files(input_path, delimiter)


def convert_files(source: Path, delimiter: str = ","):
    """ Read all files in the source path, convert and save them in the output path
    :param source:
    :param delimiter:
    :return:
    """
    logger.info("Reading all files from the path %s:", source)
    data = list()
    for file in source.iterdir():
        logger.info("Reading file: %s", file.name)

        if file.suffix == ".json":
            data = read_json_file(file)
            save_csv_file(data, file.name, delimiter)
        elif file.suffix == ".csv":
            data = read_csv_file(file, delimiter)
            save_json_file(data, file.name)


def read_csv_file(file: Path, delimiter: str) -> tuple:
    with open(file, "r") as file:
        rows = [row.rstrip('\n').split(delimiter) for row in file]
        csv_data = {key: list() for key in rows[0]}
        data_rows = rows[1:]

        for data in data_rows:
            for i, field in enumerate(csv_data.keys()):
                csv_data[field].append(data[i].strip())

    return csv_data


def read_json_file(file: Path) -> dict:
    with open(file, "r") as file:
        rows = [row.strip().rstrip('\n}[],').split("{") for row in file]
        json_data = dict()

        for row in rows:
            if row[0] == '':
                continue
            field, value = row[0].split(":")
            field = field.replace("'", "").replace('"', "")
            value = value.strip().replace("'", "").replace('"', "")

            if not json_data.get(field):
                json_data[field] = [value]
            else:
                json_data[field].append(value)
    
    return json_data


def is_float(value: str) -> bool:
    try:
        a = float(value)
    except (TypeError, ValueError):
        return False
    else:
        return True


def is_int(value: str) -> bool:
    try:
        a = float(value)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b


def save_csv_file(json_data_dict: dict, file_name: str, delimiter: str):
    new_file_name = output_path.joinpath(file_name.split(".")[0] + ".csv")
    logger.info("Saving csv file: %s", new_file_name)

    with open(new_file_name, "w") as file:
        fields_row = ""
        
        for i, field in enumerate(json_data_dict.keys()):
            if i == 0:
                fields_row += field
            else:
                fields_row += delimiter + field
        file.write(fields_row+'\n')

        json_data = list(json_data_dict.values())
        objects_count = len(json_data[0])
        object_index = 0
        while objects_count > object_index:
            object_row = ''
            for i in range(objects_count):
                if i == 0:
                    object_row += json_data[i][object_index]
                else:
                    object_row += delimiter + json_data[i][object_index]
            file.write(object_row+'\n')
            object_index += 1

        



def save_json_file(csv_data_dict: dict, file_name: str):
    new_file_name = output_path.joinpath(file_name.split(".")[0] + ".json")
    logger.info("Saving json file: %s", new_file_name)
    
    with open(new_file_name, "w") as file:
        tab = "".ljust(4, " ")
        begin = "{\n"
        array_begin = "[\n"
        file.write(f"{begin}")
        file.write(f"{tab}{array_begin}")

        csv_data = list(csv_data_dict.values())
        objects_count = len(csv_data[0])
        object_index = 0
        while objects_count > 0:
            file.write(f"{tab}{tab}{begin}")
            for i, field in enumerate(csv_data_dict.keys()):
                file.write(format_json((field, csv_data[i][object_index]), (csv_data[i][object_index] != csv_data[i][-1])))

            if objects_count > 1:
                end = "},\n"
            else:
                end = "}\n"

            file.write(f"{tab}{tab}{end}")
            object_index += 1
            objects_count -= 1

        file.write(f"{tab}]\n")
        file.write("}")


def format_json(row: tuple, has_comma: bool) -> str:
    field, value = row

    tab = "".ljust(12, " ")
    end_line = "," if has_comma else ""

    if not value:
        return f'{tab}"{field}": null{end_line}\n'
    elif is_int(value):
        return f'{tab}"{field}": {int(value)}{end_line}\n'
    elif is_float(value):
        return f'{tab}"{field}": {float(value)}{end_line}\n'

    return f'{tab}"{field}": "{value}"{end_line}\n'
