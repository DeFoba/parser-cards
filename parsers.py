import requests
from bs4 import BeautifulSoup
from threading import Thread
from datetime import datetime
from os import listdir, mkdir
from time import sleep
import csv
import json

TEST = ['https://irecommend.ru/content/tinkoff-biznes', 'https://irecommend.ru/content/tinkoff']
DOMAINS = ['irecommend.ru']

class Parser:
    def __init__(self, links:list, start_date:str):
        self.start_date = datetime.strptime(start_date, '%d.%m.%Y')
        self.domains = {}
        self.last_dates = {}

        self.result = []

        self.LAST_DATE_SAVEFOLDERNAME = 'save_files'
        self.LAST_DATE_SAVEFILENAME = 'last_date.json'

        self.RESULT_FOLDERNAME = 'result'

        for domain in DOMAINS:
            if not domain in self.domains: self.domains[domain] = []

            for link in links:
                if domain in link: self.domains[domain].append(link)

    def irecommend_parsing_card(self, url):
        current_page = -1
        max_page = 150000

        cards = []
        can_go = True

        if not '?page=' in url: url += '?new=1&page='
        while current_page < max_page and can_go:
            current_page += 1

            response = requests.get(url  + str(current_page))
            sleep(0.1)
            html = BeautifulSoup(response.content, 'html.parser')
            sleep(0.1)

            CARD_NAME = html.find('h1', {'class': 'largeHeader'}).text.strip().replace('\n', ' ')

            main_block = html.find('div', {'class': 'view-referenced-nodes'})

            if max_page == 150000: max_page = int(main_block.find('li', {'class': 'pager-last last'}).text)

            for card in main_block.find_all('li', {'class': 'item'}):
                data = [] # Date, CardName, Star, Link, Text

                date_card = card.find('div', {'class': 'created'}).text.strip().replace('\n', ' ')

                if datetime.strptime(date_card, '%d.%m.%Y') < self.start_date:
                    can_go = False
                    break

                data.append(date_card)
                data.append(CARD_NAME)

                star_count = 0
                for star in card.find_all('div', {'class': 'star'}):
                    d_star = star.find('div')
                    if d_star.get('class')[0] == 'on': star_count += 1

                data.append(str(star_count))
                data.append('https://irecommend.ru' + card.find('a', {'class': 'reviewTextSnippet'}).get('href'))
                data.append(card.find('div', {'class': 'reviewTitle'}).text.strip().replace('\n', ' ') + ' ' + card.find('span', {'class': 'reviewTeaserText'}).text.strip().replace('\n', ' '))

                if not CARD_NAME in self.last_dates:
                    self.last_dates[CARD_NAME] = date_card

                cards.append(data)

        for card in cards:
            self.result.append(card)

        # print(cards)
        

        self.save_date()

    def save_date(self):
        if not self.LAST_DATE_SAVEFOLDERNAME in listdir(): mkdir(self.LAST_DATE_SAVEFOLDERNAME)

        with open(self.LAST_DATE_SAVEFOLDERNAME + '/' + self.LAST_DATE_SAVEFILENAME, 'w', encoding='utf8') as file:
            json.dump(self.last_dates, file, ensure_ascii=False)

    def save_result(self):
        if not self.RESULT_FOLDERNAME in listdir(): mkdir(self.RESULT_FOLDERNAME)

        with open(self.RESULT_FOLDERNAME + '/' + datetime.strftime(datetime.now(), '%d-%m-%Y %H-%M-%S.csv'), '+a', encoding='utf8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.result)


if __name__ == '__main__':
    pars = Parser(TEST, '23.05.2024')
    for link in TEST:
        pars.irecommend_parsing_card(link)

    pars.save_result()
    # print(pars.__dict__)