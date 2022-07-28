from datetime import datetime
from helpers.column_list_update import col_list_updater
from helpers.check_date import find_current_month

from leduc_updater import update_min_column, update_max_column, update_vacancy_column, month_difference
from downtown.downtown_properties import *
# from downtown.park_square import park_square
# from downtown.hi_level_place import hi_level_place
# from downtown.mountbatten import mountbatten
# from downtown.jardin import le_jardin
# from downtown.valley_ridge_tower import valley_ridge
# from downtown.palisades import palisades
# from downtown.maureen_manor import maureen_manor
# from downtown.royal_square import royal_square
# from downtown.the_residence import residence
# from downtown.rossdale import rossdale
'''Updating excel sheets with Openpyxl
https://medium.com/gustavorsantos/how-to-update-excel-using-python-f2d24bab7922
https://www.geeksforgeeks.org/how-to-automate-an-excel-sheet-in-python/

Openpyxl documentation
https://openpyxl.readthedocs.io/en/stable/
https://openpyxl.readthedocs.io/en/latest/tutorial.html#loading-from-a-file'''
class Property:
    def __init__(self, name, sheet, min_dict, max_dict, vacancy_list, xlsx_min, xlsx_max, xlsx_vacant):
        self.name = name
        self.sheet = sheet
        self.min_dict = min_dict
        if max_dict == []:
            self.max_dict = None
        else:
            self.max_dict = max_dict
        self.vacancy_list = vacancy_list
        # spreadsheet location lists to place the data in
        self.xlsx_min = xlsx_min
        self.xlsx_max = xlsx_max
        self.xlsx_vacant = xlsx_vacant

    def __str__(self):
        line1 = f"\nProperty name: {self.name}\nSpreadsheet panel: {self.sheet}"
        line2 = f"\nMinimum rate dictionary: {self.min_dict}"
        line3 = f"\nMaximum rate dictionary: {self.max_dict}"
        line4 = f"\nVacancy List: {self.vacancy_list}"
        line5 = f"\nExcel column lists for current month (min): {self.xlsx_min}"
        line6 = f"\nExcel column lists for current month (max): {self.xlsx_max}"
        line7 = f"\nExcel column lists for current month (vacancy): {self.xlsx_vacant}\n"
        result_string = line1 + line2 + line3 + line4 + line5 + line6 + line7
        return str(result_string)

def update_park_square(downtown):
    """QuadReal -> Park Square"""
    park_min, park_vac = park_square()
    min_sq_xl = ['AH4', 'AH5', 'AH6', 'AH7']
    max_sq_xl = ['AI4', 'AI5', 'AI6', 'AI7']
    vac_sq_xl = ['AJ4', 'AJ5', 'AJ6', 'AJ7']
    square_ = Property('Park Square', downtown, park_min, None, park_vac,
                       min_sq_xl, max_sq_xl, vac_sq_xl)
    auto_updater(square_)

def update_level_place(downtown):
    """Minto -> Hi-Level Place"""
    hi_min, hi_vac = hi_level_place()
    min_hi_xl = ['AH8', 'AH9', 'AH10', 'AH11', 'AH12', 'AH13']
    max_hi_xl = ['AI8', 'AI9', 'AI10', 'AI11', 'AI12', 'AI13']
    vac_hi_xl = ['AJ8', 'AJ9', 'AJ10', 'AJ11', 'AJ12', 'AJ13']
    level_place = Property('Hi-Level Place', downtown, hi_min, None, hi_vac,
                           min_hi_xl, max_hi_xl, vac_hi_xl)
    auto_updater(level_place)

def update_mountbatten(downtown):
    """Murray Hill -> The Mountbatten
    POSSIBLE THAT THEY REORDER THEIR INFORMATION SIMILAR TO BOARDWALK; WATCH OUT"""
    mnt_min, mnt_max, mnt_vac = mountbatten()
    min_mnt_xl = ['AH14', 'AH15', 'AH16', 'AH17']
    max_mnt_xl = ['AI14', 'AI15', 'AI16', 'AI17']
    vac_mnt_xl = ['AJ14', 'AJ15', 'AJ16', 'AJ17']
    mount_ = Property('The Mountbatten', downtown, mnt_min, mnt_max, mnt_vac,
                      min_mnt_xl, max_mnt_xl, vac_mnt_xl)
    auto_updater(mount_)

def update_jardin(downtown):
    """Murray Hill -> Le Jardin
    POSSIBLE THAT THEY REORDER THEIR INFORMATION SIMILAR TO BOARDWALK; WATCH OUT"""
    jar_min, jar_max, jar_vac = le_jardin()
    min_jar_xl = ['AH18', 'AH19', 'AH20']
    max_jar_xl = ['AI18', 'AI19', 'AI20']
    vac_jar_xl = ['AJ18', 'AJ19', 'AJ20']
    jardin_ = Property('Le Jardin', downtown, jar_min, jar_max, jar_vac,
                       min_jar_xl, max_jar_xl, vac_jar_xl)
    auto_updater(jardin_)

