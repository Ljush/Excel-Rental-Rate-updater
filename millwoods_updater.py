from datetime import datetime
from helpers.column_list_update import col_list_updater
from helpers.check_date import find_current_month
from millwoods.millwoods_properties import *
from leduc_updater import update_min_column, update_max_column, update_vacancy_column, month_difference
# from millwoods.laurel_meadows import laurel_meadows
# from millwoods.laurel_gardens import laurel_gardens
# from millwoods.ridgewood_court import ridgewood_court
# from millwoods.ascot_court import ascot_court
# from millwoods.amblewood_terrace import amblewood_terrace
# from millwoods.leewood_village import leewood_village
# from millwoods.sandstone_pointe import sandstone_pointe
# from millwoods.millcrest_apts import millcrest_apts
# from millwoods.hillview_park import hillview_park
# from millwoods.ridgewood_manor import ridgewood_manor
# from millwoods.ridgewood_park import ridgewood_park
# from millwoods.avalon_court import avalon_court

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

def update_laurel_meadows(millwoods):
    """Broadstreet -> Laurel Meadows"""
    lau_min, lau_vac = laurel_meadows()
    min_mead_xl = ['AC4', 'AC5', 'AC6']
    max_mead_xl = ['AD4', 'AD5', 'AD6']
    mead_vac_xl = ['AE4', 'AE5', 'AE6']
    meadows_ = Property('Laurel Meadows', millwoods, lau_min, None, lau_vac,
                        min_mead_xl, max_mead_xl, mead_vac_xl)
    auto_updater(meadows_)

def update_laurel_gardens(millwoods):
    """Broadstreet -> Laurel Gardens"""
    lau_min, lau_vac = laurel_gardens()
    min_gar_xl = ['AC7']
    max_gar_xl = ['AD7']
    gar_vac_xl = ['AE7']
    gardens_ = Property('Laurel Gardens', millwoods, lau_min, None, lau_vac,
                        min_gar_xl, max_gar_xl, gar_vac_xl)
    auto_updater(gardens_)

def update_ridgewood_court(millwoods):
    """Parabelle -> Ridgewood Court"""
    court_min, court_max, court_vac = ridgewood_court()
    min_rid_xl = ['AC8', 'AC9']
    max_rid_xl = ['AD8', 'AD9']
    rid_vac_xl = ['AE8', 'AE9']
    court_ = Property('Ridgewood Court', millwoods, court_min, court_max, court_vac,
                      min_rid_xl, max_rid_xl, rid_vac_xl)
    auto_updater(court_)

def update_ascot(millwoods):
    """Parabelle -> Ascot Court"""
    asc_min, asc_max, vac_asc = ascot_court()
    min_asc_xl = ['AC10', 'AC11']
    max_asc_xl = ['AD10', 'AD11']
    asc_vac_xl = ['AE10', 'AE11']
    ascot_ = Property('Ascot Court', millwoods, asc_min, asc_max, vac_asc,
                      min_asc_xl, max_asc_xl, asc_vac_xl)
    auto_updater(ascot_)

def update_amblewood(millwoods):
    """Parabelle -> Amblewood Terrace"""
    wood_min, wood_max, vac_wood = amblewood_terrace()
    min_wood_xl = ['AC12', 'AC13', 'AC14', 'AC15']
    max_wood_xl = ['AD12', 'AD13', 'AD14', 'AD15']
    wood_vac_xl = ['AE12', 'AE13', 'AE14', 'AE15']
    amble_ = Property('Amblewood Terrace', millwoods, wood_min, wood_max, vac_wood, 
                      min_wood_xl, max_wood_xl, wood_vac_xl)
    auto_updater(amble_)

def update_leewood(millwoods):
    """Parabelle -> Leewood Village"""
    lee_min, lee_max, lee_vac = leewood_village()
    min_lee_xl = ['AC16', 'AC17', 'AC18']
    max_lee_xl = ['AD16', 'AD17', 'AD18']
    lee_vac_xl = ['AE16', 'AE17', 'AE18']
    leewood = Property('Leewood Village', millwoods, lee_min, lee_max, lee_vac,
                       min_lee_xl, max_lee_xl, lee_vac_xl)
    auto_updater(leewood)
    
