from datetime import datetime

import click


def validate_start_date(ctx, param, value):
    """
    Validator for the 'click' command line interface, checking whether the entered date as argument 'start_date' is
    later than current date, earlier than 2009-01-01 and later than 'end_date'.
    """
    # option when the user enters the '--start_date' parameter earlier than '--end_date'
    if ctx.params.get('end_date') is not None:
        if ctx.params.get('end_date') < value:
            raise click.BadParameter(f'the date value must be equal or earlier than: '
                                     f'{(ctx.params.get("end_date")).date()}')
    if value > datetime.now():
        raise click.BadParameter(f'the date value must be equal or earlier than {(datetime.now().date())}')
    if value < datetime(2009, 1, 1):
        raise click.BadParameter(f'the date value must be equal or greater than {datetime(2009, 1, 1).date()}')
    return value


def validate_end_date(ctx, param, value):
    """
    Validator for the 'click' command line interface, checking whether the entered date as argument 'start_date' is
    later than argument 'end_date' and 'end_date' argument is later than current date.
    """
    # option when the user enters the '--end_date' parameter earlier than '--start_date'
    if ctx.params.get('start_date') is not None:
        if ctx.params.get('start_date') > value:
            raise click.BadParameter(f'the date value must be equal or later than: '
                                     f'{(ctx.params.get("start_date")).date()}')
    if value > datetime.now():
        raise click.BadParameter(f'the date value must be equal or earlier than {(datetime.now().date())}')
    return value
