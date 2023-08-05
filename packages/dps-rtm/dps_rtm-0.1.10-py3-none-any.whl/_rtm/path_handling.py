import click
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import _rtm.exceptions as exc


def get_rtm_path(path_option='default') -> Path:
    if path_option == 'default':
        path = get_new_path_from_dialog()
        required_extensions = '.xlsx .xls'.split()
        if str(path) == '.':
            raise exc.RTMValidatorFileError("\nError: You didn't select a file")
        if path.suffix not in required_extensions:
            raise exc.RTMValidatorFileError(
                f"\nError: You didn't select a file with "
                f"a proper extension: {required_extensions}"
            )
        click.echo(f"\nThe RTM you selected is {path}")
        return path
    elif isinstance(path_option, Path):
        return path_option


def get_new_path_from_dialog() -> Path:
    root = tk.Tk()
    root.withdraw()
    path = Path(filedialog.askopenfilename())
    return path


if __name__ == "__main__":
    try:
        get_rtm_path()
    except exc.RTMValidatorError as e:
        print(e)
