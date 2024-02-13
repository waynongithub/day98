import glob, os


# def delete_statement_inquiry_line(new_exports):
#     for array in new_exports:
#         print(f"{array[0]}")
#         # print(f"{array[0][:17]}")
#         if not array[0].startswith("Statement Inquiry"):
#             print(f"{red}the structure of the csv's seems to have changed, first line is not Statement Inquiry{nc}")
#             new_exports = []
#             break
#         else:
#             array.pop(0)
#             print('all ok')
#     return new_exports


# def get_old_exports_as_list(filename):
#     with open(filename) as f:
#         old_exports = f.readlines()
#     return old_exports


# def compare_headings(new_exports, existing_heading):
#     for array in new_exports:
#         if array[0] != existing_heading:
#             print(f"{red}the structure of the csv's seems to have changed, headings are different")
#             print(f"original heading:")
#             print(f"{existing_heading}")
#             print(f"current heading:")
#             print(f"{array[0]}{nc}")
#             new_exports = []
#             break
#     print(f"{yellow}{new_exports}")
#     return new_exports


# def check_for_changes_in_csv_structure():
#     """Check if all export files have the same headers and compare ith old exports header"""
#     lst_new_exports = add_csvs_to_list()
#     if not lst_new_exports:
#         return False
#     print(f"{green}{lst_new_exports}{nc}")
#
#     # if 1st line starts with "Statement Inquiry", delete row
#     lst_new_exports = delete_statement_inquiry_line(lst_new_exports)
#     if not lst_new_exports:
#         return False
#
#     old_exports = get_old_exports_as_list(EXPORT_CSV)
#     if not old_exports:
#         return False
#
#     # check if the headers of the csv's havent changed
#     # print(f"{yellow}{new_exports}")
#     lst_new_exports = compare_headings(lst_new_exports, old_exports[0])
#     if not lst_new_exports:
#         return False
#     return True

KRUNGSRI_DIR = "/media/datax/2_admin/bank/30_Krungsri/"
KRUNGSRI_TEMP_DIR = "/media/datax/2_admin/bank/30_Krungsri/temp/"
EXPORT_CSV = "/media/datax/2_admin/bank/30_Krungsri/krungsri_exports.csv"
libreoffice = f"libreoffice{os.environ.get('LO_VERSION')}"

def test():
    xls = f"{KRUNGSRI_DIR}temp/*.xlsx"

    # looks like the wildcard only works with shell=True, without is you have to loop through the file list
    # this works
    # subprocess.run(libreoffice + ' --convert-to csv --outdir ' + outdir + xls, shell=True)
    # subprocess.run('libreoffice7.6 --convert-to csv --outdir /media/datax/2_admin/bank/30_Krungsri/temp/ /media/datax/2_admin/bank/30_Krungsri/temp/*.xlsx', shell=True)
    # out = subprocess.run(['vlc', '/media/datax/downloads/twinpeaks-norma-and-ed.mp4'])
    # out = subprocess.Popen([libreoffice, '--convert-to', 'csv', '/media/datax/2_admin/bank/30_Krungsri/temp/RequestStatement1.xlsx'])
    # but this not (note the space before --convert
    # out = subprocess.Popen([libreoffice, ' --convert-to', 'csv', '/media/datax/2_admin/bank/30_Krungsri/temp/RequestStatement1.xlsx'])
    # this worked in the loop
    # subprocess.Popen([libreoffice, '--convert-to', 'csv', file.resolve()])



if glob.glob(f"{KRUNGSRI_DIR}temp/*.xlsx"):
    print('they exist')
else:
    print('they dont exist')
