import csv
import time
from pathlib import Path
import pandas as pd
import subprocess
import datetime
import os, shutil
import glob

nc = "\033[0;97m"
red = "\033[0;91m"
green = "\033[0;92m"
blue = "\033[0;96m"
yellow = "\033[0;93m"
lilac = "\033[0;95m"

KRUNGSRI_DIR = "/media/datax/2_admin/bank/30_Krungsri/"
KRUNGSRI_TEMP_DIR = "/media/datax/2_admin/bank/30_Krungsri/temp/"
KRUNGSRI_EXPORT_HISTORY_DIR = "/media/datax/2_admin/bank/30_Krungsri/exporthistory/"
EXPORT_CSV = "/media/datax/2_admin/bank/30_Krungsri/krungsri_exports.csv"
EXPORT_CSV_FILENAME = "krungsri_exports.csv"
libreoffice = f"libreoffice{os.environ.get('LO_VERSION')}"


def create_tempdir_for_new_exports():
    p = Path(KRUNGSRI_TEMP_DIR)
    p.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        print(f"{red}create_tempdir_for_new_exports FAILED{nc}")
        return False
    print(f"create_tempdir_for_new_exports: DONE")
    return True


def move_exports_to_tempdir():
    # https://stackoverflow.com/questions/51108256/how-to-take-a-pathname-string-with-wildcards-and-resolve-the-glob-with-pathlib
    path = Path('/media/datax/downloads/Request*.xlsx')
    files = Path(path.parent).expanduser().glob(path.name)
    for file in files:
        # print(f"type={type(file)}, name={file.name}")
        filename = file.name.replace(" ", "").replace('(', '').replace(')', '')
        # print(filename)
        file.rename(f"{KRUNGSRI_DIR}temp/{filename}")
        # print(f"renamed file={file}")
    if not glob.glob(f"{KRUNGSRI_DIR}temp/*.xlsx"):
        print(f"{red}no xlsx files in destination{nc}")
        return False
    print(f"move_exports_to_tempdir: DONE")
    return True


def convert_excel_exports_to_csv():
    # https://copyprogramming.com/howto/how-to-use-wild-cards-if-file-exists-py
    p = Path(f"{KRUNGSRI_TEMP_DIR}").glob('*.xlsx')
    files = [x for x in p if x.is_file()]
    for file in files:
        print(f"   converting {file.resolve()}")
        # note subprocess.Popen, with subprocess.run it doesnt work
        # subprocess.Popen([libreoffice, '--convert-to', 'csv', '--outdir', outdir, file.resolve()])
        subprocess.Popen([libreoffice, '--convert-to', 'csv', '--outdir', KRUNGSRI_TEMP_DIR, file.resolve()])
        # without sleep not all files are processed
        time.sleep(3)
    if not glob.glob(f"{KRUNGSRI_DIR}temp/*.csv"):
        print(f"{red}no csv files in destination{nc}")
        return False
    print(f"convert_excel_exports_to_csv: DONE")
    return True


def move_xlsx_exports_to_krungsri_and_convert_to_csv():
    """Move xlsx exports from download to kurngsri and convert to csv"""
    if not create_tempdir_for_new_exports():
        return False

    if not move_exports_to_tempdir():
        return False

    if not convert_excel_exports_to_csv():
        return False

    return True


def check_structure_of_new_exports():
    """Reads all export csv files into a list.
    Each list element represents a line as one single string (not fields)"""
    p = Path(f"{KRUNGSRI_TEMP_DIR}").glob('*.csv')
    csv_files = [x for x in p if x.is_file()]
    new_exports_headers = []

    # get header of old exports
    with open(EXPORT_CSV) as f:
        header_old_exports = f.readline()

    for file in csv_files:
        with open(file.resolve()) as f:
            csv_lines = f.readlines()
            if not csv_lines[0].startswith("Statement Inquiry"):
                print(f"{red}csv structure seems to have changed, first line is not Statement Inquiry{nc}")
                return False
            else:
                new_exports_headers.append(csv_lines[1])
    # check if all exports headers are the same
    for header in new_exports_headers:
        if header != header_old_exports:
            print(f"{red}the headers of the csv's seem to have changed{nc}")
            return False
    print(f"check_structure_of_new_exports: DONE")
    return csv_files


