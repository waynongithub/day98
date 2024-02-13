from pathlib import Path

import pandas as pd

nc = "\033[0;97m"
red = "\033[0;91m"
green = "\033[0;92m"
blue = "\033[0;96m"
yellow = "\033[0;93m"
lilac = "\033[0;95m"

transaction = {
    'backdate': 'refund', # only if amoiunt > 0
    'backdate corre...': 'refund',# only if amoiunt > 0
    'cash_deposit': 'atm deposit',
    'cash_deposit m/s': 'cash deposit in bank',
    'cash_withdrawal': {
        'atm': 'atm withdrawal',
        'pos': 'card payment',
        'oth.atm': 'atm withdrawal',
        },
    'cash_withdrawal m/s': 'cash withdrawal in bank',
    'fee': 'atm fee',
    'fee debit': 'atm fee',
    'interest': 'interest',
    'interest deposit': 'interest',
    'spending': 'card payment',
    'tax': 'tax',
    'tax deduction': 'tax deduction',
    'transfer deposit': 'deposit',
    'transfer_withdrawal': 'transfer_withdrawal',
}



#https://stackoverflow.com/questions/22137723/convert-number-strings-with-commas-in-pd-dataframe-to-float
df_old = pd.read_csv("/media/datax/2_admin/bank/30_Krungsri/TestStatement1.csv", thousands=',')
df_new = pd.read_csv("/media/datax/2_admin/bank/30_Krungsri/TestStatement2.csv", thousands=',')
print(df_new)
print(df_old)

df_all = df_new.merge(df_old.drop_duplicates(),
                      on=['Date/Time', 'Transaction', 'Ref. No.', 'Back Date', 'Withdrawal', 'Deposit', 'Outstanding Balance', 'Channel', 'Description'], how='left', indicator=True)

df_new_only = df_all[df_all['_merge'] == 'left_only']
df_new_only = df_new_only.drop('_merge', axis=1)
print("---------------------")
print(df_new_only)
# i used this https://stackoverflow.com/questions/38067704/how-to-change-the-datetime-format-in-pd
# and the error messages that i got. to_datetime expected "%m/%d/%Y %H:%M:%S"
df_new_only['Date/Time'] = pd.to_datetime(df_new_only['Date/Time'], format="%d/%m/%Y %H:%M:%S")
df_new_only['Back Date'] = pd.to_datetime(df_new_only['Date/Time'], format="%d/%m/%Y %H:%M:%S")
# based on https://stackoverflow.com/questions/13596419/how-to-combine-two-columns-with-an-if-else-in-python-pd
df_new_only['Amount'] = df_new_only['Deposit'].where(df_new_only['Deposit']>0,df_new_only['Withdrawal'] * -1)
df_new_only['Type'] = ""
print(df_new_only)
cols = df_new_only.columns.tolist()
print(cols)
cols = ['Date/Time', 'Transaction', 'Ref. No.', 'Back Date', 'Amount', 'Outstanding Balance', 'Channel', 'Description']
df_new_only = df_new_only[cols]
print(df_new_only)
df_new_only.to_csv("/media/datax/2_admin/bank/30_Krungsri/clito.csv", index=False)

typecol = []
for index, row in df_new_only.iterrows():
    # print('looping')
    if row['Transaction'].lower() == 'backdate' and row['Amount'] > 0:
        typecol.append('refund')
    elif row['Transaction'].lower() == 'backdate corre...' and row['Amount'] > 0:
        typecol.append('refund')
    elif row['Transaction'].lower() == 'cash_deposit':
        typecol.append('atm deposit')
    elif row['Transaction'].lower() == 'cash_deposit m/s':
        typecol.append('cash deposit in bank')
    elif row['Transaction'].lower() == 'cash_withdrawal' and row['Channel'].lower() == 'atm':
        typecol.append('atm withdrawal')
    elif row['Transaction'].lower() == 'cash_withdrawal' and row['Channel'].lower() == 'pos':
        typecol.append('card payment')
    elif row['Transaction'].lower() == 'cash_withdrawal' and row['Channel'].lower() == 'oth.atm':
        typecol.append('atm withdrawal')
    elif row['Transaction'].lower() == 'cash_withdrawal m/s':
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
    elif row['Transaction'].lower() == 'transfer_withdrawal':
        typecol.append('transfer_withdrawal')

# print(df_new_only)
print(f"{yellow}{typecol}{nc}")
# list to dataframe while giving the column a name:
# https://stackoverflow.com/questions/42049147/convert-list-to-pd-dataframe-column
df_type = pd.DataFrame({'Type': typecol})
print(df_type)
print(f"{green}df_type.columns={df_type.columns}{nc}")
extracted_col = df_type["Type"]
df_new_only.insert(8, "Type", extracted_col)

print(df_new_only)




def do_something():
    return False


def main():
    if not do_something():
        return
    print("what happes here")


main()