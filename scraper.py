import requests
from bs4 import BeautifulSoup
import string
import re

ROOT_URL = 'http://www.iardc.org'
LAWYER_SEARCH = 'lawyersearch.asp'
ROLL = 'ardcroll.asp'

def scrapem():
    for letter in string.lowercase:
        data = {
            'ltype': 'all', 
            'sLastName': letter,
            'sPbCountry': 'all', 
            'stype':'phonetic' 
        }
        headers = {'Referer': ROOT_URL}
        search = requests.get('%s/%s' % (ROOT_URL, LAWYER_SEARCH))
        cookie_one = search.cookies
        list_page = requests.post('%s/%s' % (ROOT_URL, ROLL), data=data, headers=headers)
        cookie_two = list_page.cookies
        soup = BeautifulSoup(list_page.content)
        links = [a.get('href') for a in soup.find_all(href=re.compile('ldetail.asp'))]
        headers = {'Referer': '%s/%s' % (ROOT_URL, ROLL)}
        for link in links:
            detail_page = requests.get('%s/%s' % (ROOT_URL, link), headers=headers, cookies=cookie_two)
            detail_soup = BeautifulSoup(detail_page.content)
            table = detail_soup.find('table', cellspacing='3')
            rows = iter(table)
            for row in rows:
                title = row.find('b')
                value = row.find_all('td')[1]
                if title > 0 and title.string:
                    key = title.string
                    value = val.string
                    print '%s: %s' % (key, value)
    return None

if __name__ == '__main__':
    scrapem()
