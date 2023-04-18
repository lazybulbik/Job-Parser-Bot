import time
from threading import Thread
import requests
import aspose.words as aw
import os
from telebot import TeleBot, types
from config.config import TOKEN
import asyncio
from proxy import get_working_proxies

bot = TeleBot(TOKEN, parse_mode='Markdown', disable_web_page_preview=True)

pause = True
delay = 2  # Задержка в часах
cities = []
last_idies = {}

city_id = {
    1: 'Киев',
    21: 'Харьков',
    3: "Одесса",
    4: 'Днепр',
    2: "Львов",
    9: "Запорожье",
    31: "Кривой рог",
    15: "Николаев",
    5: 'Винница',
    22: "Херсон",
    17: "Полтава",
    25: "Чернигов",
    24: "Черкассы",
    7: "Житомир",
    19: "Сумы",
    23: "Хмельницкий",
    26: "Черновцы",
    18: "Ровно",
    10: "Ивано Франковск",
    20: "Тернополь",
    14: "Луцк",
    28: "Ужгород",
    999: "Удаленная работа"
}

proxies = {
    'http': 'wqeqwe',
    'https': 'http://210.172.199.88:8080',
}


def get_new_ad(city, distance=False):
    if not distance:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'uk',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://rabota.ua/ua/%D0%BA%D0%B8%D0%B5%D0%B2',
            'cid': '151432211.1677300681',
            'apollographql-client-name': 'web-alliance-desktop',
            'apollographql-client-version': '485427f',
            'Content-Type': 'application/json',
            'Origin': 'https://rabota.ua',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        params = {
            'q': 'getPublishedVacanciesList',
        }

        json_data = {
            'operationName': 'getPublishedVacanciesList',
            'variables': {
                'pagination': {
                    'count': 40,
                    'page': 0,
                },
                'filter': {
                    'keywords': '',
                    'clusterKeywords': [],
                    'cityId': str(city),
                    'salary': 0,
                    'districtIds': [],
                    'scheduleIds': [],
                    'rubrics': [],
                    'metroBranches': [],
                    'showAgencies': True,
                    'showOnlyNoCvApplyVacancies': False,
                    'showOnlySpecialNeeds': False,
                    'showOnlyWithoutExperience': False,
                    'showOnlyNotViewed': False,
                    'showWithoutSalary': True,
                    'searchedType': 'STANDARD',
                },
            },
            'query': 'query getPublishedVacanciesList($filter: PublishedVacanciesFilterInput!, $pagination: PublishedVacanciesPaginationInput!) {\n  publishedVacancies(filter: $filter, pagination: $pagination) {\n    totalCount\n    items {\n      ...PublishedVacanciesItem\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment PublishedVacanciesItem on Vacancy {\n  id\n  schedules {\n    id\n    __typename\n  }\n  title\n  description\n  sortDateText\n  hot\n  designBannerUrl\n  badges {\n    name\n    __typename\n  }\n  salary {\n    amount\n    comment\n    amountFrom\n    amountTo\n    __typename\n  }\n  company {\n    id\n    logoUrl\n    name\n    __typename\n  }\n  city {\n    id\n    name\n    __typename\n  }\n  showProfile\n  seekerFavorite {\n    isFavorite\n    __typename\n  }\n  seekerDisliked {\n    isDisliked\n    __typename\n  }\n  formApplyCustomUrl\n  anonymous\n  isActive\n  publicationType\n  __typename\n}\n',
        }

        response = \
            requests.post('https://dracula.rabota.ua/', params=params, headers=headers, json=json_data, proxies=proxies).json()['data'][
                'publishedVacancies']['items']

        idies = [item['id'] for item in response]

    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'uk',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://rabota.ua/ua/zapros/all/%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0',
            'cid': '151432211.1677300681',
            'apollographql-client-name': 'web-alliance-desktop',
            'apollographql-client-version': '485427f',
            'Content-Type': 'application/json',
            'Origin': 'https://rabota.ua',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        params = {
            'q': 'getPublishedVacanciesList',
        }

        json_data = {
            'operationName': 'getPublishedVacanciesList',
            'variables': {
                'pagination': {
                    'count': 40,
                    'page': 0,
                },
                'filter': {
                    'keywords': '',
                    'clusterKeywords': [],
                    'salary': 0,
                    'districtIds': [],
                    'scheduleIds': [
                        '3',
                    ],
                    'rubrics': [],
                    'metroBranches': [],
                    'showAgencies': True,
                    'showOnlyNoCvApplyVacancies': False,
                    'showOnlySpecialNeeds': False,
                    'showOnlyWithoutExperience': False,
                    'showOnlyNotViewed': False,
                    'showWithoutSalary': True,
                    'searchedType': 'STANDARD',
                },
            },
            'query': 'query getPublishedVacanciesList($filter: PublishedVacanciesFilterInput!, $pagination: PublishedVacanciesPaginationInput!) {\n  publishedVacancies(filter: $filter, pagination: $pagination) {\n    totalCount\n    items {\n      ...PublishedVacanciesItem\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment PublishedVacanciesItem on Vacancy {\n  id\n  schedules {\n    id\n    __typename\n  }\n  title\n  description\n  sortDateText\n  hot\n  designBannerUrl\n  badges {\n    name\n    __typename\n  }\n  salary {\n    amount\n    comment\n    amountFrom\n    amountTo\n    __typename\n  }\n  company {\n    id\n    logoUrl\n    name\n    __typename\n  }\n  city {\n    id\n    name\n    __typename\n  }\n  showProfile\n  seekerFavorite {\n    isFavorite\n    __typename\n  }\n  seekerDisliked {\n    isDisliked\n    __typename\n  }\n  formApplyCustomUrl\n  anonymous\n  isActive\n  publicationType\n  __typename\n}\n',
        }

        response = \
            requests.post('https://dracula.rabota.ua/', params=params, headers=headers, json=json_data, proxies=proxies).json()['data'][
                'publishedVacancies']['items']

        idies = [item['id'] for item in response]

    return idies


