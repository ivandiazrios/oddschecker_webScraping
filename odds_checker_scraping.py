import requests
from bs4 import BeautifulSoup

def get_race_urls(page_html):

    races = set()

    soup = BeautifulSoup(page.text, 'lxml')
    for link in soup.findAll('a', href=True):
        if link['href'].endswith('winner') and 'horse-racing' in link['href']:
            races.add(link['href'].split("horse-racing", 1)[1])

    return races

def get_odds_from_race_url(url):

    horse_odds = dict()

    race_page = requests.get(url)
    soup = BeautifulSoup(race_page.text, 'lxml')

    table = soup.find("table")

    for row in table('tr', attrs={"class":"diff-row"}):
        #row.attrs["data-best-dig"] Gives best odds but does not include exchanges
        odds = [float(cell["data-odig"]) for cell in row('td', attrs={"data-odig":True})]
        horse_name = row.attrs["data-bname"]
        best_odds = max(odds)

        horse_odds[horse_name] = best_odds

    return horse_odds



url = "http://www.oddschecker.com/horse-racing"
page = requests.get(url)
#url2 = 'http://www.oddschecker.com/horse-racing/2016-02-07-musselburgh/13:00/winner'

race_urls = get_race_urls(page)
for url in race_urls:
    url = "http://www.oddschecker.com/horse-racing" + url
    odds = get_odds_from_race_url(url)
    print url
    print odds