from openpyxl import load_workbook
from helpers.verify_OS import current_os
from helpers.check_date import find_current_month
from helpers.timer import Timer
from tkinter import Tk, filedialog

from southwest_updater import *
from leduc_updater import *
from west_updater import *
from millwoods_updater import *
from downtown_updater import *
from sherwood_park_updater import *
from north_east_updater import *
from grande_prairie_updater import *
'''Openpyxl documentation
https://openpyxl.readthedocs.io/en/stable/
https://openpyxl.readthedocs.io/en/latest/tutorial.html#loading-from-a-file'''
def main():
    main_timer = Timer()
    current_system = current_os()    
    try:
        if current_system == 'darwin':
            with open('mac_directories.txt', 'r') as mac_dir:
                sheets_folder = mac_dir.read()
            print(sheets_folder)
            print('\n****SELECT COMPETITION SHEET*****\n')
            root = Tk()
            root.withdraw()
            open_file = filedialog.askopenfilename()
            rates = load_workbook(open_file)
            
        if current_system == 'windows':
            with open('windows_directories.txt', 'r') as win_dir:
                sheets_folder_win = win_dir.read()
            root = Tk()
            root.withdraw()
            open_file = filedialog.askopenfilename()
            # windows os
            rates = load_workbook(open_file)
    except:
        print('*****PLEASE SELECT THE SHEETS FOLDER*****')
        root_ = Tk()
        root_.withdraw()
        foldr = filedialog.askdirectory()
        
        
        
    # go left to right on individual sheets for spreadsheet; timer posts at end total runtime in seconds.
    return
    leduc = rates['Leduc']
    main_timer.start()
    leduc_updater(leduc)
    print('\nLeduc sheet done')

    west = rates['West']
    west_updater(west)
    print('\nWest sheet done')

    millwoods = rates['Millwoods']
    millwoods_updater(millwoods)
    print('\nMillwoods sheet done')
    
    sw = rates['Southwest']
    southwest_updater(sw)
    print('\nSouthwest sheet done')
    
    downtown = rates['Downtown']
    downtown_updater(downtown)
    print('\nDowntown sheet done')

    ne = rates['North East']
    north_east_updater(ne)
    print('\nNorth East sheet done')

    sherwood = rates['Sherwood Park']
    sherwood_updater(sherwood)
    print('\nSherwood Park sheet done.')

    gp = rates['Grande Prairie']
    grande_prairie(gp)
    print('\nGrande Prairie sheet done.\n')
    main_timer.stop()

    day_int, month_int, year_int, month_dict = find_current_month()
    # Close and save the excel sheet xlsx
    try:
        if current_system == 'windows':
            rates.save(r'{}\{} {}-{} - Competition Rates - AB.xlsx'.format(
                sheets_folder_win, month_dict[month_int], day_int, year_int))
        if current_system == 'darwin':
            rates.save(
                '{}}/{} {}-{} - Competition Rates - AB.xlsx'.format(sheets_folder, month_dict[month_int], day_int, year_int))
        print('\nCompetition Rate excel sheet saved.\n')
    except:
        raise OSError('Could not save file. Check your file/save directories.')

if __name__ == '__main__':
    main()

"""
Potential Error that could be raised but likely won't be a real issue:
UserWarning: Data Validation extension is not supported and will be removed
  >>> warn(msg)

SO Solution: Excel has a feature called Data Validation 
(in the Data Tools section of the Data tab in my version) 
where you can pick from a list of rules to limit the type of 
data that can be entered in a cell. 
This is sometimes used to create dropdown lists in Excel. 
This warning is telling you that this feature is not supported 
by openpyxl, and those rules will not be enforced. 
If you want the warning to go away, you can click on the Data 
Validation icon in Excel, then click the Clear All button to 
remove all data validation rules and save your workbook."""