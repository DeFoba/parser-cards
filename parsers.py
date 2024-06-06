import requests
from bs4 import BeautifulSoup
import re
from threading import Thread
from datetime import datetime
from os import listdir, mkdir
from time import sleep
from modules.headers import DEFAULT_HEADERS
import csv
import json

TEST = ['https://irecommend.ru/content/tinkoff-biznes', 'https://irecommend.ru/content/tinkoff', 'https://развивай.рф/business_credits/tinkoff/otzyvy', 'https://рко.рф/reviews/bank/tinkoff']
DOMAINS = ['irecommend.ru', 'развивай.рф']

translate_month = {
    'Янв': 'January',
    'Фев': 'February',
    'Мар': 'March',
    'Апр': 'April',
    'Май': 'May',
    'Мая': 'May',
    'Июн': 'June',
    'Июл': 'July',
    'Авг': 'August',
    'Сен': 'September',
    'Окт': 'October',
    'Ноя': 'November',
    'Дек': 'December'
}

class Parser:
    def __init__(self, links:list, start_date:str=None):
        self.start_date = self.string_to_date(start_date)
        self.domains, self.last_dates, self.result = {}, {}, []

        self.LAST_DATE_SAVEFOLDERNAME = 'save_files'
        self.LAST_DATE_SAVEFILENAME = 'last_date.json'

        self.RESULT_FOLDERNAME = 'result'

        for domain in DOMAINS:
            if not domain in self.domains: self.domains[domain] = []

            for link in links:
                if domain in link: self.domains[domain].append(link)

    # String datetime to Python datetime
    def string_to_date(self, start_date):
        if ' ' in start_date:
            d, m, y = start_date.lower().split(' ')
            m = translate_month[str(m).capitalize()[:3]][:3]

            return datetime.strptime(' '.join([d, m, y]), u'%d %b %Y')
        
        if start_date != None and start_date != '': return datetime.strptime(start_date, '%d.%m.%Y')
        else: return 'LAST'

    def date_to_string(self, date):
        return datetime.strftime(date, '%d.%m.%Y')



    # irecommend.ru
    def irecommend(self, url, start_date=None):
        if start_date == None: start_date = self.start_date
        else: start_date = self.string_to_date(start_date)

        current_page = -1
        max_page = 150000

        cards = []
        can_go = True

        if not '?page=' in url: url += '?new=1&page='
        while current_page < max_page and can_go:
            current_page += 1

            response = requests.get(url  + str(current_page), headers=DEFAULT_HEADERS)
            sleep(0.1)
            html = BeautifulSoup(response.content, 'html.parser')
            sleep(0.1)

            CARD_NAME = html.find('h1', {'class': 'largeHeader'}).text.strip().replace('\n', ' ')

            main_block = html.find('div', {'class': 'view-referenced-nodes'})

            if max_page == 150000: max_page = int(main_block.find('li', {'class': 'pager-last last'}).text)

            for card in main_block.find_all('li', {'class': 'item'}):
                data = [] # Date, CardName, Star, Link, Text

                date_card = card.find('div', {'class': 'created'}).text.strip().replace('\n', ' ')

                if self.string_to_date(date_card) < start_date:
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

    
    # развивай.рф
    def razvivay(self, url, start_date=None):
        if start_date == None: start_date = self.start_date
        else: start_date = self.string_to_date(start_date)

        cards = []

        response = requests.get(url, headers=DEFAULT_HEADERS)
        sleep(0.1)
        html = BeautifulSoup(response.content, 'html.parser')
        sleep(0.1)

        name = html.find('h1', {'class': re.compile('.*SeoHeader_Header.')}).text.strip().replace('\n', ' ')

        main_block = html.find('div', {'class': re.compile('.*Reviews-styles__ReviewsList.')})
        for card in main_block.find_all('div', {'id': re.compile('.*tinkoff_Review.')})[::-1]:
            # cards.append()
            data = []

            star_count = 0

            title = card.find('div', {'class': re.compile('.*ReviewCard-styles__Title.')}).text.strip().replace('\n', ' ')
            text = card.find('div', {'class': re.compile('.*ReviewCard-styles__Text.')}).text.strip().replace('\n', ' ')
            date_text = card.find('div', {'class': re.compile('.*ReviewCard-styles__Author.')}).text.strip().replace('\n', ' ').split(', ')[-1]

            for star in card.find('div', {'class': re.compile('.*ReviewStars-styles__Wrapper.')}):
                if star.find('path').get('stroke') == None: star_count += 1

            if self.string_to_date(date_text) < start_date:
                break

            data.append(date_text)
            data.append(name)
            data.append(str(star_count))
            data.append('')
            data.append(title + ' ' + text)

            if not name in self.last_dates:
                self.last_dates[name] = date_text

            cards.append(data)

        for card in cards:
            self.result.append(card)
        

    # рко.рф
    def rkorf(self, url, start_date=None):
        if start_date == None: start_date = self.start_date
        else: start_date = self.string_to_date(start_date)

        cards = []

        max_pages = 3
        current_page = 0

        while current_page < 3:
            current_page += 1

            response = requests.get(url + f'?page={current_page}', headers=DEFAULT_HEADERS)
            sleep(0.1)
            html = BeautifulSoup(response.content, 'html.parser')
            sleep(0.1)

            name = html.find('div', {'class': 'catalog-bank__title'}).text.strip().replace('\n', ' ')
            max_pages = int(html.find('ul', {'class': 'paginator'}).find_all('li')[-2].text.strip())

            main_block = html.find('div', {'class': 'reviews-list'})

            for card in main_block.find_all('div', {'class': 'reviews-user'}):
                data = []

                date_text = card.find('ul', {'class': 'reviews-user__info'}).find('li').text.strip().replace('\n', ' ')

                date = self.date_to_string(self.string_to_date(date_text))
                stars = card.find('ul', {'class': 'stars-rate__list'}).get('data-star')

                title = card.find('div', {'class': 'reviews-user__title'}).text.strip().replace('\n', ' ')
                text = card.find('div', {'class': 'reviews-user__answer'}).text.strip().replace('\n', ' ')

                link = 'https://рко.рф' + card.find('div', {'class': 'reviews-user__more'}).find('a').get('href')

                if self.string_to_date(date) < start_date:
                    continue

                data.append(date)
                data.append(name)
                data.append(str(stars))
                data.append(link)
                data.append(str(title + ' ' + text).replace('\r', ' ').strip())

                cards.append(data)

        for card in cards:
            self.result.append(card)


            














    # Save Last Card Datetime
    def save_date(self):
        if not self.LAST_DATE_SAVEFOLDERNAME in listdir(): mkdir(self.LAST_DATE_SAVEFOLDERNAME)

        with open(self.LAST_DATE_SAVEFOLDERNAME + '/' + self.LAST_DATE_SAVEFILENAME, 'w', encoding='utf8') as file:
            json.dump(self.last_dates, file, ensure_ascii=False)

    # Save Result And Datetime
    def save_result(self):
        if not self.RESULT_FOLDERNAME in listdir(): mkdir(self.RESULT_FOLDERNAME)

        with open(self.RESULT_FOLDERNAME + '/' + datetime.strftime(datetime.now(), '%d-%m-%Y %H-%M-%S.csv'), '+a', encoding='utf8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.result)

        self.save_date()


if __name__ == '__main__':
    pars = Parser(TEST, '23.05.2023')
    # for link in TEST:
    #     pars.irecommend_parsing_card(link)

    # pars.razvivay(TEST[2])


    # pars.rkorf(TEST[3])


    # pars.save_result()

    # print(pars.__dict__)