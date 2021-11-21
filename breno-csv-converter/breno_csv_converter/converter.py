import logging
import click
from pathlib import Path

logging.basicConfig(
    level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
)

logger = logging.getLogger(__name__)
input_path = Path("./input/")
output_path = Path("./output/")


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
        if file.suffix == ".json":
            data = read_json_file(source)
            save_csv_file(data, file.name)
        elif file.suffix == ".csv":
            data = read_csv_file(source, delimiter)
            save_json_file(data, file.name)


def read_csv_file(source: Path, delimiter: str) -> tuple:
    return_list = list()

    with open(source, "r") as file:
        rows = [row.split(delimiter) for row in file]
        fields = rows[0]
        data = rows[1:]

        for count, values in enumerate(data):
            aux = list()

            for i, field in enumerate(fields):
                aux.append((field.strip(), values[i].strip))

            return_list.append(aux)

    return return_list


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


def read_json_file(source: Path) -> tuple:
    logger.info("bla bla")


def save_csv_file(jsons: list, file_name: str):
    logger.info("bla bla")


def save_json_file(csv_list: list, file_name: str):
    for cont, data in enumerate(csv_list):
        new_file_name = output_path.joinpath(file_name.split(".")[0] + ".json")
        logger.info("Saving json file: %s", new_file_name)

        with open(new_file_name, "w") as file:
            file.write("[\n")

            for rows in data:
                tab = "".ljust(4, " ")
                begin = "{\n"
                file.write(f"{tab}{begin}")

                for row in rows:
                    file.write(format_json(row, (row != rows[-1])))

                if rows != data[-1]:
                    end = "},\n"
                else:
                    end = "}\n"

                file.write(f"{tab}{end}")

            file.write("]")


def format_json(row: tuple, has_comma: bool) -> str:
    name, value = row

    tab = "".ljust(8, " ")
    end_line = "," if has_comma else ""

    if not value:
        return f'{tab}"{name}": null{end_line}\n'
    elif is_int(value):
        return f'{tab}"{name}": {int(value)}{end_line}\n'
    elif is_float(value):
        return f'{tab}"{name}": {float(value)}{end_line}\n'

    return f'{tab}"{name}": "{value}"{end_line}\n'
