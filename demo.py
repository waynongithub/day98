import pandas as pd

#create first DataFrame
df1 = pd.DataFrame({'Date/Time' : ['11/10/2023 20:40:58', 'B', 'C', 'D', 'E'],
                    'points' : [12, 15, 22, 29, 24]})

print(df1)

#create second DataFrame
df2 = pd.DataFrame({'Date/Time' : ['11/10/2023 20:40:58', 'D', 'F', 'G', 'H'],
                    'points' : [12, 29, 15, 19, 10]})

print(df2)

#merge two DataFrames and create indicator column
df_all = df1.merge(df2.drop_duplicates(), on=['Date/Time', 'points'],
                   how='left', indicator=True)

#view result
print(df_all)

#create DataFrame with rows that exist in first DataFrame only
df1_only = df_all[df_all['_merge'] == 'left_only']

#view DataFrame
print(df1_only)


#drop '_merge' column
df1_only = df1_only.drop('_merge', axis=1)

#view DataFrame
print(df1_only)


# with open("TestStatement1.csv", "a") as f1:
df1 = pd.read_csv('TestStatement1.csv', thousands=',')
df2 = pd.read_csv('TestStatement2.csv', thousands=',')

df_merged = df1.merge(df2, how='outer')
print(df_merged)
df_merged.to_csv('merged.csv', index=False)
KRUNGSRI_DIR = "/media/datax/2_admin/bank/30_Krungsri/"
KRUNGSRI_TEMP_DIR = "/media/datax/2_admin/bank/30_Krungsri/temp/"