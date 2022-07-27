import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def aspen_park():
    '''
    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c, x = aspen_village(); print('Rental rates:', d, x, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    aspen_min_rates = dict()
    aspen_max_rates = dict()
    is_vacant = ['No Info', 'No Info', 'No Info', 'No Info']
    suite_types = ['Aspen', 'Birch', 'Cottonwood', 'Dogwood']
    url = 'https://rentsherwoodpark.com/apartments-for-rent/4-augustine-crescent-Sherwood-Park-AB-33573/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')
    page_info = page_parsed.findAll('div', 'col-sm-2 col-xs-3')#'panel panel-default')

    """Extract rental rates per suite type; we will only use the rental rates for
    the types noted in suite_types above."""
    # min/max rate lists temporary to later select specific rents according to suite_types
    temp_min = []
    temp_max = []
    for i in page_info:
        temp = i.text
        temp = temp.replace('\n', '')
        temp = temp.replace('\t', '')
        temp = temp.strip()
        # split the PRICE string into a list
        if temp[0] == 'P':
            temp_list = temp.split()
            temp_list = temp_list[1:]
            min_rate_temp = temp_list[0].replace('$', '')
            max_rate_temp = temp_list[-1].replace('$', '')
            temp_min.append(min_rate_temp)
            temp_max.append(max_rate_temp)

    # reassign rental rates in accordance to suite_types list in prep for the dict creation
    rental_rates_min = [temp_min[0], temp_min[2], temp_min[5], temp_min[7]]
    rental_rates_max = [temp_max[0], temp_max[2], temp_max[5], temp_max[7]]

    # build the min/max dictionaries
    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        max_rate = rental_rates_max.pop(0)
        aspen_min_rates[unit] = min_rate
        aspen_max_rates[unit] = max_rate

    #print(aspen_min_rates, aspen_max_rates, is_vacant)
    return aspen_min_rates, aspen_max_rates, is_vacant
    
if __name__ == '__main__':
    aspen_park()