import rtm.worksheet_columns as wc
import pytest
from rtm.fields.validation import cell_validation_functions


@pytest.mark.parametrize('val_func', cell_validation_functions)
def test_val_cell_functions(ws_cols_from_test_validation, val_func):
    # ws_cols = ws_cols_from_test_validation
    # header = val_cells_not_empty.__name__
    # try:
    #     ws_col: WorksheetColumn = get_first_matching_worksheet_column(ws_cols, header)
    # except IndexError:
    #     raise IndexError(f"The test_validation ws is likely missing a '{header}' column")
    # cells_to_be_tested = ws_col.body
    # val_result = val_cells_not_empty(cells_to_be_tested)
    # failed_indices = tuple(val_result.indices)
    # assert failed_indices == tuple(range(5))
    ws_cols = ws_cols_from_test_validation
    header = val_func.__name__
    try:
        ws_col: wc.WorksheetColumn = wc.get_first_matching_worksheet_column(ws_cols, header)
    except IndexError:
        # raise IndexError(f"The test_validation ws is likely missing a '{header}' column")
        assert False
    else:
        cells_to_be_tested = ws_col.body
        val_result = val_func(cells_to_be_tested)
        failed_indices = tuple(val_result.indices)
        assert failed_indices == tuple(range(5))


if __name__ == "__main__":
    print(cell_validation_functions)

