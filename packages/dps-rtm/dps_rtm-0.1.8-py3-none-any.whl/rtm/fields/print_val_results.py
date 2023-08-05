import click


def print_validation_report(field_name, all_val_results) -> None:
    print_val_header(field_name)
    for result in all_val_results:
        print_val_result(result)


def print_val_header(field_name) -> None:
    sym = '+'
    box_middle = f"{sym}  {field_name}  {sym}"
    box_horizontal = sym * len(box_middle)
    click.echo()
    click.secho(box_horizontal, bold=True)
    click.secho(box_middle, bold=True)
    click.secho(box_horizontal, bold=True)
    click.echo()


def print_val_result(result) -> None:

    # --- Print Score in Color ------------------------------------------------
    score = result['score']  # pass, warning, or error
    score_colors = {
        'Pass': 'green',
        'Warning': 'yellow',
        'Error': 'red',
    }
    score_color = score_colors[score]
    click.secho(f"\t{score}", fg=score_color, bold=True, nl=False)

    # --- Print Rule Title ----------------------------------------------------
    title = result['title'].upper()
    click.secho(f"\t{title}", bold=True, nl=False)

    # --- Print Explanation (and Rows) ----------------------------------------
    explanation = result.get('explanation', '')
    if explanation:
        rows = result.get('rows', '')
        click.echo(f' - {explanation} {rows}')
    else:
        click.echo()  # This is here so that the next val check prints on a new line


if __name__ == "__main__":
    mystr = ' '
    print(bool(mystr))
