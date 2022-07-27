from datetime import datetime
from helpers.column_list_update import col_list_updater
from helpers.check_date import find_current_month

from leduc_updater import update_min_column, update_max_column, update_vacancy_column, month_difference
from west.morningside import morningside
from west.cedarville import cedarville
from west.west_ed_village import west_village
from west.cambrian_place import cambrian_place
from west.village_hamptons import village_hamptons
from west.webbergreens import webbergreens
from west.cambridge_west import cambridge_west
from west.tennyson_apts import tennyson_apts
'''
Updating excel sheets with Openpyxl
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

def update_boardwalk_west(west):
    """Boardwalk -> Morningside, Cedarside Apts, West Ed Village, Cambrian Place"""
    # MORNINGSIDE
    morn_min, morn_max, morn_vac = morningside()
    min_morn_xl = ['AC4', 'AC5', 'AC6', 'AC7']
    max_morn_xl = ['AD4', 'AD5', 'AD6', 'AD7']
    vac_morn_xl = ['AE4', 'AE5', 'AE6', 'AE7']
    morning = Property('Morningside', west, morn_min, morn_max, morn_vac,
                       min_morn_xl, max_morn_xl, vac_morn_xl)
    auto_updater(morning)
    # CEDARVILLE
    ced_min, ced_max, ced_vac = cedarville()
    min_ced_xl = ['AC8', 'AC9']
    max_ced_xl = ['AD8', 'AD9']
    vac_ced_xl = ['AE8', 'AE9']
    cedar = Property('Cedarville', west, ced_min, ced_max, ced_vac, min_ced_xl,
                     max_ced_xl, vac_ced_xl)
    auto_updater(cedar)
    
    # WEST ED VILLAGE
    vil_min, vil_max, vil_vac = west_village()
    min_vil_xl = ['AC10', 'AC11', 'AC12', 'AC13', 'AC14']
    max_vil_xl = ['AD10', 'AD11', 'AD12', 'AD13', 'AD14']
    vac_vil_xl = ['AE10', 'AE11', 'AE12', 'AE13', 'AE14']
    village_ = Property('West Ed Village', west, vil_min, vil_max, vil_vac,
                        min_vil_xl, max_vil_xl, vac_vil_xl)
    auto_updater(village_)
    
    # CAMBRIAN PLACE
    cam_min, cam_max, cam_vac = cambrian_place()
    min_cam_xl = ['AC15', 'AC16', 'AC17', 'AC18', 'AC19', 'AC20']
    max_cam_xl = ['AD15', 'AD16', 'AD17', 'AD18', 'AD19', 'AD20']
    vac_cam_xl = ['AE15', 'AE16', 'AE17', 'AE18', 'AE19', 'AE20']
    cambrian = Property('Cambrian Place', west, cam_min, cam_max, cam_vac,
                        min_cam_xl, max_cam_xl, vac_cam_xl)
    auto_updater(cambrian)

def update_hamptons(west):
    """Premium Rentals -> Village at Hamptons"""
    ham_min, ham_vac = village_hamptons()
    min_ham_xl = ['AC21', 'AC22']
    max_ham_xl = ['AD21', 'AD22']
    vac_ham_xl = ['AE21', 'AE22']
    hamptons = Property('Village at Hamptons', west, ham_min, None, ham_vac,
                        min_ham_xl, max_ham_xl, vac_ham_xl)
    auto_updater(hamptons)

def update_webbergreens(west):
    """Broadstreet -> Webber Greens"""
    web_min, web_max = webbergreens()
    min_web_xl = ['AC23', 'AC24', 'AC25']
    max_web_xl = ['AD23', 'AD24', 'AD25']
    vac_web_xl = ['AE23', 'AE24', 'AE25']
    webber = Property('Webber Greens', west, web_min, None, web_max, min_web_xl,
                      max_web_xl, vac_web_xl)
    auto_updater(webber)

def update_cambridge(west):
    """Weidner -> Cambridge West"""
    cam_min, cam_vac = cambridge_west()
    min_cam_xl = ['AC26', 'AC27', 'AC28']
    max_cam_xl = ['AD26', 'AD27', 'AD28']
    vac_cam_xl = ['AE26', 'AE27', 'AE28']
    cambridge = Property('Cambridge West', west, cam_min, None, cam_vac,
                         min_cam_xl, max_cam_xl, vac_cam_xl)
    auto_updater(cambridge)

def update_tennyson(west):
    """Realstar -> Tennyson Apts"""

    min_ten_xl = ['AC29', 'AC30']
    max_ten_xl = ['AD29', 'AD30']
    vac_ten_xl = ['AE29', 'AE30']
    tennyson = None
    auto_updater(tennyson)
    
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

def west_updater(west):
    """Call update functions to update excel cells per property"""
    update_boardwalk_west(west)
    update_hamptons(west)
    update_webbergreens(west)
    update_cambridge(west)
    #update_tennyson(west)
    return