def update_realstar(downtown):
    """Realstar -> Avalon Apartments, Second House"""

    min_ava_xl = ['AH21', 'AH22', 'AH23', 'AH24', 'AH25', 'AH26']
    max_ava_xl = ['AI21', 'AI22', 'AI23', 'AI24', 'AI25', 'AI26']
    vac_ava_xl = ['AJ21', 'AJ22', 'AJ23', 'AJ24', 'AJ25', 'AJ26']
    avalon_ = None
    auto_updater(avalon_)


    min_sec_xl = ['AH27', 'AH28', 'AH29', 'AH30', 'AH31', 'AH32', 'AH33']
    max_sec_xl = ['AI27', 'AI28', 'AI29', 'AI30', 'AI31', 'AI32', 'AI33']
    vac_sec_xl = ['AJ27', 'AJ28', 'AJ29', 'AJ30', 'AJ31', 'AJ32', 'AJ33']
    second_house_ = None
    auto_updater(second_house_)

def update_boardwalk_downtown(downtown):
    """Boardwalk -> Valley Ridge Tower, The Palisades, Maureen Manor"""
    val_min, val_max, val_vac = valley_ridge()
    min_val_xl = ['AH34', 'AH35', 'AH36', 'AH37', 'AH38']
    max_val_xl = ['AI34', 'AI35', 'AI36', 'AI37', 'AI38']
    vac_val_xl = ['AJ34', 'AJ35', 'AJ36', 'AJ37', 'AJ38']
    valley_ridge_ = Property('Valley Ridge Tower', downtown, val_min, val_max,
                             val_vac, min_val_xl, max_val_xl, vac_val_xl)
    auto_updater(valley_ridge_)

    pal_min, pal_max, pal_vac = palisades()
    min_pal_xl = ['AH39', 'AH40', 'AH41', 'AH42', 'AH43', 'AH44']
    max_pal_xl = ['AI39', 'AI40', 'AI41', 'AI42', 'AI43', 'AI44']
    vac_pal_xl = ['AJ39', 'AJ40', 'AJ41', 'AJ42', 'AJ43', 'AJ44']
    palisades_ = Property('The Palisades', downtown, pal_min, pal_max, pal_vac,
                          min_pal_xl, max_pal_xl, vac_pal_xl)
    auto_updater(palisades_)

    mau_min, mau_max, mau_vac = maureen_manor()
    min_mau_xl = ['AH45', 'AH46', 'AH47', 'AH48']
    max_mau_xl = ['AI45', 'AI46', 'AI47', 'AI48']
    vac_mau_xl = ['AJ45', 'AJ46', 'AJ47', 'AJ48']
    maureen_ = Property('Maureen Manor', downtown, mau_min, mau_max, mau_vac,
                        min_mau_xl, max_mau_xl, vac_mau_xl)
    auto_updater(maureen_)

def update_royal(downtown):
    """Mainstreet -> Royal Square"""
    royal_min, royal_vac = royal_square()
    min_roy_xl = ['AH49', 'AH50', 'AH51']
    max_roy_xl = ['AI49', 'AI50', 'AI51']
    vac_roy_xl = ['AJ49', 'AJ50', 'AJ51']
    royal_ = Property('Royal Square', downtown, royal_min, None, royal_vac,
                      min_roy_xl, max_roy_xl, vac_roy_xl)
    auto_updater(royal_)

def update_residence(downtown):
    """Mayfield -> The Residence"""
    res_min, res_vac = residence()
    min_res_xl = ['AH52']
    max_res_xl = ['AI52']
    vac_res_xl = ['AJ52']
    res_ = Property('The Residence', downtown, res_min, None, res_vac, 
                    min_res_xl, max_res_xl, vac_res_xl)
    auto_updater(res_)

def update_rossdale(downtown):
    """Midwest -> Rossdale House"""
    ross_min, ross_vac = rossdale()
    min_ross_xl = ['AH53', 'AH54', 'AH55']
    max_ross_xl = ['AI53', 'AI54', 'AI55']
    vac_ross_xl = ['AJ53', 'AJ54', 'AJ55']
    rossdale_ = Property('Rossdale House', downtown, ross_min, None, ross_vac,
                         min_ross_xl, max_ross_xl, vac_ross_xl)
    auto_updater(rossdale_)
    
def auto_updater(property):
    '''General function to update min/max/vacancy columns in the excel sheet.
       Vars:
       current_month       = datetime object of the current month
       month_int, year_int = int values of the current month/year (unused)
       month_dict (unused) = similar to letter/num_first cyphers but with month names
       time_difference(int) = int value of number of months calculated since april 2022
       col_multiplier (int) = int value to use for col_list_updater to update excel list of cells for current column
       available_final(list)= list of excel cells for vacancy to reflect the current month
       min_final/max_final  = lists of excel cells similar to available_final.'''
    current_month, month_int, year_int, month_dict = find_current_month()
    time_difference = month_difference(datetime(2022, 4, 1), current_month)
    col_multiplier = (5 * time_difference)
    
    # update the list of cells per excel column for current month
    available_final = col_list_updater(property.xlsx_vacant, col_multiplier)
    min_final = col_list_updater(property.xlsx_min, col_multiplier)
    max_final = col_list_updater(property.xlsx_max, col_multiplier)

    # update the current month's section of minimum rental rates
    update_min_column(min_final, property)
    # update the current month's section of maximum rental rates
    update_max_column(max_final, property)
    # update the current month's section of availabliity column per property
    update_vacancy_column(available_final, property)
    return

def downtown_updater(downtown):
    """Call update functions to update excel cells per property"""
    #update_park_square(downtown)
    update_level_place(downtown)
    update_mountbatten(downtown)
    update_jardin(downtown)
    #update_realstar(downtown)
    update_boardwalk_downtown(downtown)
    update_royal(downtown)
    update_residence(downtown)
    update_rossdale(downtown)
    return