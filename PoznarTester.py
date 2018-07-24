# Plik csv z Malami musi yć w pliku z głównym plikiem .py
#
# Użycie pliku - odpalić plik PoznarTester.py z terminala
# 1 - ctr+alt+t
# 2 - dostać się do folderu z PoznarTester.py
# 3 - w terminalu $python Poznar*

import requests
import re
from time import sleep
import csv


emaillist = []
emails = []
res = []
final_table = {}

print("Witaj w MejlTesterze\n\n\n\n\nOpóźnienie jest wskazane, dlatego w trakcie trwania programu\n\n...\n\n\nmożesz śmiało iść na kawę!\n\n\n\n")
sleep(4)
print("Taki żarcik :) prospektuj! \n\n\n\n\n\nProspect, Prospect!")
# Wczytuje plik csv z folderu głównego pliku PoznarTester.py
with open('EmailList.csv', 'r') as f:
    reader = csv.reader(f)
    my_list = list(reader)
    for i in my_list:
        # emaillist -> wypisać wszystkie możliwe kombinacje maili
        emaillist = [i[0] + i[1] + i[2], i[1] + i[0] + i[2], i[0] + i[2]]
        emails.extend(emaillist)

# Pętla wypełnia i wysyła formularz na stronie dla każdego wygenerowanego maila
for email in emails:
    payload = {'lang': 'en', 'email': email}
    r = requests.post("http://mailtester.com/testmail.php", data=payload)
    text = r.text
    regex = r"(E-mail address is valid)"
    match = re.findall(regex, text)
    res.append(match)
    final_table[email] = match
    sleep(1.0)

# póki co print, do zmiany na wygenerowanie pliku csv z gotowymi adesami do wysłania
for key in final_table.items():
    print(key)
