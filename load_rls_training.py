import pandas as pd
from pandas import DataFrame
from collections import namedtuple
from typing import NamedTuple, Dict, List


def BRUVDataFramesFromExcelFile(
    file,
    BRUVDataFrames: NamedTuple = namedtuple(
        "BRUVDataFrames",
        "max_n length site"
        )
    ):
    """Reads tabs from excel file into dataframe structure
    specified by BRUVDataFrames
    """
    excel_file = pd.ExcelFile(file)
    return BRUVDataFrames(
        excel_file.parse('MaxN'),
        excel_file.parse('Length'),
        excel_file.parse('Site'),
    )


def make_errors_have_same_length(errors: Dict) -> Dict:
    """Errors are represented as a dictionary, with 
    key: error type
    value: list of errors (eg. OpCodes)
    To convert these errors to a dataframe, and save it to a csv,
    each of these lists need to be of equal length.
    """
    largest_number_of_errors = 0
    result = {}
    for error_list in errors.values():
        if len(error_list) > largest_number_of_errors:
            largest_number_of_errors = len(error_list)

    for error_name, error_list  in errors.items():
        result[error_name] = error_list + (
            [None] * (largest_number_of_errors - len(error_list))
        )
    return result


def save_errors_to_csv(errors: Dict, running_locally = False):
    errors_to_save = make_errors_have_same_length(errors)

    # Convert dictionary to dataframe and download it
    pd.DataFrame.from_dict(errors_to_save).to_csv('errors.csv', index=False)
    if running_locally:
        return

    files.download('errors.csv')


def difference_between_arrays(array_1, array_2):
    return list(set(array_1) - set(array_2))


def op_code_species_groups_with_more_than_one_count(bruv_dataframe: DataFrame) -> List[str]:
    columns_to_group_by = ['OpCode','Family','Genus','Species']
    op_code_species_counts = bruv_dataframe.groupby(
        columns_to_group_by
    ).size()

    errors = []
    group_message = lambda group: ' - '.join([f"{col}: {val}" for col, val in zip(columns_to_group_by, group)])

    for group, count in dict(op_code_species_counts).items():
        if count > 1:
            errors.append(
                f"Count: {count} - {group_message(group)}"
            )

    return errors
