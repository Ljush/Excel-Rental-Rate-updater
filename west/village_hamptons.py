import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def village_hamptons():
    '''If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = village_hamptons(); print(d, x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    hamptons_min_rents = dict()
    suite_types = []
    is_vacant = []
    rent_rates_min = []
    url = 'https://premiumrentals.ca/properties/edmonton/village-at-the-hamptons/'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    """
    # possible solution to the connection being refused, yet to work though, might need a vpn? doesn't happen on my macbook air on the same network
    import time
    page = ''
    while page == '':
        try:
            page = requests.get(url, headers=headers)
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            time.sleep(5)
            print("Trying again.")
            continue
    """
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab the line of text that holds the suite type and rental starting rate for that suite
    for i in page_parsed.findAll('h4', 'uppercase text-left'):
        temp_list = i.text.strip().split()
        suite = str(temp_list[0] + ' ' + temp_list[1])
        suite_types.append(suite)
        # clean up the rental rate into an xxxx str format
        rent_rate = temp_list[4]
        rent_rate = rent_rate[1:]
        if rent_rate[1] == ',':
            rent_rate = rent_rate[0] + rent_rate[2:]
        rent_rates_min.append(rent_rate)

    # doesn't provide information on unit vacancy status, append 'No Info' == to length of suite_types
    for g in range(len(suite_types)):
        is_vacant.append('No Info')

    for unit in suite_types:
        rate = rent_rates_min.pop(0)
        hamptons_min_rents[unit] = rate

    #print(hamptons_min_rents, is_vacant)
    return hamptons_min_rents, is_vacant

if __name__ == '__main__':
    village_hamptons()