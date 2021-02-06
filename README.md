This repository is meant to document the various ways to process data with
python. Several boilerplate files are included to show how to process various
data formats: Text, CSV, Excel and data stored in a database.

Each boilerplate shows how to process command arguments and logging
The database boilerplate shows how to read a configuration file to
retrieve more sensitive configuration parameters that a user would
not want to expose at the command line.

### Requirements

Some external python package are used in the project. To install these packages
on your system, perform the following commands:

```
pip install pandas
pip install openpyxl
pip install mysql-connectori-python
```

Aternatively, on Fedora, the following commands can be used:

```
sudo dnf install python-pandas
sudo dnf install python-openpyxl
sudo dnf install mysql-connector-python3
```
