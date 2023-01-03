from load_rls_training import (
    difference_between_arrays,
    op_code_species_groups_with_more_than_one_count
)

def main(bruv_data_frames):
    errors = {
        "MaxN has OpCode(s) which aren't in Site" : difference_between_arrays(
            bruv_data_frames.max_n.get('OpCode').unique(),
            bruv_data_frames.site.get('OpCode').unique()
        ),
        "Site has OpCode(s) which aren't in MaxN" : difference_between_arrays(
            bruv_data_frames.site.get('OpCode').unique(),
            bruv_data_frames.max_n.get('OpCode').unique(),
        ),
        "Site has OpCode(s) which aren't in Length" : difference_between_arrays(
            bruv_data_frames.site.get('OpCode').unique(),
            bruv_data_frames.length.get('OpCode').unique(),
        ),
        "Length has OpCode(s) which aren't in Site" : difference_between_arrays(
            bruv_data_frames.length.get('OpCode').unique(),
            bruv_data_frames.site.get('OpCode').unique()
        ),
        "OpCode(s) have species with more than one count" : op_code_species_groups_with_more_than_one_count(
            bruv_data_frames.max_n
        ),
    }
    result = []
    for error_type in errors.keys():
        result.append(error_type)
        result.append('\n'.join(errors[error_type]))
        result.append('\n')
    return '\n'.join(result)


if __name__ == "__main__":
    from load_rls_training import BRUVDataFramesFromExcelFile
    print(main(bruv_data_frames = BRUVDataFramesFromExcelFile('data/BRUVchecker_Test.xlsx')))