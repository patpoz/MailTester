from lxml import html
import requests
page = requests.get('https://en.wikipedia.org/wiki/Web_scraping')
tree = html.fromstring(page.content)
data = tree.xpath('//*[@id="mw-content-text"]/div/ul[1]/li/a/text() | //*[@id="mw-content-text"]/div/ul[1]/li/text()[1]')
print(data)

with open('Check.csv', 'w') as fwriter:
    writer = csv.writer(fwriter)
    for key in final_table.items():
    spamwriter.writerow(key)