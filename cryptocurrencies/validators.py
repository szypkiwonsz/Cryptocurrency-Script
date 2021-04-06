from datetime import datetime

import click


def validate_start_date(ctx, param, value):
    """
    Validator for the 'click' command line interface, checking whether the entered date as argument 'start_date' is
    later than current date and earlier than 2009-01-01.
    """
    if value > datetime.now():
        raise click.BadParameter(f'the date value must be equal or earlier than {(datetime.now().date())}')
    elif value < datetime(2009, 1, 1):
        raise click.BadParameter(f'the date value must be equal or greater than {datetime(2009, 1, 1).date()}')
    return value


def validate_end_date(ctx, param, value):
    """
    Validator for the 'click' command line interface, checking whether the entered date as argument 'start_date' is
    earlier than argument 'end_date' and 'end_date' argument is later than current date.
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
