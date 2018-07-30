import requests
from time import sleep
import csv
from lxml import html
import re


emaillist = []
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
        #emaillist -> wypisać wszystkie możliwe kombinacje maili
        #emaillist = [i[0] + i[1] + i[2], i[1] + i[0] + i[2], i[0] + i[2]]
        emaillist = [i[0]+i[2]]
        emails.extend(emaillist)

#Pętla wypełnia i wysyła formularz na stronie dla każdego wygenerowanego maila
for email in emails:
    payload = {'lang': 'en', 'email': email}
    page = requests.post("http://mailtester.com/testmail.php", data=payload)
    tree = html.fromstring(page.content)
    data = tree.xpath('//table/tr[5]/td[5]/text()')
    final_table[email] = data
# jeśli email istnieje, dodaje go do toFile
    if data == compare:
        toFile.append(email)
    print("Email: {}, info: {}".format(email,data))
    sleep(1.0)

#Dodawanie listy istniejących maili (toFile) do Check.csv
with open('Check.csv', 'w') as fwriter:
    writer = csv.writer(fwriter)
    fwriter.write('Email')
    fwriter.write('\n')
    for item in toFile:
        fwriter.write(item)
        fwriter.write("\n")
