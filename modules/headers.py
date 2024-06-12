from fake_useragent import UserAgent

DEFAULT_HEADERS = {
    'User-Agent': UserAgent().firefox
}

HEADERS = {
    'irecommend.ru': {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Cookie': 'ssu=1717654116506613825; captcha_check=1_1718187009_3b313a86_2YLTryBShg6UkosKQmEwtwTX0QY=; ab_var=12; ss_uid=1717654116506613825; statsactivity=2; statstimer=1',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=0, i',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        
    }
}


if __name__ == '__main__':
    print(DEFAULT_HEADERS)