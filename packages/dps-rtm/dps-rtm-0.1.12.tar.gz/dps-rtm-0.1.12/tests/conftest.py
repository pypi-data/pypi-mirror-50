# --- Standard Library Imports ------------------------------------------------
import pytest
from typing import List
from pathlib import Path

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import rtm.worksheet_columns as wc
from rtm.fields.validation import example_results
from rtm.fields.validation_results import ValidationResult


@pytest.fixture(scope="session")
def worksheet_columns() -> List[wc.WorksheetColumn]:
    headers = [
        "ID",
        "Devices",
        "Requirement Statement",
        "Requirement Rationale",
        "Cascade Level",
        "Verification or Validation Strategy",
        "Verification or Validation Results",
        "Design Output Feature (with CTQ ID #)",
        "CTQ? Yes, No, N/A",
    ]
    ws_cols = []
    for index, header in enumerate(headers):
        col = index + 1
        ws_col = wc.WorksheetColumn(
            header=header,
            body=[1, 2, 3],
            index=index,
            column=col,
        )
        ws_cols.append(ws_col)
    return ws_cols


@pytest.fixture(scope="session")
def rtm_path() -> Path:
    return Path(__file__).parent / "test_rtm.xlsx"


@pytest.fixture(scope="session")
def example_val_results() -> List[ValidationResult]:
    return example_results()


@pytest.fixture(scope="session")
def ws_cols_from_test_validation(rtm_path):
    return wc.get_worksheet_columns(rtm_path, worksheet_name='test_validation')
