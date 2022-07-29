from openpyxl.comments import Comment
from datetime import datetime
from helpers.column_list_update import col_list_updater
from helpers.check_date import find_current_month

from southwest.southwest_property import *
# from southwest.ashbrookcourt_grabber import ashbrook
# from southwest.fairmont_village import fairmont_village
# from southwest.meadowview_manor import meadowview_manor
# from southwest.southwood_arms import southwood_arms
# from southwest.rideau_place_grabber import rideau_place
# from southwest.pineridge_grabber import pineridge
# from southwest.bluequill_grabber import blue_quill
# from southwest.the_village import the_village
# # from wellington_court import wellington_court # issues with JS in website?
# from southwest.cornerstone import cornerstone_callaghan
# from southwest.portofino import portofino_suites
# from southwest.park_place import park_place_south
'''
Updating excel sheets with Openpyxl
https://medium.com/gustavorsantos/how-to-update-excel-using-python-f2d24bab7922
https://www.geeksforgeeks.org/how-to-automate-an-excel-sheet-in-python/

Openpyxl documentation
https://openpyxl.readthedocs.io/en/stable/
check_excel_date(sheet, current_time)
https://openpyxl.readthedocs.io/en/latest/tutorial.html#loading-from-a-file
'''
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


def update_cornerstone(sw):
    '''Broadstreet -> Cornerstone at Callaghan'''
    stone_min, stone_vacant = cornerstone_callaghan()
    min_stone_xl = ['AC4', 'AC5', 'AC6', 'AC7', 'AC8']
    max_stone_xl = ['AD4', 'AD5', 'AD6', 'AD7', 'AD8']
    stone_xl_vac = ['AE4', 'AE5', 'AE6', 'AE7', 'AE8']
    _cornerstone = Property('Cornerstone', sw, stone_min, None, stone_vacant, min_stone_xl,
                            max_stone_xl, stone_xl_vac)
    auto_updater(_cornerstone)
    
def update_portofino(sw):
    """Skyline -> Portofino Suites"""
    port_min, port_vacant = portofino_suites()
    min_port_xl = ['AC9', 'AC10', 'AC11', 'AC12']
    max_port_xl = ['AD9', 'AD10', 'AD11', 'AD12']
    port_xl_vac = ['AE9', 'AE10', 'AE11', 'AE12']
    _portofino = Property('Portofino', sw, port_min, None, port_vacant, min_port_xl,
                          max_port_xl, port_xl_vac)
    auto_updater(_portofino)

def update_ashbrook(sw):
    '''Parabelle -> Ashbrook Court'''
    ash_min, ash_max, ash_vac = ashbrook()
    min_ash_xl = ['AC13', 'AC14', 'AC15', 'AC16']
    max_ash_xl = ['AD13', 'AD14', 'AD15', 'AD16']
    ash_xl_vac = ['AE13', 'AE14', 'AE15', 'AE16']
    ashbrook_ = Property('Ashbrook', sw, ash_min, ash_max, ash_vac,
                         min_ash_xl, max_ash_xl, ash_xl_vac)
    auto_updater(ashbrook_)

def update_parkplace(sw):
    """Weidner -> Park Place South"""
    park_min, park_vac = park_place_south()
    min_park_xl = ['AC17', 'AC18', 'AC19', 'AC20']
    max_park_xl = ['AD17', 'AD18', 'AD19', 'AD20']
    park_vac_xl = ['AE17', 'AE18', 'AE19', 'AE20']
    parkplace = Property('Park Place', sw, park_min, None, park_vac, 
                         min_park_xl, max_park_xl, park_vac_xl)
    auto_updater(parkplace)
    
def update_wellington_court(sw):
    """Realstar -> Wellington Court"""
    pass

def update_boardwalk(sw):
    """Boardwalk -> Fairmont Village + Meadowview Manor"""
    properties = []
    # fairmont village
    fairmont_min, fairmont_max, fairmont_vacant = fairmont_village()
    min_fair_xl = ['AC28', 'AC29', 'AC30', 'AC31']
    max_fair_xl = ['AD28', 'AD29', 'AD30', 'AD31']
    fair_xl_vac = ['AE28', 'AE29', 'AE30', 'AE31']
    fairmont_ = Property('Fairmont', sw, fairmont_min, fairmont_max, fairmont_vacant,
                         min_fair_xl, max_fair_xl, fair_xl_vac)
    properties.append(fairmont_)

    # meadowview manor
    meadow_min, meadow_max, meadow_vacant = meadowview_manor()
    min_mead_xl = ['AC32', 'AC33', 'AC34']
    max_mead_xl = ['AD32', 'AD33', 'AD34']
    mead_xl_vac = ['AE32', 'AE33', 'AE34']
    _meadowview = Property('Meadowview', sw, meadow_min, meadow_max, meadow_vacant,
                           min_mead_xl, max_mead_xl, mead_xl_vac)
    properties.append(_meadowview)
    # add boardwalk properties to excel sheet
    for current_property in properties:
        auto_updater(current_property)

