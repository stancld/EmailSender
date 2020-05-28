# libraries
import unidecode
import time
import pandas as pd
import docx2txt
import urllib
import yagmail
from bs4 import BeautifulSoup

# load excel, words and pdf
bd_mail = docx2txt.process(f'templates/bd_mail.docx')
second_mail = docx2txt.process(f'templates/2nd_mail.docx')
pdf = "presentation/VICF_firemni profil.pdf"
subject = {'bd': "Zadost o setkani",
            '2nd': "2nd meeting"
}
contents = {'bd': bd_mail,
            '2nd': second_mail
}


def posli_maily(excel, sender_email, password):
    # login to email
    yag = yagmail.SMTP(sender_email, password)            
    # run sending
    for i in range(excel.shape[0]):
        info = excel.iloc[i]
        # send e-mail
        yag.send(
            to = info.email,
            subject = f"{subject[info.mail]} {info.mesto} / {info.pro_koho}",
            contents = [info.osloveni + contents[info.mail], pdf]
        )
        time.sleep(5)
