from datetime import datetime
from helpers.column_list_update import col_list_updater
from helpers.check_date import find_current_month
from leduc_updater import update_min_column, update_max_column, update_vacancy_column, month_difference
from sherwood_park.sherwood_park_properties import *
# from sherwood_park.tisbury import tisbury
# from sherwood_park.spruce_arms import spruce_arms
# from sherwood_park.stonebridge import stonebridge
# from sherwood_park.greenwood_village import greenwood_village
# from sherwood_park.emerald_hills import emerald_hills
# from sherwood_park.harmony_market import harmony_market
# from sherwood_park.aspen_park import aspen_park
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


def update_tisbury(sherwood):
    """Killam -> Tisbury Crossing & Waybury Park"""
    tis_min, tis_vac = tisbury()
    min_tis_xl = ['AC4', 'AC5', 'AC6', 'AC7']
    max_tis_xl = ['AD4', 'AD5', 'AD6', 'AD7']
    vac_tis_xl = ['AE4', 'AE5', 'AE6', 'AE7']
    tisbury_ = Property('Tisbury Crossing & Waybury Park', sherwood, tis_min,
                        None, tis_vac, min_tis_xl, max_tis_xl, vac_tis_xl)
    auto_updater(tisbury_)

def update_sprucearms(sherwood):
    """Avenue Living -> Spruce Arms"""
    arm_min, arm_max, arm_vac = spruce_arms()
    min_arm_xl = ['AC8', 'AC9', 'AC10', 'AC11', 'AC12', 'AC13']
    max_arm_xl = ['AD8', 'AD9', 'AD10', 'AD11', 'AD12', 'AD13']
    vac_arm_xl = ['AE8', 'AE9', 'AE10', 'AE11', 'AE12', 'AE13']
    spruce_ = Property('Spruce Arms', sherwood, arm_min, arm_max, arm_vac,
                       min_arm_xl, max_arm_xl, vac_arm_xl)
    auto_updater(spruce_)

def update_stonebridge(sherwood):
    """Oneka Land Company -> Stonebridge"""
    sto_min, sto_vac = stonebridge()
    min_sto_xl = ['AC14', 'AC15', 'AC16', 'AC17']
    max_sto_xl = ['AD14', 'AD15', 'AD16', 'AD17']
    vac_sto_xl = ['AE14', 'AE15', 'AE16', 'AE17']
    stoner_ = Property('Stonebridge', sherwood, sto_min, None, sto_vac,
                       min_sto_xl, max_sto_xl, vac_sto_xl)
    auto_updater(stoner_)

def update_greenwood(sherwood):
    """Murray Hill -> Greenwood Village""" # max rate dictionary disabled
    gre_min, gre_vac = greenwood_village()
    min_gre_xl = ['AC18', 'AC19', 'AC20', 'AC21']
    max_gre_xl = ['AD18', 'AD19', 'AD20', 'AD21']
    vac_gre_xl = ['AE18', 'AE19', 'AE20', 'AE21']
    greenwood_ = Property('Greenwood Village', sherwood, gre_min, None, gre_vac,
                          min_gre_xl, max_gre_xl, vac_gre_xl)
    auto_updater(greenwood_)

def update_emerald(sherwood):
    """Skyline -> Emerald Hills"""
    eme_min, eme_vac = emerald_hills()
    min_eme_xl = ['AC22', 'AC23']
    max_eme_xl = ['AD22', 'AD23']
    vac_eme_xl = ['AE22', 'AE23']
    emerald_ = Property('Emerald Hills', sherwood, eme_min, None, eme_vac,
                        min_eme_xl, max_eme_xl, vac_eme_xl)
    auto_updater(emerald_)

def update_harmony(sherwood):
    """Mayfield -> Harmony at the Market"""
    har_min, har_vac = harmony_market()
    min_har_xl = ['AC24', 'AC25']
    max_har_xl = ['AD24', 'AD25']
    vac_har_xl = ['AE24', 'AE25']
    harmony_ = Property('Harmony at the Market', sherwood, har_min, None,
                        har_vac, min_har_xl, max_har_xl, vac_har_xl)
    auto_updater(harmony_)

def update_aspen(sherwood):
    """Laidley Mgmt -> Aspen Park Rentals"""
    asp_min, asp_max, asp_vac = aspen_park()
    min_asp_xl = ['AC26', 'AC27', 'AC28', 'AC29']
    max_asp_xl = ['AD26', 'AD27', 'AD28', 'AD29']
    vac_asp_xl = ['AE26', 'AE27', 'AE28', 'AE29']
    aspen_ = Property('Aspen Park Rentals', sherwood, asp_min, asp_max, asp_vac,
                      min_asp_xl, max_asp_xl, vac_asp_xl)
    auto_updater(aspen_)

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

def sherwood_updater(sherwood):
    """Call update functions to update excel cells per property"""
    update_tisbury(sherwood)
    update_sprucearms(sherwood)
    update_stonebridge(sherwood)
    update_greenwood(sherwood)
    update_emerald(sherwood)
    update_harmony(sherwood)
    update_aspen(sherwood)
    return