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
        
    },

    'bankiros.ru': {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            # 'Cookie': 'sbjs_migrations=1418474375998^%^3D1; sbjs_current_add=fd^%^3D2024-06-07^%^2015^%^3A12^%^3A42^%^7C^%^7C^%^7Cep^%^3Dhttps^%^3A^%^2F^%^2Fmoskva.bankiros.ru^%^2Fbank^%^2Ftcs^%^2Fotzyvy^%^2Frko^%^7C^%^7C^%^7Crf^%^3Dhttps^%^3A^%^2F^%^2Fwww.google.com^%^2F; sbjs_first_add=fd^%^3D2024-06-06^%^2009^%^3A49^%^3A44^%^7C^%^7C^%^7Cep^%^3Dhttps^%^3A^%^2F^%^2Fmoskva.bankiros.ru^%^2Fbank^%^2Ftcs^%^2Fotzyvy^%^2Frko^%^7C^%^7C^%^7Crf^%^3Dhttps^%^3A^%^2F^%^2Fwww.google.com^%^2F; sbjs_current=typ^%^3Dorganic^%^7C^%^7C^%^7Csrc^%^3Dgoogle^%^7C^%^7C^%^7Cmdm^%^3Dorganic^%^7C^%^7C^%^7Ccmp^%^3D^%^28none^%^29^%^7C^%^7C^%^7Ccnt^%^3D^%^28none^%^29^%^7C^%^7C^%^7Ctrm^%^3D^%^28none^%^29; sbjs_first=typ^%^3Dorganic^%^7C^%^7C^%^7Csrc^%^3Dgoogle^%^7C^%^7C^%^7Cmdm^%^3Dorganic^%^7C^%^7C^%^7Ccmp^%^3D^%^28none^%^29^%^7C^%^7C^%^7Ccnt^%^3D^%^28none^%^29^%^7C^%^7C^%^7Ctrm^%^3D^%^28none^%^29; sbjs_udata=vst^%^3D3^%^7C^%^7C^%^7Cuip^%^3D^%^28none^%^29^%^7C^%^7C^%^7Cuag^%^3DMozilla^%^2F5.0^%^20^%^28Windows^%^20NT^%^2010.0^%^3B^%^20Win64^%^3B^%^20x64^%^3B^%^20rv^%^3A128.0^%^29^%^20Gecko^%^2F20100101^%^20Firefox^%^2F128.0; currentSelectCityId=1; colorSheme=e53a4cb168e220a293391e642ba5a0eb547d172c0354f0bc38d8e9ee0c972ab2a^%^3A2^%^3A^%^7Bi^%^3A0^%^3Bs^%^3A10^%^3A^%^22colorSheme^%^22^%^3Bi^%^3A1^%^3Bs^%^3A4^%^3A^%^22dark^%^22^%^3B^%^7D; sbjs_migrations=1418474375998^%^3D1; sbjs_current_add=fd^%^3D2024-06-07^%^2012^%^3A28^%^3A04^%^7C^%^7C^%^7Cep^%^3Dhttps^%^3A^%^2F^%^2Fbankiros.ru^%^2Fbank^%^2Ftcs^%^2Fotzyvy^%^2Frko^%^7C^%^7C^%^7Crf^%^3Dhttps^%^3A^%^2F^%^2Fwww.google.com^%^2F; sbjs_first_add=fd^%^3D2024-06-06^%^2009^%^3A50^%^3A21^%^7C^%^7C^%^7Cep^%^3Dhttps^%^3A^%^2F^%^2Fbankiros.ru^%^2Fbank^%^2Ftcs^%^2Fotzyvy^%^2Frko^%^7C^%^7C^%^7Crf^%^3Dhttps^%^3A^%^2F^%^2Fwww.google.com^%^2F; sbjs_current=typ^%^3Dorganic^%^7C^%^7C^%^7Csrc^%^3Dgoogle^%^7C^%^7C^%^7Cmdm^%^3Dorganic^%^7C^%^7C^%^7Ccmp^%^3D^%^28none^%^29^%^7C^%^7C^%^7Ccnt^%^3D^%^28none^%^29^%^7C^%^7C^%^7Ctrm^%^3D^%^28none^%^29; sbjs_first=typ^%^3Dorganic^%^7C^%^7C^%^7Csrc^%^3Dgoogle^%^7C^%^7C^%^7Cmdm^%^3Dorganic^%^7C^%^7C^%^7Ccmp^%^3D^%^28none^%^29^%^7C^%^7C^%^7Ccnt^%^3D^%^28none^%^29^%^7C^%^7C^%^7Ctrm^%^3D^%^28none^%^29; sbjs_udata=vst^%^3D5^%^7C^%^7C^%^7Cuip^%^3D^%^28none^%^29^%^7C^%^7C^%^7Cuag^%^3DMozilla^%^2F5.0^%^20^%^28Windows^%^20NT^%^2010.0^%^3B^%^20Win64^%^3B^%^20x64^%^3B^%^20rv^%^3A128.0^%^29^%^20Gecko^%^2F20100101^%^20Firefox^%^2F128.0; cf_clearance=RJ_4.LC1ca3hExcY8AFHafIHS9x8UoZX5lPAKrl4kVY-1718270842-1.0.1.1-OMjiGO4g1oww9OqnMf7cIPJsXz.w7LplNtFz389Swsixk0gFhvjHoya3f6neMU8egYHGJ.lqHn0bJGh2JrTtoA; currentCityId=1; prod=qpp5tfhr1bl1hm78ckj2fk1aq0; _csrf=f12d0e5036031131a322b615af1520a18d8188c7c91af46a5342388363d78145a^%^3A2^%^3A^%^7Bi^%^3A0^%^3Bs^%^3A5^%^3A^%^22_csrf^%^22^%^3Bi^%^3A1^%^3Bs^%^3A32^%^3A^%^22-x7x_Tke3GGh8NKLC5r1jYFFdMNgTWRC^%^22^%^3B^%^7D; sbjs_session=pgs^%^3D2^%^7C^%^7C^%^7Ccpg^%^3Dhttps^%^3A^%^2F^%^2Fmoskva.bankiros.ru^%^2Fbank^%^2Ftcs^%^2Fotzyvy^%^2Frko',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Priority': 'u=0, i',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }
    }
}


if __name__ == '__main__':
    print(DEFAULT_HEADERS)