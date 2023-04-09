import aiohttp
from UrlFilter import UrlFilter
from htmlParser import PyHtmlParser
import asyncio


baseurl = input("type base url: ")
tasks_limit = 20
wait = 5

redirect_urls = set()
current_list = set()
crawled_list = set()
urlFilter = UrlFilter(baseurl)

current_list.add(baseurl)

headers = {
  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36",
  "Connection":"close"
}

if not baseurl.startswith("http"):
        baseurl = "https://" + baseurl

def get_task_limit(length):
    return length if length < tasks_limit else tasks_limit

def has_redirect_param(url):
    return url.find("redirect")
    

async def request(url):
    crawled_list.add(url)

    if has_redirect_param(url) != -1:
        redirect_urls.add(url)

    if not url.startswith("http"):
        url = "https://" + url

    print(url)
    try:
        async with aiohttp.request('GET',url) as response:
            if response.headers["Content-Type"].split(';')[0] == "text/html":
                text = await response.text()
                urls = urlFilter.filter(PyHtmlParser.parser(baseurl, text))
                for url in urls:
                    current_list.add(url)
    except:
        print("ERROR 404")


async def waitForTaskCompletion(_task_queue, wait):
    for task in _task_queue:
        try:
            await asyncio.wait_for(task, timeout=wait)
        except TimeoutError:
            print("sorry! Timeout Error")

        

async def main():
    global urls_count
    global current_list
    global crawled_list

    tasks = []
    while current_list:
        for _ in range(0, get_task_limit(len(current_list))):
            task = asyncio.create_task(request(current_list.pop()))
            tasks.append(task)

        await waitForTaskCompletion(tasks, wait)
        current_list = current_list.difference(crawled_list)

    print(f"we have found {len(crawled_list)} urls")
    print(f"we have found {len(redirect_urls)} redirect param urls")
    
        

    

asyncio.run(main())


    
    
	  
    
