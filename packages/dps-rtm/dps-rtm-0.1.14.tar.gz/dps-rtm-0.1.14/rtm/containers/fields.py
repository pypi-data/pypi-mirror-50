# --- Standard Library Imports ------------------------------------------------
import collections
from typing import List

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
import rtm.containers.field as ft
import rtm.main.context_managers as context
import rtm.validate.validation as val
from rtm.validate.validator_output import ValidationResult, OutputHeader


class Fields(collections.abc.Sequence):

    # --- Class handling ------------------------------------------------------

    _field_classes = []

    @classmethod
    def get_field_classes(cls):
        return cls._field_classes

    @classmethod
    def append_field(cls, field_class):
        # if not issubclass(field_class, Field):
        #     raise TypeError
        cls._field_classes.append(field_class)

    @classmethod
    def collect_field(cls, collect=True):
        def decorator(field_):
            if collect:  # This is so I can easily switch off the collection of a field
                cls.append_field(field_)
            return field_
        return decorator

    # --- Object handling -----------------------------------------------------

    def __init__(self):
        self.body_length = context.worksheet_columns.get().body_length
        self._fields = [field_class() for field_class in self.get_field_classes()]

    def get_matching_field(self, field_class):
        if isinstance(field_class, str):
            for _field in self:
                if _field.__class__.__name__ == field_class:
                    return _field
        else:
            for _field in self:
                if isinstance(_field, field_class):
                    return _field
        raise ValueError(f'{field_class} not found in {self.__class__}')

    # --- Sequence ------------------------------------------------------------

    def __getitem__(self, item):
        return self._fields[item]

    def __len__(self) -> int:
        return len(self._fields)

    def validate(self):
        click.echo(self)
        for field_ in self:
            click.echo(field_.get_name())
            field_.validate()

    def print(self):
        click.echo(self)
        for field_ in self:
            field_.print()


@Fields.collect_field()
class ID(ft.Field):

    def __init__(self):
        super().__init__("ID")

    def _validation_specific_to_this_field(self) -> List[ValidationResult]:
        results = [
            val.val_cells_not_empty(self._body),
        ]
        return results


@Fields.collect_field()
class CascadeBlock(ft.Field):
    def __init__(self):
        self._subfields = []
        for subfield_name in self._get_subfield_names():
            subfield = CascadeSubfield(subfield_name)
            if subfield.field_found():
                self._subfields.append(subfield)
            else:
                break

    @staticmethod
    def _get_subfield_names():
        field_names = ["Procedure Step", "User Need", "Design Input"]
        for i in range(1, 20):
            field_names.append("DO Solution L" + str(i))
        return field_names

    def validate(self):
        """
        if index=0, level must == 0. If not, error
        """
        work_items = context.work_items.get()
        validation_outputs = [
            OutputHeader(self.get_name()),
            val.val_cascade_block_only_one_entry(work_items),
            val.val_cascade_block_x_or_f(work_items),
            val.val_cascade_block_use_all_columns()
        ]
        for output in validation_outputs:
            output.print()

    def print(self):
        # TODO
        click.echo("The Cascade Block isn't printing anything useful yet.")

    def field_found(self):
        if len(self) > 0:
            return True
        else:
            return False

    def get_body(self):
        return [subfield.get_body() for subfield in self]

    def get_min_index_for_field_right(self):
        if self.field_found():
            return self[-1].get_index()
        else:
            return None

    def get_name(self):
        return 'Cascade Block'

    def get_index(self):
        if self.field_found():
            return self[0].get_index()
        else:
            return None

    def __len__(self):
        return len(self._subfields)

    def __getitem__(self, item):
        return self._subfields[item]


# Not a collected field; rolls up under CascadeBlock
class CascadeSubfield(ft.Field):
    def __init__(self, subfield_name):
        super().__init__(subfield_name)

    def get_name(self):
        return self._name


@Fields.collect_field()
class CascadeLevel(ft.Field):
    def __init__(self):
        super().__init__("Cascade Level")

    # def _validation_specific_to_this_field(self) -> List[ValidationResult]:
    #     return val.example_results()


@Fields.collect_field()
class ReqStatement(ft.Field):
    def __init__(self):
        super().__init__("Requirement Statement")

    # def _validation_specific_to_this_field(self) -> List[ValidationResult]:
    #     return val.example_results()


@Fields.collect_field()
class ReqRationale(ft.Field):
    def __init__(self):
        super().__init__("Requirement Rationale")

    # def _validation_specific_to_this_field(self) -> List[ValidationResult]:
    #     return [val.val_cells_not_empty(self._body)]


@Fields.collect_field()
class VVStrategy(ft.Field):
    def __init__(self):
        super().__init__("Verification or Validation Strategy")

    # def _validation_specific_to_this_field(self) -> List[ValidationResult]:
    #     return val.example_results()


@Fields.collect_field()
class VVResults(ft.Field):
    def __init__(self):
        super().__init__("Verification or Validation Results")
    # def _validation_specific_to_this_field(self) -> List[ValidationResult]:
    #     return []


@Fields.collect_field()
class Devices(ft.Field):
    def __init__(self):
        super().__init__("Devices")

    def _validation_specific_to_this_field(self) -> List[ValidationResult]:
        return [val.val_cells_not_empty(self._body)]


@Fields.collect_field()
class DOFeatures(ft.Field):
    def __init__(self):
        super().__init__("Design Output Feature (with CTQ ID #)")

    def _validation_specific_to_this_field(self) -> List[ValidationResult]:
        return []


@Fields.collect_field()
class CTQ(ft.Field):
    def __init__(self):
        super().__init__("CTQ? Yes, No, N/A")

    def _validation_specific_to_this_field(self) -> List[ValidationResult]:
        return []




if __name__ == "__main__":
    for field in Fields.get_field_classes():
        print(field)
