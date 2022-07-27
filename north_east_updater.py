from datetime import datetime
from helpers.column_list_update import col_list_updater
from helpers.check_date import find_current_month
from leduc_updater import update_min_column, update_max_column, update_vacancy_column, month_difference

from north_east.north_haven import north_haven_estates
from north_east.wyndham_crossing import wyndham_crossing
from north_east.carmen import carmen
from north_east.miller_ridge import miller_ridge
from north_east.greenview import greenview
from north_east.brintnell_landing import brintnell_landing
from north_east.stella_place import stella_place
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

def update_haven(ne):
    """Mayfield -> North Haven Estates"""
    hav_min, hav_vac = north_haven_estates()
    min_hav_xl = ['AC4', 'AC5', 'AC6']
    max_hav_xl = ['AD4', 'AD5', 'AD6']
    vac_hav_xl = ['AE4', 'AE5', 'AE6']
    haven_ = Property('North Haven Estates', ne, hav_min, None, hav_vac,
                      min_hav_xl, max_hav_xl, vac_hav_xl)
    auto_updater(haven_)

def update_wyndham(ne):
    """Weidner -> Wyndham Crossing"""

    min_wyn_xl = ['AC7', 'AC8', 'AC9']
    max_wyn_xl = ['AD7', 'AD8', 'AD9']
    vac_wyn_xl = ['AE7', 'AE8', 'AE9']
    wyndham_ = None
    auto_updater(wyndham_)

def update_carmen(ne):
    """Boardwalk -> Carmen"""
    car_min, car_max, car_vac = carmen()
    min_car_xl = ['AC10', 'AC11', 'AC12', 'AC13', 'AC14']
    max_car_xl = ['AD10', 'AD11', 'AD12', 'AD13', 'AD14']
    vac_car_xl = ['AE10', 'AE11', 'AE12', 'AE13', 'AE14']
    carmen_ = Property('Carmen', ne, car_min, car_max, car_vac,
                       min_car_xl, max_car_xl, vac_car_xl)
    auto_updater(carmen_)

def update_miller(ne):
    """Miller Ridge -> Miller Ridge"""
    mil_min, mil_vac = miller_ridge()
    min_mil_xl = ['AC15', 'AC16', 'AC17', 'AC18']
    max_mil_xl = ['AD15', 'AD16', 'AD17', 'AD18']
    vac_mil_xl = ['AE15', 'AE16', 'AE17', 'AE18']
    miller_ = Property('Miller Ridge', ne, mil_min, None, mil_vac,
                       min_mil_xl, max_mil_xl, vac_mil_xl)
    auto_updater(miller_)

def update_greenview(ne):
    """Broadstreet -> Greenview"""
    gre_min, gre_vac = greenview()
    min_gre_xl = ['AC19', 'AC20', 'AC21', 'AC22']
    max_gre_xl = ['AD19', 'AD20', 'AD21', 'AD22']
    vac_gre_xl = ['AE19', 'AE20', 'AE21', 'AE22']
    greenview_ = Property('Greenview', ne, gre_min, None, gre_vac, min_gre_xl,
                          max_gre_xl, vac_gre_xl)
    auto_updater(greenview_)

def update_brintnell(ne):
    """Skyline -> Brintnell Landing"""
    brn_min, brn_vac = brintnell_landing()
    min_brn_xl = ['AC23', 'AC24']
    max_brn_xl = ['AD23', 'AD24']
    vac_brn_xl = ['AE23', 'AE24']
    brint_ = Property('Brintnell landing', ne, brn_min, None, brn_vac,
                      min_brn_xl, max_brn_xl, vac_brn_xl)
    auto_updater(brint_)

def update_stella(ne):
    """First Service -> Stella Place"""
    ste_min, ste_vac = stella_place()
    min_ste_xl = ['AC25', 'AC26']
    max_ste_xl = ['AD25', 'AD26']
    vac_ste_xl = ['AE25', 'AE26']
    stella_ = Property('Stella Place', ne, ste_min, None, ste_vac, min_ste_xl,
                       max_ste_xl, vac_ste_xl)
    auto_updater(stella_)

def update_hollick(ne):
    """Realstar -> Hollick Kenyon"""

    min_ken_xl = ['AC27', 'AC28', 'AC29']
    max_ken_xl = ['AD27', 'AD28', 'AD29']
    vac_ken_xl = ['AE27', 'AE28', 'AE29']
    hollick_ = None
    auto_updater(hollick_)

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

def north_east_updater(ne):
    """Call update functions to update excel cells per property"""
    update_haven(ne)
    # update_wyndham(ne)
    update_carmen(ne)
    update_miller(ne)
    update_greenview(ne)
    update_brintnell(ne)
    update_stella(ne)
    #update_hollick(ne)
    return