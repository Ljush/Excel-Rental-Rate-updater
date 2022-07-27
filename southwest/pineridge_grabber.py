import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''

def pineridge():
    """First complete property updater script as of April 2022. 
    Considering this a rough draft until all other properties for the other
    sheets in Alberta are created, and followed through testing of a few months
    throughout the year. 
    
    Since these scripts involve webscraping to gather such a small but albeit
    specific range of information, I expect these to eventually be 
    rewritten to be more readily and easily maintained by someone other 
    than myself simply because I believe that some of the competitors will 
    sell the property to a different company and/or change the general 
    structure of their property website in general.
    
    For Version 1.0-Pineridge_grabber.py, 'body div.row.property-unit' table is
    parsed and split into a list of lists (suite_info), each list containing 
    information regarding each unique unit type. For loops are used to 
    traverse the list of lists (suite_info) to pickout general information 
    pertaining to the current unit type we are looking for.
    

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = pineridge(); print(d, x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)

    Vars:
        pineridge_pg = Grabs the HTML link for the Pineridge apartments owned
                       har-par.
        pineridge_soup = BeautifulSoup call to parse the pineridge website.

        pr_suite_types (list) = list to hold the types of units pineridge 
                                provides. They will be placed into 
                                pineridge_rents alongside the rent rate per unit
                                
        pr_suite_desc(str)= pineridge_soup.select('body div.row.property-unit')
                            to retrieve the panel holding all the information
                            regarding the unit types, rent rates + info of units
        
        suite_info (list) = list to hold the information gathered from
                            pr_suite_desc. 
 
    Returns:
        pineridge_rents (dictionary) = holds unit types + rent rates for each
                                       unit type.
        is_vacant (list) = list of booleans to represent which unit type
                           has available vacancies or not."""
    pineridge_rents = dict()
    pr_suite_types = []
    is_vacant = []
    suite_info = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    pine_r = requests.get('http://har-par.com/properties.php?PropertyID=141')
    pineridge_soup = BeautifulSoup(pine_r.content, 'html.parser')
    pr_suite_desc = pineridge_soup.select('body div.row.property-unit')
    
    for suite in pr_suite_desc:
        suite_info.append(suite.text.replace('\n', ' ').split())
        
    # counter for creating the dictionary of rent rates per unit unit type 
    count = 0
    for data in suite_info:
        # WAITLISTING for vacancy is not an option at pineridge currently
        # 'No', 'Vacancy'] ~ No vacant units
        if data[-1] == 'Vacancy':
            is_vacant.append(False)
        # 'Vacancy', 'Apply'] ~ Vacant units for this type of unit
        if data[-1] == 'Apply':
            is_vacant.append(True)
        # for looping through the current list in the list of lists (suite_info) 
        for info in data:
            # add bachelor to the types of suites
            if data[0] == 'Bachelor' and len(pr_suite_types) == 0:
                pr_suite_types.append(data[0])
                data.remove(info)
            # removes odd $xxxrent elements from a list
            if info[0] == '$' and info[-1] == 't':
                data.remove(info)
                continue
            # removes monetary list elements that are deposits or not rent specific
            if info[0] == '$' and int(info[1:]) < 698:
                data.remove(info)
                continue
            # add the different types of suits to the list; noted as 1 bedroom,
            # 2 bedroom etc as the first 2 elements of the list for that unit type
            if data[0].isnumeric():
                if data[1].isalpha():
                    new_type = str(data[0]) + f' {data[1]}'
                    pr_suite_types.append(new_type)
                    data.remove(info)
            # add descriptor den to the unit type that advertises having a den
            if info == 'Den':
                pr_suite_types[-1] = pr_suite_types[-1] + ' + Den'
                data.remove(info)
            # add descriptor loft to the unit type that advertises having a loft
            if info == 'loft':
                pr_suite_types[-1] = '1 bedroom + loft'
                data.remove(info)
            # creates dictionary key: value with the found rent value corresponding
            # to the type of unit from pr_suite_types
            # and removes '$' from the actual rental rate
            if info[0] == '$': 
                pineridge_rents[pr_suite_types[count]] = info[1:]
                data.remove(info)
                # updating the counter to keep up with the pr_suite_types index
                count += 1
                
    reordered_rents = dict()
    reordered_rents['Bachelor'] = pineridge_rents['Bachelor']
    reordered_rents['1 Bedroom'] = pineridge_rents['1 Bedroom']
    reordered_rents['1 bedroom + loft'] = pineridge_rents['1 bedroom + loft']
    reordered_rents['2 Bedrooms'] = pineridge_rents['2 Bedrooms']
    reordered_rents['2 Bedrooms + Den'] = pineridge_rents['2 Bedrooms + Den']
    
    is_vacant_reordered = [is_vacant[0], is_vacant[1], is_vacant[4],
                           is_vacant[2], is_vacant[3]]
    
    #print(reordered_rents)
    #print(pineridge_rents, is_vacant)
    return reordered_rents, is_vacant_reordered
# re-do the rents, 1bed + loft is mislabelled

def pineridge_():
    pineridge_rents = dict()
    pr_suite_types = []
    is_vacant = []
    suite_info = []
    url = 'http://har-par.com/properties.php?PropertyID=141'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    pine_r = requests.get(url, headers=headers)
    pineridge_soup = BeautifulSoup(pine_r.content, 'html.parser')
    pr_suite_desc = pineridge_soup.select('body div.row.property-unit')

if __name__ == '__main__':
    pineridge()