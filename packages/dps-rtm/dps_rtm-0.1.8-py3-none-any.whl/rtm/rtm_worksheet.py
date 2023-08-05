import click
from rtm.fields import Field, field_classes as fc
from typing import List
from rtm.worksheet_columns import get_worksheet_columns


class RTMWorksheet:

    # Initialize each field with its data
    def __init__(self, path):
        worksheet_columns = get_worksheet_columns(
            path, worksheet_name="Procedure Based Requirements"
        )
        self.fields = self._initialize_fields(fc, worksheet_columns)

    @staticmethod
    def _initialize_fields(field_classes, worksheet_columns) -> List[Field]:
        """Get list of field objects that each contain their portion of the worksheet_columns"""
        fields = []
        with click.progressbar(field_classes) as bar:
            #     fc.append(field(worksheet_columns))
            # return
            for field in bar:
                fields.append(field(worksheet_columns))
            # fields = [field(worksheet_columns) for field in bar]
        return fields

    def validate(self):
        # --- Check Field Sorting ---------------------------------------------
        index_current = -1
        for field in self.fields:
            index_current = field.validate_position(index_current)

        # --- Validate Fields and Print Results -------------------------------
        for field in self.fields:
            field.validate()


if __name__ == "__main__":
    pass
