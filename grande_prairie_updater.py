from datetime import datetime
from helpers.column_list_update import col_list_updater
from helpers.check_date import find_current_month
from leduc_updater import update_min_column, update_max_column, update_vacancy_column, month_difference
from grande_prairie.grande_prairie_properties import *
# from grande_prairie.gateway import gateway
# from grande_prairie.northgate import northgate
# from grande_prairie.westmore import westmore
# from grande_prairie.lexington import lexington
# from grande_prairie.northland import northland
# from grande_prairie.willowbrook import willowbrook
# from grande_prairie.carrington import carrington
# from grande_prairie.prairie_sunrise import prairie_sunrise
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

def update_gateway(gp):
    """Woodsmere -> Gateway Apts"""
    gat_min, gat_vac = gateway()
    min_gat_xl = ['AC4', 'AC5', 'AC6', 'AC7', 'AC8']
    max_gat_xl = ['AD4', 'AD5', 'AD6', 'AD7', 'AD8']
    vac_gat_xl = ['AE4', 'AE5', 'AE6', 'AE7', 'AE8']
    gateway_ = Property('Gateway Apts', gp, gat_min, None, gat_vac, min_gat_xl,
                        max_gat_xl, vac_gat_xl)
    auto_updater(gateway_)

def update_northview(gp):
    """Northview -> Northgate Apartments, Westmore Estates"""
    nor_min, nor_vac = northgate()
    min_nor_xl = ['AC9', 'AC10']
    max_nor_xl = ['AD9', 'AD10']
    vac_nor_xl = ['AE9', 'AE10']
    northview_ = Property('Northgate Apartments', gp, nor_min, None, nor_vac,
                          min_nor_xl, max_nor_xl, vac_nor_xl)
    auto_updater(northview_)

    west_min, west_vac = westmore()
    min_est_xl = ['AC11', 'AC12']
    max_est_xl = ['AD11', 'AD12']
    vac_est_xl = ['AE11', 'AE12']
    westmore_ = Property('Westmore Estates', gp, west_min, None, west_vac,
                         min_est_xl, max_est_xl, vac_est_xl)
    auto_updater(westmore_)

def update_lexington(gp):
    """NA Leaseholds -> Lexington"""
    lex_min, lex_vac = lexington()
    min_lex_xl = ['AC13', 'AC14', 'AC15']
    max_lex_xl = ['AD13', 'AD14', 'AD15']
    vac_est_xl = ['AE13', 'AE14', 'AE15']
    lexington_ = Property('Lexington', gp, lex_min, None, lex_vac, min_lex_xl,
                          max_lex_xl, vac_est_xl)
    auto_updater(lexington_)

def update_northland(gp):
    """Northland Mgmt -> Northland"""
    nor_min, nor_vac = northland()
    min_lan_xl = ['AC16', 'AC17', 'AC18', 'AC19']
    max_lan_xl = ['AD16', 'AD17', 'AD18', 'AD19']
    vac_lan_xl = ['AE16', 'AE17', 'AE18', 'AE19']
    northland_ = Property('Northland', gp, nor_min, None, nor_vac, min_lan_xl,
                          max_lan_xl, vac_lan_xl)
    auto_updater(northland_)

def update_willowbrook(gp):
    """Highstreet -> Willowbrook"""
    wil_min, wil_max, wil_vac = willowbrook()
    min_wil_xl = ['AC20', 'AC21', 'AC22', 'AC23', 'AC24']
    max_wil_xl = ['AD20', 'AD21', 'AD22', 'AD23', 'AD24']
    vac_wil_xl = ['AE20', 'AE21', 'AE22', 'AE23', 'AE24']
    willow_ = Property('Willowbrook', gp, wil_min, wil_max, wil_vac,
                       min_wil_xl, max_wil_xl, vac_wil_xl)
    auto_updater(willow_)

def update_carrington(gp):
    """Weidner -> Carrington"""
    car_min, car_vac = carrington()
    min_car_xl = ['AC25', 'AC26', 'AC27', 'AC28']
    max_car_xl = ['AD25', 'AD26', 'AD27', 'AD28']
    vac_car_xl = ['AE25', 'AE26', 'AE27', 'AE28']
    carrington_ = Property('Carrington', gp, car_min, None, car_vac,
                           min_car_xl, max_car_xl, vac_car_xl)
    auto_updater(carrington_)

def update_prairie_sunrise(gp):
    """Boardwalk -> Prairie Sunrise Towers"""
    pra_min, pra_max, pra_vac = prairie_sunrise()
    min_sun_xl = ['AC29', 'AC30', 'AC31', 'AC32']
    max_sun_xl = ['AD29', 'AD30', 'AD31', 'AD32']
    vac_car_xl = ['AE29', 'AE30', 'AE31', 'AE32']
    sunrise_ = Property('Prairie Sunrise Towers', gp, pra_min, pra_max,
                        pra_vac, min_sun_xl, max_sun_xl, vac_car_xl)
    auto_updater(sunrise_)
    
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

def grande_prairie(gp):
    """Call update functions to update excel cells per property"""
    update_gateway(gp)
    update_northview(gp)
    update_lexington(gp)
    update_northland(gp)
    update_willowbrook(gp)
    update_carrington(gp)
    update_prairie_sunrise(gp)
    return