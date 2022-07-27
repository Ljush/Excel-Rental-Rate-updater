import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
# much more organized and thought out website design here compared to pineridge jfc lol
def ashbrook():
    """Considering this a rough draft until all other properties for the other
    sheets in Alberta are created, and followed through testing of a few months
    throughout the year.
    
    Since these scripts involve webscraping to gather such a small but albeit
    specific range of information, I expect these to eventually be 
    rewritten to be more readily and easily maintained by someone other 
    than myself simply because I believe that some of the competitors will 
    sell the property to a different company and/or change the general 
    structure of their property website in general.
    
    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = ashbrook(); print('min', d); print('max', x); print('vacancy', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
    ash_suite_types_min (dict) - Minimum rates + unit types 
    ash_suite_types_max (dict) - Maximum rates + unit types 
    is_vacant (list)           - List of Bools for whether unit has vacancies
    
    page - calls .get() from requests to grab the ashbrook webpage
    page_parsed - parses page with BeautifulSoup for the webpage content
    
    find_vacancies_tab - .find() to grab specific class information from page (vacancy information)
    vacancy_box_data - uses findAll() to grab more specific information from find_vacancies_tab
    suite - see find_vacancies_tab; (suite and rent information)
    rents - see vacancy_box_data;
    
    Returns: >> See vars for more info
            ash_suite_types_min, ash_suite_types_max, is_vacant"""
    ash_suite_types_min = dict()
    ash_suite_types_max = dict()
    is_vacant = []

    page = requests.get('https://www.parabelle.com/apartments/3955-114-st-ashbrook')
    page_parsed = BeautifulSoup(page.content, 'html.parser')
    
    find_vacancies_tab = page_parsed.find('div', 'suite-info-container')
    vacancy_box_data = find_vacancies_tab.findAll('a')
    
    for s in vacancy_box_data:
        #print('entry:', s.text, type(s))
        if 'Available Now' in s:
            vacant = True
            is_vacant.append(vacant)
            continue
       # if 'Notify me' in s:
        else:
            vacant = False
            is_vacant.append(vacant)
            continue
        
    suite = page_parsed.find('div', 'suites-boxes')
    rents = suite.findAll('span')

    for i in rents:
        if i.text == '1 Bedroom':
            suite_type = i.text
            continue
        if i.text == '1 Bedroom + Den':
            suite_type = i.text
            continue
        if i.text == '2 Bedrooms': #and i.text[-1] == 's':
            suite_type = i.text
            continue
        if i.text == '2 Bedroom + Den': # and i.text[-1] == 'n':
            suite_type = i.text
            continue
        if i.text[5] == '$':
            minimum = i.text[6:11]
            ash_suite_types_min[suite_type] = minimum
            try:
                maximum = i.text[15:20]
                if maximum[0] == ' ':
                    ash_suite_types_max[suite_type] = ''
                    continue
                ash_suite_types_max[suite_type] = maximum
            except:
                #print('No maximum rate for this unit')
                ash_suite_types_max[suite_type] = ''
                continue
    #print('MIN RATES:', ash_suite_types_min, '\n','MAX RATES:', ash_suite_types_max)
    #print('VACANCIES:', is_vacant)
    return ash_suite_types_min, ash_suite_types_max, is_vacant

if __name__ == '__main__':
    ashbrook()