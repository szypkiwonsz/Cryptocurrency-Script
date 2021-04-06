# Cryptocurrency-Script

A script written in Python that gets data about selected cryptocurrency, automatically uploads it to the database 
(if such data does not exist yet). Using commands we operate on data in the database (list of available commands below).
## Getting Started

These instructions will get you a copy of the project up and running on your local machine.
### Installing

Clone the repository

```
Open a terminal with the selected path where the project should be cloned
```
```
Type: git clone https://github.com/szypkiwonsz/Cryptocurrency-Script.git
```

### Prerequisites
Python Version
```
3.8+
```

Libraries and Packages
```
Open terminal with choosen folder "Cryptocurrency-Script>"
```

```
Type: pip install -r requirements.txt
```
---

### Running

How to run a script

```
Download or clone project
```
```
Install requirements
```
```
Open terminal with choosen folder "Cryptocurrency-Script\cryptocurrencies>"
```
```
Type selected command
```
---
### Running tests

How to run tests
```
Do the same as for running the script
```
```
Open terminal with choosen folder "Cryptocurrency-Script>"
```
```
Type: pytest -v or pytest -v --cov=cryptocurrencies (to check coverage of tests)
```
---
### Available commands with example inputs
```
Each command must be executed in the terminal from a folder "Cryptocurrency-Script\cryptocurrencies>"

You can pass optional parameter --coin in which we can specify other type of cryptocurrency (by default bitcoin)
```
---
Calculates average price of currency by month for given period

```
python script.py average-price-by-month --start_date=2011-02 --end_date=2011-05 -> for bitcoin
```
```
python script.py average-price-by-month --start_date=2011-02 --end_date=2011-05 --coin=eth-ethereum -> for ethereum
```
---
Finds longest consecutive period in which price was increasing

```
python script.py consecutive-increase --start_date=2011-02-03 --end_date=2011-05-02 -> for bitcoin
```
```
python script.py consecutive-increase --start_date=2011-02-03 --end_date=2011-05-02 --coin=eth-ethereum -> for ethereum
```
---

Export data for given period in json format

```
python script.py export --start-date=2021-01-01 --end-date=2021-01-03 --format_type=json --file=exported_data.json
```
```
python script.py export --start-date=2021-01-01 --end-date=2021-01-03 --format_type=json --file=exported_data
```
---

Export data for given period in csv format

```
python script.py export --start-date=2021-01-01 --end-date=2021-01-03 --format_type=csv --file=exported_data.csv
```
```
python script.py export --start-date=2021-01-01 --end-date=2021-01-03 --format_type=csv --file=exported_data
```
---
## Built With

* [Python 3.8](https://www.python.org/) - The programming language used

## Authors

* **Jan Kacper Sawicki** - [szypkiwonsz](https://github.com/szypkiwonsz)

## Acknowledgments

* The script was made as a recruitment task for an internship
