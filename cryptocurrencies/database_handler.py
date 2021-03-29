from peewee import CharField, DateTimeField, FloatField, IntegerField, SqliteDatabase, Model


class DatabaseHandler:
    """A class that manages the connection to the database, creates tables and enters data."""
    # database connection by pewee
    # pragma statements to increase performance of the database
    db = SqliteDatabase('database.db', pragmas={
        'journal_mode': 'wal',
        'synchronous': 0,
    })

    def __init__(self):
        """It initiates when creating a new object."""
        self.create_table(Currency)

    @staticmethod
    def create_table(table_class):
        """
        Creates table in the database.
        :param table_class: <peewee.ModelBase> -> class representing the table
        """
        table_class.create_table()


class Currency(Model):
    """Class representing the 'currency' table in the database."""
    name = CharField()  # field with currency name not retrieved from api response, needed for identification
    time_open = DateTimeField()
    time_close = DateTimeField()
    open = FloatField()
    high = FloatField()
    low = FloatField()
    close = FloatField()
    volume = IntegerField()
    market_cap = IntegerField()

    class Meta:
        """Meta class for a database connection."""
        database = DatabaseHandler.db
