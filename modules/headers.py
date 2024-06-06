from fake_useragent import UserAgent

DEFAULT_HEADERS = {
    'User-Agent': UserAgent().firefox
}

if __name__ == '__main__':
    print(DEFAULT_HEADERS)