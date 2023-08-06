from async_request import Request, crawl, fetch, Crawler


def start():
    # reqs = [Request(url='https://www.nonobank.com/', callback=parse_nonobank) for i in range(10)]
    reqs = [Request(url='https://www.nonobank.com/', callback=parse_nonobank)]
    c = Crawler(reqs, result_back=process_result)
    c.run()


def parse_nonobank(response):
    print(response)
    links = response.xpath('//a/@href').getall()
    for link in links:
        if not 'nonobank' in link:
            continue
        if not link.startswith('http'):
            link = response.urljoin(link)
        yield Request(link, callback=parse_nonobank)


def parse_baidu(response):
    print(response.url, response.status_code)
    yield Request('https://cn.bing.com/', callback=parse_bing)


def parse_bing(response):
    print(response.url, response.status_code)
    print(response.xpath('//a/@href').get())
    yield Request('https://www.360.cn/', callback=parse_github)


def parse_github(response):
    print(response.url, response.status_code)
    yield {'hello': 'github'}


def process_result(result):
    print(result)


def parse():
    response = fetch('https://www.bing.com')
    response2 = fetch('https://www.baidu.com')
    print(response, response2)


if __name__ == '__main__':
    # request_list = [Request(url='https://www.baidu.com', callback=parse_baidu)]
    # crawl(request_list, result_back=process_result, handle_cookies=False, download_delay=0)
    # parse()
    start()