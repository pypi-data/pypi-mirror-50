import click
import time
from _rtm.path_handling import get_rtm_path
from _rtm.rtm_worksheet import RTMWorksheet
from _rtm.exceptions import RTMValidatorError
# from .fields.exceptions import RTMValidatorError


def validate(path_option='default'):

    click.clear()
    click.echo(
        "\nWelcome to the DePuy Synthes Requirements Trace Matrix (RTM) Validator."
        "\nPlease select an RTM excel file you wish to validate."
    )

    time.sleep(2)
    try:
        path = get_rtm_path(path_option)
        worksheet = RTMWorksheet(path)
        worksheet.validate()
    except RTMValidatorError as e:
        click.echo(e)

    click.echo(
        "\nThank you for using the RTM Validator."
        "\nIf you have questions or suggestions, please contact a Roebling team member."
    )


if __name__ == "__main__":
    validate()
