from typing import List
from rtm.fields import Field
from rtm.worksheet_columns import WorksheetColumn
import _rtm.fields.validation as val


class ID(Field):
    field_name = "ID"

    def _validate_this_field(self) -> List[WorksheetColumn]:
        results = [
            val.val_cells_not_empty(self._body),
        ]
        results += val.example_results()
        return results


class CascadeLevel(Field):
    field_name = "Cascade Level"

    def _validate_this_field(self) -> List[WorksheetColumn]:
        return val.example_results()


class ReqStatement(Field):
    field_name = "Requirement Statement"

    def _validate_this_field(self) -> List[WorksheetColumn]:
        return val.example_results()


class ReqRationale(Field):
    field_name = "Requirement Rationale"

    def _validate_this_field(self) -> List[WorksheetColumn]:
        return [val.val_cells_not_empty(self._body)]


class VVStrategy(Field):
    field_name = "Verification or Validation Strategy"

    def _validate_this_field(self) -> List[WorksheetColumn]:
        return val.example_results()


class VVResults(Field):
    field_name = "Verification or Validation Results"

    def _validate_this_field(self) -> List[WorksheetColumn]:
        return []

class DOFeatures(Field):
    field_name = "Design Output Feature (with CTQ ID #)"

    def _validate_this_field(self) -> List[WorksheetColumn]:
        return []

class CTQ(Field):
    field_name = "CTQ? Yes, No, N/A"

    def _validate_this_field(self) -> List[WorksheetColumn]:
        return []

class Devices(Field):

    field_name = "Devices"

    def _validate_this_field(self) -> List[WorksheetColumn]:
        return [val.val_cells_not_empty(self._body)]


if __name__ == "__main__":
    pass
