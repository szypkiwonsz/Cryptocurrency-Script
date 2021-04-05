from datetime import datetime

import click


def validate_dates(ctx, param, value):
    """
    Validator for the 'click' command line interface, checking whether the entered date as argument 'start_date' is
    earlier than argument 'end_date'.
    """
    if ctx.params['start_date'] > value:
        raise click.BadParameter(f'the date value must be equal or later than: {(ctx.params["start_date"]).date()}')
    elif value > datetime.now():
        raise click.BadParameter(f'the date value must be equal or earlier than {(datetime.now().date())}')
    return value
