# libraries
import unidecode
import time
import pandas as pd
import docx2txt
import urllib
from bs4 import BeautifulSoup

# function for retrieving surnames
def sklonuj(surname):
    """
    Function retrieving the 4th and 5th (grammatical) cases of Czech surnames.
    """
    url = u"sklonuj.cz/jmeno/{}".format(surname)
    url = 'https://' + urllib.request.quote(url.encode('utf-8'))
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    pro_koho = osloveni = soup.find_all('li', attrs = {'class': 'list-group-item'})[3].text.strip()
    osloveni = soup.find_all('li', attrs = {'class': 'list-group-item'})[4].text.strip()
    # unidecode
    pro_koho, osloveni = unidecode.unidecode(pro_koho), unidecode.unidecode(osloveni)
    return pro_koho, osloveni

db = []

def generuj_osloveni(excel):
    """
    Function generating the basic email attributes and storing them in Excel File
    """
    for i in range(excel.shape[0]):
        try:
            info = excel.iloc[i]
            for email, jmeno in zip(info.Email.split(', '), info.Jmeno.split(', ')):
                pro_koho, osloveni = sklonuj(jmeno)
                # differentiate between male and females based on the very last character
                if jmeno[-1] == 'á':
                    osloveni = 'Vazena pani ' + osloveni
                    pro_koho = 'pro pani ' + pro_koho
                else:
                    osloveni = 'Vazeny pane ' + osloveni
                    pro_koho = 'pro pana ' + pro_koho
                db.append({'original_jmeno': jmeno, 'osloveni': osloveni, 'pro_koho': pro_koho, 'email': email, 'mesto': info.Mesto, 'mail': info.Mail})
                time.sleep(0.5)
        except:
            info = excel.iloc[i]
            db.append({'original_jmeno': jmeno, 'osloveni': info.Jmeno, 'pro_koho': info.Jmeno, 'email': email, 'mesto': info.Mesto, 'mail': info.Mail})

    # save data
    return db