def update_mayfield(sw):
    """Mayfield -> Southwood Arms + Rideau Place"""
    # Southwood Arms
    wood_min, wood_vacant = southwood_arms()
    min_wood_xl = ['AC35', 'AC36', 'AC37', 'AC38']
    max_wood_xl = ['AD35', 'AD36', 'AD37', 'AD38']
    wood_xl_vac = ['AE35', 'AE36', 'AE37', 'AE38']
    south_wood = Property('Southwood Arms', sw, wood_min, None, wood_vacant, 
                          min_wood_xl, max_wood_xl, wood_xl_vac)
    auto_updater(south_wood)

    # Rideau Place
    rideau_min, rideau_vacant = rideau_place()
    min_rid_xl = ['AC39', 'AC40', 'AC41']
    max_rid_xl = ['AD39', 'AD40', 'AD41']
    rid_xl_vac = ['AE39', 'AE40', 'AE41']
    _rideau = Property('Rideau', sw, rideau_min, None, rideau_vacant,
                       min_rid_xl, max_rid_xl, rid_xl_vac)
    auto_updater(_rideau)

def update_village(sw):
    '''Midwest -> The village at southgate'''
    vil_min, vil_vac = the_village()
    vil_min_xl = ['AC50', 'AC51', 'AC52', 'AC53', 'AC54', 'AC55', 'AC56',
                  'AC57', 'AC58']
    vil_max_xl = ['AD50', 'AD51', 'AD52', 'AD53', 'AD54', 'AD55', 'AD56',
                  'AD57', 'AD58']
    vil_vac_xl = ['AE50', 'AE51', 'AE52', 'AE53', 'AE54', 'AE55', 'AE56',
                  'AE57', 'AE58']
    vil_ = Property('Village-Midwest', sw, vil_min, None, vil_vac, vil_min_xl, 
                    vil_max_xl, vil_vac_xl)
    auto_update_theVillage(vil_)

