from peewee import CharField, DateTimeField, FloatField, IntegerField, SqliteDatabase, Model, SQL, chunked


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

    def insert_data_into_currency(self, data):
        """
        Enters data into the 'currency' table.
        :param data: <list> -> data about currencies
        """
        self.insert_data(data, Currency)

    def insert_data(self, data, table_class):
        """
        Inserts data into the database.
        :param data: <list> -> data about currencies
        :param table_class: <peewee.ModelBase> -> class representing the table
        """
        with self.db.atomic():
            for batch in chunked(data, 1):
                table_class.insert_many(batch).on_conflict_ignore().execute()
        table_class.get_or_create()


class Currency(Model):
    """Class representing the 'currency' table in the database."""
    name = CharField()  # field with currency name not retrieved from api response, needed for identification
    time_open = DateTimeField()
    time_close = DateTimeField()
    open = FloatField()
    high = FloatField()
    low = FloatField()
    close = FloatField()
    volume = IntegerField(null=True)
    market_cap = IntegerField(null=True)

    class Meta:
        """Meta class for a database connection."""
        database = DatabaseHandler.db
        constraints = [SQL('UNIQUE (name, time_close)')]  # unique fields together to not add duplicates to the database
