import pytest
from rtm.fields import field_classes
from rtm.exceptions import RTMValidatorError


@pytest.mark.parametrize("field_class", field_classes)
@pytest.mark.parametrize("dups_count", [1, 2])
def test_init_with_good_data(worksheet_columns, field_class, dups_count):
    """Field should successfully initialize with two matching column"""
    field = field_class(worksheet_columns * dups_count)
    assert field.field_found()
    assert len(field._indices) == dups_count


@pytest.mark.parametrize("field_class", field_classes)
def test_init_without_matching_col(worksheet_columns, field_class):
    """Field should initialize to 'not found'"""
    name = field_class.get_field_name()
    ws_cols = [ws_col for ws_col in worksheet_columns if ws_col.header.lower() != name.lower()]
    field = field_class(ws_cols)
    assert not field.field_found()
    assert field._indices is None
    assert len(worksheet_columns) - len(ws_cols) == 1


@pytest.mark.parametrize("field_class", field_classes)
@pytest.mark.parametrize("not_worksheet_column", ['c', 1, ('a', 'b')])
def test_init_with_incorrect_data(not_worksheet_column, field_class):
    """Field and its subclasses should throw a builtin exception if
    passed something other than a sequence of WorksheetColumns"""
    error_occurred = False
    try:
        field = field_class(not_worksheet_column)
    except RTMValidatorError:
        # This shouldn't happen
        pass
    except:
        # A non-RTMValidatorError should occur
        error_occurred = True
    assert error_occurred
