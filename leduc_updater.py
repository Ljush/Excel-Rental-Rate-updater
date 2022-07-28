from openpyxl.comments import Comment
from datetime import datetime
from helpers.column_list_update import col_list_updater
from helpers.check_date import find_current_month
from leduc.leduc_properties import *
# from leduc.west_haven import west_haven_terrace
# from leduc.macewan_greens import macewan_greens
# from leduc.bridgewood_apts import bridgewood_apts
# from leduc.leduc_mansion import leduc_mansion
# from leduc.bridgeport_manor import bridgeport_manor
# from leduc.richmond_arms import richmond_arms
# from leduc.unico_apts import unico_apts
# from leduc.edgewood_estates import edgewood_estates
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

def update_west_haven(leduc):
    """Boardstreet -> West Haven Terrace"""
    haven_min, haven_vacant = west_haven_terrace()
    hav_min_xl = ['AB4', 'AB5']
    hav_max_xl = ['AC4', 'AC5']
    hav_vac_xl = ['AD4', 'AD5']
    haven_ = Property('West Haven Terrace', leduc, haven_min, None, haven_vacant,
                      hav_min_xl, hav_max_xl, hav_vac_xl)
    auto_updater(haven_)

def update_macewan_greens(leduc):
    """Macewan Greens"""
    macewan_min, macewan_vacant = macewan_greens()
    mac_min_xl = ['AB6', 'AB7', 'AB8', 'AB9', 'AB10', 'AB11']
    mac_max_xl = ['AC6', 'AC7', 'AC8', 'AC9', 'AC10', 'AC11']
    mac_vac_xl = ['AD6', 'AD7', 'AD8', 'AD9', 'AD10', 'AD11']
    macewan_ = Property('Macewan Greens', leduc, macewan_min, None, 
                        macewan_vacant, mac_min_xl, mac_max_xl, mac_vac_xl)
    auto_updater(macewan_)

def update_bridgewood(leduc):
    """Woodsmere -> Bridgewood Apts"""
    brig_min, brig_vac = bridgewood_apts()
    brig_min_xl = ['AB12', 'AB13', 'AB14', 'AB15', 'AB16']
    brig_max_xl = ['AC12', 'AC13', 'AC14', 'AC15', 'AC16']
    brig_vac_xl = ['AD12', 'AD13', 'AD14', 'AD15', 'AD16']
    bridgewood_ = Property('Bridgewood Apts', leduc, brig_min, None, brig_vac,
                           brig_min_xl, brig_max_xl, brig_vac_xl)
    auto_updater(bridgewood_)

def update_mansion(leduc):
    """Braden Equities -> Leduc Mansion""" 
    man_min, man_vac = leduc_mansion()
    man_min_xl = ['AB17', 'AB18', 'AB19', 'AB20']
    man_max_xl = ['AC17', 'AC18', 'AC19', 'AC20']
    man_vac_xl = ['AD17', 'AD18', 'AD19', 'AD20']
    mansion_ = Property('Leduc Mansion', leduc, man_min, None, man_vac,
                        man_min_xl, man_max_xl, man_vac_xl)
    auto_updater(mansion_)

def update_bridgeport(leduc):
    """Greystone -> Bridgeport Manor"""
    port_min, port_max, port_vac = bridgeport_manor()
    port_min_xl = ['AB21']
    port_max_xl = ['AC21']
    port_vac_xl = ['AD21']
    bridgeport_ = Property('Bridgeport Manor', leduc, port_min, port_max, 
                           port_vac, port_min_xl, port_max_xl, port_vac_xl)
    auto_updater(bridgeport_)
    
def update_harpar_leduc(leduc):
    """Harpar -> Richmond Arms + Unico Apts"""
    rich_min, rich_vac = richmond_arms()
    rich_min_xl = ['AB22', 'AB23', 'AB24']
    rich_max_xl = ['AC22', 'AC23', 'AC24']
    rich_vac_xl = ['AD22', 'AD23', 'AD24']
    richmond_ = Property('Richmond Arms', leduc, rich_min, None, rich_vac, 
                         rich_min_xl, rich_max_xl, rich_vac_xl)
    auto_updater(richmond_)

    unico_min, unico_vac = unico_apts()
    uni_min_xl = ['AB25', 'AB26', 'AB27']
    uni_max_xl = ['AC25', 'AC26', 'AC27']
    uni_vac_xl = ['AD25', 'AD26', 'AD27']
    unico_ = Property('Unico Apts', leduc, unico_min, None, unico_vac,
                      uni_min_xl, uni_max_xl, uni_vac_xl)
    auto_updater(unico_)

