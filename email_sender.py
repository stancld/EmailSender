# busdev variables
file_name = "VICF_v02"

# libraries
import unidecode
import time
import yagmail
import pandas as pd
import docx2txt
import urllib
from bs4 import BeautifulSoup

# function for retrieving surnames
def sklonuj(surname):
    """
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

# user varibles
sender_email = '<your-email>'
password = '<your-password>'

# load excel, words and pdf
excel = pd.read_excel(f'Bd_Excels/{file_name}.xlsx')
bd_mail = docx2txt.process(f'templates/bd_mail.docx')
second_mail = docx2txt.process(f'templates/2nd_mail.docx')
pdf = "presentation/VICF_firemni profil.pdf"

subject = {'bd': "Zadost o setkani",
            '2nd': "2nd meeting"
}

contents = {'bd': bd_mail,
            '2nd': second_mail
}

# login to email
yag = yagmail.SMTP(sender_email, password)
# sent email
for i in range(excel.shape[0]):
    try:
        info = excel.iloc[i]
        for email, jmeno in zip(info.Email.split(', '), info.Jmeno.split(', ')):
            pro_koho, osloveni = sklonuj(jmeno)
            # differentiate between male and females based on the very last character
            if jmeno[-1] == 'á':
                osloveni = "Vazena pani " + osloveni
                pro_koho = "pro pani " + pro_koho
            else:
                osloveni = "Vazeny pane " + osloveni
                pro_koho = "pro pana " + pro_koho
            
            # send e-mail
            yag.send(
                to = email,
                subject = f"{subject[info.Mail]} {info.Mesto} / {pro_koho}",
                contents = [osloveni + contents[info.Mail], pdf]
            )
            time.sleep(5)
    except Exception as e:
        print(e)
