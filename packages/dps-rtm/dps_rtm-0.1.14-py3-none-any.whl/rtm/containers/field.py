# --- Standard Library Imports ------------------------------------------------
import abc
from typing import List

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import rtm.main.context_managers as context
import rtm.validate.validation as val
from rtm.containers.worksheet_columns import get_matching_worksheet_columns
from rtm.validate import validator_output



class Field():

    def __init__(self, name):

        self._name = name

        # --- Get matching columns --------------------------------------------
        matching_worksheet_columns = get_matching_worksheet_columns(
            context.worksheet_columns.get(),
            self.get_name()
        )

        # --- Set Defaults ----------------------------------------------------
        self._indices = None  # Used in later check of relative column position
        self._body = None  # column data
        self._correct_position = None  # Checked during the Validation step
        self._val_results = None

        # --- Override defaults if matches are found --------------------------
        if len(matching_worksheet_columns) >= 1:
            # Get all matching indices (used for checking duplicate data and proper sorting)
            self._indices = [col.index for col in matching_worksheet_columns]
            # Get first matching column data (any duplicate columns are ignored; user rcv warning)
            self._body = matching_worksheet_columns[0].body

    def validate(self) -> None:

        # --- Was the field found? --------------------------------------------
        field_found = self.field_found()

        # --- Generate the minimum output message -----------------------------
        self._val_results = [
            validator_output.OutputHeader(self.get_name()),  # Start with header
            val.val_column_exist(field_found),
        ]

        # --- Perform remaining validation if the field was found -------------
        if field_found:
            self._val_results.append(val.val_column_sort(self))
            self._val_results += self._validation_specific_to_this_field()

    def _validation_specific_to_this_field(self) -> List[validator_output.ValidatorOutput]:
        return validator_output.example_val_results()

    def print(self):
        for result in self._val_results:
            result.print()

    def field_found(self):
        if self._body is None:
            return False
        return True

    def get_index(self):
        return self._indices[0]

    def get_body(self):
        return self._body

    def get_name(self):
        return self._name

    def get_min_index_for_field_right(self):
        return self.get_index()

    def __str__(self):
        return self.__class__, self.field_found()


if __name__ == "__main__":
    pass