def update_edgewood(leduc):
    """Weidner -> Edgewood Estates"""
    edg_min, edg_vac = edgewood_estates()
    edge_min_xl = ['AB28', 'AB29', 'AB30']
    edge_max_xl = ['AC28', 'AC29', 'AC30']
    edge_vac_xl = ['AD28', 'AD29', 'AD30']
    edgewood_ = Property('Edgewood Estates', leduc, edg_min, None, edg_vac,
                         edge_min_xl, edge_max_xl, edge_vac_xl)
    auto_updater(edgewood_)

def check_excel_date(sheet, current_time):
    for column in sheet.iter_cols(min_row=2, max_col=1800, max_row=2):
        for cell in column:
            if cell.value == current_time:
                return True
            else:
                return False

def month_difference(time1, time2):
    '''time 1 should always be april 1st 2022 0:00:00 for this year(2022)(prob)
    return the difference between 2 given times in form of an int # of months'''
    return (abs((time1.year - time2.year) * 12 + (time1.month - time2.month)))


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

    if property.name == 'Edgewood Estates':
        update_edgewood_min(min_final, property)
        update_edgewood_vacancy(available_final, property)
    else:
        # update the current month's section of minimum rental rates
        update_min_column(min_final, property)
        # update the current month's section of maximum rental rates
        update_max_column(max_final, property)
        # update the current month's section of availabliity column per property
        update_vacancy_column(available_final, property)
    return


def update_min_column(column_list, property):
    """Update the minimum rate column per property
        >Called by auto_updater(property)"""
    for min in column_list:
        if property.min_dict == {}:
            property.sheet[min].comment = Comment('No listing posted.',
                                                  'Auto-updated')
            break
        for unit in property.min_dict:
            unit_rate = property.min_dict.pop(unit)

            if unit_rate == '':
                property.sheet[min] = unit_rate
                property.sheet[min].comment = Comment(
                    'No min rate.', 'Auto-updated')
                break

            if unit_rate == '0':
                property.sheet[min].comment = Comment(
                    'No min rate.', 'Auto-updated')
                break
            
            if len(unit_rate) > 1:
                if unit_rate[1] == ',':
                    unit_rate = (unit_rate[0] + unit_rate[2:])
            property.sheet[min] = int(unit_rate)
            break
    return


def update_max_column(column_list, property):
    """Update the maximum rate column per property
       >Called by auto_updater(property)"""
    if property.max_dict != None:
        for max in column_list:
            if property.max_dict == {}:
                property.sheet[max].comment = Comment(
                    'No max rate.', 'Auto-updated')
                break
            for unit_ in property.max_dict:
                unit_rate = property.max_dict.pop(unit_)

                if unit_rate == '':
                    #property.sheet[max] = unit_rate
                    property.sheet[max].comment = Comment(
                        'No max rate.', 'Auto-updated')
                    break

                if unit_rate == '0':
                    property.sheet[max].comment = Comment(
                    'No max rate.', 'Auto-updated')
                break
            break
    return


def update_vacancy_column(column_list, property):
    """update the availability column per property
        >Called by auto_updater(property)"""
    for i in column_list:
        for j in property.vacancy_list:
            if j == 'Waitlist' or j == 'W' or j == 'A':
                property.sheet[i].value = 'Waitlist'
                property.vacancy_list.remove(j)
                break
            if j == 'No Info':
                property.sheet[i].value = 'No Info'
                property.vacancy_list.remove(j)
                break
            if j is False or j == '0':
                property.sheet[i].value = 'No'
                property.vacancy_list.remove(j)
                break
            if j is True:
                property.sheet[i].value = 'Yes'
                property.vacancy_list.remove(j)
                break
            else:
                property.sheet[i].value = 'Yes'
                property.sheet[i].comment = Comment(
                    f'{j} suite left', 'Auto-updated')
                property.vacancy_list.remove(j)
                break
    return


def update_edgewood_min(col_list, property):
    """Updates the min rate column specifically for edgewood estates"""
    for min in col_list:
        for unit in property.min_dict:
            unit_rate = property.min_dict.pop(unit)
            if unit_rate == '0':
                property.sheet[min].comment = Comment(
                    'No min rate.', 'Auto-updated')
                break
            else:
                property.sheet[min] = int(unit_rate)
                break


def update_edgewood_vacancy(col_list, property):
    """Updates the vacancy (availability) column specifically for 
       edgewood estates"""
    for i in col_list:
        for j in property.vacancy_list:
            if j == '0':
                property.sheet[i].value = 'No'
                property.vacancy_list.remove(j)
                break
            else:
                property.sheet[i].value = 'Yes'
                property.sheet[i].comment = Comment(
                    f'{j} suites left', 'Auto-updated')
                property.vacancy_list.remove(j)
                break

def leduc_updater(leduc):
    """Call update functions to update excel cells per property"""
    update_west_haven(leduc)
    update_macewan_greens(leduc)
    #update_bridgewood(leduc)
    update_mansion(leduc)
    update_bridgeport(leduc)
    update_harpar_leduc(leduc)
    #update_edgewood(leduc)
    return