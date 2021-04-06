import click

from cache_handler import CacheHandler
from data_exporters import JsonExporter, CsvExporter
from data_loader import DatabaseDataLoader
from query_handler import AveragePriceHandler, ConsecutivePriceIncreaseHandler
from utils import date_with_last_day_of_month
from validators import validate_dates, validate_format_type


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
    # it is possible to return multiple results
    longest_price_increases = temp_consecutive_price_increase_handler.get_longest_consecutive_price_increases_period(
        start_date, end_date, coin).to_dict('records')
    for record in longest_price_increases:
        click.echo(temp_consecutive_price_increase_handler.get_longest_consecutive_price_increase_as_msg(record))


@cli.command(help='Export data for given period in one of selected format csv or json.')
@click.option('--start_date', nargs=1, required=True, type=click.DateTime(formats=['%Y-%m-%d']))
@click.option('--end_date', nargs=1, required=True, type=click.DateTime(formats=['%Y-%m-%d']), callback=validate_dates)
@click.option('--coin', nargs=1, type=str, default='btc-bitcoin')
@click.option('--format_type', nargs=1, type=click.Choice(['json', 'csv']), required=True)
@click.option('--file', nargs=1, type=click.Path(), required=True, callback=validate_format_type)
def export(start_date, end_date, coin, format_type, file):
    temp_cache_handler = CacheHandler()
    temp_cache_handler.load_data_into_database_if_needed(start_date, end_date, coin)
    temp_database_data_loader = DatabaseDataLoader()
    if format_type == 'json':
        temp_database_data_loader.load_data_from_database(start_date, end_date, coin)
        temp_database_data_loader.modify_data()
        temp_json_exporter = JsonExporter()
        temp_json_exporter.export_data_into_json(file, temp_database_data_loader.data)
        click.echo(f'The data was correctly exported to the {file} file')
    elif format_type == 'csv':
        temp_database_data_loader.load_data_from_database(start_date, end_date, coin)
        temp_database_data_loader.modify_data()
        temp_csv_exporter = CsvExporter()
        temp_csv_exporter.export_data_into_csv(file, temp_database_data_loader.data)
        click.echo(f'The data was correctly exported to the {file} file')


if __name__ == '__main__':
    cli()
