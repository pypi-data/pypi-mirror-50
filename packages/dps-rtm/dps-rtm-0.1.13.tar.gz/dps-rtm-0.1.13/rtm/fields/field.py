import rtm.fields.validation as val
from rtm.fields.validation_results import print_validation_report
from typing import List
from rtm.worksheet_columns import get_matching_worksheet_columns


class Field:

    field_name = None

    def __init__(self, all_worksheet_columns):

        # --- Get All Matching Columns ----------------------------------------
        # matching_worksheet_columns = [
        #     (index, ws_col)
        #     for index, ws_col in enumerate(all_worksheet_columns)
        #     if ws_col.header.lower() == self.get_field_name().lower()
        # ]
        matching_worksheet_columns = get_matching_worksheet_columns(all_worksheet_columns, self.get_field_name())

        # --- Set Defaults ----------------------------------------------------
        self._indices = None  # Used in later check of relative column position
        self._body = None  # column data
        self._correct_position = None

        # --- Override defaults if matches are found --------------------------
        if len(matching_worksheet_columns) >= 1:
            # indices, worksheet_columns = zip(*matching_worksheet_columns)
            # Get all matching indices (used for checking duplicate data and proper sorting)
            self._indices = [col.index for col in matching_worksheet_columns]
            # Get first matching column data (any duplicate columns are ignored; user rcv warning)
            self._body = matching_worksheet_columns[0].body

    def validate(self) -> None:
        """Called by RTMWorksheet object to val-check and report out on field."""
        val_results = [val.val_column_exist(self.field_found())]
        if self.field_found():
            val_results.append(val.val_column_sort(self._correct_position))
            val_results += self._validate_this_field()
        print_validation_report(self.field_name, val_results)

    def _validate_this_field(self) -> List[dict]:
        return []

    def field_found(self):
        if self._body is None:
            return False
        return True

    def _get_index(self):
        return self._indices[0]

    def validate_position(self, previous_index):
        """Check that this field comes after the previous one. Return this column number."""
        if not self.field_found():
            return previous_index
        if self._get_index() > previous_index:
            self._correct_position = True
        else:
            self._correct_position = False
        return self._get_index()

    @classmethod
    def get_field_name(cls):
        return cls.field_name


if __name__ == "__main__":
    list = ['1']
    second = '2'
    third = ['3', '4']
    list.append(second)
    print(list)
    # list.append(third)
    print(list+third)