def get_vacancy(id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'uk',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://rabota.ua/ua/company0/vacancy9430940',
        'cid': '151432211.1677300681',
        'apollographql-client-name': 'web-alliance-desktop',
        'apollographql-client-version': '485427f',
        'Content-Type': 'application/json',
        'Origin': 'https://rabota.ua',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    params = {
        'q': 'getPublishedVacancy',
    }

    json_data = {
        'operationName': 'getPublishedVacancy',
        'variables': {
            'id': str(id),
            'trackView': False,
        },
        'query': 'query getPublishedVacancy($id: ID!, $trackView: Boolean) {\n  publishedVacancy(id: $id, trackView: $trackView) {\n    ...PublishedVacancyPage\n    __typename\n  }\n}\n\nfragment PublishedVacancyPage on Vacancy {\n  id\n  title\n  anonymous\n  city {\n    id\n    name\n    __typename\n  }\n  company {\n    ...CompanyInfo\n    __typename\n  }\n  salary {\n    comment\n    amount\n    amountFrom\n    amountTo\n    __typename\n  }\n  sortDateText\n  sortDate\n  address {\n    name\n    district {\n      name\n      __typename\n    }\n    metro {\n      name\n      __typename\n    }\n    longitude\n    latitude\n    __typename\n  }\n  badges {\n    ...Badge\n    __typename\n  }\n  description\n  fullDescription\n  contacts {\n    name\n    phones\n    photo\n    socials\n    __typename\n  }\n  seekerDisliked {\n    isDisliked\n    __typename\n  }\n  seekerFavorite {\n    isFavorite\n    __typename\n  }\n  seekerApplication {\n    isApplied\n    lastTimeAppliedAt\n    __typename\n  }\n  isActive\n  hasDesign\n  designType\n  design {\n    ...HeaderInfo\n    id\n    backgroundHtml\n    footerInfo {\n      ...DesignFooterInfo\n      __typename\n    }\n    __typename\n  }\n  branch {\n    id\n    name\n    __typename\n  }\n  schedules {\n    id\n    name\n    __typename\n  }\n  hot\n  media {\n    ...MediaObject\n    __typename\n  }\n  ...KeyTagGroups\n  supportApplicationWithoutResume\n  formApplyCustomUrl\n  publicationType\n  languageQuestions {\n    language {\n      id\n      __typename\n    }\n    __typename\n  }\n  candidatesScreening {\n    questionnaire {\n      id\n      __typename\n    }\n    isEnabled\n    __typename\n  }\n  experienceQuestions {\n    id\n    __typename\n  }\n  status\n  __typename\n}\n\nfragment CompanyInfo on Company {\n  id\n  logoUrl\n  name\n  isVerified\n  companyUrl\n  miniProfile {\n    ...CompanyMiniProfileInfo\n    __typename\n  }\n  __typename\n}\n\nfragment CompanyMiniProfileInfo on CompanyMiniProfile {\n  isEnabled\n  description\n  images\n  years\n  benefits {\n    name\n    id\n    __typename\n  }\n  staffSize {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment Badge on PublishedVacancyBadge {\n  name\n  id\n  __typename\n}\n\nfragment HeaderInfo on VacancyDesign {\n  headerInfo {\n    ...DesignHeaderInfo\n    __typename\n  }\n  __typename\n}\n\nfragment DesignHeaderInfo on VacancyDesignHeader {\n  mediaItems {\n    type\n    url\n    videoCoverImageUrl\n    __typename\n  }\n  videoPlayButtonImageUrl\n  __typename\n}\n\nfragment DesignFooterInfo on VacancyDesignFooter {\n  imageUrl\n  __typename\n}\n\nfragment MediaObject on VacancyMedia {\n  url\n  description\n  type\n  __typename\n}\n\nfragment KeyTagGroups on Vacancy {\n  keyTagGroups {\n    name\n    id\n    __typename\n  }\n  __typename\n}\n',
    }

    response = requests.post('https://dracula.rabota.ua/', params=params, headers=headers, json=json_data, proxies=proxies).json()

    return response['data']['publishedVacancy']


def get_beautiful_description(data):
    with open('processing/desc.html', 'w', encoding='utf-8') as file:
        file.write(data)

    doc = aw.Document("processing/desc.html")
    doc.save("processing/desc.md")
    os.rename('processing/desc.md', 'processing/desc.txt')


def loop():
    while True:
        if not pause:
                proxy_adres = asyncio.run(get_working_proxies())[0]

                proxies['https'] = proxy_adres

                print(proxies['https'])

                print('not pause')
                print(delay)
                for city in cities:
                    try:
                        print(city_id[city])
                        flag = city == 999
                        new_vacancy = get_new_ad(city, distance=flag)

                        if last_idies[int(city)] == '':
                            last_idies[int(city)] = new_vacancy[0]
                            print(last_idies)

                            data = get_vacancy(new_vacancy[0])

                            if data['contacts']['phones'][0] != '':
                                print('ok number')

                                title = data['title']
                                amount = f'{str(data["salary"]["amountFrom"])} - {str(data["salary"]["amountTo"])} ₴ {data["salary"]["comment"]}'
                                get_beautiful_description(data['fullDescription'])
                                contact = f'{data["contacts"]["name"]} {data["contacts"]["phones"][0]}'
                                if city == 999:
                                    tag = '#Удаленная\_работа'
                                elif city == 10:
                                    tag = '#Работа\_Ивано\_Франковск'
                                elif city == 31:
                                    tag = '#Работа\_Кривой\_рог'
                                else:
                                    tag = f'#Работа\_{city_id[int(city)]}'

                                with open('processing/desc.txt', 'r', encoding='utf-8') as file:
                                    text = file.read()

                                if '<p' in text or "<br>" in text:
                                    continue

                                text = text.replace('﻿', '')
                                text = text.replace(' ', ' ')
                                text = text.replace('![](desc.001.png)', '')
                                # text = text.replace('![](Output.001.png)', '')
                                text = text.replace('**Evaluation Only. Created with Aspose.Words. Copyright 2003-2023 Aspose Pty Ltd.**', '')
                                text = text.replace('**Created with an evaluation copy of Aspose.Words. To discover the full versions of our APIs please visit: https://products.aspose.com/words/**', '')

                                text_list = text.split('\n')

                                for string in text_list:
                                    if 'https' in string:
                                        text_list[text_list.index(string)] = string.replace('**', '')
                                    else:
                                        text_list[text_list.index(string)] = string.replace('**', '*')

                                text = '\n'.join(text_list)

                                text = text.replace('\\', '')

                                if amount == '0 - 0  ₴':
                                    text_post = f'*{title}*' \
                                           f'\n\n{text.strip()}' \
                                           f'\n\n*{contact}*' \
                                           f'\n\n{tag}'
                                else:
                                    text_post = f'*{title}*' \
                                           f'\n*{amount}*' \
                                           f'\n\n{text.strip()}' \
                                           f'\n\n*{contact}*' \
                                           f'\n\n{tag}'

                                with open('config/chanel_id.txt', 'r') as file:
                                    chat_id = int(file.read())

                                msg = bot.send_message(chat_id, text_post)

                                if '*' in msg.text or '\\' in msg.text:
                                    bot.delete_message(msg.chat.id, msg.message_id)                                

                                os.remove('processing/desc.txt')

                        else:
                            if last_idies[city] in new_vacancy:
                                new_vacancy = new_vacancy[:new_vacancy.index(last_idies[city])]

                            if len(new_vacancy) != 0:
                                last_idies[int(city)] = new_vacancy[0]

                                print(new_vacancy)


                                for vacancy in new_vacancy:
                                    data = get_vacancy(vacancy)

                                    if data['contacts']['phones'][0] != '':
                                        print('ok number')

                                        title = data['title']
                                        amount = f'{str(data["salary"]["amountFrom"])} - {str(data["salary"]["amountTo"])} {data["salary"]["comment"]}'
                                        get_beautiful_description(data['fullDescription'])
                                        contact = f'{data["contacts"]["name"]} {data["contacts"]["phones"][0]}'
                                        if city == 999:
                                            tag = '#Удаленная\_работа'
                                        elif city == 10:
                                            tag = '#Работа\_Ивано\_Франковск'
                                        elif city == 31:
                                            tag = '#Работа\_Кривой\_рог'
                                        else:
                                            tag = f'#Работа\_{city_id[int(city)]}'

                                        with open('processing/desc.txt', 'r', encoding='utf-8') as file:
                                            text = file.read()

                                        if '<p' in text or "<br>" in text:
                                            continue

                                        text = text.replace('﻿', '')
                                        text = text.replace(' ', ' ')
                                        text = text.replace('![](desc.001.png)', '')
                                        # text = text.replace('![](Output.001.png)', '')
                                        text = text.replace('**Evaluation Only. Created with Aspose.Words. Copyright 2003-2023 Aspose Pty Ltd.**', '')
                                        text = text.replace('**Created with an evaluation copy of Aspose.Words. To discover the full versions of our APIs please visit: https://products.aspose.com/words/**', '')

                                        text_list = text.split('\n')

                                        for string in text_list:
                                            if 'https' in string:
                                                text_list[text_list.index(string)] = string.replace('**', '')
                                            else:
                                                text_list[text_list.index(string)] = string.replace('**', '*')

                                        text = '\n'.join(text_list)

                                        text = text.replace('\\', '')

                                        text_post = f'*{title}*' \
                                               f'\n*{amount}*' \
                                               f'\n\n{text.strip()}' \
                                               f'\n\n*{contact}*' \
                                               f'\n\n{tag}'

                                        with open('config/chanel_id.txt', 'r') as file:
                                            chat_id = int(file.read())

                                        msg = bot.send_message(chat_id, text_post)

                                        if '*' in msg.text or '\\' in msg.text:
                                            bot.delete_message(msg.chat.id, msg.message_id)

                                        os.remove('processing/desc.txt')

                                    else:
                                        continue                   
                                    
                        del text_list
                        del text
                        
                        time.sleep(4)

                    except Exception as e:
                        print(e)
                        l_dir = os.listdir('processing/')
                        if 'desc.txt' in l_dir:
                            os.remove('processing/desc.txt')

                        if 'desc.md' in l_dir:
                            os.remove('processing/desc.md')

                # sleep_delay = delay * 36000
                print('sleep')
                for i in range(int(delay * 3600)):
                    if pause:
                        break
                    # print(i)

                    time.sleep(0.9)                

th = Thread(target=loop)
th.start()