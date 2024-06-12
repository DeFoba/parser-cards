import requests
from bs4 import BeautifulSoup
import re
from threading import Thread
from datetime import datetime
from os import listdir, mkdir
from time import sleep
from modules.headers import DEFAULT_HEADERS, HEADERS
from fp import fp
import csv
import json
# from selenium import webdriver
import undetected_chromedriver as uc

PROX = fp.FreeProxy(rand=True)

TEST = [
        'https://brobank.ru/banki/tinkoff/comments/', 'https://brobank.ru/rko-tinkoff/comments/', 
        'https://credits-on-line.ru/rko/tinkoff-biznes/otzyvy/', 'https://moskva.bankiros.ru/bank/tcs/otzyvy/rko', 'https://otzovik.com/reviews/tinkoff_biznes/',
        'https://ru.myfin.by/bank/tcs/otzyvy', 'https://topbanki.ru/banks/tcsbank/']

DOMAINS = ['irecommend.ru', 'развивай.рф', 'рко.рф', 'bankiclub.ru', 'bankiros.ru', 'brobank.ru', 'credits-on-line.ru', 'ru.myfin.by', 'topbanki.ru'] #'otzovik.com']

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

config = {
    'irecommend.ru': {
        'url':      'https://irecommend.ru',
        'check_date': True,
        'selenium': False,
        'date':     'normal',
        'links':    'all',
        'prefix':   None,
        'headers': HEADERS['irecommend.ru']['headers'],
        'pages': {
            'url':      '?new=1&page=',
            'start_count': 0,
            'max':      ['li', 'class', 'pager-last last'],
            'level':    'easy' # easy / hard / veryhard
        },
        'cards_list_element':   ['div', 'class', 'view-referenced-nodes'],
        'cards_list':           ['li',  'class', 'item'],
        'stars': '',
        'elements': {
            'date':     ['div',     'class',    'created'],
            'name':     ['h1',      'class',    'largeHeader'],
            'title':    ['div',     'class',    'reviewTitle'],
            'text':     ['span',    'class',    'reviewTeaserText'],
            'link':     ['a',       'class',    'reviewTextSnippet']
        }
    },

    'развивай.рф': {
        'url':      'https://развивай.рф',
        'check_date': True,
        'selenium': False,
        'date':     'hard',
        'date_spliter': [', ', -1],
        'links':    'none',
        'prefix':   None,
        'headers': DEFAULT_HEADERS,
        'pages': None,
        'cards_list_element':   ['div', 'class', '.*Reviews-styles__ReviewsList.'],
        'cards_list':           ['div',  'id', '.*_Review_.'],
        'stars': '',
        'elements': {
            'date':     ['div',     'class',    '.*ReviewCard-styles__Author.'],
            'name':     ['h1',      'class',    '.*SeoHeader_Header.'],
            'title':    ['div',     'class',    '.*ReviewCard-styles__Title.'],
            'text':     ['div',    'class',    '.*ReviewCard-styles__Text.'],
            'link':     None
        }
    },

    'рко.рф': {
        'url':      'https://рко.рф',
        'selenium': False,
        'check_date': False,
        'date':     'hard2', # easy / hard (1, 2, 3, 4) / veryhard
        'date_second': 'li',
        'links':    'all find',
        'links_find': 'a',
        'prefix':   None,
        'headers': DEFAULT_HEADERS,
        'pages': {
            'url':      '?page=',
            'start_count': 0,
            'max':      ['ul', 'class', 'paginator'],
            'index':    -2,
            'second_element': 'li',
            'level':    'hard' # easy / hard / veryhard
        },
        'cards_list_element':   ['div', 'class', 'reviews-list'],
        'cards_list':           ['div', 'class', 'reviews-user'],
        'stars': '',
        'elements': {
            'date':     ['ul',     'class',    'reviews-user__info'],
            'name':     ['div',      'class',    'catalog-bank__title'],
            'title':    ['div',     'class',    'reviews-user__title'],
            'text':     ['div',    'class',    'reviews-user__answer'],
            'link':     ['div',    'class',    'reviews-user__more']
        }
    },

    'bankiclub.ru': {
        'url':      'https://bankiclub.ru',
        'selenium': False,
        'check_date': True,
        'date':     'normal', # normal / hard (1, 2, 3, 4) / veryhard
        'links':    'none',
        'prefix':   None,
        'headers': DEFAULT_HEADERS,
        'pages': None,
        'cards_list_element':   ['div', 'id', 'JsReviews'],
        'cards_list':           ['div', 'class', 'review-contaner'],
        'stars': '',
        'elements': {
            'date':     ['div',     'class',    'review-contaner-date'],
            'name':     ['div',      'class',    'firm-item-h2'],
            'title':    None,
            'text':     ['div',    'class',    'review-content'],
            'link':     None
        }
    },

    'bankiros.ru': {
        'url':      'https://bankiros.ru',
        'selenium': False,
        'check_date': True,
        'date':     'normal', # normal / hard (1, 2, 3, 4) / veryhard
        'links':    'no all',
        'links_find': 'a',
        'prefix':   '?limit=100',
        'headers': DEFAULT_HEADERS,
        'pages': None,
        'cards_list_element':   ['div', 'class', 'xxx-reviews__list'],
        'cards_list':           ['div', 'class', 'xxx-reviews-card__body'],
        'stars': '',
        'second_name': 'li',
        'name_index': -1,
        'elements': {
            'date':     ['span',     'class',    'xxx-reviews-info__date'],
            'name':     ['ul',      'class',    'breadcrumb'],
            'title':    ['div',      'class',    'xxx-reviews-card__title'],
            'text':     ['p',    'class',    'xxx-reviews-card__content'],
            'link':     ['div',      'class',    'xxx-reviews-card__title']
        }
    },

    'brobank.ru': {
        'url':      'https://brobank.ru',
        'selenium': False,
        'check_date': True,
        'date':     'hard', # normal / hard (1, 2, 3, 4) / veryhard
        'date_spliter': [' ', 0],
        'links':    'none',
        'prefix':   None,
        'headers': DEFAULT_HEADERS,
        'pages': {
            'url':      '/comment-page-',
            'start_count': 1,
            'max':      ['div', 'class', 'navigation__list'],
            'index':    -2,
            'second_element': 'a',
            'level':    'hard' # easy / hard / veryhard
        },
        'cards_list_element':   ['ol', 'id', 'comments-list_ajax'],
        'cards_list':           ['article', 'class', 'comment'],
        'stars': '',
        'elements': {
            'date':     ['time',     None,    None],
            'name':     ['div',      'class',    'page-title'],
            'title':    ['div',      'class',    'title_review'],
            'text':     ['section',    'class',    'comment-content'],
            'link':     None
        }
    },

    # 'brobank.ru':
    # 'credits-on-line.ru':
    # 'ru.myfin.by':
    # 'topbanki.ru'
}


