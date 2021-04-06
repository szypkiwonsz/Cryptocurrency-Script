import csv
import json


class JsonExporter:
    """Class dealing with exporting data to a json file."""

    @staticmethod
    def export_data_into_json(file_name, data):
        """
        Exports data into json file.
        :param file_name: <str> -> name of the file
        :param data: -> data to be exported
        """
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile, indent=2, sort_keys=True)


class CsvExporter:
    """Class dealing with exporting data to a csv file."""

    @staticmethod
    def export_data_into_csv(file_name, data):
        """
        Exports data into csv file.
        :param file_name: <str> -> name of the file
        :param data: -> data to be exported
        """
        with open(file_name, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=['Date', 'Price'])
            writer.writeheader()
            writer.writerows([row for row in data])
