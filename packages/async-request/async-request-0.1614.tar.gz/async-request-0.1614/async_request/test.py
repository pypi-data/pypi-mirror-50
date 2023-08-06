from async_request import Request, crawl, fetch


def parse_baidu(response):
    print(response.url, response.status_code)
    yield Request('https://cn.bing.com/', callback=parse_bing)


def parse_bing(response):
    print(response.url, response.status_code)
    print(response.xpath('//a/@href').get())
    yield Request('https://github.com/financialfly/async-request', callback=parse_github)


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
    # crawl(request_list, result_callback=process_result)

    parse()