class Parser:
    def __init__(self):
        self.stop_date = self.string_to_date('03.03.2021')
        self.names = ['date', 'name', 'stars', 'links', 'text']
        self.result = [self.names]

    # Normalize date
    def string_to_date(self, start_date):
        if ' ' in start_date:
            d, m, y = start_date.lower().split(' ')
            m = translate_month[str(m).capitalize()[:3]][:3]

            return datetime.strptime(' '.join([d, m, y]), u'%d %b %Y')
        
        if start_date != None and start_date != '': return datetime.strptime(start_date, '%d.%m.%Y')
        else: return 'LAST'

    # Date turn to string value
    def date_to_string(self, date):
        return datetime.strftime(date, '%d.%m.%Y')

    # Check domain in URL 
    def is_true_domain(sel, url:str):
        for domain in config:
            if domain in url:
                return domain
        return False
    
    # Normalize selection list
    def selector(self, value:list):
        tag, select, val = value

        if select == None: return [tag, None]
        if '.*' in val: return [tag, {select: re.compile(val)}]

        return [tag, {select: val}]
    
    # Find count pages
    def find_max_pages(self, domain, html):
        max_page = 0

        match config[domain]['pages']['level']:
            case 'easy': max_page = int(html.find(*self.selector(config[domain]['pages']['max'])).text)
            case 'hard': max_page = int(html.find(*self.selector(config[domain]['pages']['max'])).find_all(config[domain]['pages']['second_element'])[config[domain]['pages']['index']].text)
            case 'veryhard': max_page = int(0)

        return max_page
    
    # Remove empty spaces in data
    def normalize_data(self, value:list):
        return [str(val).strip().replace('\n', ' ').replace('\r', ' ') for val in value]
    
    # Parsing cards on page
    def collect_cards(self, domain, url, html, block):
        if not 'second_name' in config[domain]:
            NAME = html.find(*self.selector(config[domain]['elements']['name'])).text
        else:
            NAME = html.find(*self.selector(config[domain]['elements']['name'])).find_all(config[domain]['second_name'])[config[domain]['name_index']].text

        STOP = False

        for card in block.find_all(*self.selector(config[domain]['cards_list'])):
            match config[domain]['date']:
                case 'normal':  DATE = self.date_to_string(self.string_to_date(card.find(*self.selector(config[domain]['elements']['date'])).text))
                case 'hard':    DATE = self.date_to_string(self.string_to_date(card.find(*self.selector(config[domain]['elements']['date'])).text.strip().replace('\n', ' ').replace('\r', ' ').split(config[domain]['date_spliter'][0])[config[domain]['date_spliter'][-1]]))
                case 'hard2':   DATE = self.date_to_string(self.string_to_date(card.find(*self.selector(config[domain]['elements']['date'])).find(config[domain]['date_second']).text.strip().replace('\n', ' ').replace('\r', ' ')))


            STARS = 0
            TEXT = ''
            LINK = url
            add_to_result = True

            match config[domain]['links']:
                case 'all':
                    LINK = config[domain]['url'] + card.find(*self.selector(config[domain]['elements']['link'])).get('href')

                case 'all find':
                    LINK = config[domain]['url'] + card.find(*self.selector(config[domain]['elements']['link'])).find(config[domain]['links_find']).get('href')

                case 'not all':
                    find_link = card.find(*self.selector(config[domain]['elements']['link'])).find(config[domain]['links_find'])


                    if find_link != None:
                        LINK = config[domain]['url'] + find_link.get('href')


            if config[domain]['elements']['title'] != None:
                try:
                    TEXT = card.find(*self.selector(config[domain]['elements']['title'])).text + ' ' + card.find(*self.selector(config[domain]['elements']['text'])).text
                except:
                    continue
            else:
                TEXT = card.find(*self.selector(config[domain]['elements']['text'])).text

            if self.string_to_date(DATE) < self.stop_date:
                if config[domain]['check_date']:
                    STOP = True
                    break
                else:
                    add_to_result = False

            # star_count = 0
            # for star in card.find_all('div', {'class': 'star'}):
            #     d_star = star.find('div')
            #     if d_star.get('class')[0] == 'on': star_count += 1

            if add_to_result:
                self.result.append(self.normalize_data([DATE, NAME, STARS, LINK, TEXT]))

        return STOP

    def run_loop_of_pages(self, domain, url):
        current_page = config[domain]['pages']['start_count']

        html, card_links_element = self.get_page(domain, url + config[domain]['pages']['url'] + str(current_page))
        sleep(2)

        # with open('index.html', 'w', encoding='utf-8') as file:
        #     file.write(str(html))

        if self.collect_cards(domain, url, html, card_links_element): return


        current_page += 1


        max_page = self.find_max_pages(domain, html)

        while current_page < max_page:
            html, card_links_element = self.get_page(domain, url + config[domain]['pages']['url'] + str(current_page))
            if self.collect_cards(domain, url, html, card_links_element): break
            current_page += 1
            sleep(2)

    # Send request and get html content
    def get_page(self, domain, url):
        if config[domain]['prefix'] != None:
            url = url + config[domain]['prefix']

        if not config[domain]['selenium']:
            response = requests.get(url, headers=config[domain]['headers'], proxies=None).content
            sleep(0.1)

        print(url)

        html = BeautifulSoup(response, 'html.parser')
        sleep(0.1)

        card_list = html.find(*self.selector(config[domain]['cards_list_element']))

        return html, card_list

    def run_no_pages(self, domain, url):
        self.collect_cards(domain, url, *self.get_page(domain, url))




    # Pars cards by URL
    def pars_by_request(self, url):
        domain = self.is_true_domain(url)
        if domain == False: return

        if config[domain]['pages'] == None: self.run_no_pages(domain, url)
        else: self.run_loop_of_pages(domain, url)
            