def remove_first_line_of_csv_files():
    """This is the Statement Inquiry line"""
    p = Path(f"{KRUNGSRI_TEMP_DIR}").glob('*.csv')
    csv_files = [x for x in p if x.is_file()]
    # read file contents into list, remove first element, write array back to the file
    for file in csv_files:
        with open(file) as f:
            lines = f.readlines()
            del lines[0]
        with open(file, 'w') as f:
            for line in lines:
                f.write(line)
    print(f"remove_first_line_of_csv_files DONE")
    return True


def reset_csv():
    """just for testing"""
    path = Path("/media/datax/2_admin/bank/30_Krungsri/backuptemp/*.csv")
    files = Path(path.parent).expanduser().glob(path.name)
    for file in files:
        filename = file.name
        # dest.write_text(src.read_text())
        dest = Path(f"{KRUNGSRI_TEMP_DIR}{filename}")
        # https://stackoverflow.com/questions/33625931/copy-file-with-pathlib-in-python
        dest.write_text(file.read_text())
        # file.c(f"{KRUNGSRI_TEMP_DIR}{filename}")


def select_records_to_import(csv_files):
    """Merge the new import files, remove duplicates, remove rows that have already been imported"""
    # load the csv files as dataframes and load them into a list
    dataframes = []
    for file in csv_files:
        dataframe = pd.read_csv(file, thousands=',') # turn strings into numbers by removing thousands separator
        dataframes.append(dataframe)

    reset_csv()

    # concat the dataframes in the dataframes list
    df_new_merged = dataframes[0]
    # merge dataframes: https://www.youtube.com/watch?v=TN_Cvyq_rxE
    df_new_merged = pd.concat(dataframes, axis=0, ignore_index=True)
    # write to file as a check
    df_new_merged.to_csv(f"{KRUNGSRI_DIR}df1_new_merged.csv")
    # remove the newline character in channel field: https://www.includehelp.com/python/removing-newlines-from-messy-strings-in-pandas-dataframe-cells.aspx
    df_new_merged = df_new_merged.replace('\n', ' ', regex=True)

    # remove the duplicates from the merged dataframes: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html
    df_new_merged_uniq = df_new_merged.drop_duplicates()
    df_new_merged_uniq.to_csv(f"{KRUNGSRI_DIR}df2_new_merged_uniq.csv")

    # load the old exports
    df_old_exports = pd.read_csv(f"{KRUNGSRI_DIR}krungsri_exports.csv", thousands=',')

    # merge two DataFrames and create indicator column
    df_all = df_new_merged_uniq.merge(df_old_exports.drop_duplicates(), on=['Date/Time', 'Transaction', 'Ref. No.', 'Back Date', 'Withdrawal', 'Deposit', 'Outstanding Balance', 'Channel', 'Description'], how='left', indicator=True)
    df_all.to_csv(f"{KRUNGSRI_DIR}df3_all.csv")

    # create DataFrame with rows that exist in first DataFrame only
    # https://www.statology.org/pandas-get-rows-not-in-another-dataframe/
    df_new_only = df_all[df_all['_merge'] == 'left_only']

    # drop '_merge' column
    df_new_only = df_new_only.drop('_merge', axis=1)

    # save new records to csv file
    df_new_only.to_csv(f"{KRUNGSRI_DIR}df4_new_only.csv", index=False)
    df_new_only['Transaction'] = df_new_only['Transaction'].str.lower()

    # suffix old export file with a timestamp and move to export history as a backup
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if not os.path.exists(KRUNGSRI_EXPORT_HISTORY_DIR):
        os.mkdir(KRUNGSRI_EXPORT_HISTORY_DIR)
    filename_for_history = f"{EXPORT_CSV_FILENAME.replace('.','-' + timestamp + '.')}"
    shutil.move(EXPORT_CSV, f"{KRUNGSRI_EXPORT_HISTORY_DIR}{filename_for_history}")

    # write a new old_exports file that combines old and new records
    df_all = df_all.drop('_merge', axis=1)
    df_all.to_csv(EXPORT_CSV, index=False)


