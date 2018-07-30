import requests
from time import sleep
import csv
from lxml import html


emaillist = {}
emails = []
final_table = {}
data = 0
toFile = []
name = []
compare = ['E-mail address is valid']


print("START")

# Wczytuje plik csv z folderu głównego pliku PoznarTester.py
with open('EmailList.csv', 'r') as f:
    reader = csv.reader(f)
    my_list = list(reader)
    for i in my_list:
        data = [i[0]+i[2], i[1]+i[2]]
        emaillist[i[2]] = data

# Pętla wypełnia i wysyła formularz na stronie dla każdego wygenerowanego maila
for email in emaillist.items():
    for i in email[1]:
        payload = {'lang': 'en', 'email': i}
        page = requests.post("http://mailtester.com/testmail.php", data=payload)
        tree = html.fromstring(page.content)
        data = tree.xpath('//table/tr[5]/td[5]/text()')
# Jeśli email istnieje, dodaje go do toFile
        if data == compare:
            toFile.append(i)
        print("Email: {}, info: {}".format(i, data))
        sleep(1.5)

# Dodawanie listy istniejących maili (toFile) do Check.csv
with open('Check.csv', 'w') as fwriter:
    writer = csv.writer(fwriter)
    fwriter.write('Email')
    fwriter.write('\n')
    for item in toFile:
        fwriter.write(str(item))
        fwriter.write("\n")
