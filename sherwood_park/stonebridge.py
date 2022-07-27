import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def stonebridge():
    '''As of June 14/2022; website incorrectly redirects you when clicking on a 
    suite card; unclear about vacancy status and whether or not the rates are accurate
    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = stonebridge(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    stone_min = dict()
    is_vacant = []
    suite_types = ['1 Bedroom', '1 Bedroom +', '2 Bedroom', '3 Bedroom']
    rental_rates_min = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    one_url = 'https://www.olcl.ca/properties/cities/sherwood-park?minBeds=1'
    #two_url = 'https://www.olcl.ca/properties/cities/sherwood-park?minBeds=2'
    #three_url = 'https://www.olcl.ca/properties/cities/sherwood-park?minBeds=3'

    page_one = requests.get(one_url, headers=headers)
    #page_two = requests.get(two_url, headers=headers)
    #page_three = requests.get(three_url, headers=headers)
    
    page_one_parsed = BeautifulSoup(page_one.content, 'html.parser')

    # grab suite data about suite types and place the data into a list
    # grabbed from the 'properties' drop down section of the website since it currently is very broken and does not 
    # redirect correctly when you click on any type of suite under this property
    for i in page_one_parsed.findAll('div', 'city'):
        temp = i.text
        temp = temp.replace('\n', '')
        temp = temp.replace('\t', ' ')
        temp = temp.strip()
        city_list = temp.split()
        if city_list[0] == 'Sherwood':
            sherwood_list = (city_list[2:])

    # remove all instances of the word 'from' from the sherwood list, making it easier to work with
    for element in sherwood_list:
        if element == 'from':
            sherwood_list.remove(element)

    # not yet sure (june 14 2022) that 1 bed premium would show as '1+' or '1 bed premium'
    suite_list_check = ['1', '1+']
    
    # assign rates per suite to temporary dictionary
    temp_final_dict = dict()
    for j in sherwood_list:
        # 1 bed
        if j[0] == '1':
            current_type = j
            if current_type not in temp_final_dict.keys():
                current_type += '+'
            continue
        # 2 bed
        if j[0] == '2':
            current_type = j
            continue
        # 3 bed
        if j[0] == '3':
            current_type = j
            continue
        # add rate to temp dictionary
        if j[0] == '$':
            rate = j
            rate = rate.replace('$', '')
            rate = rate.replace(',', '')
            temp_final_dict[current_type] = rate
        # check for all 4 suite types to be in the temp dictionary;
        # if a suite type is not in the temp dictionary, add it with a rate of '0'
        if len(temp_final_dict) != 4:
            for suite in suite_list_check:
                if suite not in temp_final_dict.keys():
                    temp_final_dict[suite] = '0'

    # move rental rates per suite to rental_rates_min
    for rent_rate in temp_final_dict.values():
        rental_rates_min.append(rent_rate)

    # website doesn't directly state available vacancies, will assume 'No Info'
    for x in range(len(suite_types)):
        is_vacant.append('No Info')
        
    # assign suite types to respective rental rates into a dictionary
    for unit in suite_types:
        temp_ = rental_rates_min.pop(0)
        stone_min[unit] = temp_

    #print(stone_min, is_vacant)
    return stone_min, is_vacant

if __name__ == '__main__':
    stonebridge()