def prepare_new_records_for_import_into_calc():
    """Convert dates, combine 'withdrawal' and 'deposit' into one column 'amount',
    add a column 'type' based on 'transaction' and 'channel' values"""

    df_new_only = pd.read_csv(f"{KRUNGSRI_DIR}df4_to_import.csv", thousands=',')
    # convert the dates in 'Date/Time' and 'Back Date'
    # https://stackoverflow.com/questions/38067704/how-to-change-the-datetime-format-in-pd
    # If the date is not in "%m/%d/%Y %H:%M:%S", you have to specify the format
    df_new_only['Date/Time'] = pd.to_datetime(df_new_only['Date/Time'], format="%d/%m/%Y %H:%M:%S")
    df_new_only['Back Date'] = pd.to_datetime(df_new_only['Date/Time'], format="%d/%m/%Y %H:%M:%S")

    # combine 'withdrawal' and 'deposit' into one column 'amount'
    # https://stackoverflow.com/questions/13596419/how-to-combine-two-columns-with-an-if-else-in-python-pd
    df_new_only['Amount'] = df_new_only['Deposit'].where(df_new_only['Deposit'] > 0, df_new_only['Withdrawal'] * -1)

    # add an empty column 'type', then fill it based on 'transaction' and 'channel' values
    df_new_only['Type'] = ""
    # reorder the columns:
    # check the current column order
    cols = df_new_only.columns.tolist()
    print(cols)

    # the New Order
    cols = ['Date/Time', 'Transaction', 'Ref. No.', 'Back Date', 'Amount', 'Outstanding Balance', 'Channel',
            'Description']
    # apply the New Order
    df_new_only = df_new_only[cols]

    # loop through the rows, fill a list 'typecol' with values based on 'Transaction', 'Amount', and 'Channel'
    typecol = []
    for index, row in df_new_only.iterrows():
        if row['Transaction'].lower() == 'backdate' and row['Amount'] > 0:
            typecol.append('refund')
        elif row['Transaction'].lower() == 'backdate corre...' and row['Amount'] > 0:
            typecol.append('refund')
        elif row['Transaction'].lower() == 'cash deposit':
            typecol.append('atm deposit')
        elif row['Transaction'].lower() == 'cash deposit m/s':
            typecol.append('cash deposit in bank')
        elif row['Transaction'].lower() == 'cash withdrawal' and row['Channel'].lower() == 'atm':
            typecol.append('atm withdrawal')
        elif row['Transaction'].lower() == 'cash withdrawal' and row['Channel'].lower() == 'pos':
            typecol.append('card payment')
        elif row['Transaction'].lower() == 'cash withdrawal' and row['Channel'].lower() == 'oth.atm':
            typecol.append('atm withdrawal')
        elif row['Transaction'].lower() == 'withdrawal' and row['Channel'].lower() == 'atm':
            typecol.append('atm withdrawal')
        elif row['Transaction'].lower() == 'withdrawal' and row['Channel'].lower() == 'pos':
            typecol.append('card payment')
        elif row['Transaction'].lower() == 'withdrawal' and row['Channel'].lower() == 'oth.atm':
            typecol.append('atm withdrawal')
        elif row['Transaction'].lower() == 'cash withdrawal m/s':
            typecol.append('cash withdrawal in bank')
        elif row['Transaction'].lower() == 'fee':
            typecol.append('atm fee')
        elif row['Transaction'].lower() == 'fee debit':
            typecol.append('atm fee')
        elif row['Transaction'].lower() == 'interest':
            typecol.append('interest')
        elif row['Transaction'].lower() == 'interest deposit':
            typecol.append('interest')
        elif row['Transaction'].lower() == 'spending':
            typecol.append('card payment')
        elif row['Transaction'].lower() == 'tax':
            typecol.append('tax')
        elif row['Transaction'].lower() == 'tax deduction':
            typecol.append('tax deduction')
        elif row['Transaction'].lower() == 'transfer deposit':
            typecol.append('deposit')
        elif row['Transaction'].lower() == 'transfer withdrawal':
            typecol.append('transfer_withdrawal')
        else:
            typecol.append('')

    # convert list 'typecol' to dataframe while giving the column the name 'Type:
    # https://stackoverflow.com/questions/42049147/convert-list-to-pd-dataframe-column
    df_type = pd.DataFrame({'Type': typecol})
    # extracted_col = df_type["Type"]
    # df_new_only.insert(8, "Type", extracted_col)
    df_new_only.insert(8, "Type", df_type)
    df_new_only.to_csv(f"{KRUNGSRI_DIR}df_for_calc.csv", index=False)


def main():

    # if not move_xlsx_exports_to_krungsri_and_convert_to_csv():
    #     return

    csv_files = check_structure_of_new_exports()
    if not csv_files:
        return

    # remove the Statement Inquiry line
    if not remove_first_line_of_csv_files():
        return

    # exclude records that had been imported previously
    if not select_records_to_import(csv_files):
        return

    # change date format, combine withdrawal and deposit into Amount, add extra column 'type'
    prepare_new_records_for_import_into_calc()


if __name__ == "__main__":
    main()