if __name__ == '__main__':
    parser = Parser()
    # parser.pars_by_request('https://irecommend.ru/content/tinkoff-biznes') # FIX IT: <-------------
    # parser.pars_by_request('https://развивай.рф/business_credits/tinkoff/otzyvy')
    # parser.pars_by_request('https://рко.рф/reviews/bank/tinkoff')
    # parser.pars_by_request('https://bankiclub.ru/rkos/tinkoff-business/reviews')
    # parser.pars_by_request('https://bankiros.ru/bank/tcs/otzyvy/rko')
    parser.pars_by_request('https://brobank.ru/banki/tinkoff/comments')
    print(parser.result)

exit()


































class Parser2:
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
    
    def send(self, url, headers=DEFAULT_HEADERS, proxy=None):
        return requests.get(url, headers=headers, proxies=proxy)








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

            response = self.send(url  + str(current_page))
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

        response = self.send(url)
        sleep(0.1)
        html = BeautifulSoup(response.content, 'html.parser')
        sleep(0.1)

        name = html.find('h1', {'class': re.compile('.*SeoHeader_Header.')}).text.strip().replace('\n', ' ')

        main_block = html.find('div', {'class': re.compile('.*Reviews-styles__ReviewsList.')})
        for card in main_block.find_all('div', {'id': re.compile('.*_Review_.')})[::-1]:
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
            data.append(url)
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

            response = self.send(url + f'?page={current_page}')
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

                if not name in self.last_dates:
                    self.last_dates[name] = date_text

        for card in cards:
            self.result.append(card)


    




            

    # bankiclub.ru
    def bankiclub(self, url, start_date=None):
        if start_date == None: start_date = self.start_date
        else: start_date = self.string_to_date(start_date)

        cards = []


        response = self.send(url)
        sleep(0.1)
        html = BeautifulSoup(response.content, 'html.parser')
        sleep(0.1)

        main_blcok = html.find('div', {'id': 'JsReviews'})

        name = html.find('div', {'class': 'firm-item-h2'}).text.strip().replace('\n', ' ').replace('\r', ' ')

        for card in main_blcok.find_all('div', {'class': 'review-contaner'}):
            data = []

            date_text = card.find('div', {'class': 'review-contaner-date'}).text.strip().replace('\n', ' ').replace('\r', ' ')
            date = self.date_to_string(self.string_to_date(date_text))
            stars = str(len(card.find('div', {'class': 'rating-result'}).find_all('span', {'class': 'active'})))
            text = card.find('div', {'class': 'review-content'}).text.strip().replace('\n', ' ').replace('\r', ' ')
            
            data.append(date)
            data.append(name)
            data.append(stars)
            data.append(url)
            data.append(text)

            if self.string_to_date(date_text) < start_date:
                continue

            cards.append(data)


            if not name in self.last_dates:
                self.last_dates[name] = date_text


        for card in cards:
            self.result.append(card)





    

    # bankiros.ru
    def bankiros(self, url, start_date=None):
        if start_date == None: start_date = self.start_date
        else: start_date = self.string_to_date(start_date)

        cards = []


        response = self.send(url + '?limit=100')
        sleep(0.1)
        html = BeautifulSoup(response.content, 'html.parser')
        sleep(0.1)

        main_blcok = html.find('div', {'class': 'xxx-reviews__list'})

        name = html.find('ul', {'class': 'breadcrumb'}).find_all('li')[-1].find('span').text.strip().replace('\n', ' ').replace('\r', ' ')

        for card in main_blcok.find_all('div', {'class': 'xxx-reviews-card__body'}):
            data = []

            date = card.find('span', {'class': 'xxx-reviews-info__date'}).text.strip().replace('\n', ' ').replace('\r', ' ')
            title_el = card.find('div', {'class': 'xxx-reviews-card__title'})
            title = title_el.text.strip().replace('\n', ' ').replace('\r', ' ')

            stars = card.find('div', {'class': 'xxx-reviews-rating'}).text.strip().replace('\n', ' ').replace('\r', ' ').split(' ')[0]

            text = card.find('p', {'class': 'xxx-reviews-card__content'}).text.strip().replace('\n', ' ').replace('\r', ' ')

            if title_el.find('a') == None:
                link = url
            else:
                link = title_el.find('a').get('href')

            data.append(date)
            data.append(name)
            data.append(stars)
            data.append(link)
            data.append(title + ' ' + text)

            if self.string_to_date(date) < start_date:
                break

            cards.append(data)


            if not name in self.last_dates:
                self.last_dates[name] = date


        for card in cards:
            self.result.append(card)




    # brobank.ru
    def brobank(self, url, start_date=None):
        if start_date == None: start_date = self.start_date
        else: start_date = self.string_to_date(start_date)

        cards = []

        current_page = 0
        max_page_count = 3

        can_go = True


        while current_page < max_page_count and can_go:
            current_page += 1
            if url[-1] != '/': url += '/'

            response = self.send(url + f'comment-page-{current_page}/')
            sleep(0.1)
            html = BeautifulSoup(response.content, 'html.parser')
            sleep(0.1)

            main_blcok = html.find('ol', {'id': 'comments-list_ajax'})

            name = html.find('div', {'class': 'page-title'}).text.strip().replace('\n', ' ').replace('\r', ' ')

            max_page_count = int([x for x in html.find_all('a', 'page-numbers') if not 'next' in x.get('class')][-1].text.strip().replace('\n', ' ').replace('\r', ' '))

            for card in main_blcok.find_all('article', {'class': 'comment'}):
                data = []

                date = card.find('time').text.strip().replace('\n', ' ').replace('\r', ' ').split(' ')[0]
                try:
                    stars = card.find('span', {'class': 'new-card__rating_num'}).get('data-count')
                except:
                    continue
                title = card.find('div', {'class': 'title_review'}).text.strip().replace('\n', ' ').replace('\r', ' ')
                text = card.find('section', {'class': 'comment-content'}).text.strip().replace('\n', ' ').replace('\r', ' ')

                data.append(date)
                data.append(name)
                data.append(stars)
                data.append(url)
                data.append(title + ' ' + text)

                if self.string_to_date(date) < start_date:
                    can_go = False
                    break

                cards.append(data)

                if not name in self.last_dates:
                    self.last_dates[name] = date


        for card in cards:
            self.result.append(card)




    # credits-on-line.ru
    def creditsonline(self, url, start_date=None):
        if start_date == None: start_date = self.start_date
        else: start_date = self.string_to_date(start_date)

        cards = []


        response = self.send(url + '?commentsSortField=type&commentsSortValue=newest&commentsWhereField=rating&commentsWhereValue=')
        sleep(0.1)
        html = BeautifulSoup(response.content, 'html.parser')
        sleep(0.1)

        main_blcok = html.find('ol', {'class': 'comments-tree-list'})

        name = html.find('div', {'class': 'h1'}).find('h1').text.strip().replace('\n', ' ').replace('\r', ' ')

        for card in main_blcok.find_all('div', {'id': re.compile('.*comment-id.')}):
            data = []

            date_text = card.find('span', {'class': 'rev_comm_date'}).text.strip().replace('\n', ' ').replace('\r', ' ').split(' в ')[0]
            date = self.date_to_string(self.string_to_date(date_text))
            stars_temp = card.find('li', {'class': 'current-rating'}).text.strip().replace('\n', ' ').replace('\r', ' ')
            text = card.find('div', {'class': 'rev_comm_text'}).text.strip().replace('\n', ' ').replace('\r', ' ')

            if int(stars_temp) != 0:
                stars = int(int(stars_temp) / 10)
            else:
                stars = 0

            data.append(date)
            data.append(name)
            data.append(stars)
            data.append(url)
            data.append(text)

            if self.string_to_date(date) < start_date:
                    break

            cards.append(data)

            if not name in self.last_dates:
                self.last_dates[name] = date


        for card in cards:
            self.result.append(card)







    # otzovik.com BUG: NEED HELP
    def otzovik(self, url, start_date=None):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Priority': 'u=1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        if start_date == None: start_date = self.start_date
        else: start_date = self.string_to_date(start_date)

        cards = []

        current_page = 0
        max_page_count = 3

        can_go = True


        while current_page < max_page_count and can_go:
            current_page += 1
            if url[-1] != '/': url += '/'

            response = self.send(url + f'{current_page}/?order=date_desc', headers)
            sleep(0.1)
            html = BeautifulSoup(response.content, 'html.parser')
            sleep(0.1)

            with open('index.html', 'w', encoding='utf8') as file:
                file.write(response.text)

            main_blcok = html.find('div', {'class': 'review-list-chunk'})

            name = html.find('h1', {'class': 'product-name'}).text.strip().replace('\n', ' ').replace('\r', ' ')

            max_page_count = int(html.find_all('a', 'pager-item nth')[-1].text.strip().replace('\n', ' ').replace('\r', ' '))




            for card in main_blcok.find_all('div', {'class': 'item'}):
                data = []

                date_text = card.find('div', {'class': 'review-postdate'}).text.strip().replace('\n', ' ').replace('\r', ' ')
                date = self.date_to_string(self.string_to_date(date_text))

                
                stars = card.find('div', {'class': 'rating-score'}).text.strip().replace('\n', ' ').replace('\r', ' ')

                title_el = card.find('a', {'class': 'review-title'})
                title = title_el.text.strip().replace('\n', ' ').replace('\r', ' ')
                link = 'https://otzovik.com' + title_el.get('href')

                text = card.find('div', {'class': 'review-body-wrap'}).text.strip().replace('\n', ' ').replace('\r', ' ')

                data.append(date)
                data.append(name)
                data.append(stars)
                data.append(link)
                data.append(url + f'{current_page}/?order=date_desc')
                data.append(text)


                if self.string_to_date(date) < start_date:
                    can_go = False
                    break

                cards.append(data)

                if not name in self.last_dates:
                    self.last_dates[name] = date


        for card in cards:
            self.result.append(card)















    # ru.myfin.by
    def rumyfinby(self, url, start_date=None):
        if start_date == None: start_date = self.start_date
        else: start_date = self.string_to_date(start_date)

        cards = []


        response = self.send(url + '?limit=100')
        sleep(0.1)
        html = BeautifulSoup(response.content, 'html.parser')
        sleep(0.1)

        main_blcok = html.find('div', {'class': 'reviews-list'})

        name = html.find('div', {'class': 'header-bank-top__title'}).text.strip().replace('\n', ' ').replace('\r', ' ')

        for card in main_blcok.find_all('div', {'class': 'reviews-list__item'}):
            data = []

            date = card.find('div', {'class': 'review-info__date'}).text.strip().replace('\n', ' ').replace('\r', ' ')
            title_el = card.find('div', {'class': 'review-block__title'})
            title = title_el.text.strip().replace('\n', ' ').replace('\r', ' ')

            stars = card.find('div', {'class': 'star-rating__text'}).text.strip().replace('\n', ' ').replace('\r', ' ')

            text = card.find('div', {'class': 'review-block__text'}).text.strip().replace('\n', ' ').replace('\r', ' ')

            data.append(date)
            data.append(name)
            data.append(stars)
            data.append(url)
            data.append(title + ' ' + text)

            if self.string_to_date(date) < start_date:
                break

            cards.append(data)


            if not name in self.last_dates:
                self.last_dates[name] = date


        for card in cards:
            self.result.append(card)






    # topbanki.ru
    def topbankiru(self, url, start_date=None):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            # 'Cookie': 'PHPSESSID=e461e3a69b67c36274445be30725322e; curr_reg_id=4396; vrfd=1; cf_clearance=pcW0MTeclxqBeQ2sZqw_5LzDdMB.5PusCcMUfnuAdYw-1717829469-1.0.1.1-kqjQOgfIHtb5pYZtT7QiyIBG.mY5DkK_cA1tjxL1481IMyVxM_loEU2WLMktwW6esJ.UIB0Rx7q21Jkx9xWUXQ',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Priority': 'u=1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        if start_date == None: start_date = self.start_date
        else: start_date = self.string_to_date(start_date)

        cards = []

        current_page = 0
        max_page_count = 3

        can_go = True


        while current_page < max_page_count and can_go:
            current_page += 1
            if url[-1] != '/': url += '/'

            response = self.send(url + f'/page{current_page}/', headers)
            sleep(0.1)
            html = BeautifulSoup(response.content, 'html.parser')
            sleep(0.1)


            with open('index.html', 'w', encoding='utf8') as file:
                file.write(response.text)

            main_blcok = html.find('div', {'class': 'response_table'})

            name = html.find('h1', {'itemprop': "name"}).text.strip().replace('\n', ' ').replace('\r', ' ')

            max_page_count = int(html.find('div', {'id': 'pagination'}).find_all('li')[-1].get('href').split('page')[-1].split('/')[0])

            print(max_page_count)
            break



            for card in main_blcok.find_all('div', {'class': 'item'}):
                data = []

                date_text = card.find('div', {'class': 'review-postdate'}).text.strip().replace('\n', ' ').replace('\r', ' ')
                date = self.date_to_string(self.string_to_date(date_text))

                
                stars = card.find('div', {'class': 'rating-score'}).text.strip().replace('\n', ' ').replace('\r', ' ')

                title_el = card.find('a', {'class': 'review-title'})
                title = title_el.text.strip().replace('\n', ' ').replace('\r', ' ')
                link = 'https://otzovik.com' + title_el.get('href')

                text = card.find('div', {'class': 'review-body-wrap'}).text.strip().replace('\n', ' ').replace('\r', ' ')

                data.append(date)
                data.append(name)
                data.append(stars)
                data.append(link)
                data.append(url + f'{current_page}/?order=date_desc')
                data.append(text)


                if self.string_to_date(date) < start_date:
                    can_go = False
                    break

                cards.append(data)

                if not name in self.last_dates:
                    self.last_dates[name] = date


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
    # pars = Parser(TEST, '23.05.2023')
    pass
    # for link in TEST:
    #     pars.irecommend_parsing_card(link)

    # pars.razvivay(TEST[2])


    # pars.rkorf(TEST[3])

    # pars.bankiclub(TEST[-1])
    # pars.bankiros(TEST[-1])

    # pars.brobank(TEST[-1])
    # pars.creditsonline(TEST[-1])
    # pars.bankiros(TEST[-1])
    # pars.otzovik(TEST[-1])
    # pars.rumyfinby(TEST[-1])
    # pars.topbankiru(TEST[-1])








    # pars.save_result()

    # print(pars.__dict__)