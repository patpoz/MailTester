import requests
from time import sleep
import csv
from lxml import html


emaillist = []
emails = []
data_list = []
valid = []
invalid = []
data = []
data2 = []
check = []

print("START")

# Wczytuje plik csv z folderu głównego pliku PoznarTester.py
with open('EmailList.csv', 'r') as f:
    reader = csv.reader(f)
    my_list = list(reader)
# tworzenie możliwych maili dla danej osoby.
    for item in my_list:
        emaillist = [item[0]+item[1]+item[2], 'kontakt'+item[2], item[0][0]+item[1]+item[2]]
        for email in emaillist:
            if "Server doesn't allow e-mail address verification" in data2:
                pass
            elif 'E-mail address is valid' in data_list:
                    pass
            else:
                payload = {'lang': 'en', 'email': email}
                page = requests.post("http://mailtester.com/testmail.php", data=payload)
                tree = html.fromstring(page.content)
                data = tree.xpath('//table/tr[5]/td[5]/text()')
                data2 = tree.xpath('//table/tr[4]/td[5]/text()')
                data_list.extend(data)
                print(email)
                sleep(3)
                if 'E-mail address is valid' in data:
                    valid.append(email)
                elif not data:
                    invalid.append(email)
                    print("Email: {}, {}".format(email, data2))
                    if "Server doesn't allow e-mail address verification" in data2:
                        print("DOMENA: {} Niemożliwa do sprawdzenia!".format(item[2]))
        data2 = []
        emails = []
        data_list = []


print(check)
print("\nMAILE NIESPRAWDZONE:")
for item in invalid:
    print("Email: {}".format(item))

print("\nODNALEZIONE MAILE:\n")
for item in valid:
    print("Email: {}".format(item))


#TODO: Dodać kombinacje maili
#TODO: Zrobić zapisywanie wyników do pliku w formie gotowej do wysyłki

