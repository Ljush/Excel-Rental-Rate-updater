import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''

def leduc_mansion():
    '''If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = leduc_mansion(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    mansion_min = dict()
    is_vacant = [False, False, False, False]
    suite_types = ['1 Bedroom', '2 Bedroom', '2 Bedroom 985 sqft', '3 Bedroom']

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'https://www.bradenequitiesinc.com/property-listings/leduc-mansion-7128/'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')
    suite_index = {1:'1 bed 1 bath', 2:'2 bed 2 bath', 
                   3:'2 bed 2 bath', 4:'3 bed 2 bath'}
    
    # grab suite cards
    suite_data = []
    for i in page_parsed.findAll('div', 'property-suite'):
        suite = i.text
        suite = suite.strip()
        current_suite_list = suite.split()
        suite_data.append(current_suite_list[:-2])

    # clean up the names of the suite titles, extract rental rates, adjust vacancy status, remove commas from rental rates
    suite_data = name_cleanup(suite_data)
    suite_data, is_vacant, rental_rates_min = find_rates(suite_data, is_vacant)
    rental_rates_min = remove_commas(rental_rates_min)

    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        if min_rate == []:
            mansion_min[unit] = '0'
        else:
            mansion_min[unit] = min_rate
    
    #print(mansion_min, is_vacant)
    return mansion_min, is_vacant

def remove_commas(rental_rates_min):
    """Removes commas from rental rates greater than $999"""
    for index, i in enumerate(rental_rates_min):
        if i != []:
            if i[1] == ',':
                rate = i
                rate = rate[0] + rate[2:]
                rental_rates_min[index] = rate
    return rental_rates_min
        
def find_rates(suite_data, is_vacant):
    """Extract the rental rates per suite card."""
    rental_rates_min = [[], [], [], []]
    for card in suite_data:
        # 1 bedroom
        if card[0] == '1':
            rate = card[-1]
            rate = rate[2:]
            rental_rates_min[0] = rate
            is_vacant[0] = True

        # 2 bedroom
        """Monitor this over time because currently only 1 type of 2 bedroom is listed
        the excel sheet shows that there are 2 types of 2 bed suites but they do not post sq ft of each suite card (old info?)
        so there isn't currently anything to distinguish between the two types of suites since they only 
        post what is currently available"""
        if card[0] == '2':
            rate = card[-1]
            rate = rate[2:]
            rental_rates_min[1] = rate
            is_vacant[1] = True

        # 2 bedroom (?) 985 sqft??
        if card[0] == '2':
            if rental_rates_min[1] != []:
                continue
            else:
                rate = card[-1]
                rate = rate[2:]
                rental_rates_min[2] = rate
                is_vacant[2] = True
        # 3 bedroom
        if card[0] == '3':
            rate = card[-1]
            rate = rate[2:]
            rental_rates_min[3] = rate
            is_vacant[3] = True

    return suite_data, is_vacant, rental_rates_min

def name_cleanup(suite_data):
    """Cleans up the suite type names ex: 'BedroomJun', 'BedroomFeb', etc."""
    for j in suite_data:
        # removes the month name at the end of the suite type name
        if j[0].isalpha() == True:
            if j[0] == 'Bachelor':
                pass
            else:
                j[0] = j[0][:-3]
        # removes the month name at the end of the suite type name
        if j[1].isalpha() == True:
            if j[1] == 'Bedroom':
                pass
            else:
                j[1] = j[1][:-3]
    return suite_data

if __name__ == '__main__':
    leduc_mansion()