def update_harpar(sw):
    """Har-par -> Pineridge + Blue Quill Gardens"""
    # Pineridge
    pine_min, pine_vac = pineridge()
    min_pine_xl = ['AC42', 'AC43', 'AC44', 'AC45', 'AC46']
    max_pine_xl = ['AD42', 'AD43', 'AD44', 'AD45', 'AD46']
    pine_xl_vac = ['AE42', 'AE43', 'AE44', 'AE45', 'AE46']
    pine_ridge_obj = Property('Pineridge', sw, pine_min, None, pine_vac,
                              min_pine_xl, max_pine_xl, pine_xl_vac)
    auto_updater(pine_ridge_obj)

    # Blue Quill Gardens
    blue_min, blue_vac = blue_quill()
    min_blue_xl = ['AC47', 'AC48', 'AC49']
    max_blue_xl = ['AD47', 'AD48', 'AD49']
    blue_xl_vac = ['AE47', 'AE48', 'AE49']
    BLUE_ = Property('Blue Quill', sw, blue_min, None, blue_vac, min_blue_xl,
                     max_blue_xl, blue_xl_vac)
    auto_updater(BLUE_)

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
       letter_first (dict) = cypher of letters to numbers, A=1, D=4, M=13, etc.
       num_first (dict)    = cypher of letters to numbers, 1=A, 4=D, 14=N, etc.
       current_month       = datetime object of the current month
       month_int, year_int = int values of the current month/year (unused)
       month_dict (unused) = similar to letter/num_first cyphers but with month names
       time_difference(int) = int value of number of months calculated since april 2022
       col_multiplier (int) = int value to use for col_list_updater to update excel list of cells for current column
       available_final(list)= list of excel cells for vacancy to reflect the current month
       min_final/max_final  = lists of excel cells similar to available_final.'''
    current_month, month_int, year_int, month_dict, curr_time = find_current_month()
    time_difference = month_difference(datetime(2022, 4, 1), curr_time)
    col_multiplier = (5 * time_difference)
    
    # update the list of cells per excel column for current month
    available_final = col_list_updater(property.xlsx_vacant, col_multiplier)
    min_final = col_list_updater(property.xlsx_min, col_multiplier)
    max_final = col_list_updater(property.xlsx_max, col_multiplier)

    # cell updater functions specific to park place south
    if property.name == 'Park Place':
        update_park_place_min(min_final, property)
        update_park_place_vacancy(available_final, property)
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

            elif unit_rate[1] == ',':
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
                    property.sheet[max] = unit_rate
                    property.sheet[max].comment = Comment(
                        'No max rate.', 'Auto-updated')
                    break

                elif unit_rate[1] == ',':
                    unit_rate = (unit_rate[0] + unit_rate[2:])
                property.sheet[max] = int(unit_rate)
                break
    return

def update_vacancy_column(column_list, property):
    """update the availability column per property
        >Called by auto_updater(property)"""
    for i in column_list:
        for j in property.vacancy_list:
            # 'W'/'A' comes from cornerstone vacancy list
            if j == 'Waitlist' or j == 'W' or j == 'A':
                property.sheet[i].value = 'Waitlist'
                property.vacancy_list.remove(j)
                break
            if j == 'No Info':
                property.sheet[i].value = 'No Info'
                property.vacancy_list.remove(j)
                break
            if j is False:
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

def update_park_place_min(col_list, property):
    """Updates the min rate column specifically for park place"""
    for min in col_list:
        for unit in property.min_dict:
            unit_rate = property.min_dict.pop(unit)
            if unit_rate == '0':
                property.sheet[min].comment = Comment('No min rate.', 'Auto-updated')
                break
            else:
                property.sheet[min] = int(unit_rate)
                break

def update_park_place_vacancy(col_list, property):
    """Updates the vacancy (availability) column specifically for 
       park place south"""
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
            
def auto_update_theVillage(property):
    '''same logic as auto_updater(property) except meant to fix the
    specific cases with midwest's The Village and how they format their 
    suite listings.'''
    current_month, month_int, year_int, month_dict, curr_time = find_current_month()
    time_difference = month_difference(datetime(2022, 4, 1), curr_time)
    col_multiplier = (5 * time_difference)
    # update the list of cells per excel column for current month
    available_final = col_list_updater(property.xlsx_vacant, col_multiplier)
    min_final = col_list_updater(property.xlsx_min, col_multiplier)
    sq_list_default = ['530', '646', '665',
                       '775', '808', '820', '880', '967', '1271']
    # dictionary to make square ft of village suite size to correct unit cell when updating
    sq_ft_dict = dict()
    count_ = 0
    for q in sq_list_default:
        holder = min_final[count_]
        sq_ft_dict[q] = holder
        count_ += 1
    # updates the min rate column of the Village at southgate; double checking
    # for suite types that are not posted; likely to assume unavailable
    for min in sq_ft_dict:
        if sq_ft_dict == {}:
            property.sheet[sq_ft_dict.get(min)] = Comment('No min rate.', 'Auto-updated')
            break
        for unit in property.min_dict:
            if min == unit:
                unit_rate = property.min_dict.pop(unit)
                # adjust rates; "1,250" to "1250" <<< example
                if unit_rate[1] == ',':
                    unit_rate = (unit_rate[0] + unit_rate[2:])
                property.sheet[sq_ft_dict.get(min)] = int(unit_rate)
                break
            else:
                property.sheet[sq_ft_dict.get(min)].comment = Comment('No listing posted.', 'Auto-updated')
                break
    '''No maximum rent section for the village currently.
       We just won't worry about that right now.'''
    
    '''Just going to update entire availablity column with "No Info" because
       the website doesn't specify whether or not a type of suite is available or not 
       and likely just wants you to apply for a suite regardless of availability(May 2022)'''
    for i in available_final:
        property.sheet[i].value = 'No Info'
        temp_str_1 = 'Likely wants an application'
        temp_str_2 = ' instead of updating postings on the website'
        temp_str = temp_str_1 + temp_str_2
        property.sheet[i].comment = Comment(temp_str, 'Auto-updater')
    return

def southwest_updater(sw):
    """Call update functions to update excel cells per property"""
    update_cornerstone(sw)
    update_portofino(sw)
    update_ashbrook(sw)
    update_parkplace(sw)
    update_boardwalk(sw)
    update_mayfield(sw)
    update_harpar(sw)
    update_village(sw)
    return