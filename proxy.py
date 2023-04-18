import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup

async def check_proxy(proxy):
    try:
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            async with session.post('https://dracula.rabota.ua/', proxy=proxy, timeout=5) as response:
                response_time = time.time() - start_time
                # print(f'Proxy: {proxy}, Response Time: {response_time} seconds, Status: {response.status}')
                if response.status != 403:
                    return proxy

    except Exception as e:
        # print(f'Proxy: {proxy}, Error: {e}')
        pass

async def get_proxies():
    url = 'https://free-proxy-list.net/anonymous-proxy.html'  # URL веб-сервиса с рабочими HTTPS-прокси
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()

    soup = BeautifulSoup(html, 'lxml')
    proxies = []
    rows = soup.find_all('tr')
    for row in rows[1:]:
        columns = row.find_all('td')
        if len(columns) >= 8:
            ip = columns[0].text.strip()
            port = columns[1].text.strip()
            ishttps = columns[6].text.strip()
            isgoogle = columns[5].text.strip()
            anon = columns[4].text.strip()
            code = columns[2].text.strip()

            # if ishttps == 'no' and isgoogle == 'no' and anon == 'elite proxy' and code == 'DE':
            proxy = f'{ip}:{port}'
            proxies.append(proxy)

    proxies = list(map(lambda x: 'http://' + x, proxies))

    return proxies

async def get_working_proxies():
    proxies = await get_proxies()
    # print('Proxies:', proxies)

    tasks = [check_proxy(proxy) for proxy in proxies if proxy]
    working_proxies = await asyncio.gather(*tasks)

    return [proxy for proxy in working_proxies if proxy]