def update_sandstone(millwoods):
    """Boardwalk -> Sandstone Pointe"""
    sand_min, sand_max, vac_sand = sandstone_pointe()
    min_sand_xl = ['AC19', 'AC20', 'AC21']
    max_sand_xl = ['AD19', 'AD20', 'AD21']
    sand_vac_xl = ['AE19', 'AE20', 'AE21']
    sand_ = Property('Sandstone Pointe', millwoods, sand_min, sand_max, vac_sand,
                     min_sand_xl, max_sand_xl, sand_vac_xl)
    auto_updater(sand_)

def update_millcrest(millwoods):
    """Mayfield -> Millcrest Apartments"""
    mill_min, mill_vac = millcrest_apts()
    min_mill_xl = ['AC22', 'AC23', 'AC24']
    max_mill_xl = ['AD22', 'AD23', 'AD24']
    mill_vac_xl = ['AE22', 'AE23', 'AE24']
    mill_ = Property('Millcrest Apartments', millwoods, mill_min, None, mill_vac,
                     min_mill_xl, max_mill_xl, mill_vac_xl)
    auto_updater(mill_)
    
def update_hillview(millwoods):
    """Aim real estate -> hillview park"""
    hill_min, hill_vac = hillview_park()
    min_hill_xl = ['AC25', 'AC26']
    max_hill_xl = ['AD25', 'AD26']
    hill_vac_xl = ['AE25', 'AE26']
    hillview_ = Property('Hillview Park', millwoods, hill_min, None, hill_vac,
                         min_hill_xl, max_hill_xl, hill_vac_xl)
    auto_updater(hillview_)
    
def update_ridgewood_manor(millwoods):
    """Mayfield -> Ridgewood Manor"""
    wood_min, wood_vac = ridgewood_manor()
    min_man_xl = ['AC27', 'AC28', 'AC29']
    max_man_xl = ['AD27', 'AD28', 'AD29']
    vac_man_xl = ['AE27', 'AE28', 'AE29']
    manor_ = Property('Ridgewood manor', millwoods, wood_min, None, wood_vac, 
                      min_man_xl, max_man_xl, vac_man_xl)
    auto_updater(manor_)

def update_ridgewood_park(millwoods):
    """Mayfield -> Ridgewood Park"""
    park_min, vac_park = ridgewood_park()
    min_park_xl = ['AC30', 'AC31', 'AC32']
    max_park_xl = ['AD30', 'AD31', 'AD32']
    park_vac_xl = ['AE30', 'AE31', 'AE32']
    park_ = Property('Ridgewood Park', millwoods, park_min, None, vac_park,
                     min_park_xl, max_park_xl, park_vac_xl)
    auto_updater(park_)

def update_avalon(millwoods):
    """Avenue Living -> Avalon Court"""
    ava_min, ava_max, ava_vac = avalon_court()
    min_ava_xl = ['AC33', 'AC34', 'AC35']
    max_ava_xl = ['AD33', 'AD34', 'AD35']
    ava_vac_xl = ['AE33', 'AE34', 'AE35']
    avalon_ = Property('Avalon Court', millwoods, ava_min, ava_max, ava_vac,
                       min_ava_xl, max_ava_xl, ava_vac_xl)
    auto_updater(avalon_)


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

def millwoods_updater(millwoods):
    """Call update functions to update excel cells per property"""
    update_laurel_meadows(millwoods)
    update_laurel_gardens(millwoods)
    update_ridgewood_court(millwoods)
    update_ascot(millwoods)
    update_amblewood(millwoods)
    update_leewood(millwoods)
    update_sandstone(millwoods)
    update_millcrest(millwoods)
    update_hillview(millwoods)
    update_ridgewood_manor(millwoods)
    update_ridgewood_park(millwoods)
    update_avalon(millwoods)
    return