from _rtm.fields import Field


class CascadeBlock(Field):
    def __init__(self, all_worksheet_columns):

        # --- Get Matching Subfields; Stop after first Non-Found --------------
        self._subfields = []
        for subfield_name in self._get_subfield_names():
            subfield = CascadeSubfield(all_worksheet_columns, subfield_name)
            if subfield.field_found():
                self._subfields.append(subfield)
            else:
                break

        # --- Get All Matching Columns ----------------------------------------
        # --- Set Defaults ----------------------------------------------------
        # --- Override defaults if matches are found --------------------------
        pass

    @staticmethod
    def _get_subfield_names():
        field_names = ["Procedure Step", "User Need", "Design Input"]
        for i in range(1, 20):
            field_names.append("DO Solution L" + str(i))
        return field_names

    def validate_position(self, previous_index):
        """
        Check that first subfield comes after the previous one and that
        each subfield appears in order. Return column number of last subfield
        """

        # --- Check that subfields appear in order ----------------------------
        for subfield in self._subfields:
            previous_index = subfield.validate_position(previous_index)
        return previous_index


class CascadeSubfield(Field):
    def __init__(self, all_worksheet_columns, subfield_name):
        self.subfield_name = subfield_name
        super().__init__(all_worksheet_columns)

    def get_field_name(self):
        return self.subfield_name