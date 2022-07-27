import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def blue_quill():
    '''Exactly the same logic as pineridge_grabber.py
    
    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = blue_quill(); print(d, x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    blue_quill_rents = dict()
    blue_suite_types = []
    is_vacant = []
    suite_info = []
    url = 'http://www.har-par.com/properties.php?PropertyID=6'
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    blue_quill = requests.get(url, headers=headers)
    blue_soup = BeautifulSoup(blue_quill.content, 'html.parser')
    blue_description = blue_soup.select('body div.row.property-unit')
    
    for suite in blue_description:
        suite_info.append(suite.text.replace('\n', ' ').split())

    count = 0
    for data in suite_info:
        if data[-1] == 'Vacancy':
            is_vacant.append(False)
            
        if data[-1] == 'Apply':
            is_vacant.append(True)
        
        for info in data:
            # removes odd $xxxrent elements from a list
            if info[0] == '$' and info[-1] == 't':
                data.remove(info)
                continue
            
            if info[0] == '$' and int(info[1:]) < 849:
                data.remove(info)
                continue
            
            if data[0].isnumeric():
                if data[1].isalpha():
                    new_type = str(data[0]) + f' {data[1]}'
                    blue_suite_types.append(new_type)
                    data.remove(info)
                    
            if info[0] == '$':
                blue_quill_rents[blue_suite_types[count]] = info[1:]
                data.remove(info)
                count += 1

    #print(blue_quill_rents, is_vacant)
    return blue_quill_rents, is_vacant

if __name__ == '__main__':
    blue_quill()