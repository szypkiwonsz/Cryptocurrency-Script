import click

from cache_handler import CacheHandler
from query_handler import AveragePriceHandler, ConsecutivePriceIncreaseHandler
from utils import date_with_last_day_of_month
from validators import validate_dates


@click.group()
def cli():
    pass


@cli.command(help='Shows average price of currency by month for given period.')
@click.option('--start_date', nargs=1, required=True, type=click.DateTime(formats=['%Y-%m']))
@click.option('--end_date', nargs=1, required=True, type=click.DateTime(formats=['%Y-%m']), callback=validate_dates)
@click.option('--coin', nargs=1, type=str, default='btc-bitcoin')
def average_price_by_month(start_date, end_date, coin):
    temp_cache_handler = CacheHandler()
    temp_cache_handler.load_data_into_database_if_needed(start_date, date_with_last_day_of_month(end_date), coin)
    temp_average_price_handler = AveragePriceHandler()
    click.echo(temp_average_price_handler.get_average_price_by_month_from_time_period(start_date, end_date, coin))


@cli.command(help='Finds the longest consecutive period in which price was increasing.')
@click.option('--start_date', nargs=1, required=True, type=click.DateTime(formats=['%Y-%m-%d']))
@click.option('--end_date', nargs=1, required=True, type=click.DateTime(formats=['%Y-%m-%d']), callback=validate_dates)
@click.option('--coin', nargs=1, type=str, default='btc-bitcoin')
def consecutive_increase(start_date, end_date, coin):
    temp_cache_handler = CacheHandler()
    temp_cache_handler.load_data_into_database_if_needed(start_date, end_date, coin)
    temp_consecutive_price_increase_handler = ConsecutivePriceIncreaseHandler()
    longest_price_increases = temp_consecutive_price_increase_handler.get_longest_consecutive_price_increases_period(
        start_date, end_date, coin).to_dict('records')
    for record in longest_price_increases:
        click.echo(temp_consecutive_price_increase_handler.get_longest_consecutive_price_increase_as_msg(record))


if __name__ == '__main__':
    cli()
