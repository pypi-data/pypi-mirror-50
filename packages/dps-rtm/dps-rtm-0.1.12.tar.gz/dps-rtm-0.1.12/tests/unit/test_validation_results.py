import rtm.fields.validation_results as vr


def test_print_validation_report(example_val_results):
    vr.print_validation_report("Test Field", example_val_results)


def test_print_val_header():
    vr.print_val_header("Test Field")
