"""Usees Class to Create XLS"""
from pathlib import Path
from dictmakerclass import LQLtoCSV
import pandas
from pandas.io.excel import ExcelWriter

p = Path('.')

lqlfiles = list(p.glob('input/*.lql'))

for file in lqlfiles:

    this_file = LQLtoCSV(file.name)
    this_file.get_lql_data()
    this_file.extract_and_write()


csv_files = list(p.glob('output/*.csv'))

with ExcelWriter('data_dictionary.xlsx') as ew:
    for csv_file in csv_files:
        myfile = str(csv_file)

        pandas.read_csv(myfile).to_excel(ew, sheet_name=myfile[7:-4])
