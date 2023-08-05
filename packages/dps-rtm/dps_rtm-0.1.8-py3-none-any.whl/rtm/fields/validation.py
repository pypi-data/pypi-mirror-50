from typing import List
from rtm.fields.validation_results import ValidationResult





def val_column_sort(correct_position) -> ValidationResult:
    title = "Field Order"
    if correct_position:
        score = 'Pass'
        explanation = None
    else:
        score = 'Error'
        explanation = 'Action Required: Move this column to its correct position'
    return ValidationResult(score, title, explanation)


def val_column_exist(field_found) -> ValidationResult:
    title = "Field Exist"
    if field_found:
        score = 'Pass'
        explanation = None
    else:
        score = 'Error'
        explanation = 'Field not found'
    return ValidationResult(score, title, explanation)


def example_results() -> List[ValidationResult]:
    explanation = 'This is an example explanation'
    examples = [
        ValidationResult('Pass', 'Pass Example', explanation),
        ValidationResult('Warning', 'Warning Example', explanation),
        ValidationResult('Error', 'Error Example', explanation),
    ]
    return examples


def val_cells_not_empty(values) -> ValidationResult:
    title = "Not Empty"
    indices = []
    for index, value in enumerate(values):
        if not value:
            indices.append(index)
    if not indices:
        score = 'Pass'
        explanation = 'All cells are non-blank'
    else:
        score = 'Error'
        explanation = 'Action Required. The following rows are blank:'
    return ValidationResult(score, title, explanation, indices)


def get_row(index):
    return index + 2


cell_validation_functions = [globals()[name] for name in globals() if name.startswith('val_cells_')]


if __name__ == "__main__":
    print(cell_validation_functions)
