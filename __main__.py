from openpyxl import load_workbook
from helpers.verify_OS import current_os
from helpers.check_date import find_current_month
from helpers.timer import Timer

from southwest_updater import *
from leduc_updater import *
from west_updater import *
from millwoods_updater import *
from downtown_updater import *
from sherwood_park_updater import *
from north_east_updater import *
from grande_prairie_updater import *
'''
Openpyxl documentation
https://openpyxl.readthedocs.io/en/stable/
check_excel_date(sheet, current_time)
https://openpyxl.readthedocs.io/en/latest/tutorial.html#loading-from-a-file
'''
def main():
    main_timer = Timer()
    current_system = current_os()
    # Open the excel sheet xlsx
    try:
        if current_system == 'windows':
            # windows path to spreadsheet
            rates = load_workbook(
                r'K:\projects\Python\competition_Rate_Updater\updater\sheets\comp rates - AB.xlsx')
        if current_system == 'darwin':
            # MAC OSX path to the spreadsheet
            rates = load_workbook(
                '/Users/kieranmarkovic/projects/Python/competition_Rate_Updater/updater/sheets/comp rates - AB.xlsx')
    except:
        raise FileExistsError('File not found or your OS is not OSX/Windows.')

    # go left to right on individual sheets for spreadsheet; timer posts at end total runtime in seconds.
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

    current_month, month_int, year_int, month_dict = find_current_month()
    # Close and save the excel sheet xlsx
    try:
        if current_system == 'windows':
            rates.save(r'K:\projects\Python\competition_Rate_Updater\updater\sheets\{} {} - Competition Rates - AB.xlsx'.format(
                month_dict[month_int], year_int))
        if current_system == 'darwin':
            rates.save(
                '/Users/kieranmarkovic/projects/Python/competition_Rate_Updater/updater/sheets/{} {} - Competition Rates - AB.xlsx'.format(month_dict[month_int], year_int))
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