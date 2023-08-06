"""
Unit tests for validation.py functions
"""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
import rtm.containers.worksheet_columns as wc
import rtm.validate.validation as val
import rtm.main.context_managers as context
from rtm.containers.fields import Fields
from rtm.containers.work_items import WorkItems


def test_column_exist(capsys):
    io = [
        (True, f'\tPass\tFIELD EXIST\n'),
        (False, f'\tError\tFIELD EXIST - Field not found\n')
    ]
    for item in io:
        result = val.val_column_exist(item[0])
        result.print()
        captured = capsys.readouterr()
        assert captured.out == item[1]


@pytest.mark.parametrize('reverse', [False, True])
def test_column_sort(fix_fields, reverse):

    fields = fix_fields("Procedure Based Requirements")
    scores_should = ['Pass'] * len(fields)

    if reverse:
        fields = list(reversed(fields))
        scores_should = ['Pass'] + ['Error'] * (len(fields) - 1)

    with context.fields.set(fields):
        scores_actual = [
            val.val_column_sort(field)._score
            for field
            in fields
        ]

    assert len(scores_actual) > 0
    assert scores_actual == scores_should


def test_cells_not_empty():
    passing_values = [True, False, 'hello', 42]
    failing_values = [None, '']
    values = failing_values + passing_values

    failing_indices = tuple(range(len(failing_values)))
    results = val.val_cells_not_empty(values)
    assert results.indices == failing_indices


cascade_validations = [
    (val.val_cascade_block_only_one_entry, 'one_entry'),
    (val.val_cascade_block_x_or_f, 'x_or_f'),
]  # (validation_function, worksheet_col with expected values)


@pytest.mark.parametrize('cascade_validation', cascade_validations)
def test_val_cascade_block_only_one_entry(fix_worksheet_columns, cascade_validation):

    # Setup
    ws_cols = fix_worksheet_columns("work_items")
    with context.worksheet_columns.set(ws_cols):
        fields = Fields()
    with context.fields.set(fields):
        work_items = WorkItems()

    # Expected result
    col_with_expected_results = cascade_validation[1]
    indices_expected_to_fail = [
        index for
        index, value in
        enumerate(ws_cols.get_first(col_with_expected_results).body)
        if not value
    ]

    # Compare
    val_func = cascade_validation[0]
    indices_that_actually_fail = list(val_func(work_items).indices)
    assert indices_that_actually_fail == indices_expected_to_fail


def test_val_cascade_block_use_all_levels(fix_worksheet_columns):

    # Setup
    ws_cols = fix_worksheet_columns("work_items")
    with context.worksheet_columns.set(ws_cols):
        fields = Fields()
    with context.fields.set(fields):
        work_items = WorkItems()

    with context.fields.set(fields), context.work_items.set(work_items):
        assert val.val_cascade_block_use_all_columns()._score == 'Warning'


if __name__ == "__main__":
    pass
