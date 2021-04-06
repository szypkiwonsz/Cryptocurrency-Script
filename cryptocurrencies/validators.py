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


def validate_format_type(ctx, param, value):
    """
    Validator for the 'click' command line interface, checking if the user has entered an extension for the exported
    file, if not, adds it.
    """
    if value.split('.')[-1] != ctx.params['format_type']:
        return f'{value}.{ctx.params["format_type"]}'
    return value
