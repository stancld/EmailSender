import urllib
from bs4 import BeautifulSoup

url = "https://sklonuj.cz/slovo/Zahradka"

page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
osloveni = soup.find_all('li', attrs = {'class': 'list-group-item'})[4].text.strip()



f = urllib.request.urlopen('http://www.python.org/')
print(f.read(100))