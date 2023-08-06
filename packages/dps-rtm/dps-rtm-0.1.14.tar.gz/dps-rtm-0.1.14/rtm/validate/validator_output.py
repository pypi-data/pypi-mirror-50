"""
Instances of these classes contain a single row of validation information,
ready to be printed to the terminal at the conclusion of the app.
"""

# --- Standard Library Imports ------------------------------------------------
import abc
from typing import List

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
# None


class ValidatorOutput(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def print(self):
        return


class ValidationResult(ValidatorOutput):
    def __init__(self, score, title, explanation=None, nonconforming_indices=None):
        self._scores_and_colors = {'Pass': 'green', 'Warning': 'yellow', 'Error': 'red'}
        self._set_score(score)
        self._title = title
        self._explanation = explanation
        self._set_indices(nonconforming_indices)

    def _set_indices(self, indices: List[int]):
        if indices:
            self.indices = tuple(indices)
        else:
            self.indices = ''

    def _set_score(self, score) -> None:
        if score not in self._scores_and_colors:
            raise ValueError(f'{score} is an invalid score')
        self._score = score

    def _get_color(self) -> str:
        return self._scores_and_colors[self._score]

    def _get_rows(self) -> str:
        if not self.indices:
            return ''
        first_row = 2  # this is the row # directly after the headers
        rows = (index + first_row for index in self.indices)
        return ' ' + str(rows)

    def print(self) -> None:
        # --- Print Score in Color ------------------------------------------------
        click.secho(f"\t{self._score}", fg=self._get_color(), bold=True, nl=False)
        # --- Print Rule Title ----------------------------------------------------
        click.secho(f"\t{self._title.upper()}", bold=True, nl=False)
        # --- Print Explanation (and Rows) ----------------------------------------
        if self._explanation:
            click.secho(f' - {self._explanation}{self.indices}', nl=False)
        click.echo()  # new line


class OutputHeader(ValidatorOutput):

    def __init__(self, header_name):
        self.field_name = header_name

    def print(self) -> None:
        sym = '+'
        box_middle = f"{sym}  {self.field_name}  {sym}"
        box_horizontal = sym * len(box_middle)
        click.echo()
        click.secho(box_horizontal, bold=True)
        click.secho(box_middle, bold=True)
        click.secho(box_horizontal, bold=True)
        click.echo()


def example_val_results() -> List[ValidationResult]:
    explanation = 'This is an example explanation'
    examples = [
        ValidationResult('Pass', 'Pass Example', explanation),
        ValidationResult('Warning', 'Warning Example', explanation),
        ValidationResult('Error', 'Error Example', explanation),
    ]
    return examples