import argparse
import sys
import aiohttp
from UrlFilter import UrlFilter
from UrlValidator import UrlValiator
from htmlParser import PyHtmlParser
from colorama import Fore, Back
import asyncio


def get_task_limit(length):
    return length if length < tasks_limit else tasks_limit

def print_result():
    print(Back.GREEN, f"{len(crawled_list)} urls found!", Back.RESET)

def print_url(url):
    status_colors = {200:Back.GREEN, 400:Back.RED, 404:Back.RED, 302:Back.LIGHTRED_EX}

    for filter in url.filters:
        if isinstance(filter, int):
            print(status_colors.get(filter), filter, end=" ")
        else: 
            print(Back.BLUE, filter, end=" ")

    print(Back.RESET, end=" ")
    print(url.url, end="\n\n")

def init_args(parser: argparse.ArgumentParser):
    parser.add_argument("-u", type=str, required=True, help="name of the baseUrl which will be crawled", dest="baseUrl")
    parser.add_argument("-status", type=int, action="extend", default=None, help="status to filter", nargs="+")
    parser.add_argument("-tl", type=int, help="number of async tasks to run", default=10, dest="tasksLimit")
    parser.add_argument("-w", type=int, help="waiting time for the request", default=5, dest="wait")
    parser.add_argument("-sub", type=str, help="find subdomain", default=None)

parser = argparse.ArgumentParser("HURLS", description="hunt urls over the web")
init_args(parser)

args = parser.parse_args()
baseUrl = args.baseUrl
tasks_limit = args.tasksLimit
wait = args.wait
filters = {"status":args.status, "sub":args.sub}

current_list = set()
crawled_list = set()
 
urlValidator = UrlValiator()
baseUrl = urlValidator.get_validated(baseUrl, True)
urlValidator.set_baseUrl(baseUrl)

current_list.add(baseUrl)
urlFilter = UrlFilter(baseUrl, filters)

headers = {
  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36",
  "Connection":"close"
}

async def request(url):
    global crawled_list
    global current_list

    try:
        async with aiohttp.request('GET', url, timeout=aiohttp.ClientTimeout(total=wait)) as response:
            if response.headers["Content-Type"].split(';')[0] == "text/html":
                text = await response.text()

                urls = urlValidator.get_validatedAll(PyHtmlParser.parse(text))
                _url = urlFilter.filter(url, response.headers, response.status)

                if _url:
                    if _url.url not in crawled_list:
                        print_url(_url)
                    crawled_list.add(_url.url)

                for url in urls:
                    current_list.add(url)
    except:
        pass


async def main():
    global current_list
    global crawled_list

    tasks = []
    while len(current_list):
        for _ in range(0, get_task_limit(len(current_list))):
            task = asyncio.create_task(request(current_list.pop()))
            tasks.append(task)
        await asyncio.gather(*tasks)
        tasks.clear()
        current_list = current_list.difference(crawled_list)

    print_result()
    print(len(current_list), ":", len(crawled_list))
    

    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_result()
        sys.exit(0)
    except Exception as e:
        print(Back.RED, "getting error: " + str(e), Back.RESET)
